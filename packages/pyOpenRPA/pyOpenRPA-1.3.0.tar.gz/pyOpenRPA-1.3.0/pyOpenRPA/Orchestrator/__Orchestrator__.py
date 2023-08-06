from re import I
import subprocess, json, psutil, time, os
from pyOpenRPA.Tools import CrossOS
if CrossOS.IS_WINDOWS_BOOL: import win32security #CrossOS
if CrossOS.IS_LINUX_BOOL: from simplepam import authenticate #CrossOS
import sys, base64, logging, ctypes, copy #Get input argument
import pickle
import inspect
import schedule
#from partd import Server

from . import Server
from . import Timer
from . import Processor
from . import BackwardCompatibility # Backward compatibility from v1.1.13
from . import Core
from . import Managers
from ..Tools import License

if CrossOS.IS_WINDOWS_BOOL: from subprocess import CREATE_NEW_CONSOLE

from .Utils import LoggerHandlerDumpLogList
from ..Tools import Debugger

# ATTENTION! HERE IS NO Relative import because it will be imported dynamically
# All function check the flag SessionIsWindowResponsibleBool == True else no cammand is processed
# All functions can return None, Bool or Dict { "IsSuccessful": True }
from .RobotRDPActive import CMDStr # Create CMD Strings
from .RobotRDPActive import Connector # RDP API

#from .Settings import Settings
import importlib
from importlib import util
import threading # Multi-threading for RobotRDPActive
from .RobotRDPActive import RobotRDPActive #Start robot rdp active
from .RobotScreenActive import Monitor #Start robot screen active
from . import SettingsTemplate # Settings template
import uuid # Generate uuid
import datetime # datetime
import math
import glob # search the files
import urllib

#Единый глобальный словарь (За основу взять из Settings.py)
gSettingsDict = None

# AGENT DEFS

def AgentActivityItemAdd(inHostNameStr, inUserStr, inActivityItemDict, inGSettings=None):
    """L+,W+: Добавить активность в словарь активностей выбранного Агента

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inHostNameStr: Наименование хоста, на котором запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inUserStr: Наименование пользователя, на графической сессии которого запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inActivityItemDict: Активность (ActivityItem). См. функцию ProcessorActivityitemCreate
    :return: ГУИД (GUID) строка Активности (ActivityItem). Далее можно ожидать результат этой функции по ГУИД с помощью функции AgentActivityItemReturnGet
    """

    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = copy.deepcopy(inActivityItemDict)
    # Add GUIDStr if not exist
    lGUIDStr = None
    if "GUIDStr" not in lActivityItemDict:
        lGUIDStr = str(uuid.uuid4()) # generate new GUID
        lActivityItemDict["GUIDStr"] = lGUIDStr
    else: lGUIDStr = lActivityItemDict["GUIDStr"]
    # Add CreatedByDatetime
    lActivityItemDict["CreatedByDatetime"] = datetime.datetime.now()
    # Main alg
    lAgentDictItemKeyTurple = (inHostNameStr.upper(),inUserStr.upper())
    if lAgentDictItemKeyTurple not in inGSettings["AgentDict"]:
        inGSettings["AgentDict"][lAgentDictItemKeyTurple] = SettingsTemplate.__AgentDictItemCreate__()
    lThisAgentDict = inGSettings["AgentDict"][lAgentDictItemKeyTurple]
    lThisAgentDict["ActivityList"].append(lActivityItemDict)
    # Return the result
    return lGUIDStr


def AgentActivityItemExists(inHostNameStr, inUserStr, inGUIDStr, inGSettings = None):
    """L+,W+: Выполнить проверку, что активность (ActivityItem) была отправлена на сторону Агента.

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inGUIDStr: ГУИД (GUID) активности (ActivityItem)
    :return: True - Активность присутствует ; False - Активность еще не была отправлена на сторону Агента
    """
    # Check if GUID is exists in dict - has been recieved
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Main alg
    lAgentDictItemKeyTurple = (inHostNameStr.upper(),inUserStr.upper())
    lResultBool = False
    if lAgentDictItemKeyTurple in inGSettings["AgentDict"]:
        for lActivityItem in inGSettings["AgentDict"][lAgentDictItemKeyTurple]["ActivityList"]:
            if inGUIDStr == lActivityItem.get("GUIDStr",None):
                lResultBool = True
                break
    return lResultBool

def AgentActivityItemReturnExists(inGUIDStr, inGSettings = None):
    """L+,W+: Выполнить проверку, что активность (ActivityItem) была выполнена на стороне Агента и результат был получен на стороне Оркестратора.

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inGUIDStr: ГУИД (GUID) активности (ActivityItem)
    :return: True - Активность присутствует; False - Активность еще не была выполнена на стороне Агента
    """

    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check if GUID is exists in dict - has been recieved
    return inGUIDStr in inGSettings["AgentActivityReturnDict"]


def AgentActivityItemReturnGet(inGUIDStr, inCheckIntervalSecFloat = 0.5, inGSettings=None):
    """L+,W+: Ожидает появления результата по активности (ActivityItem). Возвращает результат выполнения активности.
    
    !ВНИМАНИЕ! Замораживает поток, пока не будет получен результат. 
    !ВНИМАНИЕ! Запускать следует после того как будет инициализировано ядро Оркестратора (см. функцию OrchestratorInitWait), иначе будет инициирована ошибка. 

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inGUIDStr: ГУИД (GUID) активности (ActivityItem)
    :param inCheckIntervalSecFloat: Интервал в секундах, с какой частотой выполнять проверку результата. По умолчанию 0.5
    :return: Результат выполнения активности. !ВНИМАНИЕ! Возвращаются только то результаты, которые могут быть интерпретированы в JSON формате.
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    #Check if Orchestrator has been initialized - else raise exception
    if Core.IsOrchestratorInitialized(inGSettings=inGSettings) == True:
        # Wait while result will not come here
        while not AgentActivityItemReturnExists(inGSettings=inGSettings, inGUIDStr=inGUIDStr):
            time.sleep(inCheckIntervalSecFloat)
        # Return the result
        return inGSettings["AgentActivityReturnDict"][inGUIDStr]["Return"]
    else:
        raise Exception(f"__Orchestrator__.AgentActivityItemReturnGet !ATTENTION! Use this function only after Orchestrator initialization! Before orchestrator init exception will be raised.")

def AgentOSCMD(inHostNameStr, inUserStr, inCMDStr, inRunAsyncBool=True, inSendOutputToOrchestratorLogsBool=True, inCMDEncodingStr="cp1251", inGSettings=None, inCaptureBool=True):
    """L+,W+: Отправка команды командной строки на сессию, где работает pyOpenRPA.Agent. Результат выполнения команды можно выводить в лог оркестратора.

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inHostNameStr: Наименование хоста, на котором запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inUserStr: Наименование пользователя, на графической сессии которого запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inCMDStr: Команда для исполнения на стороне сессии Агента
    :param inRunAsyncBool: True - Агент не ожидает окончания выполнения команды. !ВНИМАНИЕ! Логирование в такой ситуации будет невозможно; False - Агент ожидает окончания выполнения операции.
    :param inSendOutputToOrchestratorLogsBool: True - отправлять весь вывод от команды в логи Оркестратора; Flase - Не отправлять; Default True
    :param inCMDEncodingStr: Кодировка DOS среды, в которой исполняется команда. Если некорректно установить кодировку - русские символы будут испорчены. По умолчанию установлена "cp1251"
    :param inCaptureBool: True - не запускать приложение как отдельное. Результат выполнения команды будет выводиться в окне Агента (если окно Агента присутствует на экране). False - команда будет запущена в отдельном DOS окне.
    :return: ГУИД (GUID) строка Активности (ActivityItem). Далее можно ожидать результат этой функции по ГУИД с помощью функции AgentActivityItemReturnGet
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = {
        "Def":"OSCMD", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inCMDStr":inCMDStr,"inRunAsyncBool":inRunAsyncBool, "inSendOutputToOrchestratorLogsBool": inSendOutputToOrchestratorLogsBool, "inCMDEncodingStr": inCMDEncodingStr, "inCaptureBool":inCaptureBool}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)

def AgentOSLogoff(inHostNameStr, inUserStr):
    """L+,W+: Выполнить операцию logoff на стороне пользователя.

    :param inHostNameStr: Наименование хоста, на котором запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inUserStr: Наименование пользователя, на графической сессии которого запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :return: ГУИД (GUID) строка Активности (ActivityItem). Далее можно ожидать результат этой функции по ГУИД с помощью функции AgentActivityItemReturnGet
    """
    inGSettings = GSettingsGet()  # Set the global settings
    lCMDStr = "shutdown /l"
    if CrossOS.IS_LINUX_BOOL: lCMDStr="logout"
    lActivityItemDict = {
        "Def":"OSCMD", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inCMDStr":lCMDStr,"inRunAsyncBool":False, "inSendOutputToOrchestratorLogsBool": True, "inCMDEncodingStr": "cp1251"}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)

def AgentOSFileSend(inHostNameStr, inUserStr, inOrchestratorFilePathStr, inAgentFilePathStr, inGSettings = None):
    """L+,W+: Отправить файл по адресу inOrchestratorFilePathStr со стороны Оркестратора и сохранить по адресу inAgentFilePathStr на стороне Агента.
    Поддерживает передачу крупных файлов (более 2-х Гб.). Функция является синхронной - не закончит свое выполнение, пока файл не будет передан полностью.

    !ВНИМАНИЕ - ПОТОКОБЕЗОПАСНАЯ! Вы можете вызвать эту функцию до инициализации ядра Оркестратора. Оркестратор добавит эту функцию в процессорную очередь на исполение. Если вам нужен результат функции, то необходимо сначала убедиться в том, что ядро Оркестратора было инициализированно (см. функцию OrchestratorInitWait). 
    
    :param inHostNameStr: Наименование хоста, на котором запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inUserStr: Наименование пользователя, на графической сессии которого запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inOrchestratorFilePathStr: Полный путь к передаваемому файлу на стороне Оркестратора.
    :param inAgentFilePathStr: Полный путь к локации, в которую требуется сохранить передаваемый файл.
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :return: ГУИД (GUID) строка Активности (ActivityItem). Далее можно ожидать результат этой функции по ГУИД с помощью функции AgentActivityItemReturnGet
    """

    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    if  inGSettings["ServerDict"]["ServerThread"] is None:
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"AgentOSFileSend run before server init - activity will be append in the processor queue.")
        lResult = {
            "Def": AgentOSFileSend, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inHostNameStr":inHostNameStr, "inUserStr":inUserStr, "inOrchestratorFilePathStr":inOrchestratorFilePathStr, "inAgentFilePathStr": inAgentFilePathStr},  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else: # In processor - do execution
        lActivityItemCheckIntervalSecFloat = inGSettings["ServerDict"]["AgentFileChunkCheckIntervalSecFloat"]

        # Get the chunk limit
        lChunkByteSizeInt = inGSettings["ServerDict"]["AgentFileChunkBytesSizeInt"]

        lL = inGSettings.get("Logger",None)

        # Open the file and get the size (in bytes)
        lFile = open(inOrchestratorFilePathStr,"rb")
        lFileSizeBytesInt = lFile.seek(0,2)
        lFile.seek(0)
        #import pdb
        #pdb.set_trace()
        lChunkCountInt = math.ceil(lFileSizeBytesInt/lChunkByteSizeInt)
        if lL: lL.info(f"О2А: Старт передачи крупного бинарного файла по частям. Общее количество частей: {lChunkCountInt}, от (сторона оркестратора): {inOrchestratorFilePathStr}, на (сторона агента): {inAgentFilePathStr}")
        for lChunkNumberInt in range(lChunkCountInt):
            # Read chunk
            lFileChunkBytes = lFile.read(lChunkByteSizeInt)
            # Convert to base64
            lFileChunkBase64Str = base64.b64encode(lFileChunkBytes).decode("utf-8")
            # Send chunk
            if lChunkNumberInt == 0:
                lActivityItemGUIDStr = AgentOSFileBinaryDataBase64StrCreate(inGSettings=inGSettings,inHostNameStr=inHostNameStr,
                                                     inUserStr=inUserStr,inFilePathStr=inAgentFilePathStr,
                                                     inFileDataBase64Str=lFileChunkBase64Str)
            else:
                lActivityItemGUIDStr = AgentOSFileBinaryDataBase64StrAppend(inGSettings=inGSettings, inHostNameStr=inHostNameStr,
                                                     inUserStr=inUserStr, inFilePathStr=inAgentFilePathStr,
                                                     inFileDataBase64Str=lFileChunkBase64Str)
            # Wait for the activity will be deleted
            while AgentActivityItemExists(inGSettings=inGSettings,inHostNameStr=inHostNameStr,inUserStr=inUserStr,inGUIDStr=lActivityItemGUIDStr):
                time.sleep(lActivityItemCheckIntervalSecFloat)
            if lL: lL.debug(
                    f"О2А: БИНАРНАЯ ОТПРАВКА: Номер текущей части: {lChunkNumberInt}")
        if lL: lL.info(
            f"О2А: БИНАРНАЯ ОТПРАВКА: Отправка завершена успешно")
        # Close the file
        lFile.close()

def AgentOSFileBinaryDataBytesCreate(inHostNameStr, inUserStr, inFilePathStr, inFileDataBytes, inGSettings=None):
    """L+,W+: Создать бинарный файл, который будет расположен по адресу inFilePathStr на стороне Агента с содержимым inFileDataBytes

    :param inHostNameStr: Наименование хоста, на котором запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inUserStr: Наименование пользователя, на графической сессии которого запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inFilePathStr: Полный путь к сохраняемому файлу на стороне Агента.
    :param inFileDataBytes: Строка байт (b'') для отправки в создаваемый файл на стороне Агента.
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :return: ГУИД (GUID) строка Активности (ActivityItem). Далее можно ожидать результат этой функции по ГУИД с помощью функции AgentActivityItemReturnGet
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lFileDataBase64Str = base64.b64encode(inFileDataBytes).decode("utf-8")
    lActivityItemDict = {
        "Def":"OSFileBinaryDataBase64StrCreate", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inFilePathStr":inFilePathStr,"inFileDataBase64Str":lFileDataBase64Str}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)


def AgentOSFileBinaryDataBase64StrCreate(inHostNameStr, inUserStr, inFilePathStr, inFileDataBase64Str, inGSettings=None):
    """L+,W+: Создать бинарный файл, который будет расположен по адресу inFilePathStr на стороне Агента с содержимым, декодированным с формата base64: inFileDataBase64Str
    
    :param inHostNameStr: Наименование хоста, на котором запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inUserStr: Наименование пользователя, на графической сессии которого запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inFilePathStr: Полный путь к сохраняемому файлу на стороне Агента.
    :param inFileDataBase64Str: Строка в формате base64 для отправки в создаваемый файл на стороне Агента.
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :return: ГУИД (GUID) строка Активности (ActivityItem). Далее можно ожидать результат этой функции по ГУИД с помощью функции AgentActivityItemReturnGet
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = {
        "Def":"OSFileBinaryDataBase64StrCreate", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inFilePathStr":inFilePathStr,"inFileDataBase64Str":inFileDataBase64Str}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)


def AgentOSFileBinaryDataBase64StrAppend(inHostNameStr, inUserStr, inFilePathStr, inFileDataBase64Str, inGSettings = None):
    """L+,W+: Добавить бинарную информацию в существующий бинарный файл, который будет расположен по адресу inFilePathStr на стороне Агента с содержимым, декодированным с формата base64: inFileDataBase64Str
    
    :param inHostNameStr: Наименование хоста, на котором запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inUserStr: Наименование пользователя, на графической сессии которого запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inFilePathStr: Полный путь к сохраняемому файлу на стороне Агента.
    :param inFileDataBase64Str: Строка в формате base64 для отправки в создаваемый файл на стороне Агента.
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :return: ГУИД (GUID) строка Активности (ActivityItem). Далее можно ожидать результат этой функции по ГУИД с помощью функции AgentActivityItemReturnGet
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = {
        "Def":"OSFileBinaryDataBase64StrAppend", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inFilePathStr":inFilePathStr,"inFileDataBase64Str":inFileDataBase64Str}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)


# Send text file to Agent (string)
def AgentOSFileTextDataStrCreate(inHostNameStr, inUserStr, inFilePathStr, inFileDataStr, inEncodingStr = "utf-8",inGSettings=None):
    """L+,W+: Создать текстовый файл, который будет расположен по адресу inFilePathStr на стороне Агента с содержимым inFileDataStr в кодировке inEncodingStr
    
    :param inHostNameStr: Наименование хоста, на котором запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inUserStr: Наименование пользователя, на графической сессии которого запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inFilePathStr: Полный путь к сохраняемому файлу на стороне Агента.
    :param inFileDataStr: Строка для отправки в создаваемый файл на стороне Агента.
    :param inEncodingStr: Кодировка текстового файла. По умолчанию utf-8
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :return: ГУИД (GUID) строка Активности (ActivityItem). Далее можно ожидать результат этой функции по ГУИД с помощью функции AgentActivityItemReturnGet
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = {
        "Def":"OSFileTextDataStrCreate", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inFilePathStr":inFilePathStr,"inFileDataStr":inFileDataStr, "inEncodingStr": inEncodingStr}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)

def AgentOSFileBinaryDataBase64StrReceive(inHostNameStr, inUserStr, inFilePathStr, inGSettings = None):
    """L+,W+: Выполнить чтение бинарного файла и получить содержимое в формате base64 (строка)

    :param inHostNameStr: Наименование хоста, на котором запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inUserStr: Наименование пользователя, на графической сессии которого запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inFilePathStr: Путь к бинарному файлу на чтение на стороне Агента
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :return: ГУИД (GUID) строка Активности (ActivityItem). Далее можно ожидать результат этой функции по ГУИД с помощью функции AgentActivityItemReturnGet
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = {
        "Def":"OSFileBinaryDataBase64StrReceive", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inFilePathStr":inFilePathStr}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)


def AgentOSFileBinaryDataReceive(inHostNameStr, inUserStr, inFilePathStr):
    """L+,W+: Чтение бинарного файла на стороне Агента по адресу inFilePathStr.
    
    !ВНИМАНИЕ - СИНХРОННАЯ! Функция не завершится, пока не будет получен результат чтения на стороне Агента.
    
    :param inHostNameStr: Наименование хоста, на котором запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inUserStr: Наименование пользователя, на графической сессии которого запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inFilePathStr: Путь к бинарному файлу, который требуется прочитать на стороне Агента
    :return: Строка байт (b'') - содержимое бинарного файла
    """
    lFileDataBytes = None
    inGSettings = GSettingsGet()  # Set the global settings
    # Check thread
    if  OrchestratorIsInited() == False:
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"AgentOSFileBinaryDataReceive run before orc init - activity will be append in the processor queue.")
        lResult = {
            "Def": AgentOSFileBinaryDataReceive, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inHostNameStr":inHostNameStr, "inUserStr":inUserStr, "inFilePathStr":inFilePathStr},  # Args dictionary
            "ArgGSettings": None,  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else: # In processor - do execution
        lActivityItemDict = {
            "Def":"OSFileBinaryDataBase64StrReceive", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
            "ArgList":[], # Args list
            "ArgDict":{"inFilePathStr":inFilePathStr}, # Args dictionary
            "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        
        #Send item in AgentDict for the futher data transmition
        lGUIDStr = AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)
        lFileBase64Str = AgentActivityItemReturnGet(inGUIDStr=lGUIDStr)
        if lFileBase64Str is not None: lFileDataBytes = base64.b64decode(lFileBase64Str)
        return lFileDataBytes

def AgentOSFileTextDataStrReceive(inHostNameStr, inUserStr, inFilePathStr, inEncodingStr="utf-8", inGSettings = None):
    """L+,W+: Чтение текстового файла на стороне Агента по адресу inFilePathStr. По ГИУД с помощью функции AgentActivityItemReturnGet можно будет получить текстовую строку данных, которые были расположены в файле.
    
    !ВНИМАНИЕ - АСИНХРОННАЯ! Функция завершится сразу, не дожидаясь окончания выполнения операции на стороне Агента.
    
    :param inHostNameStr: Наименование хоста, на котором запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inUserStr: Наименование пользователя, на графической сессии которого запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inFilePathStr: Путь к бинарному файлу, который требуется прочитать на стороне Агента
    :param inEncodingStr: Кодировка текстового файла. По умолчанию utf-8
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :return: ГУИД (GUID) строка Активности (ActivityItem). Далее можно ожидать результат этой функции по ГУИД с помощью функции AgentActivityItemReturnGet
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = {
        "Def":"OSFileTextDataStrReceive", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inFilePathStr":inFilePathStr, "inEncodingStr": inEncodingStr}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)

def AgentProcessWOExeUpperUserListGet(inHostNameStr, inUserStr, inGSettings = None):
    """L-,W+: Получить список процессов, которые выполняется на сессии Агента. Все процессы фиксируются без постфикса .exe, а также в верхнем регистре.

    ПРИМЕР РЕЗУЛЬТАТА, КОТОРЫЙ МОЖНО ПОЛУЧИТЬ ПО ГУИД ЧЕРЕЗ ФУНКЦИЮ AgentActivityItemReturnGet: ["ORCHESTRATOR", "AGENT", "CHROME", "EXPLORER", ...]

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inHostNameStr: Наименование хоста, на котором запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :param inUserStr: Наименование пользователя, на графической сессии которого запущен Агент. Наименования подключенных агентов доступно для просмотра в панели управления
    :return: ГУИД (GUID) строка Активности (ActivityItem). Далее можно ожидать результат этой функции по ГУИД с помощью функции AgentActivityItemReturnGet
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = {
        "Def":"ProcessWOExeUpperUserListGet", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)

# OS DEFS
def OSLogoff():
    """L+,W+: Выполнить отключение сессии, на которой выполняется Оркестратор.
    
    :return:
    """
    if CrossOS.IS_WINDOWS_BOOL: os.system("shutdown /l")
    elif CrossOS.IS_LINUX_BOOL: os.system("logout")

def OSCredentialsVerify(inUserStr, inPasswordStr, inDomainStr=""): ##
    """L+,W+: Выполнить верификацию доменного (локального) пользователя по паре логин/пароль

    :param inUserStr: Наименование пользователя
    :param inPasswordStr: Пароль
    :param inDomainStr: Домен. Если домена нет - не указывать или ""
    :return: True - Учетные данные верны; False - Учетные данные представлены некорректно    
    """
    if CrossOS.IS_WINDOWS_BOOL:
        try:
            hUser = win32security.LogonUser(
                inUserStr,inDomainStr, inPasswordStr,
                win32security.LOGON32_LOGON_NETWORK, win32security.LOGON32_PROVIDER_DEFAULT
            )
        except win32security.error:
            return False
        else:
            return True
    if CrossOS.IS_LINUX_BOOL:
        return authenticate(inUserStr, inPasswordStr, service='login', encoding='utf-8', resetcred=True)

def OSRemotePCRestart(inHostStr, inForceBool=True, inLogger = None):
    """L-,W+: Отправить сигнал на удаленную перезагрузку операционной системы. 
    
    !ВНИМАНИЕ! Перезапуск будет принят, если учетная запись имеет полномочия на перезапуск на соответсвующей машине.

    :param inHostStr: Имя хоста, который требуется перезагрузить
    :param inForceBool: True - принудительная перезагрузка; False - мягкая перезагрузка (дождаться окончания выполнения всех операций). По умолчанию True
    :param inLogger: Логгер, в который отправлять информацию о результате выполнения команды
    :return:
    """
    if inLogger is None: inLogger = OrchestratorLoggerGet()
    lCMDStr = f"powershell -Command Restart-Computer -ComputerName {inHostStr}"
    if inForceBool == True: lCMDStr = lCMDStr + " -Force"
    OSCMD(inCMDStr=lCMDStr,inLogger=inLogger)

def OSRestart(inForceBool=True, inLogger = None):
    """L+,W+: Отправить сигнал на перезагрузку операционной системы. 
    
    !ВНИМАНИЕ! Перезапуск будет принят, если учетная запись имеет полномочия на перезапуск на соответсвующей машине.
    
    :param inForceBool: True - принудительная перезагрузка; False - мягкая перезагрузка (дождаться окончания выполнения всех операций). По умолчанию True
    :param inLogger: Логгер, в который отправлять информацию о результате выполнения команды
    :return:
    """
    if inLogger is None: inLogger = OrchestratorLoggerGet()
    if CrossOS.IS_WINDOWS_BOOL: 
        lCMDStr = f"shutdown -r"
        if inForceBool == True: lCMDStr = lCMDStr + " -f"
    elif CrossOS.IS_LINUX_BOOL:
        lCMDStr = f"reboot"
        if inForceBool == True: lCMDStr = lCMDStr + " -f" 
    OSCMD(inCMDStr=lCMDStr,inLogger=inLogger)

def OSCMD(inCMDStr, inRunAsyncBool=True, inLogger = None):
    """L-,W+: Отправить команду на выполнение на сессию, где выполняется Оркестратор.

    :param inCMDStr: Команда на отправку
    :param inRunAsyncBool: True - выполнить команду в асинхронном режиме (не дожидаться окончания выполнения программы и не захватывать результат выполнения); False - Ждать окончания выполнения и захватывать результат
    :param inLogger: Логгер, в который отправлять информацию о результате выполнения команды
    :return: Строка результата выполнения команды. Если inRunAsyncBool = False
    """
    if inLogger is None: inLogger = OrchestratorLoggerGet()
    lResultStr = ""
    # New feature
    if inRunAsyncBool == True:
        inCMDStr = f"start {inCMDStr}"
    # Subdef to listen OS result
    def _CMDRunAndListenLogs(inCMDStr, inLogger):
        lResultStr = ""
        lOSCMDKeyStr = str(uuid.uuid4())[0:4].upper()
        # CROSS OS
        if CrossOS.IS_WINDOWS_BOOL: lCMDProcess = subprocess.Popen(f'cmd /c {inCMDStr}', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=CREATE_NEW_CONSOLE)
        if CrossOS.IS_LINUX_BOOL: lCMDProcess = subprocess.Popen(f'cmd /c {inCMDStr}', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if inLogger:
            lListenBool = True
            inLogger.info(f"{lOSCMDKeyStr}: # # # # Терминальная сессия запущена успешно # # # # ")
            inLogger.info(f"{lOSCMDKeyStr}: {inCMDStr}")
            while lListenBool:
                lOutputLineBytes = lCMDProcess.stdout.readline()
                if lOutputLineBytes == b"":
                    lListenBool = False
                lStr = lOutputLineBytes.decode('cp866')
                if lStr.endswith("\n"): lStr = lStr[:-1]
                inLogger.info(f"{lOSCMDKeyStr}: {lStr}")
                lResultStr+=lStr
            inLogger.info(f"{lOSCMDKeyStr}: # # # # Терминальная сессия завершена успешно # # # # ")
        return lResultStr
    # New call
    if inRunAsyncBool:
        lThread = threading.Thread(target=_CMDRunAndListenLogs, kwargs={"inCMDStr":inCMDStr, "inLogger":inLogger})
        lThread.start()
        lResultStr="Список ActivityList был запущен в асинхронном режиме - захватить содержимое невозможно"
    else:
        lResultStr = _CMDRunAndListenLogs(inCMDStr=inCMDStr, inLogger=inLogger)
    #lCMDCode = "cmd /c " + inCMDStr
    #subprocess.Popen(lCMDCode)
    #lResultCMDRun = 1  # os.system(lCMDCode)
    return lResultStr

def OrchestratorRestart(inGSettings=None):
    """L+,W+: Перезапуск Оркестратора с сохранением информации о запущенных RDP сессиях.

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    OrchestratorSessionSave(inGSettings=inGSettings) # Dump RDP List in file json
    if inGSettings is not None:
        lL = inGSettings["Logger"]
        if lL: lL.info(f"Выполнить перезапуск оркестратора")
    # Restart session
    if CrossOS.IS_WINDOWS_BOOL: os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    if CrossOS.IS_LINUX_BOOL: os.execl(sys.executable, sys.executable, *sys.argv)
    sys.exit(0)

def OrchestratorLoggerGet() -> logging.Logger:
    """L+,W+: Получить логгер Оркестратора

    :return: Логгер
    """
    return GSettingsGet().get("Logger",None)


def OrchestratorScheduleGet() -> schedule:
    """L+,W+: Базовый объект расписания, который можно использовать для запуска / остановки роботов.
    Подробнее про объект schedule и его примеры использования см. по адресу: schedule.readthedocs.io

    .. code-block:: python
        
        # Однопоточный schedule
        Orchestrator.OrchestratorScheduleGet().every(5).seconds.do(lProcess.StatusCheckStart)

        #Многопоточный schedule. cм. описание Orchestrator.OrchestratorThreadStart
        Orchestrator.OrchestratorScheduleGet().every(5).seconds.do(Orchestrator.OrchestratorThreadStart,lProcess.StatusCheckStart)

    :return: schedule объект
    """
    if GSettingsGet().get("SchedulerDict",{}).get("Schedule",None) is None:
        GSettingsGet()["SchedulerDict"]["Schedule"]=schedule
    return GSettingsGet().get("SchedulerDict",{}).get("Schedule",None)

def OrchestratorThreadStart(inDef, *inArgList, **inArgDict):
    """L+,W+: Запустить функцию в отдельном потоке. В таком случае получить результат выполнения функции можно только через общие переменные. (Например через GSettings) 

    :param inDef: Python функция
    :param inArgList: Список неименованных аргументов функции inDef
    :param inArgDict: Словарь именованных аргументов функции inDef
    :return: threading.Thread экземпляр
    """
    lDefThread = threading.Thread(target=inDef,args=inArgList,kwargs=inArgDict)
    lDefThread.start()
    return lDefThread

def OrchestratorIsAdmin():
    """L+,W+: Проверить, запущен ли Оркестратор с правами администратора. Права администратора нужны Оркестратору только для контроля графической сессии, на которой он запущен. Если эти права выделить индивидуально, то права администратора будут необязательны.

    :return: True - Запущен с правами администратора; False - Не запущен с правами администратора
    """
    if CrossOS.IS_WINDOWS_BOOL:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    elif CrossOS.IS_LINUX_BOOL: return os.getuid()==0
    else: return True

def OrchestratorIsInited() -> bool:
    """L+,W+: Проверить, было ли проинициализировано ядро Оркестратора

    :return: True - Ядро Оркестратора было проинициализировано; False - Требуется время на инициализацию
    :rtype: bool
    """    

    return Core.IsOrchestratorInitialized(inGSettings=GSettingsGet())

def OrchestratorInitWait() -> None:
    """L+,W+: Ожидать инициализацию ядра Оркестратора

    !ВНИМАНИЕ!: НИ В КОЕМ СЛУЧАЕ НЕ ЗАПУСКАТЬ ЭТУ ФУНКЦИЮ В ОСНОВНОМ ПОТОКЕ, ГДЕ ПРОИСХОДИТ ИНИЦИАЛИЗАЦИЯ ЯДРА ОРКЕСТРАТОРА - ВОЗНИКНЕТ ВЕЧНЫЙ ЦИКЛ
    """
    lIntervalSecFloat = 0.5
    while not OrchestratorIsInited():
        time.sleep(lIntervalSecFloat)
    

def OrchestratorRerunAsAdmin():
    """L-,W+: Перезапустить Оркестратор с правами локального администратора. Права администратора нужны Оркестратору только для контроля графической сессии, на которой он запущен. Если эти права выделить индивидуально, то права администратора будут необязательны.

    :return: True - Запущен с правами администратора; False - Не запущен с правами администратора
    """
    if not OrchestratorIsAdmin():
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        print(f"Уже запущено с правами администратора!")

def OrchestratorPySearchInit(inGlobPatternStr, inDefStr = None, inDefArgNameGSettingsStr = None, inAsyncInitBool = False):
    """L+,W+: Выполнить поиск и инициализацию пользовательских .py файлов в Оркестраторе (например панелей управления роботов)

    Добавляет инициализированный модуль в пространство sys.modules как imported (имя модуля = имя файла без расширения).
    
    ВНИМАНИЕ! ПРЕОБРАЗУЕТ ПУТИ МЕЖДУ WINDOWS И LINUX НОТАЦИЯМИ

    .. code-block:: python

        # ВАРИАНТ ИСПОЛЬЗОВАНИЯ 1 (инициализация модуля py без вызова каких-либо функций внутри)
        # автоинициализация всех .py файлов, с префиксом CP_, которые расположены в папке ControlPanel
        Orchestrator.OrchestratorPySearchInit(inGlobPatternStr="ControlPanel\\CP_*.py")

        # ВАРИАНТ ИСПОЛЬЗОВАНИЯ 2 (инициализация модуля py с вызовом функции внутри) - преимущественно для обратной совместимости старых версий панелей управления < 1.2.7
        # автоинициализация всех .py файлов, с префиксом CP_, которые расположены в папке ControlPanel
        Orchestrator.OrchestratorPySearchInit(inGlobPatternStr="ControlPanel\\CP_*.py", inDefStr="SettingsUpdate", inDefArgNameGSettingsStr="inGSettings")

        # ДЛЯ СПРАВКИ & ИСТОРИИ: Код выше позволил отказаться от блока кода ниже для каждого .py файла
        ## !!! For Relative import !!! CP Version Check
        try:
            sys.path.insert(0,os.path.abspath(os.path.join(r"")))
            from ControlPanel import CP_VersionCheck
            CP_VersionCheck.SettingsUpdate(inGSettings=gSettings)
        except Exception as e:
            gSettings["Logger"].exception(f"Exception when init CP. See below.")

    :param inGlobPatternStr: Пример "..\\*\\*\\*_CP*.py"
    :param inDefStr: ОПЦИОНАЛЬНО Строковое наименование функции. Преимущественно для обратной совместимости
    :param inDefArgNameGSettingsStr: ОПЦИОНАЛЬНО Наименование аргумента, в который требуется передать GSettings (если необходимо)
    :param inAsyncInitBool: ОПЦИОНАЛЬНО True - Инициализация py модулей в отдельных параллельных потоках - псевдопараллельное выполнение. False - последовательная инициализация
    :return: Сведения об инициализированных модулях в структуре: { "ModuleNameStr":{"PyPathStr": "", "Module": ...},  ...}
    """
    inGlobPatternStr = CrossOS.PathStr(inGlobPatternStr)
    # # # # # # # #
    def __execute__(inResultDict, inPyPathItemStr, inDefStr = None, inDefArgNameGSettingsStr = None):
        try:
            lPyPathItemStr = inPyPathItemStr
            lModuleNameStr = os.path.basename(lPyPathItemStr)[0:-3]
            lTechSpecification = importlib.util.spec_from_file_location(lModuleNameStr, lPyPathItemStr)
            lTechModuleFromSpec = importlib.util.module_from_spec(lTechSpecification)
            sys.modules[lModuleNameStr] = lTechModuleFromSpec  # Add initialized module in sys - python will not init this module enought
            lTechSpecificationModuleLoader = lTechSpecification.loader.exec_module(lTechModuleFromSpec)
            lItemDict = {"ModuleNameStr": lModuleNameStr, "PyPathStr": lPyPathItemStr, "Module": lTechModuleFromSpec}
            if lL: lL.info(f"Модуль .py {lModuleNameStr} был успешно инициализирован")
            inResultDict[lModuleNameStr]=lItemDict
            # Backward compatibility to call def with gsettings when init
            if inDefStr is not None and inDefStr != "":
                lDef = getattr(lTechModuleFromSpec, inDefStr)
                lArgDict = {}
                if inDefArgNameGSettingsStr is not None and inDefArgNameGSettingsStr != "":
                    lArgDict = {inDefArgNameGSettingsStr:GSettingsGet()}
                lDef(**lArgDict)
        except Exception as e:
            if lL: lL.exception(f"Exception when init the .py file {os.path.abspath(lPyPathItemStr)}")
    # # # # # # # #

    lResultDict = {}
    inGlobPatternStr = CrossOS.PathStr(inPathStr=inGlobPatternStr)
    lPyPathStrList = glob.glob(inGlobPatternStr) # get the file list
    lL = OrchestratorLoggerGet() # get the logger
    for lPyPathItemStr in lPyPathStrList:
        if inAsyncInitBool == True:
            # ASYNC EXECUTION
            lThreadInit = threading.Thread(target=__execute__,kwargs={
                "inResultDict":lResultDict, "inPyPathItemStr": lPyPathItemStr, 
                "inDefStr": inDefStr, "inDefArgNameGSettingsStr": inDefArgNameGSettingsStr}, daemon=True)
            lThreadInit.start()
        else:
            # SYNC EXECUTION
            __execute__(inResultDict=lResultDict, inPyPathItemStr=lPyPathItemStr, inDefStr = inDefStr, inDefArgNameGSettingsStr = inDefArgNameGSettingsStr)
    return lResultDict

def OrchestratorSessionSave(inGSettings=None):
    """L+,W+: Сохранить состояние Оркестратора (для дальнейшего восстановления в случае перезапуска): 
    
    - RDP сессий, которые контролирует Оркестратор
    - Хранилища DataStorage в глобальном словаре настроек GSettings. DataStorage поддерживает хранение объектов Python

    (до версии 1.2.7)
        _SessionLast_GSettings.pickle (binary)

    (начиная с версии 1.2.7)
        _SessionLast_RDPList.json (encoding = "utf-8")
        _SessionLast_StorageDict.pickle (binary)

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lL = inGSettings["Logger"]
    try:
        # Dump RDP List in file json
        #lFile = open("_SessionLast_RDPList.json", "w", encoding="utf-8")
        #lFile.write(json.dumps(inGSettings["RobotRDPActive"]["RDPList"]))  # dump json to file
        #lFile.close()  # Close the file
        #if inGSettings is not None:
        #    if lL: lL.info(
        #        f"Orchestrator has dump the RDP list before the restart.")
        ## _SessionLast_StorageDict.pickle (binary)
        #if "StorageDict" in inGSettings:
        #    with open('_SessionLast_StorageDict.pickle', 'wb') as lFile:
        #        pickle.dump(inGSettings["StorageDict"], lFile)
        #        if lL: lL.info(
        #            f"Orchestrator has dump the StorageDict before the restart.")

        #SessionLast
        lDumpDict = {"StorageDict":inGSettings["StorageDict"], "ManagersProcessDict":inGSettings["ManagersProcessDict"],
                     "RobotRDPActive":{"RDPList": inGSettings["RobotRDPActive"]["RDPList"]}}
        with open('_SessionLast_GSettings.pickle', 'wb') as lFile:
            pickle.dump(lDumpDict, lFile)
            if lL: lL.info(
                f"Оркестратор сохранил в рабочую директорию список РДП соединений и словарь DataStorage. При следующем запуске оркестратора информация востановится с диска")

    except Exception as e:
        if lL: lL.exception(f"Произошла ошибка при сохранении данных в файл")
    return True

def OrchestratorSessionRestore(inGSettings=None):
    """L+,W+: Восстановить состояние Оркестратора, если ранее состояние Оркестратора было сохранено с помощью функции OrchestratorSessionSave: 
    
    - RDP сессий, которые контролирует Оркестратор
    - Хранилища DataStorage в глобальном словаре настроек GSettings. DataStorage поддерживает хранение объектов Python

    (до версии 1.2.7)
        _SessionLast_GSettings.pickle (binary)

    (начиная с версии 1.2.7)
        _SessionLast_RDPList.json (encoding = "utf-8")
        _SessionLast_StorageDict.pickle (binary)

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lL = inGSettings.get("Logger",None)
    # _SessionLast_RDPList.json (encoding = "utf-8")
    if os.path.exists("_SessionLast_RDPList.json"):
        lFile = open("_SessionLast_RDPList.json", "r", encoding="utf-8")
        lSessionLastRDPList = json.loads(lFile.read())
        lFile.close()  # Close the file
        os.remove("_SessionLast_RDPList.json")  # remove the temp file
        inGSettings["RobotRDPActive"]["RDPList"] = lSessionLastRDPList  # Set the last session dict
        if lL: lL.warning(f"Список РДП был восстановлен из прошлой сессии оркестратора")
    # _SessionLast_StorageDict.pickle (binary)
    if os.path.exists("_SessionLast_StorageDict.pickle"):
        if "StorageDict" not in inGSettings:
            inGSettings["StorageDict"] = {}
        with open('_SessionLast_StorageDict.pickle', 'rb') as lFile:
            lStorageDictDumpDict = pickle.load(lFile)
            Server.__ComplexDictMerge2to1Overwrite__(in1Dict=inGSettings["StorageDict"],
                                                     in2Dict=lStorageDictDumpDict)  # Merge dict 2 into dict 1
            if lL: lL.warning(f"Словарь StorageDict был восстановлен из прошлой сессии оркестратора")
        os.remove("_SessionLast_StorageDict.pickle")  # remove the temp file
    # _SessionLast_Gsettings.pickle (binary)
    if os.path.exists("_SessionLast_GSettings.pickle"):
        if "StorageDict" not in inGSettings:
            inGSettings["StorageDict"] = {}
        if "ManagersProcessDict" not in inGSettings:
            inGSettings["ManagersProcessDict"] = {}
        with open('_SessionLast_GSettings.pickle', 'rb') as lFile:
            lStorageDictDumpDict = pickle.load(lFile)
            Server.__ComplexDictMerge2to1Overwrite__(in1Dict=inGSettings,
                                                     in2Dict=lStorageDictDumpDict)  # Merge dict 2 into dict 1
            if lL: lL.warning(f"Словарь GSettings был восстановлен из прошлой сессии оркестратора")
        os.remove("_SessionLast_GSettings.pickle")  # remove the temp file

def UACKeyListCheck(inRequest, inRoleKeyList) -> bool:
    """L+,W+: Проверить права доступа для пользователя запроса по списку ключей до права.

    .. code-block:: python

        # ВАРИАНТ ИСПОЛЬЗОВАНИЯ 1 (инициализация модуля py без вызова каких-либо функций внутри)
        # автоинициализация всех .py файлов, с префиксом CP_, которые расположены в папке ControlPanel
        Orchestrator.UACKeyListCheck(inRequest=lRequest, inRoleKeyList=["ROBOT1","DISPLAY_DASHBOARD"])

    :param inRequest: Экземпляр request (from http.server import BaseHTTPRequestHandler)
    :param inRoleKeyList: Список ключей, права доступа к которому требуется проверить
    :return: True - Пользователь обладает соответствующим правом; False - Пользователь не обладает соответствующим правом
    """
    return inRequest.UACClientCheck(inRoleKeyList=inRoleKeyList)

def UACUserDictGet(inRequest) -> dict:
    """L+,W+: Вернуть UAC (User Access Control) словарь доступов для пользователя, который отправил запрос. Пустой словарь - супердоступ (доступ ко всему)

    :param inRequest: Экземпляр request (from http.server import BaseHTTPRequestHandler)
    :return: Словарь доступов пользователя. Пустой словарь - супердоступ (доступ ко всему)
    """
    return inRequest.UserRoleHierarchyGet() # get the Hierarchy

def UACUpdate(inADLoginStr, inADStr="", inADIsDefaultBool=True, inURLList=None, inRoleHierarchyAllowedDict=None, inGSettings = None):
    """L+,W+: Дообогащение словаря доступа UAC пользователя inADStr\\inADLoginStr. Если ранее словарь не устанавливался, то по умолчанию он {}. Далее идет дообогащение теми ключами, которые присутствуют в inRoleHierarchyAllowedDict

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inADLoginStr: Логин пользователя
    :param inADStr: Домен пользователя. Если пусто - локальный компьютер или домен по-умолчанию, который настроен в ОС
    :param inADIsDefaultBool: True - домен настроен по умолчанию; False - домен требуется обязательно указывать
    :param inURLList: Список разрешенных URL для пользователя. Для добавления URL рекомендуем использовать функции WebURLConnectDef, WebURLConnectFile, WebURLConnectFolder
        Формат: {
            "Method": "GET" || "POST", 
            "URL": "/GetScreenshot", 
            "MatchType": "BeginWith" || "Equal" || "EqualCase" || "Contains" || "EqualNoParam", 
            "ResponseDefRequestGlobal": Функция python || "ResponseFilePath": Путь к файлу ||  "ResponseFolderPath": Путь к папке, в которой искать файлы,
            "ResponseContentType": пример MIME "image/png",
            "UACBool":False - не выполнять проверку прав доступа по запросу, 
            "UseCacheBool": True - кэшировать ответ},
    :param inRoleHierarchyAllowedDict: Словарь доступа пользователя UAC. Пустой словарь - полный доступ
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lUserTurple = (inADStr.upper(),inADLoginStr.upper()) # Create turple key for inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"]
    if inURLList is None: inURLList = [] # Check if None
    if inRoleHierarchyAllowedDict is None: inRoleHierarchyAllowedDict = {} # Check if None
    # Get the old URLList
    try:
        inURLList += inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"][lUserTurple]["MethodMatchURLBeforeList"]
    except:
        pass
    # Check RoleHierarchyAllowedDict in gSettings for the old role hierarchy - include in result.
    if lUserTurple in inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"] and "RoleHierarchyAllowedDict" in inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"][lUserTurple]:
        lRoleHierarchyAllowedOLDDict = inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"][lUserTurple]["RoleHierarchyAllowedDict"]
        Server.__ComplexDictMerge2to1__(in1Dict=inRoleHierarchyAllowedDict, in2Dict=lRoleHierarchyAllowedOLDDict) # Merge dict 2 into dict 1

    # Create Access item
    lRuleDomainUserDict = {
        "MethodMatchURLBeforeList": inURLList,
        "RoleHierarchyAllowedDict": inRoleHierarchyAllowedDict
    }
    # Case add domain + user
    inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"].update({(inADStr.upper(),inADLoginStr.upper()):lRuleDomainUserDict})
    if inADIsDefaultBool:
        # Case add default domain + user
        inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"].update({("",inADLoginStr.upper()):lRuleDomainUserDict})

def UACSuperTokenUpdate(inSuperTokenStr, inGSettings=None):
    """L+,W+: Добавить супертокен (полный доступ). Супертокены используются для подключения к Оркестратору по API

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inSuperTokenStr: Кодовая строковая комбинация, которая будет предоставлять доступ роботу / агенту для взаимодействия с Оркестратором по API
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lLoginStr = "SUPERTOKEN"
    UACUpdate(inGSettings=inGSettings, inADLoginStr=lLoginStr)
    inGSettings["ServerDict"]["AccessUsers"]["AuthTokensDict"].update(
        {inSuperTokenStr:{"User":lLoginStr, "Domain":"", "TokenDatetime":  datetime.datetime.now(), "FlagDoNotExpire":True}}
    )

# # # # # # # # # # # # # # # # # # # # # # #
# OrchestratorWeb defs
# # # # # # # # # # # # # # # # # # # # # # #
def WebURLIndexChange(inURLIndexStr:str ="/"):
    """L+,W+: Изменить адрес главной страницы Оркестратора. По умолчанию '/'

    :param inURLIndexStr: Новый адрес главной страницы Оркестратора.
    :type inURLIndexStr: str, опционально
    """
    GSettingsGet()["ServerDict"]["URLIndexStr"] = inURLIndexStr

def WebURLConnectDef(inMethodStr, inURLStr, inMatchTypeStr, inDef, inContentTypeStr="application/octet-stream", inGSettings = None, inUACBool = None):
    """L+,W+: Подключить функцию Python к URL.
    
    :param inMethodStr: Метод доступа по URL "GET" || "POST"
    :param inURLStr: URL адрес. Пример  "/index"
    :param inMatchTypeStr: Тип соответсвия строки URL с inURLStr: "BeginWith" || "Contains" || "Equal" || "EqualCase" || "EqualNoParam"
    :param inDef: Функция Python. Допускаются функции, которые принимают следующие наборы параметров: 2:[inRequest, inGSettings], 1: [inRequest], 0: []
    :param inContentTypeStr: МИМЕ тип. По умолчанию: "application/octet-stream"
    :param inUACBool: True - Выполнять проверку прав доступа пользователя перед отправкой ответа; False - не выполнять проверку прав доступа пользователя
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lURLItemDict = {
        "Method": inMethodStr.upper(),
        "URL": inURLStr,  # URL of the request
        "MatchType": inMatchTypeStr,  # "BeginWith|Contains|Equal|EqualCase",
        # "ResponseFilePath": "", #Absolute or relative path
        #"ResponseFolderPath": "C:\Abs\Archive\scopeSrcUL\OpenRPA\Orchestrator\Settings",
        # Absolute or relative path
        "ResponseContentType": inContentTypeStr, #HTTP Content-type
        "ResponseDefRequestGlobal": inDef, #Function with str result
        "UACBool": inUACBool
    }
    inGSettings["ServerDict"]["URLList"].append(lURLItemDict)


def WebURLConnectFolder(inMethodStr, inURLStr, inMatchTypeStr, inFolderPathStr, inGSettings = None, inUACBool = None, inUseCacheBool= False):
    """L+,W+: Подключить папку к URL.

    :param inMethodStr: Метод доступа по URL "GET" || "POST"
    :param inURLStr: URL адрес. Пример  "/index"
    :param inMatchTypeStr: Тип соответсвия строки URL с inURLStr: "BeginWith" || "Contains" || "Equal" || "EqualCase" || "EqualNoParam"
    :param inFolderPathStr: Путь к папке на диске, в которой искать файл и возвращать пользователю по HTTP
    :param inUACBool: True - Выполнять проверку прав доступа пользователя перед отправкой ответа; False - не выполнять проверку прав доступа пользователя
    :param inUseCacheBool: True - выполнить кэширование страницы, чтобы в следющих запросах открыть быстрее; False - не кэшировать
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check if last symbol is "/" - append if not exist
    lFolderPathStr = os.path.abspath(inFolderPathStr)
    if lFolderPathStr[-1]!="/":lFolderPathStr+="/"
    # Prepare URLItem
    lURLItemDict = {
        "Method": inMethodStr.upper(),
        "URL": inURLStr,  # URL of the request
        "MatchType": inMatchTypeStr,  # "BeginWith|Contains|Equal|EqualCase",
        # "ResponseFilePath": "", #Absolute or relative path
        "ResponseFolderPath": lFolderPathStr, # Absolute or relative path
        "ResponseContentType": None, #HTTP Content-type
        #"ResponseDefRequestGlobal": inDef #Function with str result
        "UACBool": inUACBool,
        "UseCacheBool": inUseCacheBool
    }
    inGSettings["ServerDict"]["URLList"].append(lURLItemDict)


def WebURLConnectFile(inMethodStr, inURLStr, inMatchTypeStr, inFilePathStr, inContentTypeStr=None, inGSettings = None, inUACBool = None, inUseCacheBool = False):
    """L+,W+: Подключить файл к URL.

    :param inMethodStr: Метод доступа по URL "GET" || "POST"
    :param inURLStr: URL адрес. Пример  "/index"
    :param inMatchTypeStr: Тип соответсвия строки URL с inURLStr: "BeginWith" || "Contains" || "Equal" || "EqualCase" || "EqualNoParam"
    :param inFilePathStr: Путь к файлу на диске, который возвращать пользователю по HTTP
    :param inContentTypeStr: МИМЕ тип. Если None - выполнить автоматическое определение
    :param inUACBool: True - Выполнять проверку прав доступа пользователя перед отправкой ответа; False - не выполнять проверку прав доступа пользователя
    :param inUseCacheBool: True - выполнить кэширование страницы, чтобы в следющих запросах открыть быстрее; False - не кэшировать
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)

    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lURLItemDict = {
        "Method": inMethodStr.upper(),
        "URL": inURLStr,  # URL of the request
        "MatchType": inMatchTypeStr,  # "BeginWith|Contains|Equal|EqualCase",
        "ResponseFilePath": os.path.abspath(inFilePathStr), #Absolute or relative path
        #"ResponseFolderPath": os.path.abspath(inFilePathStr), # Absolute or relative path
        "ResponseContentType": inContentTypeStr, #HTTP Content-type
        #"ResponseDefRequestGlobal": inDef #Function with str result
        "UACBool":inUACBool,
        "UseCacheBool": inUseCacheBool
    }
    inGSettings["ServerDict"]["URLList"].append(lURLItemDict)

def WebListenCreate(inServerKeyStr="Default", inAddressStr="", inPortInt=80, inCertFilePEMPathStr=None, inKeyFilePathStr=None, inGSettings = None):
    """L+,W+: Настроить веб-сервер Оркестратора.
    
    :param inAddressStr: IP адрес для прослушивания. Если "", то прослушивать запросы со всех сетевых карт. Если "127.0.0.1", то слушать запросы только с той ОС, на которой работает Оркестратор
    :param inPortInt: Номер порта для прослушивания. Если HTTP - 80; Если HTTPS - 443. По умолчанию 80. Допускается установка других портов
    :param inCertFilePEMPathStr: Путь файлу сертификата, сгенерированного в .pem (base64) формате. Обязателен при использовании защищенного HTTPS/SSL соединения.
    :param inKeyFilePathStr: Путь к файлу закрытого ключа в base64 формате
    :param inGSettings:  Глобальный словарь настроек Оркестратора (синглтон)
    :return: 
    """
    inCertFilePEMPathStr=CrossOS.PathStr(inPathStr=inCertFilePEMPathStr)
    inKeyFilePathStr=CrossOS.PathStr(inPathStr=inKeyFilePathStr)
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    inGSettings["ServerDict"]["ListenDict"][inServerKeyStr]={
        "AddressStr":inAddressStr,
        "PortInt":inPortInt,
        "CertFilePEMPathStr":inCertFilePEMPathStr,
        "KeyFilePathStr":inKeyFilePathStr,
        "ServerInstance": None
    }


def WebCPUpdate(inCPKeyStr, inHTMLRenderDef=None, inJSONGeneratorDef=None, inJSInitGeneratorDef=None, inGSettings = None):
    """L+,W+: Добавить панель управления робота в Оркестратор. Для панели управления открыт доступ для использования функции-генератора HTML, генератора JSON данных, генератора JS кода.

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inCPKeyStr: Текстовый ключ панели управления. Ключ для каждой панели управления должен быть уникальным!
    :param inHTMLRenderDef: Функция Python для генерации HTML кода. Для использования Jinja2 шаблонов HTML см. pyOpenRPA.Orchestrator.Managers.ControlPanel
    :param inJSONGeneratorDef: Функция Python для генерации JSON контейнера для отправки на клиентскую часть Оркестратора
    :param inJSInitGeneratorDef: Функция Python для генерации JS кода для отправки на клиентскую часть Оркестратора
    """
    lCPManager = Managers.ControlPanel(inControlPanelNameStr=inCPKeyStr, inRefreshHTMLJinja2TemplatePathStr=None)
    # CASE HTMLRender
    if inHTMLRenderDef is not None: lCPManager.mBackwardCompatibilityHTMLDef = inHTMLRenderDef
    # CASE JSONGenerator
    if inJSONGeneratorDef is not None: lCPManager.mBackwardCompatibilityJSONDef = inJSONGeneratorDef
    # CASE JSInitGeneratorDef
    if inJSInitGeneratorDef is not None: lCPManager.mBackwardCompatibilityJSDef = inJSInitGeneratorDef


def WebAuditMessageCreate(inRequest=None, inOperationCodeStr="-", inMessageStr="-"):
    """L+,W+: Создание сообщения ИТ аудита с такими сведениями как (Домен, IP, логин и тд.). Данная функция особенно актуальна в том случае, если требуется реализовать дополнительные меры контроля ИТ системы. 
    
    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        lWebAuditMessageStr = Orchestrator.WebAuditMessageCreate(
            inRequest = lRequest,
            inOperationCodeStr = "OP_CODE_1",
            inMessageStr="Success"):

        # Логгирование сообщения
        lLogger.info(lWebAuditMessageStr)

    :param inRequest: Экземпляр HTTP request. Опционален, если сообщение фиксируется из под потока, который был инициирован запросом пользователя
    :param inOperationCodeStr: Код операции, который принят в компании в соответствии с регламентными процедурами
    :param inMessageStr: Дополнительное сообщение, которое необходимо отправить в сообщение об ИТ аудите
    :return: Формат сообщения: "WebAudit :: DOMAIN\\USER@101.121.123.12 :: operation code :: message"
    """
    try:
        if inRequest is None: inRequest = WebRequestGet()
        lClientIPStr = inRequest.client_address[0]
        lUserDict = WebUserInfoGet(inRequest=inRequest)
        lDomainUpperStr = lUserDict["DomainUpperStr"]
        lUserLoginStr = lUserDict["UserNameUpperStr"]
        lResultStr = f"ВебАудит :: {lDomainUpperStr}\\\\{lUserLoginStr}@{lClientIPStr} :: {inOperationCodeStr} :: {inMessageStr}"
    except Exception as e:
        print(str(e)) # Has no logger - must be dead alg branch
        lResultStr = inMessageStr
    return lResultStr

def WebRequestParseBodyBytes(inRequest=None):
    """L+,W+: Извлечь данные в байт виде из тела (body) HTTP запроса.

    :param inRequest: Экземпляр HTTP request. Опционален, если сообщение фиксируется из под потока, который был инициирован запросом пользователя
    :return: Строка байт b'' или None (если тело запроса было пустым)
    """
    if inRequest is None: inRequest = WebRequestGet()
    lBodyBytes=None
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
        lBodyBytes = inRequest.rfile.read(lInputByteArrayLength)
    return lBodyBytes

def WebRequestParseBodyStr(inRequest=None):
    """L+,W+: Извлечь данные в виде строки из тела (body) HTTP запроса.

    :param inRequest: Экземпляр HTTP request. Опционален, если сообщение фиксируется из под потока, который был инициирован запросом пользователя
    :return: Текстовая строка '' или None (если тело запроса было пустым)
    """
    if inRequest is None: inRequest = WebRequestGet()
    return WebRequestParseBodyBytes(inRequest=inRequest).decode('utf-8')

def WebRequestParseBodyJSON(inRequest=None):
    """L+,W+: Извлечь из тела (body) запроса HTTP JSON данные и преобразовать в Dict / List структуры языка Python.

    :param inRequest: Экземпляр HTTP request. Опционален, если сообщение фиксируется из под потока, который был инициирован запросом пользователя
    :return: Словарь (dict), список (list) или None (если тело запроса было пустым)
    """
    if inRequest is None: inRequest = WebRequestGet()
    return json.loads(WebRequestParseBodyStr(inRequest=inRequest))

def WebRequestParsePath(inRequest=None):
    """L+,W+: Извлечь декодированный URL путь из HTTP запроса пользователя в формате строки.   

    :param inRequest: Экземпляр HTTP request. Опционален, если сообщение фиксируется из под потока, который был инициирован запросом пользователя
    :return: str, пример: /pyOpenRPA/Debugging/DefHelper
    """
    if inRequest is None: inRequest = WebRequestGet()
    return urllib.parse.unquote(inRequest.path)

def WebRequestParseFile(inRequest=None):
    """L+,W+: Извлечь файл (наименование + содержимое в виде строки байт b'') из HTTP запроса пользователя.

    :param inRequest: Экземпляр HTTP request. Опционален, если сообщение фиксируется из под потока, который был инициирован запросом пользователя
    :return: Кортеж формата (FileNameStr, FileBodyBytes) or (None, None), если файл не был обнаружен
    """
    if inRequest is None: inRequest = WebRequestGet()
    lResultTurple=(None,None)
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArray = WebRequestParseBodyBytes(inRequest=inRequest)
        #print(f"BODY:ftInputByteArrayl")
        # Extract bytes data
        lBoundaryStr = str(inRequest.headers.get('Content-Type'))
        lBoundaryStr = lBoundaryStr[lBoundaryStr.index("boundary=")+9:] # get the boundary key #print(LBoundoryStr)
        lSplit = lInputByteArray.split('\r\n\r\n')
        lDelimiterRNRNIndex = lInputByteArray.index(b'\r\n\r\n') #print(LSplit) # Get file name
        lSplit0 = lInputByteArray[:lDelimiterRNRNIndex].split(b'\r\n')[1]
        lFileNameBytes = lSplit0[lSplit0.index(b'filename="')+10:-1]
        lFileNameStr = lFileNameBytes.decode("utf-8")
        # File data bytes
        lFileDataBytes = lInputByteArray[lDelimiterRNRNIndex+4:]
        lFileDataBytes = lFileDataBytes[:lFileDataBytes.index(b"\r\n--"+lBoundaryStr.encode("utf-8"))]
        lResultTurple = (lFileNameStr, lFileDataBytes)

    return lResultTurple

def WebRequestResponseSend(inResponeStr, inRequest=None, inContentTypeStr: str = None, inHeadersDict: dict = None):
    """L+,W+: Установить ответ на HTTP запрос пользователя.

    :param inResponeStr: Тело ответа (строка)
    :param inRequest: Экземпляр HTTP request. Опционален, если сообщение фиксируется из под потока, который был инициирован запросом пользователя
    :param inContentTypeStr: МИМЕ тип. Пример: "html/text"
    :param inHeadersDict: Словарь (dict) ключей, которые добавить в headers HTTP ответа на запрос пользователя
    """
    if inRequest is None: inRequest = WebRequestGet()
    inRequest.OpenRPAResponseDict["Body"] = bytes(inResponeStr, "utf8")
    if inHeadersDict is not None:
        inRequest.OpenRPAResponseDict["Headers"].update(inHeadersDict)
    if inContentTypeStr is not None:
        inRequest.OpenRPAResponseDict["Headers"]["Content-type"] = inContentTypeStr


def WebRequestGet():
    """L+,W+: Вернуть экземпляр HTTP запроса, если функция вызвана в потоке, который был порожден для отработки HTTP запроса пользователя.
    """
    lCurrentThread = threading.current_thread()
    if hasattr(lCurrentThread, "request"):
        return lCurrentThread.request

def WebUserInfoGet(inRequest=None):
    """L+,W+: Информация о пользователе, который отправил HTTP запрос.

    :param inRequest: Экземпляр HTTP request. Опционален, если сообщение фиксируется из под потока, который был инициирован запросом пользователя
    :return: Сведения в формате {"DomainUpperStr": "PYOPENRPA", "UserNameUpperStr": "IVAN.MASLOV"}
    """
    if inRequest is None: inRequest = WebRequestGet()
    lDomainUpperStr = inRequest.OpenRPA["Domain"].upper()
    lUserUpperStr = inRequest.OpenRPA["User"].upper()
    return {"DomainUpperStr": lDomainUpperStr, "UserNameUpperStr": lUserUpperStr}

def WebUserIsSuperToken(inRequest = None, inGSettings = None):
    """L+,W+: Проверить, авторизован ли HTTP запрос с помощью супер токена (токен, который не истекает).

    :param inRequest: Экземпляр HTTP request. Опционален, если сообщение фиксируется из под потока, который был инициирован запросом пользователя
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :return: True - является супертокеном; False - не является супертокеном
    """
    if inRequest is None: inRequest = WebRequestGet()
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lIsSuperTokenBool = False
    # Get Flag is supertoken (True|False)
    lIsSuperTokenBool = inGSettings.get("ServerDict", {}).get("AccessUsers", {}).get("AuthTokensDict", {}).get(inRequest.OpenRPA["AuthToken"], {}).get("FlagDoNotExpire", False)
    return lIsSuperTokenBool

def WebUserUACHierarchyGet(inRequest = None):
    """L+,W+: Вернуть словарь доступа UAC в отношении пользователя, который выполнил HTTP запрос inRequest

    :param inRequest: Экземпляр HTTP request. Опционален, если сообщение фиксируется из под потока, который был инициирован запросом пользователя
    :return: UAC словарь доступа или {}, что означает полный доступ
    """
    if inRequest is None: inRequest = WebRequestGet()
    return inRequest.UserRoleHierarchyGet()


## GSettings defs

from . import SettingsTemplate

GSettings = SettingsTemplate.Create(inModeStr = "BASIC")
# Modules alias for pyOpenRPA.Orchestrator and pyOpenRPA.Orchestrator.__Orchestrator__
lCurrentModule = sys.modules[__name__]
if __name__ == "pyOpenRPA.Orchestrator" and "pyOpenRPA.Orchestrator.__Orchestrator__" not in sys.modules:
    sys.modules["pyOpenRPA.Orchestrator.__Orchestrator__"] = lCurrentModule
if __name__ == "pyOpenRPA.Orchestrator.__Orchestrator__" and "pyOpenRPA.Orchestrator" not in sys.modules:
    sys.modules["pyOpenRPA.Orchestrator"] = lCurrentModule

def GSettingsGet(inGSettings=None):
    """L+,W+: Вернуть глобальный словарь настроек Оркестратора. Во время выполнения программы глобальный словарь настроек существует в единственном экземпляре (синглтон)

    :param inGSettings: Дополнительный словарь настроек, который необходимо добавить в основной глобальный словарь настроек Оркестратора (синглтон)
    :return: Глобальный словарь настроек GSettings
    """
    global GSettings # identify the global variable
    # Merge dictionaries if some new dictionary has come
    if inGSettings is not None and GSettings is not inGSettings:
        GSettings = Server.__ComplexDictMerge2to1Overwrite__(in1Dict = inGSettings, in2Dict = GSettings)
    return GSettings # Return the result

def GSettingsKeyListValueSet(inValue, inKeyList=None, inGSettings = None):
    """L+,W+: Установить значение из глобального словаря настроек Оркестратора GSettings по списку ключей.

    Пример: Для того, чтобы установить значение для ключа car в словаре {"complex":{"car":"green"}, "simple":"HELLO"}, необходимо передать список ключей: ["complex", "car"]

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inValue: Значение для установки в глобальный словарь настроек Оркестратора GSettings
    :param inKeyList: Список ключей, по адресу которого установить значение в GSettings
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inKeyList is None: inKeyList = []
    lDict = inGSettings
    for lItem2 in inKeyList[:-1]:
        #Check if key - value exists
        if lItem2 in lDict:
            pass
        else:
            lDict[lItem2]={}
        lDict=lDict[lItem2]
    lDict[inKeyList[-1]] = inValue #Set value
    return True

def GSettingsKeyListValueGet(inKeyList=None, inGSettings = None):
    """L+,W+: Получить значение из глобального словаря настроек Оркестратора GSettings по списку ключей.

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inKeyList: Список ключей, по адресу которого получить значение из GSettings
    :return: Значение (тип данных определяется форматом хранения в GSettings)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inKeyList is None: inKeyList = []
    lDict = inGSettings
    for lItem2 in inKeyList[:-1]:
        #Check if key - value exists
        if lItem2 in lDict:
            pass
        else:
            lDict[lItem2]={}
        lDict=lDict[lItem2]
    return lDict.get(inKeyList[-1],None)

def GSettingsKeyListValueAppend(inValue, inKeyList=None, inGSettings = None):
    """L+,W+: Применить операцию .append к обьекту, расположенному по адресу списка ключей inKeyList в глобальном словаре настроек Оркестратора GSettings. Пример: Добавить значение в конец списка (list).

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        Orchestrator.GSettingsKeyListValueAppend(
            inGSettings = gSettings,
            inValue = "NewValue",
            inKeyList=["NewKeyDict","NewKeyList"]):
        # result inGSettings: {
        #    ... another keys in gSettings ...,
        #    "NewKeyDict":{
        #        "NewKeyList":[
        #            "NewValue"
        #        ]
        #    }
        #}

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inValue: Значение для установки в глобальный словарь настроек Оркестратора GSettings
    :param inKeyList: Список ключей, по адресу которого выполнить добавление в конец списка (list)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inKeyList is None: inKeyList = []
    lDict = inGSettings
    for lItem2 in inKeyList[:-1]:
        #Check if key - value exists
        if lItem2 in lDict:
            pass
        else:
            lDict[lItem2]={}
        lDict=lDict[lItem2]
    lDict[inKeyList[-1]].append(inValue) #Set value
    return True

def GSettingsKeyListValueOperatorPlus(inValue, inKeyList=None, inGSettings = None):
    """L+,W+: Применить оператор сложения (+) к обьекту, расположенному по адресу списка ключей inKeyList в глобальном словаре настроек Оркестратора GSettings. Пример: соединить 2 списка (list).

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        Orchestrator.GSettingsKeyListValueOperatorPlus(
            inGSettings = gSettings,
            inValue = [1,2,3],
            inKeyList=["NewKeyDict","NewKeyList"]):
        # result inGSettings: {
        #    ... another keys in gSettings ...,
        #    "NewKeyDict":{
        #        "NewKeyList":[
        #            "NewValue",
        #            1,
        #            2,
        #            3
        #        ]
        #    }
        #}

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inValue: Значение для установки в глобальный словарь настроек Оркестратора GSettings
    :param inKeyList: Список ключей, по адресу которого выполнить добавление в конец списка (list)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inKeyList is None: inKeyList = []
    lDict = inGSettings
    for lItem2 in inKeyList[:-1]:
        #Check if key - value exists
        if lItem2 in lDict:
            pass
        else:
            lDict[lItem2]={}
        lDict=lDict[lItem2]
    lDict[inKeyList[-1]] += inValue #Set value
    return True

def StorageRobotExists(inRobotNameStr):
    """L+,W+: Проверить, существует ли ключ inRobotNameStr в хранилище пользовательской информации StorageDict (GSettings > StarageDict)

    :param inRobotNameStr: Наименование (ключ) робота. !ВНИМАНИЕ! Наименование чувствительно к регистру
    :return: True - ключ робота присутствует в хранилище; False - отсутствует
    """
    return inRobotNameStr in GSettingsGet()["StorageDict"]

def StorageRobotGet(inRobotNameStr):
    """L+,W+: Получить содержимое по ключу робота inRobotNameStr в хранилище пользовательской информации StorageDict (GSettings > StarageDict)

    :param inRobotNameStr: Наименование (ключ) робота. !ВНИМАНИЕ! Наименование чувствительно к регистру
    :return: Значение или структура, которая расположена по адресу (GSettings > StarageDict > inRobotNameStr)
    """
    if inRobotNameStr not in GSettingsGet()["StorageDict"]:
        GSettingsGet()["StorageDict"][inRobotNameStr]={}
    return GSettingsGet()["StorageDict"][inRobotNameStr]

def ProcessorAliasDefCreate(inDef, inAliasStr=None, inGSettings = None):
    """L+,W+: Создать синоним (текстовый ключ) для инициации выполнения функции в том случае, если запрос на выполнения пришел из вне (передача функций невозможна). 
    
    Старая версия. Новую версию см. ActivityItemDefAliasCreate

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        def TestDef():
            pass
        lAliasStr = Orchestrator.ProcessorAliasDefCreate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        # Now you can call TestDef by the alias from var lAliasStr with help of ActivityItem (key Def = lAliasStr)

    
    :param inDef: функция Python
    :param inAliasStr: Строковый ключ (синоним), который можно будет использовать в Активности (ActivityItem)
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :return: Строковый ключ, который был назначен. Ключ может быть изменен, если входящий текстовый ключ был уже занят.
    """
    return ActivityItemDefAliasCreate(inDef=inDef, inAliasStr=inAliasStr, inGSettings = inGSettings)

def ProcessorAliasDefUpdate(inDef, inAliasStr, inGSettings = None):
    """L+,W+: Обновить синоним (текстовый ключ) для инициации выполнения функции в том случае, если запрос на выполнения пришел из вне (передача функций невозможна). 
    
    Старая версия. Новую версию см. ActivityItemDefAliasUpdate

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        def TestDef():
            pass
        Orchestrator.ProcessorAliasDefUpdate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        # Now you can call TestDef by the alias "TestDefAlias" with help of ActivityItem (key Def = "TestDefAlias")

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inDef: функция Python
    :param inAliasStr: Строковый ключ (синоним), который можно будет использовать в Активности (ActivityItem)
    :return: Строковый ключ, который был назначен. Ключ будет тем же, если входящий текстовый ключ был уже занят.
    """
    return ActivityItemDefAliasUpdate(inDef=inDef, inAliasStr=inAliasStr, inGSettings = inGSettings)

# ActivityItem defs
def ActivityItemHelperDefList(inDefQueryStr=None):
    """L+,W+: Получить список синонимов (текстовых ключей), доступных для использования в Активностях (ActivityItem).

    :param inDefStr: Часть текстового ключ (начало / середина / конец)
    :return: Список доступных ключей в формате: ["ActivityItemDefAliasUpdate", "ActivityItemDefAliasCreate", etc...]
    """
    lResultList = []
    if inDefQueryStr is not None: # do search alg
        for lKeyStr in GSettingsGet()["ProcessorDict"]["AliasDefDict"]:
            if inDefQueryStr.upper() in lKeyStr.upper():
                lResultList.append(lKeyStr)
    else:
        for lKeyStr in GSettingsGet()["ProcessorDict"]["AliasDefDict"]:
            lResultList.append(lKeyStr)
    return lResultList

def ActivityItemHelperDefAutofill(inDef):
    """L+,W+: Анализ аргументов функции по синониму (текстовому ключу).

    :param inDef: Часть текстового ключ (начало / середина / конец)
    :return: Преднастроенная структура активности (ActivityItem)         
        {
            "Def": None,
            "ArgList": [],
            "ArgDict": {},
            "ArgGSettingsStr": None,
            "ArgLoggerStr": None
        }
    """
    lResultDict = {
        "Def": None,
        "ArgList": [],
        "ArgDict": {},
        "ArgGSettingsStr": None,
        "ArgLoggerStr": None
    }
    lResultDict["Def"] = inDef
    lGS = GSettingsGet()
    if inDef in lGS["ProcessorDict"]["AliasDefDict"]:
        lDefSignature = inspect.signature(lGS["ProcessorDict"]["AliasDefDict"][inDef])
        for lItemKeyStr in lDefSignature.parameters:
            lItemValue = lDefSignature.parameters[lItemKeyStr]
            # Check if arg name contains "GSetting" or "Logger"
            if "GSETTING" in lItemKeyStr.upper():
                lResultDict["ArgGSettingsStr"] = lItemKeyStr
            elif "LOGGER" in lItemKeyStr.upper():
                lResultDict["ArgLoggerStr"] = lItemKeyStr
            else:
                if lItemValue.default is inspect._empty:
                    lResultDict["ArgDict"][lItemKeyStr] = None
                else:
                    lResultDict["ArgDict"][lItemKeyStr] = lItemValue.default
    return lResultDict

def ActivityItemCreate(inDef, inArgList=None, inArgDict=None, inArgGSettingsStr=None, inArgLoggerStr=None, inGUIDStr = None, inThreadBool = False):
    """L+,W+: Создать Активность (ActivityItem). Активность можно использовать в ProcessorActivityItemAppend или в Processor.ActivityListExecute или в функциях работы с Агентами.

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        # ВАРИАНТ 1
        def TestDef(inArg1Str, inGSettings, inLogger):
            pass
        lActivityItem = Orchestrator.ActivityItemCreate(
            inDef = TestDef,
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = "inGSettings",
            inArgLoggerStr = "inLogger")
        # lActivityItem:
        #   {
        #       "Def":TestDef,
        #       "ArgList":inArgList,
        #       "ArgDict":inArgDict,
        #       "ArgGSettings": "inArgGSettings",
        #       "ArgLogger": "inLogger"
        #   }

        # ВАРИАНТ 2
        def TestDef(inArg1Str):
            pass
        Orchestrator.ActivityItemDefAliasUpdate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        lActivityItem = Orchestrator.ActivityItemCreate(
            inDef = "TestDefAlias",
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = None,
            inArgLoggerStr = None)
        # lActivityItem:
        #   {
        #       "Def":"TestDefAlias",
        #       "ArgList":inArgList,
        #       "ArgDict":inArgDict,
        #       "ArgGSettings": None,
        #       "ArgLogger": None
        #   }

    :param inDef: Функция Python или синоним (текстовый ключ)
    :param inArgList: Список (list) неименованных аргументов к функции
    :param inArgDict: Словарь (dict) именованных аргументов к функции
    :param inArgGSettingsStr: Текстовое наименование аргумента GSettings (если требуется передавать)
    :param inArgLoggerStr: Текстовое наименование аргумента logger (если требуется передавать)
    :param inGUIDStr: ГУИД идентификатор активности (ActivityItem). Если ГУИД не указан, то он будет сгенерирован автоматически
    :param inThreadBool: True - выполнить ActivityItem в новом потоке; False - выполнить последовательно в общем потоке процессорной очереди
    :return: 
        lActivityItemDict= {
            "Def":inDef, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList":inArgList, # Args list
            "ArgDict":inArgDict, # Args dictionary
            "ArgGSettings": inArgGSettingsStr, # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": inArgLoggerStr, # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "GUIDStr": inGUIDStr,
            "ThreadBool": inThreadBool
        }
    """
    # Work about GUID in Activity items
    if inGUIDStr is None:
        inGUIDStr = str(uuid.uuid4())  # generate new GUID
    if inArgList is None: inArgList=[]
    if inArgDict is None: inArgDict={}
    lActivityItemDict= {
        "Def":inDef, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
        "ArgList":inArgList, # Args list
        "ArgDict":inArgDict, # Args dictionary
        "ArgGSettings": inArgGSettingsStr, # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": inArgLoggerStr, # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "GUIDStr": inGUIDStr,
        "ThreadBool": inThreadBool
    }
    return lActivityItemDict


def ActivityItemDefAliasCreate(inDef, inAliasStr=None, inGSettings = None):
    """L+,W+: Создать синоним (текстовый ключ) для инициации выполнения функции в том случае, если запрос на выполнения пришел из вне (передача функций невозможна). 
    
    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        def TestDef():
            pass
        lAliasStr = Orchestrator.ActivityItemDefAliasCreate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        # Now you can call TestDef by the alias from var lAliasStr with help of ActivityItem (key Def = lAliasStr)

    :param inDef: функция Python
    :param inAliasStr: Строковый ключ (синоним), который можно будет использовать в Активности (ActivityItem)
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :return: Строковый ключ, который был назначен. Ключ может быть изменен, если входящий текстовый ключ был уже занят.
    """
    #TODO Pay attention - New alias can be used too - need to create more complex algorythm to create new alias!
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lL = inGSettings["Logger"]
    if inAliasStr is None: inAliasStr = str(inDef)
    # Check if key is not exists
    if inAliasStr in inGSettings["ProcessorDict"]["AliasDefDict"]:
        inAliasStr = str(inDef)
        if lL: lL.warning(f"Orchestrator.ProcessorAliasDefCreate: Alias {inAliasStr} already exists in alias dictionary. Another alias will be generated and returned")
    inGSettings["ProcessorDict"]["AliasDefDict"][inAliasStr] = inDef
    return inAliasStr

def ActivityItemDefAliasModulesLoad():
    """L+,W+: Загрузить все функции из импортированных модулей sys.modules в ActivityItem синонимы - полезно для отладки со стороны панели управления.
    """
    lL = OrchestratorLoggerGet()
    lL.info(f"Синонимы функций: старт инициализации sys.modules")
    lSysModulesSnapshot = copy.copy(sys.modules) # Actual when start from jupyter
    for lModuleItemStr in lSysModulesSnapshot:
        lModuleItem = lSysModulesSnapshot[lModuleItemStr]
        for lDefItemStr in dir(lModuleItem):
            try:
                lDefItem = getattr(lModuleItem,lDefItemStr)
                if callable(lDefItem) and not lDefItemStr.startswith("_"):
                    ActivityItemDefAliasCreate(inDef=lDefItem, inAliasStr=f"{lModuleItemStr}.{lDefItemStr}")
            except ModuleNotFoundError:
                pass
    lL.info(f"Синонимы функций: окончание инициализации sys.modules")

def ActivityItemDefAliasUpdate(inDef, inAliasStr, inGSettings = None):
    """L+,W+: Обновить синоним (текстовый ключ) для инициации выполнения функции в том случае, если запрос на выполнения пришел из вне (передача функций невозможна). 
    
    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        def TestDef():
            pass
        Orchestrator.ActivityItemDefAliasUpdate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        # Now you can call TestDef by the alias "TestDefAlias" with help of ActivityItem (key Def = "TestDefAlias")

    :param inDef: функция Python
    :param inAliasStr: Строковый ключ (синоним), который можно будет использовать в Активности (ActivityItem)
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :return: Строковый ключ, который был назначен. Ключ будет тем же, если входящий текстовый ключ был уже занят.
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if callable(inDef): inGSettings["ProcessorDict"]["AliasDefDict"][inAliasStr] = inDef
    else: raise Exception(f"pyOpenRPA Exception: You can't use Orchestrator.ActivityItemDefAliasUpdate with arg 'inDef' string value. inDef is '{inDef}', inAliasStr is '{inAliasStr}'")
    return inAliasStr



def ProcessorActivityItemCreate(inDef, inArgList=None, inArgDict=None, inArgGSettingsStr=None, inArgLoggerStr=None, inGUIDStr = None, inThreadBool = False):
    """L+,W+: Создать Активность (ActivityItem). Активность можно использовать в ProcessorActivityItemAppend или в Processor.ActivityListExecute или в функциях работы с Агентами.

    Старая версия. Новую версию см. в ActivityItemCreate
    
    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        # ВАРИАНТ 1
        def TestDef(inArg1Str, inGSettings, inLogger):
            pass
        lActivityItem = Orchestrator.ProcessorActivityItemCreate(
            inDef = TestDef,
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = "inGSettings",
            inArgLoggerStr = "inLogger")
        # lActivityItem:
        #   {
        #       "Def":TestDef,
        #       "ArgList":inArgList,
        #       "ArgDict":inArgDict,
        #       "ArgGSettings": "inArgGSettings",
        #       "ArgLogger": "inLogger"
        #   }

        # ВАРИАНТ 2
        def TestDef(inArg1Str):
            pass
        Orchestrator.ProcessorAliasDefUpdate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        lActivityItem = Orchestrator.ProcessorActivityItemCreate(
            inDef = "TestDefAlias",
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = None,
            inArgLoggerStr = None)
        # lActivityItem:
        #   {
        #       "Def":"TestDefAlias",
        #       "ArgList":inArgList,
        #       "ArgDict":inArgDict,
        #       "ArgGSettings": None,
        #       "ArgLogger": None
        #   }

    :param inDef: Функция Python или синоним (текстовый ключ)
    :param inArgList: Список (list) неименованных аргументов к функции
    :param inArgDict: Словарь (dict) именованных аргументов к функции
    :param inArgGSettingsStr: Текстовое наименование аргумента GSettings (если требуется передавать)
    :param inArgLoggerStr: Текстовое наименование аргумента logger (если требуется передавать)
    :param inGUIDStr: ГУИД идентификатор активности (ActivityItem). Если ГУИД не указан, то он будет сгенерирован автоматически
    :param inThreadBool: True - выполнить ActivityItem в новом потоке; False - выполнить последовательно в общем потоке процессорной очереди
    :return: 
        lActivityItemDict= {
            "Def":inDef, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList":inArgList, # Args list
            "ArgDict":inArgDict, # Args dictionary
            "ArgGSettings": inArgGSettingsStr, # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": inArgLoggerStr, # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "GUIDStr": inGUIDStr,
            "ThreadBool": inThreadBool
        }
    """
    return ActivityItemCreate(inDef=inDef, inArgList=inArgList, inArgDict=inArgDict, inArgGSettingsStr=inArgGSettingsStr, inArgLoggerStr=inArgLoggerStr,
                           inGUIDStr=inGUIDStr, inThreadBool=inThreadBool)

def ProcessorActivityItemAppend(inGSettings = None, inDef=None, inArgList=None, inArgDict=None, inArgGSettingsStr=None, inArgLoggerStr=None, inActivityItemDict=None):
    """L+,W+: Добавить активность (ActivityItem) в процессорную очередь.
    
    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        # EXAMPLE 1
        def TestDef(inArg1Str, inGSettings, inLogger):
            pass
        lActivityItem = Orchestrator.ProcessorActivityItemAppend(
            inGSettings = gSettingsDict,
            inDef = TestDef,
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = "inGSettings",
            inArgLoggerStr = "inLogger")
        # Activity have been already append in the processor queue

        # EXAMPLE 2
        def TestDef(inArg1Str):
            pass
        Orchestrator.ProcessorAliasDefUpdate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        lActivityItem = Orchestrator.ProcessorActivityItemCreate(
            inDef = "TestDefAlias",
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = None,
            inArgLoggerStr = None)
        Orchestrator.ProcessorActivityItemAppend(
            inGSettings = gSettingsDict,
            inActivityItemDict = lActivityItem)
        # Activity have been already append in the processor queue

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inDef: Функция Python или синоним (текстовый ключ)
    :param inArgList: Список (list) неименованных аргументов к функции
    :param inArgDict: Словарь (dict) именованных аргументов к функции
    :param inArgGSettingsStr: Текстовое наименование аргумента GSettings (если требуется передавать)
    :param inArgLoggerStr: Текстовое наименование аргумента logger (если требуется передавать)
    :param inGUIDStr: ГУИД идентификатор активности (ActivityItem). Если ГУИД не указан, то он будет сгенерирован автоматически
    :param inThreadBool: True - выполнить ActivityItem в новом потоке; False - выполнить последовательно в общем потоке процессорной очереди
    :param inActivityItemDict: Альтернативный вариант заполнения, если уже имеется Активность (ActivityItem). В таком случае не требуется заполнять аргументы inDef, inArgList, inArgDict, inArgGSettingsStr, inArgLoggerStr
    :return ГУИД активности (ActivityItem)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inActivityItemDict is None:
        if inArgList is None: inArgList=[]
        if inArgDict is None: inArgDict={}
        if inDef is None: raise Exception(f"pyOpenRPA Exception: ProcessorActivityItemAppend need inDef arg if you dont use inActivityItemDict")
        lActivityList=[
            {
                "Def":inDef, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
                "ArgList":inArgList, # Args list
                "ArgDict":inArgDict, # Args dictionary
                "ArgGSettings": inArgGSettingsStr, # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
                "ArgLogger": inArgLoggerStr # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            }
        ]
    else:
        lActivityList = [inActivityItemDict]
    # Work about GUID in Activity items
    lGUIDStr = None
    for lItemDict in lActivityList:
        # Add GUIDStr if not exist
        if "GUIDStr" not in lItemDict:
            lGUIDStr = str(uuid.uuid4())  # generate new GUID
            lItemDict["GUIDStr"] = lGUIDStr
    # Add activity list in ProcessorDict
    inGSettings["ProcessorDict"]["ActivityList"]+=lActivityList
    return lGUIDStr

## Process defs
def ProcessIsStarted(inProcessNameWOExeStr): # Check if process is started
    """L-,W+: Проверить, запущен ли процесс, который в наименовании содержит inProcessNameWOExeStr.

    !ВНИМАНИЕ! ПРОВЕРЯЕТ ВСЕ ПРОЦЕССЫ ОПЕРАЦИОННОЙ СИСТЕМЫ. И ДРУГИХ ПОЛЬЗОВАТЕЛЬСКИХ СЕССИЙ, ЕСЛИ ОНИ ЗАПУЩЕНЫ НА ЭТОЙ МАШИНЕ. 
 
    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        lProcessIsStartedBool = Orchestrator.ProcessIsStarted(inProcessNameWOExeStr = "notepad")
        # lProcessIsStartedBool is True - notepad.exe is running on the Orchestrator machine

    :param inProcessNameWOExeStr: Наименование процесса без расширения .exe (WO = WithOut = Без) Пример: Для проверки процесса блокнота нужно указывать "notepad", не "notepad.exe"
    :return: True - Процесс запущен на ОС ; False - Процесс не запущен на ОС, где работает Оркестратор
    """
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if inProcessNameWOExeStr.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def ProcessStart(inPathStr, inArgList, inStopProcessNameWOExeStr=None):
    """L-,W+: Запуск процесса на сессии Оркестратора, если на ОС не запущен процесс inStopProcessNameWOExeStr.

    !ВНИМАНИЕ! ПРИ ПРОВЕРКЕ РАНЕЕ ЗАПУЩЕННЫХ ПРОЦЕССОВ ПРОВЕРЯЕТ ВСЕ ПРОЦЕССЫ ОПЕРАЦИОННОЙ СИСТЕМЫ. И ДРУГИХ ПОЛЬЗОВАТЕЛЬСКИХ СЕССИЙ, ЕСЛИ ОНИ ЗАПУЩЕНЫ НА ЭТОЙ МАШИНЕ. 

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        Orchestrator.ProcessStart(
            inPathStr = "notepad"
            inArgList = []
            inStopProcessNameWOExeStr = "notepad")
        # notepad.exe will be started if no notepad.exe is active on the machine

    :param inPathStr: Путь к файлу запускаемого процесса
    :param inArgList: Список аргументов, передаваемых в запускаемый процесс. Пример: ["test.txt"]
    :param inStopProcessNameWOExeStr: Доп. контроль: Не запускать процесс, если обнаружен запущенный процесс под наименованием inStopProcessNameWOExeStr без расширения .exe (WO = WithOut = Без)
    """
    lStartProcessBool = True
    if inStopProcessNameWOExeStr is not None: #Check if process running
        lCheckTaskName = inStopProcessNameWOExeStr
        if len(lCheckTaskName)>4:
            if lCheckTaskName[-4:].upper() != ".EXE":
                lCheckTaskName = lCheckTaskName+".exe"
        else:
            lCheckTaskName = lCheckTaskName+".exe"
        #Check if process exist
        if not ProcessIsStarted(inProcessNameWOExeStr=lCheckTaskName): lStartProcessBool=True

    if lStartProcessBool == True: # Start if flag is true
        lItemArgs=[inPathStr]
        if inArgList is None: inArgList = [] # 2021 02 22 Minor fix default value
        lItemArgs.extend(inArgList)
        subprocess.Popen(lItemArgs,shell=True)

def ProcessStop(inProcessNameWOExeStr, inCloseForceBool, inUserNameStr = "%username%"):
    """L-,W+: Остановить процесс на ОС, где работает Оркестратор, под учетной записью inUserNameStr.

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        Orchestrator.ProcessStop(
            inProcessNameWOExeStr = "notepad"
            inCloseForceBool = True
            inUserNameStr = "USER_99")
        # Will close process "notepad.exe" on the user session "USER_99" (!ATTENTION! if process not exists no exceptions will be raised)

    :param inProcessNameWOExeStr: Наименование процесса без расширения .exe (WO = WithOut = Без). Пример: Для проверки процесса блокнота нужно указывать "notepad", не "notepad.exe"
    :param inCloseForceBool: True - принудительно завершить процесс. False - отправить сигнал на безопасное отключение (!ВНИМАНИЕ! - ОС не позволяет отправлять сигнал на безопасное отключение на другую сесиию - только на той, где работает Оркестратор)
    :param inUserNameStr: Наименование пользователя, под именем которого искать процесс для остановки. По умолчанию "%username%" - искать процесс на текущей сессии
    """
    # Support input arg if with .exe
    lProcessNameWExeStr = inProcessNameWOExeStr
    if len(lProcessNameWExeStr) > 4:
        if lProcessNameWExeStr[-4:].upper() != ".EXE":
            lProcessNameWExeStr = lProcessNameWExeStr + ".exe"
    else:
        lProcessNameWExeStr = lProcessNameWExeStr + ".exe"
    # Flag Force
    lActivityCloseCommand = 'taskkill /im ' + lProcessNameWExeStr
    if inCloseForceBool == True:
        lActivityCloseCommand += " /F"
    # None - all users, %username% - current user, another str - another user
    if inUserNameStr is not None:
        lActivityCloseCommand += f' /fi "username eq {inUserNameStr}"'
    # Kill process
    os.system(lActivityCloseCommand)

def ProcessListGet(inProcessNameWOExeList=None):
    """L-,W+: Вернуть список процессов, запущенных на ОС, где работает Оркестратор. В списке отсортировать процессы по количеству используемой оперативной памяти. Также можно указать перечень процессов, которые интересуют - функция будет показывать активные из них.

    !ВНИМАНИЕ! ДЛЯ ПОЛУЧЕНИЯ СПИСКА ВСЕХ ПРОЦЕССОВ ОС НЕОБХОДИМО ЗАПУСКАТЬ ОРКЕСТРАТОР С ПРАВАМИ АДМИНИСТРАТОРА.

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        lProcessList = Orchestrator.ProcessListGet()
        # Return the list of the process on the machine.
        # !ATTENTION! RUn orchestrator as administrator to get all process list on the machine.

    :param inProcessNameWOExeList: Список процессов, среди которых искать активные. Если параметр не указывать - вернет перечень всех доступных процессов 
    :return: Сведения о запущенных процессах в следующем формате {
        "ProcessWOExeList": ["notepad","..."],
        "ProcessWOExeUpperList": ["NOTEPAD","..."],
        "ProcessDetailList": [
            {
                'pid': 412, # Идентификатор процесса
                'username': "DESKTOP\\USER",
                'name': 'notepad.exe',
                'vms': 13.77767775, # В Мб
                'NameWOExeUpperStr': 'NOTEPAD',
                'NameWOExeStr': "'notepad'"},
            {...}]

    """
    if inProcessNameWOExeList is None: inProcessNameWOExeList = []
    lMapUPPERInput = {} # Mapping for processes WO exe
    lResult = {"ProcessWOExeList":[], "ProcessWOExeUpperList":[],"ProcessDetailList":[]}
    # Create updated list for quick check
    lProcessNameWOExeList = []
    for lItem in inProcessNameWOExeList:
        if lItem is not None:
            lProcessNameWOExeList.append(f"{lItem.upper()}.EXE")
            lMapUPPERInput[f"{lItem.upper()}.EXE"]= lItem
    # Iterate over the list
    for proc in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
            pinfo['NameWOExeUpperStr'] = pinfo['name'][:-4].upper()
            # Add if empty inProcessNameWOExeList or if process in inProcessNameWOExeList
            if len(lProcessNameWOExeList)==0 or pinfo['name'].upper() in lProcessNameWOExeList:
                try: # 2021 02 22 Minor fix if not admin rights
                    pinfo['NameWOExeStr'] = lMapUPPERInput[pinfo['name'].upper()]
                except Exception as e:
                    pinfo['NameWOExeStr'] = pinfo['name'][:-4]
                lResult["ProcessDetailList"].append(pinfo) # Append dict to list
                lResult["ProcessWOExeList"].append(pinfo['NameWOExeStr'])
                lResult["ProcessWOExeUpperList"].append(pinfo['NameWOExeUpperStr'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    return lResult


def ProcessDefIntervalCall(inDef, inIntervalSecFloat, inIntervalAsyncBool=False, inDefArgList=None, inDefArgDict=None, inDefArgGSettingsNameStr=None, inDefArgLoggerNameStr=None, inExecuteInNewThreadBool=True, inLogger=None, inGSettings = None):
    """L+,W+: Периодический вызов функции Python.

    :param inDef: Функция Python, которую потребуется периодически вызывать
    :param inIntervalSecFloat: Интервал между вызовами функции в сек.
    :param inIntervalAsyncBool: False - ожидать интервал inIntervalSecFloat только после окончания выполнения предыдущей итерации; True - Ожидать интервал сразу после запуска итерации
    :param inDefArgList: Список (list) неименованных аргументов для передачи в функцию. По умолчанию None
    :param inDefArgDict: Словарь (dict) именованных аргументов для передачи в функцию. По умолчанию None
    :param inDefArgGSettingsNameStr: Наименование аргумента глобального словаря настроек Оркестратора GSettings (опционально)
    :param inDefArgLoggerNameStr: Наименование аргумента логгера Оркестратора (опционально)
    :param inExecuteInNewThreadBool: True - периодический вызов выполнять в отдельном потоке (не останавливать выполнение текущего потока); False - Выполнение периодического вызова в текущем потоке, в котором была вызвана функция ProcessDefIntervalCall. По умолчанию: True
    :param inLogger: Логгер для фиксации сообщений выполнения функции (опционально)
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inLogger is None: inLogger = OrchestratorLoggerGet()
    #Some edits on start
    if inDefArgDict is None: inDefArgDict = {}
    if inDefArgList is None: inDefArgList = []
    # Check if inDefArgLogger is set and inLogger is exist
    if inDefArgLoggerNameStr=="": inDefArgLoggerNameStr=None
    if inDefArgGSettingsNameStr=="": inDefArgGSettingsNameStr=None
    if inDefArgLoggerNameStr is not None and not inLogger:
        raise Exception(f"__Orchestrator__.ProcessDefIntervalCall: Вызываемая функция требует передачи логгера, а он не указан")

    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"__Orchestrator__.ProcessDefIntervalCall: функция вызвана не из процессорной очереди - активность будет перемещена в процессорную очередь")
        lProcessorActivityDict = {
            "Def": ProcessDefIntervalCall, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inDef": inDef, "inIntervalSecFloat": inIntervalSecFloat,
                        "inIntervalAsyncBool":inIntervalAsyncBool, "inDefArgList": inDefArgList,
                        "inDefArgDict": inDefArgDict, "inDefArgGSettingsNameStr":inDefArgGSettingsNameStr,
                        "inDefArgLoggerNameStr": inDefArgLoggerNameStr, "inExecuteInNewThreadBool": inExecuteInNewThreadBool},  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": "inLogger"  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lProcessorActivityDict)
    else:
        # Internal def to execute periodically
        def __Execute__(inGSettings, inDef, inIntervalSecFloat, inIntervalAsyncBool, inDefArgList, inDefArgDict, inLogger,  inDefArgGSettingsNameStr, inDefArgLoggerNameStr):
            if inLogger: inLogger.info(f"__Orchestrator__.ProcessDefIntervalCall: вызов функции по циклу инициализирован. Функция: {str(inDef)}")
            # Prepare gSettings and logger args
            if inDefArgGSettingsNameStr is not None:
                inDefArgDict[inDefArgGSettingsNameStr] = inGSettings
            if inDefArgLoggerNameStr is not None:
                inDefArgDict[inDefArgLoggerNameStr] = inLogger
            while True:
                try:
                    # Call async if needed
                    if inIntervalAsyncBool == False:  # Case wait result then wait
                        inDef(*inDefArgList, **inDefArgDict)
                    else:  # Case dont wait result - run sleep then new iteration (use many threads)
                        lThread2 = threading.Thread(target=inDef,
                                                    args=inDefArgList,
                                                    kwargs=inDefArgDict)
                        lThread2.start()
                except Exception as e:
                    if inLogger: inLogger.exception(
                        f"ProcessDefIntervalCall: Interval call has been failed. Traceback is below. Code will sleep for the next call")
                # Sleep interval
                time.sleep(inIntervalSecFloat)

        # Check to call in new thread
        if inExecuteInNewThreadBool:
            lThread = threading.Thread(target=__Execute__,
                                       kwargs={"inGSettings":inGSettings, "inDef": inDef, "inIntervalSecFloat": inIntervalSecFloat,
                                               "inIntervalAsyncBool": inIntervalAsyncBool, "inDefArgList": inDefArgList,
                                               "inDefArgDict": inDefArgDict, "inLogger": inLogger,
                                               "inDefArgGSettingsNameStr":inDefArgGSettingsNameStr , "inDefArgLoggerNameStr":inDefArgLoggerNameStr})
            lThread.start()
        else:
            __Execute__(inGSettings=inGSettings, inDef=inDef, inIntervalSecFloat=inIntervalSecFloat, inIntervalAsyncBool=inIntervalAsyncBool,
                        inDefArgList=inDefArgList, inDefArgDict=inDefArgDict, inLogger=inLogger,
                        inDefArgGSettingsNameStr=inDefArgGSettingsNameStr , inDefArgLoggerNameStr=inDefArgLoggerNameStr)


# Python def - start module function
def PythonStart(inModulePathStr, inDefNameStr, inArgList=None, inArgDict=None, inLogger = None):
    """L+,W+: Импорт модуля и выполнение функции в процессе Оркестратора.

    .. note::

        Импорт модуля inModulePathStr будет происходить каждый раз в вызовом функции PythonStart.

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        Orchestrator.PythonStart(
            inModulePathStr="ModuleToCall.py", # inModulePathStr: Working Directory\\ModuleToCall.py
            inDefNameStr="TestDef")
        # Import module in Orchestrator process and call def "TestDef" from module "ModuleToCall.py"

    :param inModulePathStr: Абсолютный или относительный путь (относительно рабочей директории процесса Оркестратора), по которому расположен импортируемый .py файл
    :param inDefNameStr: Наименование функции в модуле .py
    :param inArgList: Список (list) неименованных аргументов для передачи в функцию. По умолчанию None
    :param inArgDict: Словарь (dict) именованных аргументов для передачи в функцию. По умолчанию None
    :param inLogger: Логгер для фиксации сообщений выполнения функции (опционально)
    """
    inModulePathStr=CrossOS.PathStr(inPathStr=inModulePathStr)
    if inLogger is None: inLogger = OrchestratorLoggerGet()
    if inArgList is None: inArgList=[]
    if inArgDict is None: inArgDict={}
    try:
        lModule=importlib.import_module(inModulePathStr) #Подключить модуль для вызова
        lFunction=getattr(lModule,inDefNameStr) #Найти функцию
        return lFunction(*inArgList,**inArgDict)
    except Exception as e:
        if inLogger: inLogger.exception("Loop activity error: module/function not founded")

# # # # # # # # # # # # # # # # # # # # # # #
# Scheduler
# # # # # # # # # # # # # # # # # # # # # # #
def SchedulerActivityTimeAddWeekly(inTimeHHMMStr="23:55:", inWeekdayList=None, inActivityList=None, inGSettings = None):
    """L+,W+: Добавить активность по расписанию. Допускается указание времени и дней недели, в которые производить запуск.

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        # ВАРИАНТ 1
        def TestDef(inArg1Str):
            pass
        lActivityItem = Orchestrator.ProcessorActivityItemCreate(
            inDef = TestDef,
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = None,
            inArgLoggerStr = None)
        Orchestrator.SchedulerActivityTimeAddWeekly(
            inGSettings = gSettingsDict,
            inTimeHHMMStr = "04:34",
            inWeekdayList=[2,3,4],
            inActivityList = [lActivityItem])
        # Activity will be executed at 04:34 Wednesday (2), thursday (3), friday (4)

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inTimeHHMMStr: Время запуска активности. Допускаются значения от "00:00" до "23:59". Example: "05:29"
    :param inWeekdayList: Список (list) дней недели, в которые выполнять запуск список активностей (ActivityItem list). 0 (понедельник) - 6 (воскресенье). Пример: [0,1,2,3,4]. По умолчанию устанавливается каждый день [0,1,2,3,4,5,6]
    :param inActivityList: Список активностей (ActivityItem list) на исполнение
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inWeekdayList is None: inWeekdayList=[0,1,2,3,4,5,6]
    if inActivityList is None: inActivityList=[]
    Processor.__ActivityListVerify__(inActivityList=inActivityList) # DO VERIFICATION FOR THE inActivityList
    lActivityTimeItemDict = {
        "TimeHH:MMStr": inTimeHHMMStr,  # Time [HH:MM] to trigger activity
        "WeekdayList": inWeekdayList, # List of the weekday index when activity is applicable, Default [1,2,3,4,5,6,7]
        "ActivityList": inActivityList,
        "GUID": None  #    # Will be filled in Orchestrator automatically - is needed for detect activity completion
    }
    inGSettings["SchedulerDict"]["ActivityTimeList"].append(lActivityTimeItemDict)

# # # # # # # # # # # # # # # # # # # # # # #
# RDPSession
# # # # # # # # # # # # # # # # # # # # # # #

def RDPTemplateCreate(inLoginStr, inPasswordStr, inHostStr="127.0.0.1", inPortInt = 3389, inWidthPXInt = 1680,  inHeightPXInt = 1050,
                      inUseBothMonitorBool = False, inDepthBitInt = 32, inSharedDriveList=None, inRedirectClipboardBool=True):
    """L-,W+: Создать шаблон подключения RDP (dict). Данный шаблон далее можно использовать в Orchestrator.RDPSessionConnect

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        lRDPItemDict = Orchestrator.RDPTemplateCreate(
            inLoginStr = "USER_99",
            inPasswordStr = "USER_PASS_HERE",
            inHostStr="127.0.0.1",
            inPortInt = 3389,
            inWidthPXInt = 1680,
            inHeightPXInt = 1050,
            inUseBothMonitorBool = False,
            inDepthBitInt = 32,
            inSharedDriveList=None,
            inRedirectClipboardBool=False)

    :param inLoginStr: Логин учетной записи, на которую будет происходить вход по RDP
    :param inPasswordStr: Пароль учетной записи, на которую будет происходить вход по RDP. !ВНИМАНИЕ! Пароль нигде не сохраняется - конфиденциальность обеспечена
    :param inHostStr: Имя хоста, к которому планируется подключение по RDP. Пример "77.77.22.22"
    :param inPortInt: RDP порт, по которому будет происходить подключение. По умолчанию 3389 (стандартный порт RDP)
    :param inWidthPXInt: Разрешение ширины RDP графической сессии в пикселях. По умолчанию 1680
    :param inHeightPXInt: Разрешение высоты RDP графической сессии в пикселях. По умолчанию 1050
    :param inUseBothMonitorBool: True - Использовать все подключенные мониторы на RDP сессии; False - Использовать только один монитор на подключенной RDP сессии
    :param inDepthBitInt: Глубина цвета на удаленной RDP графической сессии. Допустимые варианты: 32 || 24 || 16 || 15. По умолчанию 32
    :param inSharedDriveList: Перечень общих дисков, доступ к которым предоставить на сторону удаленной RDP сессии. Пример: ["c", "d"]
    :param inRedirectClipboardBool: True - Синхронизировать буфер обмена между сессией Оркестратора и удаленной RDP сессией; False - Не синхронизировать буфер обмена. По умолчанию True (в целях обратной совместимости). !ВНИМАНИЕ! Для учетных записей роботов мы рекомендуем не синхронизировать буфер обмена, так как это может привести к ошибкам роботов, которые работают с клавиатурой и буфером обмена
    :return:
        {
            "Host": inHostStr,  # Адрес хоста, пример "77.77.22.22"
            "Port": str(inPortInt),  # RDP порт, пример "3389"
            "Login": inLoginStr,  # Логин УЗ, пример "test"
            "Password": inPasswordStr,  # Пароль УЗ, пример "test"
            "Screen": {
                "Width": inWidthPXInt,  # Разрешение ширины RDP графической сессии в пикселях. По умолчанию 1680
                "Height": inHeightPXInt,  Разрешение высоты RDP графической сессии в пикселях. По умолчанию 1050
                "FlagUseAllMonitors": inUseBothMonitorBool,  
                "DepthBit": str(inDepthBitInt) 
            },
            "SharedDriveList": inSharedDriveList,  
            "RedirectClipboardBool": True, 
            ###### PROGRAM VARIABLE ############
            "SessionHex": "77777sdfsdf77777dsfdfsf77777777",  
            "SessionIsWindowExistBool": False,
            "SessionIsWindowResponsibleBool": False,
            "SessionIsIgnoredBool": False
        }

    """
    if inSharedDriveList is None: inSharedDriveList = ["c"]
    if inPortInt is None: inPortInt = 3389
    if inRedirectClipboardBool is None: inRedirectClipboardBool = True
    lRDPTemplateDict= {  # Init the configuration item
        "Host": inHostStr,  # Host address, example "77.77.22.22"
        "Port": str(inPortInt),  # RDP Port, example "3389"
        "Login": inLoginStr,  # Login, example "test"
        "Password": inPasswordStr,  # Password, example "test"
        "Screen": {
            "Width": inWidthPXInt,  # Width of the remote desktop in pixels, example 1680
            "Height": inHeightPXInt,  # Height of the remote desktop in pixels, example 1050
            # "640x480" or "1680x1050" or "FullScreen". If Resolution not exists set full screen, example
            "FlagUseAllMonitors": inUseBothMonitorBool,  # True or False, example False
            "DepthBit": str(inDepthBitInt)  # "32" or "24" or "16" or "15", example "32"
        },
        "SharedDriveList": inSharedDriveList,  # List of the Root sesion hard drives, example ["c"],
        "RedirectClipboardBool": inRedirectClipboardBool, # True - share clipboard to RDP; False - else
        ###### Will updated in program ############
        "SessionHex": "77777sdfsdf77777dsfdfsf77777777",  # Hex is created when robot runs, example ""
        "SessionIsWindowExistBool": False,
        # Flag if the RDP window is exist, old name "FlagSessionIsActive". Check every n seconds , example False
        "SessionIsWindowResponsibleBool": False,
        # Flag if RDP window is responsible (recieve commands). Check every nn seconds. If window is Responsible - window is Exist too , example False
        "SessionIsIgnoredBool": False  # Flag to ignore RDP window False - dont ignore, True - ignore, example False
    }
    return lRDPTemplateDict

# TODO Search dublicates in GSettings RDPlist !
# Return list if dublicates
def RDPSessionDublicatesResolve(inGSettings):
    pass
    #for lItemKeyStr in inGSettings["RobotRDPActive"]["RDPList"]:
    #   lItemDict = inGSettings["RobotRDPActive"]["RDPList"][lItemKeyStr]

def RDPSessionConnect(inRDPSessionKeyStr, inRDPTemplateDict=None, inHostStr=None, inPortStr=None, inLoginStr=None, inPasswordStr=None, inGSettings = None, inRedirectClipboardBool=True):
    """L-,W+: Выполнить подключение к RDP и следить за стабильностью соединения со стороны Оркестратора.
    !ВНИМАНИЕ! - Подключение будет проигнорировано, если соединение по таком RDP ключу уже было инициализировано ранее.

    2 способа использования функции:
    ВАРИАНТ 1 (ОСНОВНОЙ): inGSettings, inRDPSessionKeyStr, inRDPTemplateDict. Для получения inRDPTemplateDict см. функцию Orchestrator.RDPTemplateCreate
    ВАРИАНТ 2 (ОБРАТНАЯ СОВМЕСТИМОСТЬ ДО ВЕРСИИ 1.1.20): inGSettings, inRDPSessionKeyStr, inHostStr, inPortStr, inLoginStr, inPasswordStr

    .. code-block:: python

        # ПРИМЕР (ВАРИАНТ 1)
        from pyOpenRPA import Orchestrator

        lRDPItemDict = Orchestrator.RDPTemplateCreate(
            inLoginStr = "USER_99",
            inPasswordStr = "USER_PASS_HERE", inHostStr="127.0.0.1", inPortInt = 3389, inWidthPXInt = 1680,
            inHeightPXInt = 1050, inUseBothMonitorBool = False, inDepthBitInt = 32, inSharedDriveList=None)
        Orchestrator.RDPSessionConnect(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inRDPTemplateDict = lRDPItemDict)
        # Orchestrator will create RDP session by the lRDPItemDict configuration
    
    :param inRDPSessionKeyStr: Ключ RDP сессии - необходим для дальнейшей идентификации
    :param inRDPTemplateDict: Конфигурационный словарь (dict) RDP подключения (см. функцию Orchestrator.RDPTemplateCreate)
    :param inLoginStr: Логин учетной записи, на которую будет происходить вход по RDP. Обратная совместимость до версии v 1.1.20. Мы рекомендуем использовать inRDPTemplateDict (см. функцию Orchestrator.RDPTemplateCreate)
    :param inPasswordStr: Пароль учетной записи, на которую будет происходить вход по RDP. !ВНИМАНИЕ! Пароль нигде не сохраняется - конфиденциальность обеспечена. Обратная совместимость до версии v 1.1.20. Мы рекомендуем использовать inRDPTemplateDict (см. функцию Orchestrator.RDPTemplateCreate)
    :param inHostStr: Имя хоста, к которому планируется подключение по RDP. Пример "77.77.22.22". Обратная совместимость до версии v 1.1.20. Мы рекомендуем использовать inRDPTemplateDict (см. функцию Orchestrator.RDPTemplateCreate)
    :param inPortInt: RDP порт, по которому будет происходить подключение. По умолчанию 3389 (стандартный порт RDP). Обратная совместимость до версии v 1.1.20. Мы рекомендуем использовать inRDPTemplateDict (см. функцию Orchestrator.RDPTemplateCreate)
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inRedirectClipboardBool: True - Синхронизировать буфер обмена между сессией Оркестратора и удаленной RDP сессией; False - Не синхронизировать буфер обмена. По умолчанию True (в целях обратной совместимости). !ВНИМАНИЕ! Для учетных записей роботов мы рекомендуем не синхронизировать буфер обмена, так как это может привести к ошибкам роботов, которые работают с клавиатурой и буфером обмена
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionConnect, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr, "inRDPTemplateDict":inRDPTemplateDict, "inHostStr": inHostStr, "inPortStr": inPortStr,
                    "inLoginStr": inLoginStr, "inPasswordStr": inPasswordStr, "inRedirectClipboardBool": inRedirectClipboardBool},  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else: # In processor - do execution
        # Var 1 - if RDPTemplateDict is input
        lRDPConfigurationItem=inRDPTemplateDict
        # Var 2 - backward compatibility
        if lRDPConfigurationItem is None:
            lRDPConfigurationItem = RDPTemplateCreate(inLoginStr=inLoginStr, inPasswordStr=inPasswordStr,
                  inHostStr=inHostStr, inPortInt = int(inPortStr), inRedirectClipboardBool=inRedirectClipboardBool)            # ATTENTION - dont connect if RDP session is exist
        # Start the connect
        if inRDPSessionKeyStr not in inGSettings["RobotRDPActive"]["RDPList"]:
            inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr] = lRDPConfigurationItem # Add item in RDPList
            Connector.Session(lRDPConfigurationItem) # Create the RDP session
            Connector.SystemRDPWarningClickOk()  # Click all warning messages
        else:
            if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP session was not created because it is alredy exists in the RDPList. Use RDPSessionReconnect if you want to update RDP configuration.")
    return True

def RDPSessionDisconnect(inRDPSessionKeyStr, inBreakTriggerProcessWOExeList = None, inGSettings = None):
    """L-,W+: Выполнить отключение RDP сессии и прекратить мониторить его активность.

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        Orchestrator.RDPSessionDisconnect(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey")
        # Orchestrator will disconnect RDP session and will stop to monitoring current RDP

    :param inRDPSessionKeyStr: Ключ RDP сессии - необходим для дальнейшей идентификации
    :param inBreakTriggerProcessWOExeList: Список процессов, наличие которых в диспетчере задач приведет к прерыванию задачи по остановке RDP соединения. Пример ["notepad"]
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inBreakTriggerProcessWOExeList is None: inBreakTriggerProcessWOExeList = []
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionDisconnect, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr, "inBreakTriggerProcessWOExeList": inBreakTriggerProcessWOExeList },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else: # In processor - do execution
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        if lSessionHex:
            lProcessListResult = {"ProcessWOExeList":[],"ProcessDetailList":[]}
            if len(inBreakTriggerProcessWOExeList) > 0:
                lProcessListResult = ProcessListGet(inProcessNameWOExeList=inBreakTriggerProcessWOExeList)  # Run the task manager monitor
            if len(lProcessListResult["ProcessWOExeList"]) == 0: # Start disconnect if no process exist
                inGSettings["RobotRDPActive"]["RDPList"].pop(inRDPSessionKeyStr,None)
                Connector.SessionClose(inSessionHexStr=lSessionHex)
                Connector.SystemRDPWarningClickOk()  # Click all warning messages
    return True

def RDPSessionReconnect(inRDPSessionKeyStr, inRDPTemplateDict=None, inGSettings = None):
    """L-,W+: Выполнить переподключение RDP сессии и продолжить мониторить его активность.

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        lRDPItemDict = Orchestrator.RDPTemplateCreate(
            inLoginStr = "USER_99",
            inPasswordStr = "USER_PASS_HERE", inHostStr="127.0.0.1", inPortInt = 3389, inWidthPXInt = 1680,
            inHeightPXInt = 1050, inUseBothMonitorBool = False, inDepthBitInt = 32, inSharedDriveList=None)
        Orchestrator.RDPSessionReconnect(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inRDPTemplateDict = inRDPTemplateDict)
        # Orchestrator will reconnect RDP session and will continue to monitoring current RDP

    :param inRDPSessionKeyStr: Ключ RDP сессии - необходим для дальнейшей идентификации
    :param inRDPTemplateDict: Конфигурационный словарь (dict) RDP подключения (см. функцию Orchestrator.RDPTemplateCreate)
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionReconnect, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr, "inRDPTemplateDict":inRDPTemplateDict },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lRDPConfigurationItem = inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr]
        RDPSessionDisconnect(inGSettings = inGSettings, inRDPSessionKeyStr=inRDPSessionKeyStr) # Disconnect the RDP 2021 02 22 minor fix by Ivan Maslov
        # Replace Configuration item if inRDPTemplateDict exists
        if inRDPTemplateDict is not None: lRDPConfigurationItem=inRDPTemplateDict
        # Add item in RDPList
        inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr] = lRDPConfigurationItem
        # Create the RDP session
        Connector.Session(lRDPConfigurationItem)
    return True

def RDPSessionMonitorStop(inRDPSessionKeyStr, inGSettings = None):
    """L-,W+: Прекратить мониторить активность RDP соединения со стороны Оркестратора. Данная функция не уничтожает активное RDP соединение.
    
    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        Orchestrator.RDPSessionMonitorStop(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey")
        # Orchestrator will stop the RDP monitoring

    :param inRDPSessionKeyStr: Ключ RDP сессии - необходим для дальнейшей идентификации
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lResult = True
    inGSettings["RobotRDPActive"]["RDPList"].pop(inRDPSessionKeyStr,None) # Remove item from RDPList
    return lResult

def RDPSessionLogoff(inRDPSessionKeyStr, inBreakTriggerProcessWOExeList = None, inGSettings = None):
    """L-,W+: Выполнить отключение (logoff) на RDP сессии и прекратить мониторить активность со стороны Оркестратора.

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        Orchestrator.RDPSessionLogoff(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inBreakTriggerProcessWOExeList = ['Notepad'])
        # Orchestrator will logoff the RDP session

    
    :param inRDPSessionKeyStr: Ключ RDP сессии - необходим для дальнейшей идентификации
    :param inBreakTriggerProcessWOExeList: Список процессов, наличие которых в диспетчере задач приведет к прерыванию задачи по остановке RDP соединения. Пример ["notepad"]
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :return: True - Отключение прошло успешно; False - были зафиксированы ошибки при отключении.
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inBreakTriggerProcessWOExeList is None: inBreakTriggerProcessWOExeList = []
    lResult = True
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionLogoff, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr, "inBreakTriggerProcessWOExeList": inBreakTriggerProcessWOExeList },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lCMDStr = "shutdown -L" # CMD logoff command
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        if lSessionHex:
            lProcessListResult = {"ProcessWOExeList":[],"ProcessDetailList":[]}
            if len(inBreakTriggerProcessWOExeList) > 0:
                lProcessListResult = ProcessListGet(inProcessNameWOExeList=inBreakTriggerProcessWOExeList)  # Run the task manager monitor
            if len(lProcessListResult["ProcessWOExeList"]) == 0: # Start logoff if no process exist
                # Run CMD - dont crosscheck because CMD dont return value to the clipboard when logoff
                Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="RUN", inLogger=inGSettings["Logger"], inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
                inGSettings["RobotRDPActive"]["RDPList"].pop(inRDPSessionKeyStr,None) # Remove item from RDPList
    return lResult

def RDPSessionResponsibilityCheck(inRDPSessionKeyStr, inGSettings = None):
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionResponsibilityCheck, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lRDPConfigurationItem = inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr] # Get the alias
        # set the fullscreen
        # ATTENTION!!! Session hex can be updated!!!
        Connector.SessionScreenFull(inSessionHex=lRDPConfigurationItem["SessionHex"], inLogger=inGSettings["Logger"], inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
        time.sleep(1)
        # Check RDP responsibility
        lDoCheckResponsibilityBool = True
        lDoCheckResponsibilityCountMax = 20
        lDoCheckResponsibilityCountCurrent = 0
        while lDoCheckResponsibilityBool:
            # Check if counter is exceed - raise exception
            if lDoCheckResponsibilityCountCurrent >= lDoCheckResponsibilityCountMax:
                pass
                #raise ConnectorExceptions.SessionWindowNotResponsibleError("Error when initialize the RDP session - RDP window is not responding!")
            # Check responding
            lDoCheckResponsibilityBool = not Connector.SystemRDPIsResponsible(inSessionHexStr = lRDPConfigurationItem["SessionHex"])
            # Wait if is not responding
            if lDoCheckResponsibilityBool:
                time.sleep(3)
            # increase the couter
            lDoCheckResponsibilityCountCurrent+=1
    return True

def RDPSessionProcessStartIfNotRunning(inRDPSessionKeyStr, inProcessNameWEXEStr, inFilePathStr, inFlagGetAbsPathBool=True, inGSettings = None):
    """L-,W+: Выполнить запуск процесса на RDP сессии через графические UI инструменты (без Агента). 

    !ВНИМАНИЕ! Данная функция может работать нестабильно из-за использования графических элементов UI при работе с RDP. Мы рекомендуем использовать конструкцию взаимодействия Оркестратора с Агентом.

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        Orchestrator.RDPSessionProcessStartIfNotRunning(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inProcessNameWEXEStr = 'Notepad.exe',
            inFilePathStr = "path\\to\the\\executable\\file.exe"
            inFlagGetAbsPathBool = True)
        # Orchestrator will start the process in RDP session

    :param inRDPSessionKeyStr: Ключ RDP сессии - необходим для дальнейшей идентификации
    :param inProcessNameWEXEStr: Наименование процесса с расширением .exe (WEXE - WITH EXE - С EXE). Параметр позволяет не допустить повторного запуска процесса, если он уже был запущен. Example: "Notepad.exe"
    :param inFilePathStr: Путь к файлу запуска процесса на стороне RDP сессии
    :param inFlagGetAbsPathBool: True - Преобразовать относительный путь inFilePathStr в абсолютный с учетом рабочей директории Оркестратора; False - Не выполнять преобразований
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    lResult = True
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lActivityItem = {
            "Def": RDPSessionProcessStartIfNotRunning, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr,  "inProcessNameWEXEStr": inProcessNameWEXEStr, "inFilePathStr": inFilePathStr, "inFlagGetAbsPathBool": inFlagGetAbsPathBool },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lActivityItem)
    else:
        lCMDStr = CMDStr.ProcessStartIfNotRunning(inProcessNameWEXEStr, inFilePathStr, inFlagGetAbsPath= inFlagGetAbsPathBool)
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        # Run CMD
        if lSessionHex:
            Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="CROSSCHECK", inLogger=inGSettings["Logger"],
                                    inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult

def RDPSessionCMDRun(inRDPSessionKeyStr, inCMDStr, inModeStr="CROSSCHECK", inGSettings = None):
    """L-,W+: Отправить CMD команду на удаленную сесиию через RDP окно (без Агента).

    !ВНИМАНИЕ! Данная функция может работать нестабильно из-за использования графических элементов UI при работе с RDP. Мы рекомендуем использовать конструкцию взаимодействия Оркестратора с Агентом.

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        lResultDict = Orchestrator.RDPSessionCMDRun(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inModeStr = 'LISTEN')
        # Orchestrator will send CMD to RDP and return the result (see return section)
    
    :param inRDPSessionKeyStr: Ключ RDP сессии - необходим для дальнейшей идентификации
    :param inCMDStr: Команда CMD, которую отправить на удаленную сессию
    :param inModeStr: По умолчанию "CROSSCHECK". Варианты:
        "LISTEN" - Получить результат выполнения операции. Внимание! необходим общий буфер обмена с сессией Оркестратора!
        "CROSSCHECK" - Выполнить проверку, что операция была выполнена (без получения результата отработки CMD команды). Внимание! необходим общий буфер обмена с сессией Оркестратора!
        "RUN" - Не получать результат и не выполнять проверку
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :return: Результат выполнения операции в соответсвии с параметрами инициализации функции. Выходная структура:
         {
          "OutStr": <> # Результат выполнения CMD (если inModeStr = "LISTEN")
          "IsResponsibleBool": True|False # True - RDP приняло команду; False - обратная связь не была получена (если inModeStr = "CROSSCHECK")  
        }
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lResult = {
        "OutStr": None,  # Result string
        "IsResponsibleBool": False  # Flag is RDP is responsible - works only when inModeStr = CROSSCHECK
    }
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lProcessorActivityDict = {
            "Def": RDPSessionCMDRun, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr,  "inCMDStr": inCMDStr, "inModeStr": inModeStr },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lProcessorActivityDict)
    else:
        #lResult = True
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        # Run CMD
        if lSessionHex:
            lResult = Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=inCMDStr, inModeStr=inModeStr, inLogger=inGSettings["Logger"],
                                    inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult

def RDPSessionProcessStop(inRDPSessionKeyStr, inProcessNameWEXEStr, inFlagForceCloseBool, inGSettings = None):
    """L-,W+: Отправка CMD команды в RDP окне на остановку процесса (без Агента).

    !ВНИМАНИЕ! Данная функция может работать нестабильно из-за использования графических элементов UI при работе с RDP. Мы рекомендуем использовать конструкцию взаимодействия Оркестратора с Агентом.

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        lResultDict = Orchestrator.RDPSessionProcessStop(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inProcessNameWEXEStr = 'notepad.exe',
            inFlagForceCloseBool = True)
        # Orchestrator will send CMD to RDP and return the result (see return section)

    
    :param inRDPSessionKeyStr: Ключ RDP сессии - необходим для дальнейшей идентификации
    :param inProcessNameWEXEStr: Наименование процесса, который требуется выключить с расширением .exe (WEXE - WITH EXE - С EXE). Пример: "Notepad.exe"
    :param inFlagForceCloseBool: True - Принудительное отключение. False - Отправка сигнала на безопасное отключение (если процесс поддерживает)
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionProcessStop, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr,  "inProcessNameWEXEStr": inProcessNameWEXEStr, "inFlagForceCloseBool": inFlagForceCloseBool },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lResult = True
        lCMDStr = f'taskkill /im "{inProcessNameWEXEStr}" /fi "username eq %USERNAME%"'
        if inFlagForceCloseBool:
            lCMDStr+= " /F"
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        # Run CMD
        if lSessionHex:
            Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="CROSSCHECK", inLogger=inGSettings["Logger"], inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult

def RDPSessionFileStoredSend(inRDPSessionKeyStr, inHostFilePathStr, inRDPFilePathStr, inGSettings = None):
    """L-,W+: Отправка файла со стороны Оркестратора на сторону RDP сессии через UI инструменты RDP окна (без Агента).

    !ВНИМАНИЕ! Данная функция может работать нестабильно из-за использования графических элементов UI при работе с RDP. Мы рекомендуем использовать конструкцию взаимодействия Оркестратора с Агентом.

    !ВНИМАНИЕ! Для работы функции требуется открыть доступ по RDP к тем дискам, с которых будет производится копирование файла.

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        lResultDict = Orchestrator.RDPSessionFileStoredSend(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inHostFilePathStr = "TESTDIR\\Test.py",
            inRDPFilePathStr = "C:\\RPA\\TESTDIR\\Test.py")
        # Orchestrator will send CMD to RDP and return the result (see return section)

    :param inRDPSessionKeyStr: Ключ RDP сессии - необходим для дальнейшей идентификации
    :param inHostFilePathStr: Откуда взять файл. Относительный или абсолютный путь к файлу на стороне Оркестратора. Пример: "TESTDIR\\Test.py"
    :param inRDPFilePathStr: Куда скопировать файл. !Абсолютный! путь на стороне RDP сессии. Пример: "C:\\RPA\\TESTDIR\\Test.py"
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionFileStoredSend, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr,  "inHostFilePathStr": inHostFilePathStr, "inRDPFilePathStr": inRDPFilePathStr },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lResult = True
        lCMDStr = CMDStr.FileStoredSend(inHostFilePath = inHostFilePathStr, inRDPFilePath = inRDPFilePathStr)
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr, {}).get("SessionHex", None)
        #lSessionHex = inGlobalDict["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr]["SessionHex"]
        # Run CMD
        if lSessionHex:
            Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="LISTEN", inClipboardTimeoutSec = 120, inLogger=inGSettings["Logger"], inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult

def RDPSessionFileStoredRecieve(inRDPSessionKeyStr, inRDPFilePathStr, inHostFilePathStr, inGSettings = None):
    """L-,W+: Получение файла со стороны RDP сессии на сторону Оркестратора через UI инструменты RDP окна (без Агента).

    !ВНИМАНИЕ! Данная функция может работать нестабильно из-за использования графических элементов UI при работе с RDP. Мы рекомендуем использовать конструкцию взаимодействия Оркестратора с Агентом.

    !ВНИМАНИЕ! Для работы функции требуется открыть доступ по RDP к тем дискам, с которых будет производится копирование файла.

    .. code-block:: python

        # ПРИМЕР
        from pyOpenRPA import Orchestrator

        lResultDict = Orchestrator.RDPSessionFileStoredRecieve(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inHostFilePathStr = "TESTDIR\\Test.py",
            inRDPFilePathStr = "C:\\RPA\\TESTDIR\\Test.py")
        # Orchestrator will send CMD to RDP and return the result (see return section)

    :param inRDPSessionKeyStr: Ключ RDP сессии - необходим для дальнейшей идентификации
    :param inRDPFilePathStr: Откуда скопировать файл. !Абсолютный! путь на стороне RDP сессии. Пример: "C:\\RPA\\TESTDIR\\Test.py"
    :param inHostFilePathStr: Куда скопировать файл. Относительный или абсолютный путь к файлу на стороне Оркестратора. Пример: "TESTDIR\\Test.py"
    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionFileStoredRecieve, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr, "inRDPFilePathStr": inRDPFilePathStr, "inHostFilePathStr": inHostFilePathStr },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lResult = True
        lCMDStr = CMDStr.FileStoredRecieve(inRDPFilePath = inRDPFilePathStr, inHostFilePath = inHostFilePathStr)
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        # Run CMD
        if lSessionHex:
            Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="LISTEN", inClipboardTimeoutSec = 120, inLogger=inGSettings["Logger"], inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult

# # # # # # # # # # # # # # # # # # # # # # #
# # # # # Start orchestrator
# # # # # # # # # # # # # # # # # # # # # # #

#HIDDEN Interval gSettings auto cleaner def to clear some garbage.
def GSettingsAutocleaner(inGSettings=None):
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    while True:
        time.sleep(inGSettings["Autocleaner"]["IntervalSecFloat"])  # Wait for the next iteration
        lL = inGSettings["Logger"]
        lNowDatetime = datetime.datetime.now() # Get now time
        # Clean old items in Client > Session > TechnicalSessionGUIDCache
        lTechnicalSessionGUIDCacheNew = {}
        for lItemKeyStr in inGSettings["Client"]["Session"]["TechnicalSessionGUIDCache"]:
            lItemValue = inGSettings["Client"]["Session"]["TechnicalSessionGUIDCache"][lItemKeyStr]
            if (lNowDatetime - lItemValue["InitDatetime"]).total_seconds() < inGSettings["Client"]["Session"]["LifetimeSecFloat"]: # Add if lifetime is ok
                lTechnicalSessionGUIDCacheNew[lItemKeyStr]=lItemValue # Lifetime is ok - set
            else:
                if lL: lL.debug(f"Client > Session > TechnicalSessionGUIDCache > lItemKeyStr: Lifetime is expired. Remove from gSettings")  # Info
        inGSettings["Client"]["Session"]["TechnicalSessionGUIDCache"] = lTechnicalSessionGUIDCacheNew # Set updated Cache
        # Clean old items in AgentActivityReturnDict > GUIDStr > ReturnedByDatetime
        lTechnicalAgentActivityReturnDictNew = {}
        for lItemKeyStr in inGSettings["AgentActivityReturnDict"]:
            lItemValue = inGSettings["AgentActivityReturnDict"][lItemKeyStr]
            if (lNowDatetime - lItemValue["ReturnedByDatetime"]).total_seconds() < inGSettings["Autocleaner"]["AgentActivityReturnLifetimeSecFloat"]: # Add if lifetime is ok
                lTechnicalAgentActivityReturnDictNew[lItemKeyStr]=lItemValue # Lifetime is ok - set
            else:
                if lL: lL.debug(f"AgentActivityReturnDict lItemKeyStr: Lifetime is expired. Remove from gSettings")  # Info
        inGSettings["AgentActivityReturnDict"] = lTechnicalAgentActivityReturnDictNew # Set updated Cache
    # # # # # # # # # # # # # # # # # # # # # # # # # #

from .. import __version__ # Get version from the package

def Start(inDumpRestoreBool = True, inRunAsAdministratorBool = True):
    Orchestrator(inDumpRestoreBool = True, inRunAsAdministratorBool = True)

def Orchestrator(inGSettings=None, inDumpRestoreBool = True, inRunAsAdministratorBool = True):
    """L+,W+: Инициализация ядра Оркестратора (всех потоков)

    :param inGSettings: Глобальный словарь настроек Оркестратора (синглтон)
    :param inDumpRestoreBool: True - Восстановить информацию о RDP сессиях и StorageDict; False - не восстанавливать
    :param inRunAsAdministratorBool: True - Проверить права администратратора и обеспечить их; False - Не обеспечивать права администратора
    """
    lL = inGSettings["Logger"]
    # https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script
    License.ConsoleVerify()
    if not OrchestratorIsAdmin() and inRunAsAdministratorBool==True and CrossOS.IS_WINDOWS_BOOL:
        OrchestratorRerunAsAdmin()
    else:
        # Code of your program here
        inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
        #mGlobalDict = Settings.Settings(sys.argv[1])
        global gSettingsDict
        gSettingsDict = inGSettings # Alias for old name in alg
        inGSettings["VersionStr"] = __version__
        #Logger alias
        lL = gSettingsDict["Logger"]

        Processor.gSettingsDict = gSettingsDict
        Timer.gSettingsDict = gSettingsDict
        Timer.Processor.gSettingsDict = gSettingsDict
        Server.gSettingsDict = gSettingsDict
        Server.ProcessorOld.gSettingsDict = gSettingsDict # Backward compatibility

        #Backward compatibility - restore in Orc def if old def
        if inDumpRestoreBool == True:
            OrchestratorSessionRestore(inGSettings=inGSettings)

        # Init SettingsUpdate defs from file list (after RDP restore)
        lSettingsUpdateFilePathList = gSettingsDict.get("OrchestratorStart", {}).get("DefSettingsUpdatePathList",[])
        lSubmoduleFunctionName = "SettingsUpdate"
        lSettingsPath = "\\".join(os.path.join(os.getcwd(), __file__).split("\\")[:-1])
        for lModuleFilePathItem in lSettingsUpdateFilePathList:  # Import defs with try catch
            try:  # Try to init - go next if error and log in logger
                lModuleName = lModuleFilePathItem[0:-3]
                lFileFullPath = os.path.join(lSettingsPath, lModuleFilePathItem)
                lTechSpecification = importlib.util.spec_from_file_location(lModuleName, lFileFullPath)
                lTechModuleFromSpec = importlib.util.module_from_spec(lTechSpecification)
                lTechSpecificationModuleLoader = lTechSpecification.loader.exec_module(lTechModuleFromSpec)
                if lSubmoduleFunctionName in dir(lTechModuleFromSpec):
                    # Run SettingUpdate function in submodule
                    getattr(lTechModuleFromSpec, lSubmoduleFunctionName)(gSettingsDict)
            except Exception as e:
                if lL: lL.exception(f"Error when init .py file in orchestrator '{lModuleFilePathItem}'. Exception is below:")

        # Turn on backward compatibility
        BackwardCompatibility.Update(inGSettings= gSettingsDict)

        # Append Orchestrator def to ProcessorDictAlias
        lModule = sys.modules[__name__]
        lModuleDefList = dir(lModule)
        for lItemDefNameStr in lModuleDefList:
            # Dont append alias for defs Orchestrator and ___deprecated_orchestrator_start__
            if lItemDefNameStr not in ["Orchestrator", "___deprecated_orchestrator_start__"]:
                lItemDef = getattr(lModule,lItemDefNameStr)
                if callable(lItemDef): inGSettings["ProcessorDict"]["AliasDefDict"][lItemDefNameStr]=lItemDef

        #Load all defs from sys.modules
        ActivityItemDefAliasModulesLoad()

        #Инициализация настроечных параметров
        gSettingsDict["ServerDict"]["WorkingDirectoryPathStr"] = os.getcwd() # Set working directory in g settings

        #Инициализация сервера (инициализация всех интерфейсов)
        lListenDict = gSettingsDict.get("ServerDict",{}).get("ListenDict",{})
        for lItemKeyStr in lListenDict:
            lItemDict = lListenDict[lItemKeyStr]
            lThreadServer = Server.RobotDaemonServer(lItemKeyStr, gSettingsDict)
            lThreadServer.start()
            gSettingsDict["ServerDict"]["ServerThread"] = lThreadServer
            lItemDict["ServerInstance"] = lThreadServer

        # Init the RobotScreenActive in another thread
        lRobotScreenActiveThread = threading.Thread(target= Monitor.CheckScreen)
        lRobotScreenActiveThread.daemon = True # Run the thread in daemon mode.
        lRobotScreenActiveThread.start() # Start the thread execution.
        if lL: lL.info("Модуль активного рабочего стола инициализирован")  #Logging

        # Init the RobotRDPActive in another thread
        lRobotRDPThreadControlDict = {"ThreadExecuteBool":True} # inThreadControlDict = {"ThreadExecuteBool":True}
        lRobotRDPActiveThread = threading.Thread(target= RobotRDPActive.RobotRDPActive, kwargs={"inGSettings":gSettingsDict, "inThreadControlDict":lRobotRDPThreadControlDict})
        lRobotRDPActiveThread.daemon = True # Run the thread in daemon mode.
        lRobotRDPActiveThread.start() # Start the thread execution.
        if lL: lL.info("Модуль подключения по РДП инициализированн")  #Logging

        # Init autocleaner in another thread
        lAutocleanerThread = threading.Thread(target= GSettingsAutocleaner, kwargs={"inGSettings":gSettingsDict})
        lAutocleanerThread.daemon = True # Run the thread in daemon mode.
        lAutocleanerThread.start() # Start the thread execution.
        if lL: lL.info("Модуль автоочистки инициализирован")  #Logging

        # Set flag that orchestrator has been initialized
        inGSettings["HiddenIsOrchestratorInitializedBool"] = True

        # Orchestrator start activity
        if lL: lL.info("Исполнение списка Активностей")  #Logging
        for lActivityItem in gSettingsDict["OrchestratorStart"]["ActivityList"]:
            # Processor.ActivityListOrDict(lActivityItem)
            Processor.ActivityListExecute(inGSettings=gSettingsDict,inActivityList=[BackwardCompatibility.v1_2_0_ProcessorOld2NewActivityDict(lActivityItem)])
        # Processor thread
        lProcessorThread = threading.Thread(target= Processor.ProcessorRunSync, kwargs={"inGSettings":gSettingsDict, "inRobotRDPThreadControlDict":lRobotRDPThreadControlDict})
        lProcessorThread.daemon = True # Run the thread in daemon mode.
        lProcessorThread.start() # Start the thread execution.
        if lL: lL.info("Модуль процессора инициализирован")  #Logging

        # Processor monitor thread
        lProcessorMonitorThread = threading.Thread(target= Processor.ProcessorMonitorRunSync, kwargs={"inGSettings":gSettingsDict})
        lProcessorMonitorThread.daemon = True # Run the thread in daemon mode.
        lProcessorMonitorThread.start() # Start the thread execution.
        if lL: lL.info("Модуль контроля процессора инициализирован")  #Logging

        # Scheduler loop
        lSchedulerThread = threading.Thread(target= __deprecated_orchestrator_loop__)
        lSchedulerThread.daemon = True # Run the thread in daemon mode.
        lSchedulerThread.start() # Start the thread execution.
        if lL: lL.info("Модуль расписания (старая версия) инициализирован")  #Logging

        # Schedule (new) loop
        lScheduleThread = threading.Thread(target= __schedule_loop__)
        lScheduleThread.daemon = True # Run the thread in daemon mode.
        lScheduleThread.start() # Start the thread execution.
        if lL: lL.info("Модуль расписания (новая версия) инициализирован")  #Logging

        # Restore state for process
        for lProcessKeyTuple in inGSettings["ManagersProcessDict"]:
            lProcess = inGSettings["ManagersProcessDict"][lProcessKeyTuple]
            lProcess.StatusCheckIntervalRestore()
            lThread = threading.Thread(target= lProcess.StatusRestore)
            lThread.start()

        # Init debug thread (run if "init_dubug" file exists)
        Debugger.LiveDebugCheckThread(inGSettings=GSettingsGet())

def __schedule_loop__():
    while True:
        schedule.run_pending()
        time.sleep(3)

# Backward compatibility below to 1.2.7
def __deprecated_orchestrator_loop__():
    lL = OrchestratorLoggerGet()
    inGSettings = GSettingsGet()
    lDaemonLoopSeconds = gSettingsDict["SchedulerDict"]["CheckIntervalSecFloat"]
    lDaemonActivityLogDict = {}  # Словарь отработанных активностей, ключ - кортеж (<activityType>, <datetime>, <processPath || processName>, <processArgs>)
    lDaemonLastDateTime = datetime.datetime.now()
    gDaemonActivityLogDictRefreshSecInt = 10  # The second period for clear lDaemonActivityLogDict from old items
    gDaemonActivityLogDictLastTime = time.time()  # The second perioad for clean lDaemonActivityLogDict from old items
    while True:
        try:
            lCurrentDateTime = datetime.datetime.now()
            # Циклический обход правил
            lFlagSearchActivityType = True
            # Periodically clear the lDaemonActivityLogDict
            if time.time() - gDaemonActivityLogDictLastTime >= gDaemonActivityLogDictRefreshSecInt:
                gDaemonActivityLogDictLastTime = time.time()  # Update the time
                for lIndex, lItem in enumerate(lDaemonActivityLogDict):
                    if lItem["ActivityEndDateTime"] and lCurrentDateTime <= lItem["ActivityEndDateTime"]:
                        pass
                        # Activity is actual - do not delete now
                    else:
                        # remove the activity - not actual
                        lDaemonActivityLogDict.pop(lIndex, None)
            lIterationLastDateTime = lDaemonLastDateTime  # Get current datetime before iterator (need for iterate all activities in loop)
            # Iterate throught the activity list
            for lIndex, lItem in enumerate(gSettingsDict["SchedulerDict"]["ActivityTimeList"]):
                try:
                    # Prepare GUID of the activity
                    lGUID = None
                    if "GUID" in lItem and lItem["GUID"]:
                        lGUID = lItem["GUID"]
                    else:
                        lGUID = str(uuid.uuid4())
                        lItem["GUID"] = lGUID

                    # Проверка дней недели, в рамках которых можно запускать активность
                    lItemWeekdayList = lItem.get("WeekdayList", [0, 1, 2, 3, 4, 5, 6])
                    if lCurrentDateTime.weekday() in lItemWeekdayList:
                        if lFlagSearchActivityType:
                            #######################################################################
                            # Branch 1 - if has TimeHH:MM
                            #######################################################################
                            if "TimeHH:MMStr" in lItem:
                                # Вид активности - запуск процесса
                                # Сформировать временной штамп, относительно которого надо будет проверять время
                                # часовой пояс пока не учитываем
                                lActivityDateTime = datetime.datetime.strptime(lItem["TimeHH:MMStr"], "%H:%M")
                                lActivityDateTime = lActivityDateTime.replace(year=lCurrentDateTime.year,
                                                                              month=lCurrentDateTime.month,
                                                                              day=lCurrentDateTime.day)
                                # Убедиться в том, что время наступило
                                if (
                                        lActivityDateTime >= lDaemonLastDateTime and
                                        lCurrentDateTime >= lActivityDateTime):
                                    # Log info about activity
                                    if lL: lL.info(
                                        f"Модуль расписания (старая версия):: Активность была инициализирована в отдельном потоке. В целях информационной безопасности параметры недоступны для просмотра")  # Logging
                                    # Do the activity
                                    lThread = threading.Thread(target=Processor.ActivityListExecute,
                                                               kwargs={"inGSettings": inGSettings,
                                                                       "inActivityList": lItem["ActivityList"]})
                                    lThread.start()
                                    lIterationLastDateTime = datetime.datetime.now()  # Set the new datetime for the new processor activity
                except Exception as e:
                    if lL: lL.exception(
                        f"Модуль расписания (старая версия): Ошибка. Элемент ActivityTimeItem: {lItem}")
            lDaemonLastDateTime = lIterationLastDateTime  # Set the new datetime for the new processor activity
            # Уснуть до следующего прогона
            time.sleep(lDaemonLoopSeconds)
        except Exception as e:
            if lL: lL.exception(f"Модуль расписания (старая версия): Глобальная ошибка инициализации - обратитесь в тех. поддержку pyOpenRPA")

# Backward compatibility below to 1.2.0
def __deprecated_orchestrator_start__():
    lSubmoduleFunctionName = "Settings"
    lFileFullPath = sys.argv[1]
    lModuleName = (lFileFullPath.split("\\")[-1])[0:-3]
    lTechSpecification = importlib.util.spec_from_file_location(lModuleName, lFileFullPath)
    lTechModuleFromSpec = importlib.util.module_from_spec(lTechSpecification)
    lTechSpecificationModuleLoader = lTechSpecification.loader.exec_module(lTechModuleFromSpec)
    gSettingsDict = None
    if lSubmoduleFunctionName in dir(lTechModuleFromSpec):
        # Run SettingUpdate function in submodule
        gSettingsDict = getattr(lTechModuleFromSpec, lSubmoduleFunctionName)()
    #################################################
    Orchestrator(inGSettings=gSettingsDict) # Call the orchestrator
