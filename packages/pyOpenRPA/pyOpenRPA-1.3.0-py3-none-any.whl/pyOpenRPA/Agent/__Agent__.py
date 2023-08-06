import threading, socket, getpass, sys, uuid, subprocess, base64, psutil, getpass, time
from . import O2A, A2O # Data flow Orchestrator To Agent
from . import Processor # Processor Queue
from ..Tools import Usage
from ..Tools import License
from pyOpenRPA.Tools import CrossOS
if CrossOS.IS_WINDOWS_BOOL: from subprocess import CREATE_NEW_CONSOLE # Flag to create new process in another CMD
if CrossOS.IS_LINUX_BOOL: pass

import os

gSettings = None

# Create binary file by the base64 string (safe for JSON transmition)
def OSFileBinaryDataBase64StrCreate(inFilePathStr, inFileDataBase64Str,inGSettings = None):
    """L+,W+: Создать бинарный файл на стороне Агента по полученной строке в формате base64 (формат безопасен для передачи по JSON протоколу)

    """
    inFilePathStr = CrossOS.PathStr(inPathStr=inFilePathStr)
    lFile = open(inFilePathStr, "wb")
    lFile.write(base64.b64decode(inFileDataBase64Str))
    lFile.close()
    lL = inGSettings.get("Logger", None) if type(inGSettings) is dict else None
    lMessageStr = f"АГЕНТ: бинарный файл {inFilePathStr} создан успешно"
    if lL: lL.info(lMessageStr)
    A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])

# Append binary file by the base64 string (safe for JSON transmition)
def OSFileBinaryDataBase64StrAppend(inFilePathStr, inFileDataBase64Str,inGSettings = None):
    """L+,W+: Create binary file by the base64 string (safe for JSON transmition)

    """
    inFilePathStr = CrossOS.PathStr(inPathStr=inFilePathStr)
    lFile = open(inFilePathStr, "ab")
    lFile.write(base64.b64decode(inFileDataBase64Str))
    lFile.close()
    lL = inGSettings.get("Logger", None) if type(inGSettings) is dict else None
    lMessageStr = f"АГЕНТ: Данные успешно добавлены в бинарный файл {inFilePathStr}"
    if lL: lL.info(lMessageStr)
    A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])

# Create text file by the string
def OSFileTextDataStrCreate(inFilePathStr, inFileDataStr, inEncodingStr = "utf-8",inGSettings = None):
    """L+,W+:Создать текстовый файл на стороне Агента

    :param inFilePathStr: Абсолютный путь к создаваемому файлу
    :param inFileDataStr: Текст, отправляемый в создаваемый файл
    :param inEncodingStr:  Кодировка создаваемого файла. По-умолчанию 'utf-8' 
    :param inGSettings: Глобальный файл настроек
    :return:
    """
    inFilePathStr = CrossOS.PathStr(inPathStr=inFilePathStr)
    lFile = open(inFilePathStr, "w", encoding=inEncodingStr)
    lFile.write(inFileDataStr)
    lFile.close()
    lL = inGSettings.get("Logger", None) if type(inGSettings) is dict else None
    lMessageStr = f"АГЕНТ: Текстовый файл {inFilePathStr} успешно создан"
    if lL: lL.info(lMessageStr)
    A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])

def OSFileBinaryDataBase64StrReceive(inFilePathStr, inGSettings=None):
    """L+,W+: Прочитать бинарный файл на стороне агента и отправить на сторону оркестратора в формате base64 (формат безопасный для передачи в формате JSON)

    :param inFilePathStr: Абсолютный путь к читаемому файлу
    :param inGSettings:  Глобальный словарь настроек Агента (необязательный)
    :return: Содержимое бинарного файле, преобразованное в формат base64 (используй base64.b64decode для декодирования в байты). Вернет None запрашиваемый файл не существует
    """
    inFilePathStr = CrossOS.PathStr(inPathStr=inFilePathStr)
    lL = inGSettings.get("Logger", None) if type(inGSettings) is dict else None
    lFileDataBase64Str = None
    if os.path.exists(inFilePathStr):
        lFile = open(inFilePathStr, "rb")
        lFileDataBytes = lFile.read()
        lFile.close()
        lFileDataBase64Str = base64.b64encode(lFileDataBytes).decode("utf-8")
        lMessageStr = f"Функция OSFileBinaryDataBase64StrReceive: файл {inFilePathStr} прочитан успешно"
        if lL: lL.debug(lMessageStr)
        #A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])
    else: 
        if lL: lL.debug(f"Функция OSFileBinaryDataBase64StrReceive: файл {inFilePathStr} не существует - отправить None")
    return lFileDataBase64Str

def OSFileMTimeGet(inFilePathStr: str) -> float or None:
    """L+,W+: Read file modification time timestamp format (float)

    :param inFilePathStr: Абсолютный путь к файлу, дату которого требуется получить
    :return: Временной слепок (timestamp) в формате float. Вернет None, если запрашиваемый файл не существует
    """
    inFilePathStr = CrossOS.PathStr(inPathStr=inFilePathStr)
    global gSettings
    lL = gSettings.get("Logger", None) if type(gSettings) is dict else None
    lFileMTimeFloat = None
    if os.path.exists(inFilePathStr):
        lFileMTimeFloat = os.path.getmtime(inFilePathStr)
        if lL: lL.debug(f"Функция OSFileMTimeGet: файл {inFilePathStr} прочитан успешно")
    else: 
        if lL: lL.debug(f"Функция OSFileMTimeGet: file {inFilePathStr} не существует - вернуть None")
    return lFileMTimeFloat

def OSFileTextDataStrReceive(inFilePathStr, inEncodingStr="utf-8", inGSettings=None):
    """L+,W+: Прочитать текстовый файл на стороне агента и отправить на сторону оркестратора

    :param inFilePathStr: Абсолютный путь к читаемому файлу
    :param inEncodingStr:  Кодировка создаваемого файла. По-умолчанию 'utf-8' 
    :param inGSettings: Глобальный словарь настроек
    :return: Строка - содержимое текстового файла. Возвращает None, если файл не существует
    """
    inFilePathStr = CrossOS.PathStr(inPathStr=inFilePathStr)
    lFileDataStr = None
    lL = inGSettings.get("Logger", None) if type(inGSettings) is dict else None
    if os.path.exists(inFilePathStr):
        lFile = open(inFilePathStr, "r", encoding=inEncodingStr)
        lFileDataStr = lFile.read()
        lFile.close()
        lMessageStr = f"АГЕНТ: Текстовый файл {inFilePathStr} прочитан успешно"
        if lL: lL.info(lMessageStr)
        #A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])
    else:
        if lL: lL.info(f"АГЕНТ: Текстовый файл {inFilePathStr} не существует - вернуть None")
    return lFileDataStr

# Send CMD to OS. Result return to log + Orchestrator by the A2O connection
def OSCMD(inCMDStr, inRunAsyncBool=True, inGSettings = None, inSendOutputToOrchestratorLogsBool = True, inCMDEncodingStr = "cp1251", inCaptureBool = True):
    """L-,W+: Execute CMD on the Agent daemonic process

    :param inCMDStr: command to execute on the Agent session
    :param inRunAsyncBool: True - Agent processor don't wait execution; False - Agent processor wait cmd execution
    :param inGSettings: Agent global settings dict
    :param inSendOutputToOrchestratorLogsBool: True - catch cmd execution output and send it to the Orchestrator logs; Flase - else case; Default True
    :param inCMDEncodingStr: Set the encoding of the DOS window on the Agent server session. Windows is beautiful :) . Default is "cp1251" early was "cp866" - need test
    :param inCaptureBool: !ATTENTION! If you need to start absolutely encapsulated app - set this flag as False. If you set True - the app output will come to Agent
    :return:
    """
    lResultStr = ""
    # New feature
    if inSendOutputToOrchestratorLogsBool == False and inCaptureBool == False:
        inCMDStr = f"start {inCMDStr}"
    # Subdef to listen OS result
    def _CMDRunAndListenLogs(inCMDStr, inSendOutputToOrchestratorLogsBool, inCMDEncodingStr,  inGSettings = None, inCaptureBool = True):
        lL = inGSettings.get("Logger",None) if type(inGSettings) is dict else None
        lResultStr = ""
        lOSCMDKeyStr = str(uuid.uuid4())[0:4].upper()
        lCMDProcess = None
        if inCaptureBool == True:
            lCMDProcess = subprocess.Popen(f'cmd /c {inCMDStr}', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            if CrossOS.IS_WINDOWS_BOOL:
                lCMDProcess = subprocess.Popen(f'cmd /c {inCMDStr}', stdout=None, stderr=None,
                                            creationflags=CREATE_NEW_CONSOLE)
            if CrossOS.IS_LINUX_BOOL:
                lCMDProcess = subprocess.Popen(f'cmd /c {inCMDStr}', stdout=None, stderr=None)
        lListenBool = True
        lMessageStr = f"{lOSCMDKeyStr}: # # # # АГЕНТ: Терминальная сессия запущена # # # # "
        if lL: lL.info(lMessageStr)
        if inSendOutputToOrchestratorLogsBool == True:  # Capturing can be turned on!
            A2O.LogListSend(inGSettings=inGSettings,inLogList=[lMessageStr])
        lMessageStr = f"{lOSCMDKeyStr}: {inCMDStr}"
        if lL: lL.info(lMessageStr)
        if inSendOutputToOrchestratorLogsBool == True:  # Capturing can be turned on!
            A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])
        while lListenBool:
            #if inSendOutputToOrchestratorLogsBool == True: # Capturing can be turned on!
            if inCaptureBool == True: # Capturing can be turned on!
                lOutputLineBytes = lCMDProcess.stdout.readline()
                if lOutputLineBytes == b"":
                    lListenBool = False
                lStr = lOutputLineBytes.decode(inCMDEncodingStr) # was cp866, on win server don't work properly - set cp1251
                if lStr.endswith("\n"): lStr = lStr[:-1]
                lMessageStr = f"{lOSCMDKeyStr}: {lStr}"
                if lL: lL.info(lMessageStr)
                if inSendOutputToOrchestratorLogsBool == True:  # Capturing can be turned on!
                    A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])
                lResultStr+=lStr
            else: #Capturing is not turned on - wait until process will be closed
                lCMDProcessPoll = lCMDProcess.poll()
                if lCMDProcessPoll is None: # Process is alive - wait
                    time.sleep(2)
                else:
                    lListenBool = False
        lMessageStr = f"{lOSCMDKeyStr}: # # # # АГЕНТ: Терминальная сессия завершена # # # # "
        if lL: lL.info(lMessageStr)
        if inSendOutputToOrchestratorLogsBool == True:  # Capturing can be turned on!
            A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])
        return lResultStr
    # New call
    if inRunAsyncBool:
        lThread = threading.Thread(target=_CMDRunAndListenLogs, kwargs={"inCMDStr":inCMDStr, "inGSettings":inGSettings, "inSendOutputToOrchestratorLogsBool":inSendOutputToOrchestratorLogsBool, "inCMDEncodingStr":inCMDEncodingStr, "inCaptureBool": inCaptureBool })
        lThread.start()
        lResultStr="Список ActivityList отправлен на исполнение в асинхронном режиме - захват текста недоступен"
    else:
        lResultStr = _CMDRunAndListenLogs(inCMDStr=inCMDStr, inGSettings=inGSettings, inSendOutputToOrchestratorLogsBool = inSendOutputToOrchestratorLogsBool, inCMDEncodingStr = inCMDEncodingStr, inCaptureBool=inCaptureBool)
    #lCMDCode = "cmd /c " + inCMDStr
    #subprocess.Popen(lCMDCode)
    #lResultCMDRun = 1  # os.system(lCMDCode)
    return lResultStr


def ProcessWOExeUpperUserListGet():
    """L-,W+: Вернуть список процессов, запущенных под пользователем на стороне агента

    :return: Список процессов в формате: ["NOTEPAD","..."] (без постфикса .exe и в верхнем регистре)

    """
    lUserNameStr = getpass.getuser()
    lResult = []
    # Create updated list for quick check
    lProcessNameWOExeList = []
    # Iterate over the list
    for proc in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            # Add if empty inProcessNameWOExeList or if process in inProcessNameWOExeList
            lUserNameWODomainStr = proc.username().split('\\')[-1]
            if lUserNameWODomainStr == lUserNameStr:
                lResult.append(pinfo['name'][:-4].upper())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    return lResult

# Main def
def Agent(inGSettings):
    License.ConsoleVerify()
    lL = inGSettings["Logger"]
    global gSettings
    gSettings = inGSettings
    # Append Orchestrator def to ProcessorDictAlias
    lModule = sys.modules[__name__]
    lModuleDefList = dir(lModule)
    for lItemDefNameStr in lModuleDefList:
        # Dont append alias for defs Agent
        if lItemDefNameStr not in ["Agent"]:
            lItemDef = getattr(lModule,lItemDefNameStr)
            if callable(lItemDef): inGSettings["ProcessorDict"]["AliasDefDict"][lItemDefNameStr]=lItemDef

    # Detect Machine host name and username
    inGSettings["AgentDict"]["HostNameUpperStr"] = socket.gethostname().upper()
    inGSettings["AgentDict"]["UserUpperStr"] = getpass.getuser().upper()

    # Processor thread
    lProcessorThread = threading.Thread(target= Processor.ProcessorRunSync, kwargs={"inGSettings":inGSettings})
    lProcessorThread.daemon = True # Run the thread in daemon mode.
    lProcessorThread.start() # Start the thread execution.
    if lL: lL.info("Модуль процессора pyOpenRPA был успешно запущен")  #Logging

    # Start thread to wait data from Orchestrator (O2A)
    lO2AThread = threading.Thread(target=O2A.O2A_Loop, kwargs={"inGSettings":inGSettings})
    lO2AThread.start()
    Usage.Process(inComponentStr="Agent")
    
    
    # Send log that Agent has been started
    A2O.LogListSend(inGSettings=inGSettings, inLogList=[f'Хост: {inGSettings["AgentDict"]["HostNameUpperStr"]}, Логин: {inGSettings["AgentDict"]["UserUpperStr"]}, Агент инициализирован успешно'])