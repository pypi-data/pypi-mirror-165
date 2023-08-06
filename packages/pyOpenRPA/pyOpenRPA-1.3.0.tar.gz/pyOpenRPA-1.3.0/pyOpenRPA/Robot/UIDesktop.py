from pyOpenRPA.Tools import CrossOS
if CrossOS.IS_WINDOWS_BOOL:
    from pywinauto import win32defines, win32structures, win32functions
    import pywinauto
    import win32api

import ctypes
import struct

import time
from .Utils import ProcessCommunicator
from . import Utils #For ProcessBitness
from pyOpenRPA.Tools import Usage
from pyOpenRPA.Tools import License
import re
import copy

############################################
# When import UIDesktop init the other bitness python
# For this type
# UIDesktop.Utils.ProcessBitness.SettingsInit(inSettingsDict)
# inSettingsDict = {
#    "Python32FullPath": None, #Set from user: "..\\Resources\\WPy32-3720\\python-3.7.2\\OpenRPARobotGUIx32.exe"
#    "Python64FullPath": None, #Set from user
#    "Python32ProcessName": "OpenRPAUIDesktopX32.exe", #Config set once
#    "Python64ProcessName": "OpenRPAUIDesktopX64.exe" #Config set once
#}
############################################

#logging.basicConfig(filename="Reports\ReportRobotGUIRun_"+datetime.datetime.now().strftime("%Y_%m_%d")+".log", level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

#####Внимание#######
#TODO В перспективе нужно реализовать алгоритм определения разрядности не в Robot.py, а в UIDesktop.py, тк начинают появляться функции, на входе в которые еще неизвестна разрядность элемента + селектор может охватить сразу два элемента из 2-х разных разрядностей - обрабатываться это должно непосредственно при выполнении

####################################
#Info: GUI module of the Robot app (pyOpenRPA - Robot)
####################################
# GUI Module - interaction with Desktop application

#GUI Naming convention
#<InArgument>_<ActivityName>_<OutArgument - if exist>

#UIO - UI Object (class of pywinauto UI object)
#UIOSelector - List of dict (key attributes)
#PWA - PyWinAuto
#PWASpecification - List of dict (key attributes in pywinauto.find_window notation)
#UIOTree - Recursive Dict of Dict ... (UI Parent -> Child hierarchy)
#UIOInfo - Dict of UIO attributes
#UIOActivity - Activity of the UIO (UI object) from the Pywinauto module
#UIOEI - UI Object info object

#inActivitySpecificationDict:
#{
#   ModuleName: <"GUI", str>, - optional
#   ActivityName: <Function or procedure name in module, str>,
#   ArgumentList: [<Argument 1, any type>, ...] - optional,
#   ArgumentDict: {<Argument 1 name, str>:<Argument 1 value, any type>, ...} - optional
#}

#outActivityResultDict:
#{
#   ActivitySpecificationDict: {
#       ModuleName: <"GUI", str>, -optional
#       ActivityName: <Function or procedure name in module, str>,
#       ArgumentList: [<Argument 1, any type>, ...] - optional,
#       ArgumentDict: {<Argument 1 name, str>: <Argument 1 value, any type>, ...} - optional
#   },
#   ErrorFlag: <Boolean flag - Activity result has error (true) or not (false), boolean>,
#   ErrorMessage: <Error message, str> - required if ErrorFlag is true,
#   ErrorTraceback: <Error traceback log, str> - required if ErrorFlag is true,
#   Result: <Result, returned from the Activity, int, str, boolean, list, dict> - required if ErrorFlag is false
#}

#inUIOSelector:
#[
#   {
#       "index":<Позиция элемента в родительском объекте>,
#       "depth_start" - глубина, с которой начинается поиск (по умолчанию 1),
#       "depth_end" - глубина, до которой ведется поиск (по умолчанию 1),
#       "class_name" - наименование класса, который требуется искать,
#       "title" - наименование заголовка,
#       "rich_text" - наименование rich_text,
#       "backend": <"win32"||"uia", only for the 1-st list element> - if not specified, use mDefaultPywinautoBackend
#   },
#   { ... }
#
#]

#Default parameters
mDefaultPywinautoBackend="win32"

############################
#Новая версия
############################
#Получить список элементов, который удовлетворяет условиям через расширенный движок поиска
#[
#   {
#       "index":<Позиция элемента в родительском объекте>,
#       "depth_start" - глубина, с которой начинается поиск (по умолчанию 1)
#       "depth_end" - глубина, до которой ведется поиск (по умолчанию 1)
#       "class_name" - наименование класса, который требуется искать
#       "title" - наименование заголовка
#       "rich_text" - наименование rich_text
#   }
#]

#old:PywinautoExtElementsGet
def UIOSelector_Get_UIOList (inSpecificationList,inElement=None,inFlagRaiseException=True):
    '''L-,W+: Получить список UIO объектов по UIO селектору
    
    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"},{"title":"DEMO", "depth_start": 5, "depth_end": 5}]		
        lDemoBaseUIOList = UIDesktop.UIOSelector_Get_UIOList(lDemoBaseUIOSelector) #Получить список UIO объектов, которые удовлетворяют требованиям UIO селектора. В нашем примере либо [], либо [UIO объект]

    :param inSpecificationList: UIO Селектор, который определяет критерии поиска UI элементов
    :type inSpecificationList: list, обязательный
    :param inElement: Родительский элемент, от которого выполнить поиск UIO объектов по заданному UIO селектору. Если аргумент не задан, платформа выполнит поиск UIO объектов среди всех доступных приложений windows, которые запущены на текущей сессии
    :type inElement: UIO объект, опциональный
    :param inFlagRaiseException: True - формировать ошибку exception, если платформа не обнаружина ни одного UIO объекта по заданному UIO селектору. False - обратный случай. По умолчанию True
    :type inFlagRaiseException: bool, опциональный
    :return: Список UIO объектов, которые удовлетворяют условиям UIO селектора
    '''
    #Создать копию входного листа, чтобы не менять массив в других верхнеуровневых функциях
    inSpecificationList=copy.deepcopy(inSpecificationList)
    lResultList=[]
    lChildrenList=[]
    #Получить родительский объект если на вход ничего не поступило
    if inElement is None:
        #сформировать спецификацию на получение элемента
        lRootElementSpecification=[inSpecificationList[0]]
        lRootElementList=PWASpecification_Get_UIO(lRootElementSpecification)
        for lRootItem in lRootElementList:
            if lRootItem is not None:
                lChildrenList.append(lRootItem.wrapper_object())
    #Елемент на вход поступил - выполнить его анализ
    else:
        #Получить список элементов
        lElementChildrenList=inElement.children()
        #Поступил index - точное добавление
        if 'index' in inSpecificationList[0]:
            if inSpecificationList[0]['index']<len(lElementChildrenList):
                #Получить дочерний элемент - точное добавление
                lChildrenList.append(lElementChildrenList[inSpecificationList[0]['index']])
            else:
                if inFlagRaiseException:
                    raise ValueError('Object has no children with index: ' + str(inSpecificationList[0]['index']))
        #Поступил ctrl_index - точное добавление
        elif 'ctrl_index' in inSpecificationList[0]:
            if inSpecificationList[0]['ctrl_index']<len(lElementChildrenList):
                #Получить дочерний элемент
                lChildrenList.append(lElementChildrenList[inSpecificationList[0]['ctrl_index']])
            else:
                if inFlagRaiseException:
                    raise ValueError('Object has no children with index: ' + str(inSpecificationList[0]['ctrl_index']))
        #Если нет точного обозначения элемента
        else:
            lFlagGoCheck=True
            #Учесть поле depth_start (если указано)
            if 'depth_start' in inSpecificationList[0]:
                if inSpecificationList[0]["depth_start"]>1:
                    lFlagGoCheck=False
            #Циклический обход по детям, на предмет соответствия всем условиям
            for lChildrenItem in lElementChildrenList:
                #Обработка глубины depth (рекурсивный вызов для всех детей с занижением индекса глубины)
                #По умолчанию значение глубины 1
                if 'depth_end' in inSpecificationList[0]:
                    if inSpecificationList[0]['depth_end']>1:
                        #Подготовка новой версии спецификации
                        lChildrenItemNewSpecificationList=inSpecificationList.copy()
                        lChildrenItemNewSpecificationList[0]=lChildrenItemNewSpecificationList[0].copy()
                        lChildrenItemNewSpecificationList[0]["depth_end"]=lChildrenItemNewSpecificationList[0]["depth_end"]-1
                        if 'depth_start' in lChildrenItemNewSpecificationList[0]:
                            lChildrenItemNewSpecificationList[0]["depth_start"]=lChildrenItemNewSpecificationList[0]["depth_start"]-1
                        #Циклический вызов для всех детей со скорректированной спецификацией
                        lResultList.extend(UIOSelector_Get_UIOList(lChildrenItemNewSpecificationList,lChildrenItem,inFlagRaiseException))
                #Фильтрация
                #TODO Сделать поддержку этих атрибутов для первого уровня селектора
                if lFlagGoCheck:
                    lFlagAddChild=True
                    #Фильтрация по title
                    if 'title' in inSpecificationList[0]:
                        if lChildrenItem.element_info.name != inSpecificationList[0]["title"]:
                            lFlagAddChild=False
                    #Фильтрация по title_re (regexp)
                    if 'title_re' in inSpecificationList[0]:
                        if re.fullmatch(inSpecificationList[0]["title_re"],lChildrenItem.element_info.name) is None:
                            lFlagAddChild=False
                    #Фильтрация по rich_text
                    if 'rich_text' in inSpecificationList[0]:
                        if lChildrenItem.element_info.rich_text != inSpecificationList[0]["rich_text"]:
                            lFlagAddChild=False
                    #Фильтрация по rich_text_re (regexp)
                    if 'rich_text_re' in inSpecificationList[0]:
                        if re.fullmatch(inSpecificationList[0]["rich_text_re"],lChildrenItem.element_info.rich_text) is None:
                            lFlagAddChild=False
                    #Фильтрация по class_name
                    if 'class_name' in inSpecificationList[0]:
                        if lChildrenItem.element_info.class_name != inSpecificationList[0]["class_name"]:
                            lFlagAddChild=False
                    #Фильтрация по class_name_re (regexp)
                    if 'class_name_re' in inSpecificationList[0]:
                        if re.fullmatch(inSpecificationList[0]["class_name_re"],lChildrenItem.element_info.class_name) is None:
                            lFlagAddChild=False
                    #Фильтрация по friendly_class_name
                    if 'friendly_class_name' in inSpecificationList[0]:
                        if lChildrenItem.friendly_class_name() != inSpecificationList[0]["friendly_class_name"]:
                            lFlagAddChild=False
                    #Фильтрация по friendly_class_name_re (regexp)
                    if 'friendly_class_name_re' in inSpecificationList[0]:
                        if re.fullmatch(inSpecificationList[0]["friendly_class_name_re"],lChildrenItem.friendly_class_name) is None:
                            lFlagAddChild=False
                    #Фильтрация по control_type
                    if 'control_type' in inSpecificationList[0]:
                        if lChildrenItem.element_info.control_type != inSpecificationList[0]["control_type"]:
                            lFlagAddChild=False
                    #Фильтрация по control_type_re (regexp)
                    if 'control_type_re' in inSpecificationList[0]:
                        if re.fullmatch(inSpecificationList[0]["control_type_re"],lChildrenItem.element_info.control_type) is None:
                            lFlagAddChild=False
                    #Фильтрация по is_enabled (bool)
                    if 'is_enabled' in inSpecificationList[0]:
                        if lChildrenItem.is_enabled()!=inSpecificationList[0]["is_enabled"]:
                            lFlagAddChild=False
                    #Фильтрация по is_visible (bool)
                    if 'is_visible' in inSpecificationList[0]:
                        if lChildrenItem.is_visible()!=inSpecificationList[0]["is_visible"]:
                            lFlagAddChild=False
                    #####
                    #Все проверки пройдены - флаг добавления
                    if lFlagAddChild:
                        lChildrenList.append(lChildrenItem)
    #Выполнить рекурсивный вызов (уменьшение количества спецификаций), если спецификация больше одного элемента
    #????????Зачем в условии ниже is not None ???????????
    if len(inSpecificationList)>1 and len(lChildrenList)>0:
        #Вызвать рекурсивно функцию получения следующего объекта, если в спецификации есть следующий объект
        for lChildElement in lChildrenList:
            lResultList.extend(UIOSelector_Get_UIOList(inSpecificationList[1:],lChildElement,inFlagRaiseException))
    else:
        lResultList.extend(lChildrenList)
    #Условие, если результирующий список пустой и установлен флаг создания ошибки (и inElement is None - не следствие рекурсивного вызова)
    if inElement is None and len(lResultList)==0 and inFlagRaiseException:
        raise pywinauto.findwindows.ElementNotFoundError("Robot can't find element by the UIOSelector")
    return lResultList

#old:PywinautoExtElementGet
def UIOSelector_Get_UIO (inSpecificationList,inElement=None,inFlagRaiseException=True):
    '''L-,W+: Получить список UIO объект по UIO селектору. Если критериям UIO селектора удовлетворяет несколько UIO объектов - вернуть первый из списка
    
    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"},{"title":"DEMO", "depth_start": 5, "depth_end": 5}]		
        lDemoBaseUIOList = UIDesktop.UIOSelector_Get_UIO(lDemoBaseUIOSelector) #Получить 1-й UIO объект, которые удовлетворяет требованиям UIO селектора. В нашем примере либо None, либо UIO объект

    :param inSpecificationList: UIO Селектор, который определяет критерии поиска UI элементов
    :type inSpecificationList: list, обязательный
    :param inElement: Родительский элемент, от которого выполнить поиск UIO объектов по заданному UIO селектору. Если аргумент не задан, платформа выполнит поиск UIO объектов среди всех доступных приложений windows, которые запущены на текущей сессии
    :type inElement: UIO объект, опциональный
    :param inFlagRaiseException: True - формировать ошибку exception, если платформа не обнаружина ни одного UIO объекта по заданному UIO селектору. False - обратный случай. По умолчанию True
    :type inFlagRaiseException: bool, опциональный
    :return: UIO объект, которые удовлетворяют условиям UIO селектора, или None
    '''
    lResult=None
    #Получить родительский объект если на вход ничего не поступило
    lResultList=UIOSelector_Get_UIOList(inSpecificationList,inElement,False)
    if len(lResultList)>0:
        lResult=lResultList[0]
    #Условие, если результирующий список пустой и установлен флаг создания ошибки (и inElement is None - не следствие рекурсивного вызова)
    if lResult is None and inFlagRaiseException:
        raise pywinauto.findwindows.ElementNotFoundError("Robot can't find element by the UIOSelector")
    return lResult
    
#old:-
def UIOSelector_Exist_Bool (inUIOSelector):
    '''L-,W+: Проверить существование хотя бы 1-го UIO объекта по заданному UIO селектору
    
    !ВНИМАНИЕ! ДАННАЯ ФУНКЦИОНАЛЬНОСТЬ В АВТОМАТИЧЕСКОМ РЕЖИМЕ ПОДДЕРЖИВАЕТ ВСЕ РАЗРЯДНОСТИ ПРИЛОЖЕНИЙ (32|64), КОТОРЫЕ ЗАПУЩЕНЫ В СЕСИИ. PYTHON x64 ИМЕЕТ ВОЗМОЖНОСТЬ ВЗЗАИМОДЕЙСТВИЯ С x32 UIO ОБЪЕКТАМИ, НО МЫ РЕКОМЕНДУЕМ ДОПОЛНИТЕЛЬНО ИСПОЛЬЗОВАТЬ ИНТЕРПРЕТАТОР PYTHON x32 (ПОДРОБНЕЕ СМ. ФУНКЦИЮ Configure())
    
    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"},{"title":"DEMO", "depth_start": 5, "depth_end": 5}]		
        lDemoBaseUIOExistBool = UIDesktop.UIOSelector_Exist_Bool(lDemoBaseUIOSelector) # Получить булевый результат проверки существования UIO объекта

    :param inUIOSelector: UIO Селектор, который определяет критерии поиска UIO объектов
    :type inUIOSelector: list, обязательный
    :return: True - существует хотя бы 1 UIO объект. False - не существует ни одного UIO объекта по заданному UIO селектору
    '''
    lResult=False
    #Check the bitness
    lSafeOtherProcess = UIOSelector_SafeOtherGet_Process(inUIOSelector)
    if lSafeOtherProcess is None:
        #Получить родительский объект если на вход ничего не поступило
        lResultList=UIOSelector_Get_UIOList(inUIOSelector, None, False)
        if len(lResultList)>0:
            lResult=True
    else:
        # Run function from other process with help of PIPE
        lPIPEResuestDict = {"ModuleName": "UIDesktop", "ActivityName": "UIOSelector_Exist_Bool",
                            "ArgumentList": [inUIOSelector],
                            "ArgumentDict": {}}
        # Отправить запрос в дочерний процесс, который отвечает за работу с Windows окнами
        ProcessCommunicator.ProcessChildSendObject(lSafeOtherProcess, lPIPEResuestDict)
        # Get answer from child process
        lPIPEResponseDict = ProcessCommunicator.ProcessChildReadWaitObject(lSafeOtherProcess)
        if lPIPEResponseDict["ErrorFlag"]:
            raise Exception(
                f"Exception was occured in child process (message): {lPIPEResponseDict['ErrorMessage']}, (traceback): {lPIPEResponseDict['ErrorTraceback']}")
        else:
            lResult = lPIPEResponseDict["Result"]
    return lResult

#old: -
def UIOSelectorsSecs_WaitAppear_List (inSpecificationListList,inWaitSecs=86400.0,inFlagWaitAllInMoment=False):
    '''L-,W+: Ожидать появление хотя бы 1-го / всех UIO объектов по заданным UIO селекторам
    
    !ВНИМАНИЕ! ДАННАЯ ФУНКЦИОНАЛЬНОСТЬ В АВТОМАТИЧЕСКОМ РЕЖИМЕ ПОДДЕРЖИВАЕТ ВСЕ РАЗРЯДНОСТИ ПРИЛОЖЕНИЙ (32|64), КОТОРЫЕ ЗАПУЩЕНЫ В СЕСИИ. PYTHON x64 ИМЕЕТ ВОЗМОЖНОСТЬ ВЗЗАИМОДЕЙСТВИЯ С x32 UIO ОБЪЕКТАМИ, НО МЫ РЕКОМЕНДУЕМ ДОПОЛНИТЕЛЬНО ИСПОЛЬЗОВАТЬ ИНТЕРПРЕТАТОР PYTHON x32 (ПОДРОБНЕЕ СМ. ФУНКЦИЮ Configure())
    
    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"},{"title":"DEMO", "depth_start": 5, "depth_end": 5}]		
        lNotepadOKSelector = [{"title":"notepad"},{"title":"OK"}]
        lNotepadCancelSelector = [{"title":"notepad"},{"title":"Cancel"}]
        lDemoBaseUIOExistList = UIDesktop.UIOSelectorsSecs_WaitAppear_List([lDemoBaseUIOSelector, lNotepadOKSelector, lNotepadCancelSelector]) # Ожидать появление UIO объекта

    :param inSpecificationListList: Список UIO селекторов, которые определяют критерии поиска UIO объектов
            Пример: [
            [{"title":"notepad"},{"title":"OK"}],
            [{"title":"notepad"},{"title":"Cancel"}]
        ]
    :type inSpecificationListList: list, обязательный
    :param inWaitSecs: Количество секунд, которые отвести на ожидание UIO объектов. По умолчанию 24 часа (86400 секунд)
    :type inWaitSecs: float, необязательный
    :param inFlagWaitAllInMoment: True - Ожидать до того момента, пока не появятся все запрашиваемые UIO объекты на рабочей области
    :return: Список индексов, которые указывают на номер входящих UIO селекторов, которые были обнаружены на рабочей области. Пример: [0,2]
    '''
    lResultFlag=False
    lSecsSleep = 1 #Настроечный параметр
    lSecsDone = 0
    lResultList = None
    #Цикл проверки
    while lResultFlag == False and lSecsDone<inWaitSecs:
        #pdb.set_trace()
        lResultList=[]
        #Итерация проверки
        lIndex = 0
        for lItem in inSpecificationListList:
            lItemResultFlag=UIOSelector_Exist_Bool(lItem)
            #Если обнаружен элемент - добавить его индекс в массив
            if lItemResultFlag:
                lResultList.append(lIndex)
            #Инкремент индекса
            lIndex=lIndex + 1
        #Проверка в зависимости от флага
        if inFlagWaitAllInMoment and len(lResultList)==len(inSpecificationListList):
            #Условие выполнено
            lResultFlag=True
        elif not inFlagWaitAllInMoment and len(lResultList)>0:
            #Условие выполнено
            lResultFlag=True
        #Если флаг не изменился - увеличить время и уснуть
        if lResultFlag == False:
            lSecsDone=lSecsDone+lSecsSleep
            time.sleep(lSecsSleep)
    return lResultList

#old: -
def UIOSelectorsSecs_WaitDisappear_List (inSpecificationListList,inWaitSecs=86400.0,inFlagWaitAllInMoment=False):
    '''L-,W+:  Ожидать исчезновение хотя бы 1-го / всех UIO объектов по заданным UIO селекторам
    
    !ВНИМАНИЕ! ДАННАЯ ФУНКЦИОНАЛЬНОСТЬ В АВТОМАТИЧЕСКОМ РЕЖИМЕ ПОДДЕРЖИВАЕТ ВСЕ РАЗРЯДНОСТИ ПРИЛОЖЕНИЙ (32|64), КОТОРЫЕ ЗАПУЩЕНЫ В СЕСИИ. PYTHON x64 ИМЕЕТ ВОЗМОЖНОСТЬ ВЗЗАИМОДЕЙСТВИЯ С x32 UIO ОБЪЕКТАМИ, НО МЫ РЕКОМЕНДУЕМ ДОПОЛНИТЕЛЬНО ИСПОЛЬЗОВАТЬ ИНТЕРПРЕТАТОР PYTHON x32 (ПОДРОБНЕЕ СМ. ФУНКЦИЮ Configure())
    
    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"},{"title":"DEMO", "depth_start": 5, "depth_end": 5}]		
        lNotepadOKSelector = [{"title":"notepad"},{"title":"OK"}]
        lNotepadCancelSelector = [{"title":"notepad"},{"title":"Cancel"}]
        lDemoBaseUIOExistList = UIDesktop.UIOSelectorsSecs_WaitDisappear_List([lDemoBaseUIOSelector, lNotepadOKSelector, lNotepadCancelSelector]) # Ожидать исчезновение UIO объектов

    :param inSpecificationListList: Список UIO селекторов, которые определяют критерии поиска UIO объектов
            Пример: [
            [{"title":"notepad"},{"title":"OK"}],
            [{"title":"notepad"},{"title":"Cancel"}]
        ]
    :type inSpecificationListList: list, обязательный
    :param inWaitSecs: Количество секунд, которые отвести на ожидание исчезновения UIO объектов. По умолчанию 24 часа (86400 секунд)
    :type inWaitSecs: float, необязательный
    :param inFlagWaitAllInMoment: True - Ожидать до того момента, пока не исчезнут все запрашиваемые UIO объекты на рабочей области
    :return: Список индексов, которые указывают на номер входящих UIO селекторов, которые были обнаружены на рабочей области. Пример: [0,2]
    '''
    
    lResultFlag=False
    lSecsSleep = 1 #Настроечный параметр
    lSecsDone = 0
    lResultList = None
    #Цикл проверки
    while lResultFlag == False and lSecsDone<inWaitSecs:
        #pdb.set_trace()
        lResultList=[]
        #Итерация проверки
        lIndex = 0
        for lItem in inSpecificationListList:
            lItemResultFlag=UIOSelector_Exist_Bool(lItem)
            #Если обнаружен элемент - добавить его индекс в массив
            if not lItemResultFlag:
                lResultList.append(lIndex)
            #Инкремент индекса
            lIndex=lIndex + 1
        #Проверка в зависимости от флага
        if inFlagWaitAllInMoment and len(lResultList)==len(inSpecificationListList):
            #Условие выполнено
            lResultFlag=True
        elif not inFlagWaitAllInMoment and len(lResultList)>0:
            #Условие выполнено
            lResultFlag=True
        #Если флаг не изменился - увеличить время и уснуть
        if lResultFlag == False:
            lSecsDone=lSecsDone+lSecsSleep
            time.sleep(lSecsSleep)
    return lResultList

#old: -
def UIOSelectorSecs_WaitAppear_Bool (inSpecificationList,inWaitSecs):
    '''L-,W+: Ожидать появление 1-го UIO объекта по заданному UIO селектору
    
    !ВНИМАНИЕ! ДАННАЯ ФУНКЦИОНАЛЬНОСТЬ В АВТОМАТИЧЕСКОМ РЕЖИМЕ ПОДДЕРЖИВАЕТ ВСЕ РАЗРЯДНОСТИ ПРИЛОЖЕНИЙ (32|64), КОТОРЫЕ ЗАПУЩЕНЫ В СЕСИИ. PYTHON x64 ИМЕЕТ ВОЗМОЖНОСТЬ ВЗЗАИМОДЕЙСТВИЯ С x32 UIO ОБЪЕКТАМИ, НО МЫ РЕКОМЕНДУЕМ ДОПОЛНИТЕЛЬНО ИСПОЛЬЗОВАТЬ ИНТЕРПРЕТАТОР PYTHON x32 (ПОДРОБНЕЕ СМ. ФУНКЦИЮ Configure())
    
    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"},{"title":"DEMO", "depth_start": 5, "depth_end": 5}]		
        lDemoBaseUIOExistBool = UIDesktop.UIOSelectorSecs_WaitAppear_Bool(lDemoBaseUIOSelector) # Ожидать появление UIO объекта

    :param inSpecificationList: UIO селектор, который определяет критерии поиска UIO объекта
    :type inSpecificationList: list, обязательный
    :param inWaitSecs: Количество секунд, которые отвести на ожидание UIO объекта. По умолчанию 24 часа (86400 секунд)
    :type inWaitSecs: float, необязательный
    :return: True - UIO объект был обнаружен. False - обратная ситуациая
    '''
    lWaitAppearList=UIOSelectorsSecs_WaitAppear_List([inSpecificationList],inWaitSecs)
    lResult=False
    if len(lWaitAppearList)>0:
        lResult=True
    return lResult

#old name - -
def UIOSelectorSecs_WaitDisappear_Bool (inSpecificationList,inWaitSecs):
    '''L-,W+: Ожидать исчезновение 1-го UIO объекта по заданному UIO селектору
    
    !ВНИМАНИЕ! ДАННАЯ ФУНКЦИОНАЛЬНОСТЬ В АВТОМАТИЧЕСКОМ РЕЖИМЕ ПОДДЕРЖИВАЕТ ВСЕ РАЗРЯДНОСТИ ПРИЛОЖЕНИЙ (32|64), КОТОРЫЕ ЗАПУЩЕНЫ В СЕСИИ. PYTHON x64 ИМЕЕТ ВОЗМОЖНОСТЬ ВЗЗАИМОДЕЙСТВИЯ С x32 UIO ОБЪЕКТАМИ, НО МЫ РЕКОМЕНДУЕМ ДОПОЛНИТЕЛЬНО ИСПОЛЬЗОВАТЬ ИНТЕРПРЕТАТОР PYTHON x32 (ПОДРОБНЕЕ СМ. ФУНКЦИЮ Configure())
    
    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"},{"title":"DEMO", "depth_start": 5, "depth_end": 5}]		
        lDemoBaseUIOExistBool = UIDesktop.UIOSelectorSecs_WaitDisappear_Bool(lDemoBaseUIOSelector) # Ожидать исчезновение UIO объекта

    :param inSpecificationList: UIO селектор, который определяет критерии поиска UIO объекта
    :type inSpecificationList: list, обязательный
    :param inWaitSecs: Количество секунд, которые отвести на исчезновение UIO объекта. По умолчанию 24 часа (86400 секунд)
    :type inWaitSecs: float, необязательный
    :return: True - UIO объект был обнаружен. False - обратная ситуациая
    '''
    lWaitDisappearList=UIOSelectorsSecs_WaitDisappear_List([inSpecificationList],inWaitSecs)
    lResult=False
    if len(lWaitDisappearList)>0:
        lResult=True
    return lResult

#old: -
def UIOSelector_Get_BitnessInt (inSpecificationList):
    '''L-,W+: Определить разрядность приложения по UIO селектору. Вернуть результат в формате целого числа (64 или 32)

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"},{"title":"DEMO", "depth_start": 5, "depth_end": 5}]		
        lDemoBaseBitInt = UIDesktop.UIOSelector_Get_BitnessInt(lDemoBaseUIOSelector) # Определить разрядность приложения, в котором обнаружен UIO объект по селектору

    :param inSpecificationList: UIO селектор, который определяет критерии поиска UIO объекта
    :type inSpecificationList: list, обязательный
    :return: None - UIO объект не обнаружен; 64 (int) - разрядность приложения равна 64 битам; 32 (int) - разрядность приложения равна 32 битам
    '''
    lResult=None
    #Получить объект Application (Для проверки разрядности)
    lRootElement=PWASpecification_Get_PWAApplication(inSpecificationList)
    if lRootElement is not None:
        if lRootElement.is64bit():
            lResult=64
        else:
            lResult=32
    return lResult

#old: -
def UIOSelector_Get_BitnessStr (inSpecificationList):
    """L-,W+: Определить разрядность приложения по UIO селектору. Вернуть результат в формате строки ("64" или "32")

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"},{"title":"DEMO", "depth_start": 5, "depth_end": 5}]		
        lDemoBaseBitStr = UIDesktop.UIOSelector_Get_BitnessStr(lDemoBaseUIOSelector) # Определить разрядность приложения, в котором обнаружен UIO объект по селектору

    :param inSpecificationList: UIO селектор, который определяет критерии поиска UIO объекта
    :type inSpecificationList: list, обязательный
    :return: None - UIO объект не обнаружен; "64" (str) - разрядность приложения равна 64 битам; "32" (str) - разрядность приложения равна 32 битам
    """
    lResult=None
    #Получить объект Application (Для проверки разрядности)
    lRootElement=PWASpecification_Get_PWAApplication(inSpecificationList)
    if lRootElement is not None:
        if lRootElement.is64bit():
            lResult="64"
        else:
            lResult="32"
    return lResult

#old: -
def Get_OSBitnessInt ():
    '''L-,W+: Определить разрядность робота, в котором запускается данная функция

    .. code-block:: python

        from pyOpenRPA.Robot import UIDesktop
        lRobotBitInt = UIDesktop.Get_OSBitnessInt() # Определить разрядность робота, в котором была вызвана это функция
    
    :return: 64 (int) - разрядность приложения равна 64 битам; 32 (int) - разрядность приложения равна 32 битам
    '''
    lResult=32
    if pywinauto.sysinfo.is_x64_OS():
        lResult=64
    return lResult
#old: -
def UIOSelector_SafeOtherGet_Process(inUIOSelector):
    """L-,W+: Получить процесс робота другой разрядности (если приложение UIO объекта выполняется в другой разрядности). Функция возвращает None, если разрядность робота совпадает с разрядностью приложения UIO объекта, либо если при инициализации робота не устанавливался интерпретатор другой разрядности.

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"},{"title":"DEMO", "depth_start": 5, "depth_end": 5}]		
        lOtherBitnessProcess = UIDesktop.UIOSelector_SafeOtherGet_Process(lDemoBaseUIOSelector) # Вернуть процесс робота, схожей разрядности

    :param inUIOSelector: UIO селектор, который определяет критерии поиска UIO объекта
    :type inUIOSelector: list, обязательный
    :return: Процесс робота схожей разрядности
    """
    #Default value
    lResult = None
    #Go check bitness if selector exists
    if inUIOSelector:
        #Get selector bitness
        lUIOSelectorAppBitness = UIOSelector_Get_BitnessStr(inUIOSelector)
        if lUIOSelectorAppBitness and Utils.ProcessBitness.mSettingsDict["BitnessProcessCurrent"] != lUIOSelectorAppBitness:
            lResult = Utils.ProcessBitness.OtherProcessGet()
    return lResult
#old: GetControl
def PWASpecification_Get_UIO(inControlSpecificationArray):
    """L-,W+: Получить UIO объект по PWA (pywinauto) селектору. (https://pywinauto.readthedocs.io/en/latest/code/pywinauto.findwindows.html). Мы рекомендуем использовать метод UIOSelector_UIO_Get, так как UIO селектор обладает большей функциональностью.

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lUIOObject = UIDesktop.PWASpecification_Get_UIO(lDemoBaseUIOSelector) # Получить UIO объект по PWA селектору

    :param inControlSpecificationArray: PWA селектор, который определяет критерии поиска UIO объекта
        Допустимые ключи PWA селектора:

        - class_name содержимое атрибута class UIO объекта
        - class_name_re содержимое атрибута class UIO объекта, которое удовлетворяет установленному рег. выражению
        - process идентификатор процесса, в котором находится UIO объект
        - title содержимое атрибута title UIO объекта
        - title_re содержимое атрибута title UIO объекта, которое удовлетворяет установленному рег. выражению
        - top_level_only признак поиска только на верхнем уровне приложения. По умолчанию True
        - visible_only признак поиска только среди видимых UIO объектов. По умолчанию True
        - enabled_only признак поиска только среди разблокированных UIO объектов. По умолчанию False
        - best_match содержимое атрибута title UIO объекта максимально приближено к заданному
        - handle идентификатор handle искомого UIO объекта 
        - ctrl_index индекс UIO объекта среди всех дочерних объектов в списке родительского
        - found_index индекс UIO объекта среди всех обнаруженных
        - predicate_func пользовательская функция проверки соответсвия UIO элемента
        - active_only признак поиска только среди активных UIO объектов. По умолчанию False
        - control_id идентификатор control_id искомого UIO объекта 
        - control_type тип элемента (применимо, если backend == "uia")
        - auto_id идентификатор auto_id искомого UIO объекта (применимо, если backend == "uia")
        - framework_id идентификатор framework_id искомого UIO объекта (применимо, если backend == "uia")
        - backend вид технологии подключения к поиску UIO объекта ("uia" или "win32")
    :type inControlSpecificationArray: list, обязательный
    :return: UIO объект
    """
    #Определение backend
    lBackend=mDefaultPywinautoBackend
    if "backend" in inControlSpecificationArray[0]:
        lBackend=inControlSpecificationArray[0]["backend"]
        inControlSpecificationArray[0].pop("backend")
    #Подготовка входного массива
    inControlSpecificationOriginArray=copy.deepcopy(inControlSpecificationArray)
    inControlSpecificationArray=UIOSelector_SearchProcessNormalize_UIOSelector(inControlSpecificationArray)
    #Выполнить идентификацию объектов, если передан массив
    lResultList=[]
    lTempObject=None
    if len(inControlSpecificationArray) > 0:
        #Сформировать выборку элементов, которые подходят под первый уровень спецификации
        lSpecDeepCopy = copy.deepcopy(inControlSpecificationArray)
        lSpecDeepCopy[0]["backend"]=lBackend
        lSpecificationLvL1List = pywinauto.findwindows.find_elements(**lSpecDeepCopy[0])
        for lItem in lSpecificationLvL1List:
            #Сделать независимую копию и установить информацию о process_id и handle
            lItemControlSpecificationArray=copy.deepcopy(inControlSpecificationArray)
            lItemControlSpecificationArray[0]["process_id"]=lItem.process_id
            lItemControlSpecificationArray[0]["handle"]=lItem.handle
            lItemControlSpecificationOriginArray=copy.deepcopy(inControlSpecificationOriginArray)
            lItemControlSpecificationOriginArray[0]["process_id"]=lItem.process_id
            lItemControlSpecificationOriginArray[0]["handle"]=lItem.handle
            #Выполнить подключение к объекту
            lRPAApplication = pywinauto.Application(backend=lBackend)
            #Проверка разрядности
            try:
                lRPAApplication.connect(**lItemControlSpecificationArray[0])
            except Exception as e:
                UIOSelector_TryRestore_Dict(lItemControlSpecificationArray)
                try:
                    lRPAApplication.connect(**lItemControlSpecificationArray[0])
                except Exception as e:
                    lRPAApplication = None
            if lRPAApplication is not None:
                #lTempObject=lRPAApplication.window(**lItemControlSpecificationArray[0])
                #Скорректировано из-за недопонимания структуры
                lTempObject=lRPAApplication
                #Нормализация массива для целей выборки объекта (удаление конфликтующих ключей)
                lItemControlSpecificationArray=UIOSelector_SearchUIONormalize_UIOSelector(lItemControlSpecificationOriginArray)
                #Циклическое прохождение к недрам объекта
                for lWindowSpecification in lItemControlSpecificationArray[0:]:
                    lTempObject=lTempObject.window(**lWindowSpecification)
                #Добавить объект в результирующий массив
                lResultList.append(lTempObject)
    return lResultList

def PWASpecification_Get_PWAApplication(inControlSpecificationArray):
    """L-,W+: Получить значение атрибута backend по PWA (pywinauto) селектору. Мы рекомендуем использовать метод UIOSelector_UIO_Get, так как UIO селектор обладает большей функциональностью.

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lBackendStr = UIDesktop.PWASpecification_Get_PWAApplication(lDemoBaseUIOSelector) # Получить backend по PWA селектору

    :param inControlSpecificationArray: PWA селектор, который определяет критерии поиска UIO объекта
        Допустимые ключи PWA селектора:

        - class_name содержимое атрибута class UIO объекта
        - class_name_re содержимое атрибута class UIO объекта, которое удовлетворяет установленному рег. выражению
        - process идентификатор процесса, в котором находится UIO объект
        - title содержимое атрибута title UIO объекта
        - title_re содержимое атрибута title UIO объекта, которое удовлетворяет установленному рег. выражению
        - top_level_only признак поиска только на верхнем уровне приложения. По умолчанию True
        - visible_only признак поиска только среди видимых UIO объектов. По умолчанию True
        - enabled_only признак поиска только среди разблокированных UIO объектов. По умолчанию False
        - best_match содержимое атрибута title UIO объекта максимально приближено к заданному
        - handle идентификатор handle искомого UIO объекта 
        - ctrl_index индекс UIO объекта среди всех дочерних объектов в списке родительского
        - found_index индекс UIO объекта среди всех обнаруженных
        - predicate_func пользовательская функция проверки соответсвия UIO элемента
        - active_only признак поиска только среди активных UIO объектов. По умолчанию False
        - control_id идентификатор control_id искомого UIO объекта 
        - control_type тип элемента (применимо, если backend == "uia")
        - auto_id идентификатор auto_id искомого UIO объекта (применимо, если backend == "uia")
        - framework_id идентификатор framework_id искомого UIO объекта (применимо, если backend == "uia")
        - backend вид технологии подключения к поиску UIO объекта ("uia" или "win32")
    :type inControlSpecificationArray: list, обязательный
    :return: "win32" или "uia"
    """
    inControlSpecificationArray=copy.deepcopy(inControlSpecificationArray)
    #Определение backend
    lBackend=mDefaultPywinautoBackend
    if "backend" in inControlSpecificationArray[0]:
        lBackend=inControlSpecificationArray[0]["backend"]
        inControlSpecificationArray[0].pop("backend")
    #Подготовка входного массива
    inControlSpecificationOriginArray=inControlSpecificationArray
    inControlSpecificationArray=UIOSelector_SearchProcessNormalize_UIOSelector(inControlSpecificationArray)
    #Выполнить идентификацию объектов, если передан массив
    lResultList=[]
    lTempObject=None
    if len(inControlSpecificationArray) > 0:
        #Выполнить подключение к объекту
        lRPAApplication = pywinauto.Application(backend=lBackend)
        #Проверка разрядности
        try:
            lRPAApplication.connect(**inControlSpecificationArray[0])
        except Exception as e:
            UIOSelector_TryRestore_Dict(inControlSpecificationArray)
            try:
                lRPAApplication.connect(**inControlSpecificationArray[0])
            except Exception as e:
                lRPAApplication = None
        if lRPAApplication is not None:
            #lTempObject=lRPAApplication.window(**inControlSpecificationArray[0])
            #Скорректировано из-за недопонимания структуры
            lTempObject=lRPAApplication
    return lTempObject
#old: AutomationSearchMouseElement
def UIOSelector_SearchChildByMouse_UIO(inElementSpecification):
    """L-,W+: Инициировать визуальный поиск UIO объекта с помощью указателя мыши. При наведении указателя мыши UIO объект выделяется зеленой рамкой. Остановить режим поиска можно с помощью зажима клавиши ctrl left на протяжении нескольких секунд. После этого в веб окне студии будет отображено дерево расположения искомого UIO объекта.

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lUIO = UIDesktop.UIOSelector_SearchChildByMouse_UIO(lDemoBaseUIOSelector) # Инициировать поиск дочернего UIO объекта, который расположен внутри lDemoBaseUIOSelector.

    :param inElementSpecification: UIO селектор, который определяет критерии поиска родительского UIO объекта, в котором будет производиться поиск дочернего UIO объекта
    :type inElementSpecification: list, обязательный
    :return: UIO объект или None (если UIO не был обнаружен)
    """
    lGUISearchElementSelected=None
    #Настройка - частота обновления подсвечивания
    lTimeSleepSeconds=0.4
    lElementFoundedList=[]
    #Ветка поиска в режиме реального времени
    #Сбросить нажатие Ctrl, если оно было
    bool(win32api.GetAsyncKeyState(16))
    bool(win32api.GetAsyncKeyState(17))
    bool(win32api.GetAsyncKeyState(18))
    #Оптимизация - получить объект для опроса единажды
    lUIORoot=UIOSelector_Get_UIO(inElementSpecification)
    lFlagLoop = True
    (lX,lY) = win32api.GetCursorPos()
    while lFlagLoop:
        #Проверить, нажата ли клавиша Ctrl (код 17)
        lFlagKeyPressedCtrl=bool(win32api.GetAsyncKeyState(17))
        lAltBool=bool(win32api.GetAsyncKeyState(18)) or bool(win32api.GetAsyncKeyState(16))
        #Подсветить объект, если мышка наведена над тем объектом, который не подсвечивался в прошлый раз
        if not lFlagKeyPressedCtrl:
            #Получить координаты мыши
            if lAltBool == False: # СВЕТИТЬ, НО НЕ ВЫБИРАТЬ
                (lX,lY) = win32api.GetCursorPos()
            lElementFounded={}
            #Создать карту пикселей и элементов
            #####Внимание! Функция UIOXY_SearchChild_ListDict не написана
            lElementFoundedList=UIOXY_SearchChild_ListDict(lUIORoot,lX,lY)
            lElementFounded=lElementFoundedList[-1]["element"]
            #Подсветить объект, если он мышь раньше стояла на другом объекте
            if lGUISearchElementSelected != lElementFounded:
                lGUISearchElementSelected = lElementFounded
            #Доработанная функция отрисовки
            if lElementFounded is not None:
                UIO_Highlight(lElementFounded)
        else:
            #Была нажата клавиша Ctrl - выйти из цикла
            lFlagLoop=False
        #Заснуть до следующего цикла
        time.sleep(lTimeSleepSeconds)
    #Вернуть результат поиска
    return lElementFoundedList

#old: - AutomationSearchMouseElementHierarchy
def UIOSelector_SearchChildByMouse_UIOTree(inUIOSelector):
    """L-,W+: Получить список уровней UIO объекта с указнием всех имеющихся атрибутов по входящему UIO селектору.

    !ВНИМАНИЕ! ДАННАЯ ФУНКЦИОНАЛЬНОСТЬ В АВТОМАТИЧЕСКОМ РЕЖИМЕ ПОДДЕРЖИВАЕТ ВСЕ РАЗРЯДНОСТИ ПРИЛОЖЕНИЙ (32|64), КОТОРЫЕ ЗАПУЩЕНЫ В СЕСИИ. PYTHON x64 ИМЕЕТ ВОЗМОЖНОСТЬ ВЗЗАИМОДЕЙСТВИЯ С x32 UIO ОБЪЕКТАМИ, НО МЫ РЕКОМЕНДУЕМ ДОПОЛНИТЕЛЬНО ИСПОЛЬЗОВАТЬ ИНТЕРПРЕТАТОР PYTHON x32 (ПОДРОБНЕЕ СМ. ФУНКЦИЮ Configure())

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lBackendStr = UIDesktop.UIOSelector_SearchChildByMouse_UIOTree(lDemoBaseUIOSelector) # Получить список атрибутов всех родительских элементов lDemoBaseUIOSelector.

    :param inUIOSelector: UIO селектор, который определяет UIO объект, для которого будет произведено извлечение всех атрибутов на всех уровнях.
    :type inUIOSelector: list, обязательный
    :return: list, список атрибутов на каждом уровне UIO объекта
    """

    lItemInfo = []
    #Check the bitness
    lSafeOtherProcess = UIOSelector_SafeOtherGet_Process(inUIOSelector)
    if lSafeOtherProcess is None:
        #Запустить функцию поиска элемента по мыши
        lElementList = UIOSelector_SearchChildByMouse_UIO(inUIOSelector)
        lElement = lElementList[-1]['element']
        #Detect backend of the elements
        lFlagIsBackendWin32 = True
        #Если объект имеется (не None), то выполнить построение иерархии
        if lElement is not None:
            if lElement.backend.name == 'uia':
                lFlagIsBackendWin32 = False
            #Циклическое создание дерева
            #while lElement is not None:
            lListIterator=0
            lItemInfo2=lItemInfo
            for lListItem in lElementList:
                lElement = lListItem["element"]
                #Продолжать построение иерархии во всех случаях кроме бэк uia & parent() is None
                #if not lFlagIsBackendWin32 and lElement.parent() is None:
                #    lElement = None
                #else:
                #Получить информацию про объект
                lItemInfo2.append(UIOEI_Convert_UIOInfo(lElement.element_info))
                #Дообогатить информацией об индексе ребенка в родительском объекте
                if "index" in lListItem:
                    if lListItem["index"] is not None:
                        lItemInfo2[-1]['ctrl_index']=lListItem["index"]
                    else:
                        if "ctrl_index" in lListItem:
                            lItemInfo2[-1]['ctrl_index']=lListItem["ctrl_index"]
                else:
                    if "ctrl_index" in lListItem:
                        lItemInfo2[-1]['ctrl_index']=lListItem["ctrl_index"]
                #Оборачиваем потомка в массив, потому что у родителя по структуре интерфейса может быть больше одного наследников
                lItemInfo2[-1]['SpecificationChild']=[]
                lItemInfo2=lItemInfo2[-1]['SpecificationChild']
                #Переход на родительский объект
                #lElement = lElement.parent()
                lListIterator=lListIterator+1
            #Добавить информацию о Backend в первый объект
            lItemInfo[0]["backend"]=lElement.backend.name
    else:
        # Run function from other process with help of PIPE
        lPIPEResuestDict = {"ModuleName": "UIDesktop", "ActivityName": "UIOSelector_SearchChildByMouse_UIOTree",
                            "ArgumentList": [inUIOSelector],
                            "ArgumentDict": {}}
        # Отправить запрос в дочерний процесс, который отвечает за работу с Windows окнами
        ProcessCommunicator.ProcessChildSendObject(lSafeOtherProcess, lPIPEResuestDict)
        # Get answer from child process
        lPIPEResponseDict = ProcessCommunicator.ProcessChildReadWaitObject(lSafeOtherProcess)
        if lPIPEResponseDict["ErrorFlag"]:
            raise Exception(
                f"Exception was occured in child process (message): {lPIPEResponseDict['ErrorMessage']}, (traceback): {lPIPEResponseDict['ErrorTraceback']}")
        else:
            lItemInfo = lPIPEResponseDict["Result"]
    #Вернуть результат
    return lItemInfo
#old name - PywinautoExtElementCtrlIndexGet
def UIO_GetCtrlIndex_Int(inElement):
    """L-,W+: Получить индекс UIO объекта inElement в списке родительского UIO объекта.

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lUIO = UIDesktop.UIOSelector_Get_UIO(lDemoBaseUIOSelector) # Получить UIO объект по UIO селектору.
        lUIOIndexInt = UIDesktop.UIO_GetCtrlIndex_Int(lUIO) # Получить индекс UIO объекта в списке у родительского UIO объекта.

    :param inElement: UIO объект, для которого требуется определить индекс в списке родительского UIO объекта.
    :type inElement: list, обязательный
    :return: int, индекс UIO объекта в списке родительского UIO объекта
    """
    lResult = None
    #Выполнить алгоритм, если есть Element
    if inElement is not None:
        lElementParent = inElement.parent()
        if lElementParent is not None:
            lResult = 0
            lFlagFind = True
            #Получить список потомков
            lElementParentChildrenList = lElementParent.children()
            #Циклический поиск до того момента, пока не упремся в текущий элемент
            while lFlagFind:
                if lResult<len(lElementParentChildrenList):
                    #Прекратить поиск, если элемент был обнаружен
                    if inElement == lElementParentChildrenList[lResult]:
                        lFlagFind = False
                    else:
                        #Прекратить поиски, если итератор вышел за пределы списка
                        if lResult>=len(lElementParentChildrenList):
                            lResult = None
                            lFlagFind = False
                        else:
                            lResult = lResult + 1
                else:
                    lResult=-1
                    lFlagFind=False
    #Вернуть результат    
    return lResult

#old: - PywinautoExtElementsGetInfo
def UIOSelector_Get_UIOInfoList (inUIOSelector, inElement=None):
    """L-,W+: Техническая функция: Получить список параметров последних уровней UIO селектора по UIO объектам, которые удовлетворяют входящим inUIOSelector, поиск по которым будет производится от уровня inElement.

    !ВНИМАНИЕ! ДАННАЯ ФУНКЦИОНАЛЬНОСТЬ В АВТОМАТИЧЕСКОМ РЕЖИМЕ ПОДДЕРЖИВАЕТ ВСЕ РАЗРЯДНОСТИ ПРИЛОЖЕНИЙ (32|64), КОТОРЫЕ ЗАПУЩЕНЫ В СЕСИИ. PYTHON x64 ИМЕЕТ ВОЗМОЖНОСТЬ ВЗЗАИМОДЕЙСТВИЯ С x32 UIO ОБЪЕКТАМИ, НО МЫ РЕКОМЕНДУЕМ ДОПОЛНИТЕЛЬНО ИСПОЛЬЗОВАТЬ ИНТЕРПРЕТАТОР PYTHON x32 (ПОДРОБНЕЕ СМ. ФУНКЦИЮ Configure())

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lUIOInfoList = UIDesktop.UIOSelector_Get_UIOInfoList(lDemoBaseUIOSelector) # Получить словарь параметров по UIO селектору.

    :param inUIOSelector: UIO селектор, который определяет UIO объект, для которого будет произведено извлечение всех атрибутов на всех уровнях.
    :type inUIOSelector: list, обязательный
    :param inElement: UIO объект, от которого выполнить поиск дочерних UIO объектов по UIO селектору inUIOSelector. По умолчанию None - поиск среди всех приложений.
    :type inElement: UIO объект, необязательный
    :return: dict, пример: {"title":None,"rich_text":None,"process_id":None,"process":None,"handle":None,"class_name":None,"control_type":None,"control_id":None,"rectangle":{"left":None,"top":None,"right":None,"bottom":None}, 'runtime_id':None}
    """
    #Check the bitness
    lSafeOtherProcess = UIOSelector_SafeOtherGet_Process(inUIOSelector)
    if lSafeOtherProcess is None:
        #Получить родительский объект если на вход ничего не поступило
        lResultList=UIOSelector_Get_UIOList(inUIOSelector, inElement)
        lIterator = 0
        for lItem in lResultList:
            lResultList[lIterator]=UIOEI_Convert_UIOInfo(lResultList[lIterator].element_info)
            lIterator = lIterator + 1
    else:
        # Run function from other process with help of PIPE
        lPIPEResuestDict = {"ModuleName": "UIDesktop", "ActivityName": "UIOSelector_Get_UIOInfoList",
                            "ArgumentList": [inUIOSelector, inElement],
                            "ArgumentDict": {}}
        # Отправить запрос в дочерний процесс, который отвечает за работу с Windows окнами
        ProcessCommunicator.ProcessChildSendObject(lSafeOtherProcess, lPIPEResuestDict)
        # Get answer from child process
        lPIPEResponseDict = ProcessCommunicator.ProcessChildReadWaitObject(lSafeOtherProcess)
        if lPIPEResponseDict["ErrorFlag"]:
            raise Exception(
                f"Exception was occured in child process (message): {lPIPEResponseDict['ErrorMessage']}, (traceback): {lPIPEResponseDict['ErrorTraceback']}")
        else:
            lResultList = lPIPEResponseDict["Result"]
    return lResultList

#old: - PywinautoExtTryToRestore
def UIOSelector_TryRestore_Dict(inSpecificationList):
    """L-,W+: Восстановить окно приложения на экране по UIO селектору inSpecificationList, если оно было свернуто. Функция обернута в try .. except - ошибок не возникнет.

    !ВНИМАНИЕ! ДАННАЯ ФУНКЦИОНАЛЬНОСТЬ УЖЕ ИСПОЛЬЗУЕТСЯ В РЯДЕ ДРУГИХ ФУНКЦИЙ ТАК КАК АДРЕССАЦИЯ ПО UIA FRAMEWORK НЕДОСТУПНА, ЕСЛИ ПРИЛОЖЕНИЕ СВЕРНУТО.

    !ВНИМАНИЕ! ДАННАЯ ФУНКЦИОНАЛЬНОСТЬ В АВТОМАТИЧЕСКОМ РЕЖИМЕ ПОДДЕРЖИВАЕТ ВСЕ РАЗРЯДНОСТИ ПРИЛОЖЕНИЙ (32|64), КОТОРЫЕ ЗАПУЩЕНЫ В СЕСИИ. PYTHON x64 ИМЕЕТ ВОЗМОЖНОСТЬ ВЗЗАИМОДЕЙСТВИЯ С x32 UIO ОБЪЕКТАМИ, НО МЫ РЕКОМЕНДУЕМ ДОПОЛНИТЕЛЬНО ИСПОЛЬЗОВАТЬ ИНТЕРПРЕТАТОР PYTHON x32 (ПОДРОБНЕЕ СМ. ФУНКЦИЮ Configure())

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        UIDesktop.UIOSelector_TryRestore_Dict(lDemoBaseUIOSelector) # Попытка восстановления свернутого окна по UIO селектору.

    :param inSpecificationList: UIO селектор, который определяет UIO объект, для которого будет произведено извлечение всех атрибутов на всех уровнях.
    :type inSpecificationList: list, обязательный
    """
    lResult={}
    try:
        #Подготовка взодного массива
        inControlSpecificationArray=UIOSelector_SearchUIONormalize_UIOSelector(inSpecificationList)
        #Выполнить подключение к объекту. Восстановление необходимо только в бэке win32,
        #так как в uia свернутое окно не распознается
        lRPAApplication = pywinauto.Application(backend="win32")
        lRPAApplication.connect(**inSpecificationList[0])
        lRPAApplication.top_window().restore()
    except Exception:
        True==False
    return lResult

#old: - ElementActionGetList
def UIOSelector_Get_UIOActivityList (inUIOSelector):
    """L-,W+: Получить список доступных действий/функций по UIO селектору inUIOSelector. Описание возможных активностей см. ниже.

    !ВНИМАНИЕ! ДАННАЯ ФУНКЦИОНАЛЬНОСТЬ В АВТОМАТИЧЕСКОМ РЕЖИМЕ ПОДДЕРЖИВАЕТ ВСЕ РАЗРЯДНОСТИ ПРИЛОЖЕНИЙ (32|64), КОТОРЫЕ ЗАПУЩЕНЫ В СЕСИИ. PYTHON x64 ИМЕЕТ ВОЗМОЖНОСТЬ ВЗЗАИМОДЕЙСТВИЯ С x32 UIO ОБЪЕКТАМИ, НО МЫ РЕКОМЕНДУЕМ ДОПОЛНИТЕЛЬНО ИСПОЛЬЗОВАТЬ ИНТЕРПРЕТАТОР PYTHON x32 (ПОДРОБНЕЕ СМ. ФУНКЦИЮ Configure())

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lActivityList = UIDesktop.UIOSelector_Get_UIOActivityList(lDemoBaseUIOSelector) # Получить список активностей по UIO селектору.

    :param inUIOSelector: UIO селектор, который определяет UIO объект, для которого будет представлен перечень доступных активностей.
    :type inUIOSelector: list, обязательный
    """
    #Check the bitness
    lSafeOtherProcess = UIOSelector_SafeOtherGet_Process(inUIOSelector)
    if lSafeOtherProcess is None:
        #Получить объект
        lObject=UIOSelector_Get_UIO(inUIOSelector)
        lActionList=dir(lObject)
        lResult=dir(lObject)
        #Выполнить чистку списка от неактуальных методов
        for lActionItem in lActionList:
            #Удалить те, которые начинаются на _
            if lActionItem[0]=='_':
                lResult.remove(lActionItem)
            #Удалить те, которые начинаются с символа верхнего регистра
            if lActionItem[0].isupper():
                lResult.remove(lActionItem)
    else:
        # Run function from other process with help of PIPE
        lPIPEResuestDict = {"ModuleName": "UIDesktop", "ActivityName": "UIOSelector_Get_UIOActivityList",
                            "ArgumentList": [inUIOSelector],
                            "ArgumentDict": {}}
        # Отправить запрос в дочерний процесс, который отвечает за работу с Windows окнами
        ProcessCommunicator.ProcessChildSendObject(lSafeOtherProcess, lPIPEResuestDict)
        # Get answer from child process
        lPIPEResponseDict = ProcessCommunicator.ProcessChildReadWaitObject(lSafeOtherProcess)
        if lPIPEResponseDict["ErrorFlag"]:
            raise Exception(
                f"Exception was occured in child process (message): {lPIPEResponseDict['ErrorMessage']}, (traceback): {lPIPEResponseDict['ErrorTraceback']}")
        else:
            lResult = lPIPEResponseDict["Result"]
    return lResult

#old: - ElementRunAction
def UIOSelectorUIOActivity_Run_Dict(inUIOSelector, inActionName, inArgumentList=None, inkwArgumentObject=None):
    """L-,W+: Выполнить активность inActionName над UIO объектом, полученным с помощью UIO селектора inUIOSelector. Описание возможных активностей см. ниже.

    !ВНИМАНИЕ! ДАННАЯ ФУНКЦИОНАЛЬНОСТЬ В АВТОМАТИЧЕСКОМ РЕЖИМЕ ПОДДЕРЖИВАЕТ ВСЕ РАЗРЯДНОСТИ ПРИЛОЖЕНИЙ (32|64), КОТОРЫЕ ЗАПУЩЕНЫ В СЕСИИ. PYTHON x64 ИМЕЕТ ВОЗМОЖНОСТЬ ВЗЗАИМОДЕЙСТВИЯ С x32 UIO ОБЪЕКТАМИ, НО МЫ РЕКОМЕНДУЕМ ДОПОЛНИТЕЛЬНО ИСПОЛЬЗОВАТЬ ИНТЕРПРЕТАТОР PYTHON x32 (ПОДРОБНЕЕ СМ. ФУНКЦИЮ Configure())

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lActivityResult = UIDesktop.UIOSelectorUIOActivity_Run_Dict(lDemoBaseUIOSelector, "click") # выполнить действие над UIO объектом с помощью UIO селектора.

    :param inUIOSelector: UIO селектор, который определяет UIO объект, для которого будет представлен перечень доступных активностей.
    :type inUIOSelector: list, обязательный
    :param inActionName: наименование активности, которую требуется выполнить над UIO объектом
    :type inActionName: str, обязательный
    :param inArgumentList: список передаваемых неименованных аргументов в функцию inActionName
    :type inArgumentList: list, необязательный
    :param inkwArgumentObject: словарь передаваемых именованных аргументов в функцию inActionName
    :type inkwArgumentObject: dict, необязательный
    :return: возвращает результат запускаемой функции с наименованием inActionName над UIO объектом
    """
    if inArgumentList is None: inArgumentList=[] # 2021 02 22 Minor fix by Ivan Maslov
    if inkwArgumentObject is None: inkwArgumentObject={} # 2021 02 22 Minor fix by Ivan Maslov
    lResult={}
    #Check the bitness
    lSafeOtherProcess = UIOSelector_SafeOtherGet_Process(inUIOSelector)
    #Run activity if SafeOtherProcess is None
    if lSafeOtherProcess is None:
        #Определить объект
        lObject=UIOSelector_Get_UIO(inUIOSelector)
        #Получить метод для вызова
        lFunction = getattr(lObject, inActionName)
        #Выполнить действие
        #Обернуто в безопасную обработку, тк для некоторых объектов метод не работает и может выдавать ошибку типа: NotImplementedError: This method not work properly for WinForms DataGrid, use cells()
        try:
            return lFunction(*inArgumentList,**inkwArgumentObject)
        except Exception as e:
            #Если ошибка возникла на action get_properties
            if inActionName=="get_properties":
                lResult={}
                #Ручное формирование
                lResult["class_name"]=lObject.class_name()
                lResult["friendly_class_name"]=lObject.friendly_class_name()
                lResult["texts"]=lObject.texts()
                lResult["control_id"]=lObject.control_id()
                lResult["control_count"]=lObject.control_count()
                lResult["automation_id"]=lObject.automation_id()
                return lResult
            else:
                raise e
    else:
        #Run function from other process with help of PIPE
        lPIPEResuestDict = {"ModuleName": "UIDesktop", "ActivityName": "UIOSelectorUIOActivity_Run_Dict",
         "ArgumentList": [inUIOSelector, inActionName, inArgumentList, inkwArgumentObject],
         "ArgumentDict": {}}
        # Отправить запрос в дочерний процесс, который отвечает за работу с Windows окнами
        ProcessCommunicator.ProcessChildSendObject(lSafeOtherProcess, lPIPEResuestDict)
        # Get answer from child process
        lPIPEResponseDict = ProcessCommunicator.ProcessChildReadWaitObject(lSafeOtherProcess)
        if lPIPEResponseDict["ErrorFlag"]:
            raise Exception(f"Exception was occured in child process (message): {lPIPEResponseDict['ErrorMessage']}, (traceback): {lPIPEResponseDict['ErrorTraceback']}")
        else:
            lResult = lPIPEResponseDict["Result"]
    return lResult

#old name - ElementGetInfo
def UIOSelector_Get_UIOInfo(inUIOSelector):
    """L-,W+: Получить свойства UIO объекта (element_info), по заданному UIO селектору. Ниже представлен перечень возвращаемых свойств.

    Для backend = win32:
    
    - automation_id (int)
    - class_name (str)
    - control_id (int)
    - control_type (str)
    - full_control_type (str)
    - enabled (bool)
    - handle (int)
    - name (str)
    - parent (object/UIO)
    - process_id (int)
    - rectangle (object/rect)
    - rich_text (str)
    - visible (bool)

    Для backend = uia:

    - automation_id (int)
    - class_name (str)
    - control_id (int)
    - control_type (str)
    - enabled (bool)
    - framework_id (int)
    - handle (int)
    - name (str)
    - parent (object/UIO)
    - process_id (int)
    - rectangle (object/rect)
    - rich_text (str)
    - runtime_id (int)
    - visible (bool)

    !ВНИМАНИЕ! ДАННАЯ ФУНКЦИОНАЛЬНОСТЬ В АВТОМАТИЧЕСКОМ РЕЖИМЕ ПОДДЕРЖИВАЕТ ВСЕ РАЗРЯДНОСТИ ПРИЛОЖЕНИЙ (32|64), КОТОРЫЕ ЗАПУЩЕНЫ В СЕСИИ. PYTHON x64 ИМЕЕТ ВОЗМОЖНОСТЬ ВЗЗАИМОДЕЙСТВИЯ С x32 UIO ОБЪЕКТАМИ, НО МЫ РЕКОМЕНДУЕМ ДОПОЛНИТЕЛЬНО ИСПОЛЬЗОВАТЬ ИНТЕРПРЕТАТОР PYTHON x32 (ПОДРОБНЕЕ СМ. ФУНКЦИЮ Configure())

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lUIOElementInfoDict = UIDesktop.UIOSelector_Get_UIOInfo(lDemoBaseUIOSelector) #Получить свойства над UIO объектом с помощью UIO селектора.

    :param inUIOSelector: UIO селектор, который определяет UIO объект, для которого будет представлен перечень доступных активностей.
    :type inUIOSelector: list, обязательный
    :return: словарь свойств element_info: Пример {"control_id": ..., "process_id": ...}
    """
    #Check the bitness
    lSafeOtherProcess = UIOSelector_SafeOtherGet_Process(inUIOSelector)
    if lSafeOtherProcess is None:
        #Подготовка входного массива
        inUIOSelector=UIOSelector_SearchUIONormalize_UIOSelector(inUIOSelector)
        #Выполнить идентификацию объектов, если передан массив
        lResultList=[]
        if len(inUIOSelector) > 0:
            #Получить объект
            lTempObject=UIOSelector_Get_UIO(inUIOSelector)
            #Получить инфо объект
            lTempObjectInfo = lTempObject.element_info
            #Добавить информацию об обнаруженом объекте
            lResultList.append(UIOEI_Convert_UIOInfo(lTempObjectInfo))
    else:
        # Run function from other process with help of PIPE
        lPIPEResuestDict = {"ModuleName": "UIDesktop", "ActivityName": "UIOSelector_Get_UIOInfo",
                            "ArgumentList": [inUIOSelector],
                            "ArgumentDict": {}}
        # Отправить запрос в дочерний процесс, который отвечает за работу с Windows окнами
        ProcessCommunicator.ProcessChildSendObject(lSafeOtherProcess, lPIPEResuestDict)
        # Get answer from child process
        lPIPEResponseDict = ProcessCommunicator.ProcessChildReadWaitObject(lSafeOtherProcess)
        if lPIPEResponseDict["ErrorFlag"]:
            raise Exception(
                f"Exception was occured in child process (message): {lPIPEResponseDict['ErrorMessage']}, (traceback): {lPIPEResponseDict['ErrorTraceback']}")
        else:
            lResultList = lPIPEResponseDict["Result"]
    return lResultList
#old: - GUISearchElementByRootXY
def UIOXY_SearchChild_ListDict(inRootElement,inX,inY,inHierarchyList=None):
    """L-,W+: Техническая функция: Получить иерархию вложенности UIO объекта по заданным корневому UIO объекту, координатам X и Y.

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lUIO = UIDesktop.UIOSelector_Get_UIO(lDemoBaseUIOSelector) # Получить UIO объект с помощью UIO селектора
        lUIOHierarchyList = UIDesktop.UIOXY_SearchChild_ListDict(lUIO, 100, 200) # Получить UIO объект с помощью UIO селектора родительского элемента и координат X / Y

    :param inRootElement: родительский UIO объект, полученный ранее с помощью UIO селектора.
    :type inRootElement: object UIO, обязательный
    :param inX: родительский UIO объект, полученный ранее с помощью UIO селектора.
    :type inX: int, обязательный
    :param inY: родительский UIO объект, полученный ранее с помощью UIO селектора.
    :type inY: int, обязательный
    :return: Список словарей - уровней UIO объектов
    """
    if inHierarchyList is None: inHierarchyList = []
    #Инициализация результирующего значения
    lResultElement = None
    lResultElementX1 = None
    lResultElementX2 = None
    lResultElementY1 = None
    lResultElementY2 = None
    lResultHierarchyList=[{'index':None,'element':None}]
    #Получить координаты текущего объекта
    try:
        lRootElementRectX1=inRootElement.element_info.rectangle.left
        lRootElementRectX2=inRootElement.element_info.rectangle.right
        lRootElementRectY1=inRootElement.element_info.rectangle.top
        lRootElementRectY2=inRootElement.element_info.rectangle.bottom
        #Добавить объект в результирующий, если координаты попадают в него
        if inX>=lRootElementRectX1 and inX<=lRootElementRectX2 and inY>=lRootElementRectY1 and inY<=lRootElementRectY2:
            lResultElement = inRootElement
            lResultElementX1 = lRootElementRectX1
            lResultElementX2 = lRootElementRectX2
            lResultElementY1 = lRootElementRectY1
            lResultElementY2 = lRootElementRectY2
            #Сформировать результирующий обьъект
            lParentHierarchy = inHierarchyList
            if len(lParentHierarchy)==0:
                lParentHierarchy.append({"index":None,"element":lResultElement})
            else:
                lParentHierarchy[-1]["element"] = lResultElement
            lResultHierarchyList=lParentHierarchy
            #Получить список детей и добавить в карту
            lChildIterator=0
            for lChildElement in inRootElement.children():
                #Сформировать результирующий массив
                lChildFoundedHierarchyList = lParentHierarchy.copy()
                lChildFoundedHierarchyList.append({'index': lChildIterator})
                lChildFoundedHierarchyList = UIOXY_SearchChild_ListDict(lChildElement,inX,inY, lChildFoundedHierarchyList)
                lChildFoundedElement = lChildFoundedHierarchyList[-1]["element"]
                #Установить обнаруженный элемент, если текущий результат пустой
                if lResultElement is None and lChildFoundedElement is not None:
                    lResultElement = lChildFoundedElement
                    lResultElementX1 = lResultElement.element_info.rectangle.left
                    lResultElementX2 = lResultElement.element_info.rectangle.right
                    lResultElementY1 = lResultElement.element_info.rectangle.top
                    lResultElementY2 = lResultElement.element_info.rectangle.bottom
                    lResultHierarchyList = lChildFoundedHierarchyList
                #Выполнить сверку lChildFoundedElement и lResultElement если оба имеются
                elif lResultElement is not None and lChildFoundedElement is not None: 
                    #Правила перезатирания карты, если имеется старый объект
                    #[Накладываемый объект] - НО - ElementNew
                    #[Имеющийся объект] - ИО - ElementOld
                    #3 типа вхождения объектов
                    #тип 1 - [имеющийся объект] полностью входит в [накладываемый объект] (ИО X1 Y1 >= НО X1 Y1; ИО X2 Y2 <= НО X2 Y2) - не вносить НО в bitmap в эти диапазоны
                    #тип 2 - [имеющийся объект] полностью выходит за пределы [накладываемого объекта] (ИО X1 Y1 < НО X1 Y1; ИО X2 Y2 > НО X2 Y2) - вносить НО в bitmap
                    #тип 3 - [имеющийся объект] частично входит в [накладываемый объект] (все остальные случаи)- вносить НО в bitmap
                    #Получить координаты ИО
                    lChildFoundedElementInfo = lChildFoundedElement.element_info
                    #lElementNew = inElement
                    lChildFoundedElementX1 = lChildFoundedElementInfo.rectangle.left
                    lChildFoundedElementX2 = lChildFoundedElementInfo.rectangle.right
                    lChildFoundedElementY1 = lChildFoundedElementInfo.rectangle.top
                    lChildFoundedElementY2 = lChildFoundedElementInfo.rectangle.bottom
                    #Проверка вхождения по типу 1
                    if (lResultElementX1>=lChildFoundedElementX1) and (lResultElementY1>=lChildFoundedElementY1) and (lResultElementX2<=lChildFoundedElementX2) and (lResultElementY2<=lChildFoundedElementY2):
                        False == True
                    #Проверка вхождения по типу 3
                    elif (lResultElementX1<lChildFoundedElementX1) and (lResultElementY1<lChildFoundedElementY1) and (lResultElementX2>lChildFoundedElementX2) and (lResultElementY2>lChildFoundedElementY2):
                        lResultElement = lChildFoundedElement
                        lResultElementX1 = lChildFoundedElementX1
                        lResultElementX2 = lChildFoundedElementX2
                        lResultElementY1 = lChildFoundedElementY1
                        lResultElementY2 = lChildFoundedElementY2
                        lResultHierarchyList = lChildFoundedHierarchyList
                    #Проверка вхождения по типу 2
                    else:
                        lResultElement = lChildFoundedElement
                        lResultElementX1 = lChildFoundedElementX1
                        lResultElementX2 = lChildFoundedElementX2
                        lResultElementY1 = lChildFoundedElementY1
                        lResultElementY2 = lChildFoundedElementY2
                        lResultHierarchyList = lChildFoundedHierarchyList
                lChildIterator=lChildIterator+1
    except Exception as e:
        False == False
    return lResultHierarchyList

#old: - ElementGetChildElementList
def UIOSelector_GetChildList_UIOList(inUIOSelector=None, inBackend=mDefaultPywinautoBackend):
    """L-,W+: Получить список дочерних UIO объектов по входящему UIO селектору inUIOSelector.
    
    !ВНИМАНИЕ! ДАННАЯ ФУНКЦИОНАЛЬНОСТЬ В АВТОМАТИЧЕСКОМ РЕЖИМЕ ПОДДЕРЖИВАЕТ ВСЕ РАЗРЯДНОСТИ ПРИЛОЖЕНИЙ (32|64), КОТОРЫЕ ЗАПУЩЕНЫ В СЕСИИ. PYTHON x64 ИМЕЕТ ВОЗМОЖНОСТЬ ВЗЗАИМОДЕЙСТВИЯ С x32 UIO ОБЪЕКТАМИ, НО МЫ РЕКОМЕНДУЕМ ДОПОЛНИТЕЛЬНО ИСПОЛЬЗОВАТЬ ИНТЕРПРЕТАТОР PYTHON x32 (ПОДРОБНЕЕ СМ. ФУНКЦИЮ Configure())

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lUIOList = UIDesktop.UIOSelector_GetChildList_UIOList(lDemoBaseUIOSelector) # Получить список дочерних UIO объектов с помощью UIO селектора

    :param inUIOSelector: родительский UIO объект, полученный ранее с помощью UIO селектора.
    :type inUIOSelector: list, обязательный
    :param inBackend: вид backend "win32" или "uia". По умолчанию mDefaultPywinautoBackend ("win32")
    :type inBackend: str, необязательный
    :return: список дочерних UIO объектов
    """
    if inUIOSelector is None: inUIOSelector = []
    #mRobotLogger.info(f"File!!!!")
    #mRobotLogger.info(f"inSelector:{str(inUIOSelector)}, inBackend:{str(inBackend)}")
    #pdb.set_trace()
    #Check the bitness
    lSafeOtherProcess = UIOSelector_SafeOtherGet_Process(inUIOSelector)
    if lSafeOtherProcess is None:
        #Подготовка входного массива
        inUIOSelector=UIOSelector_SearchUIONormalize_UIOSelector(inUIOSelector)
        #Выполнить идентификацию объектов, если передан массив
        lResultList=[]
        #ctypes.windll.user32.MessageBoxW(0, str(inControlSpecificationArray), "Your title", 1)
        if len(inUIOSelector) > 0:
            #Получить объект
            lTempObject = UIOSelector_Get_UIO(inUIOSelector)
            #Получить список дочерних объектов
            lTempChildList = lTempObject.children()
            lIterator=0
            #Подготовить результирующий объект
            for lChild in lTempChildList:
                lTempObjectInfo=lChild.element_info
                #Добавить информацию об обнаруженом объекте
                lObjectInfoItem=UIOEI_Convert_UIOInfo(lTempObjectInfo)
                #Итератор внутри объекта (для точной идентификации)
                lObjectInfoItem['ctrl_index']=lIterator
                lResultList.append(lObjectInfoItem)
                #Инкремент счетчика
                lIterator=lIterator+1
        else:
            lResultList=BackendStr_GetTopLevelList_UIOInfo(inBackend)
            #Установка бэк-енда на первый элемент
            for lItem in lResultList:
                lItem["backend"]=inBackend
    else:
        # Run function from other process with help of PIPE
        lPIPEResuestDict = {"ModuleName": "UIDesktop", "ActivityName": "UIOSelector_GetChildList_UIOList",
                            "ArgumentList": [inUIOSelector, inBackend],
                            "ArgumentDict": {}}
        # Отправить запрос в дочерний процесс, который отвечает за работу с Windows окнами
        ProcessCommunicator.ProcessChildSendObject(lSafeOtherProcess, lPIPEResuestDict)
        # Get answer from child process
        lPIPEResponseDict = ProcessCommunicator.ProcessChildReadWaitObject(lSafeOtherProcess)
        if lPIPEResponseDict["ErrorFlag"]:
            raise Exception(
                f"Exception was occured in child process (message): {lPIPEResponseDict['ErrorMessage']}, (traceback): {lPIPEResponseDict['ErrorTraceback']}")
        else:
            lResultList = lPIPEResponseDict["Result"]
    return lResultList

#old1: - ElementSpecificationArraySearchPrepare
#old2: - ElementSpecificationListNormalize
def UIOSelector_SearchUIONormalize_UIOSelector (inControlSpecificationArray):
    """L-,W+: Нормализовать UIO селектор для дальнейшего использования в функциях поиск UIO объекта. Если недопустимых атрибутов не присутствует, то оставить как есть.

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelectorDitry = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lDemoBaseUIOSelectorClean = UIDesktop.UIOSelector_SearchUIONormalize_UIOSelector(lDemoBaseUIOSelectorDitry) # Очистить UIO селектор от недопустимых ключей для дальнейшего использования

    :param inControlSpecificationArray: UIO селектор, который определяет UIO объект, для которого будет представлен перечень доступных активностей.
    :type inControlSpecificationArray: list, обязательный
    :return: нормализованный UIO селектор
    """
    lResult=[]
    #Циклический обход
    for lSpecificationItem in inControlSpecificationArray:
        lSpecificationItemNew=lSpecificationItem.copy()
        #Перебор всех элементов
        for lItemKey,lItemValue in lSpecificationItem.items():
            #Флаг удаления атрибута
            lFlagRemoveAttribute=False
            #############################
            #Если является вложенным словарем - удалить
            if type(lItemValue) is dict:
                lFlagRemoveAttribute=True
            #Является типом None
            if lItemValue is None:
                lFlagRemoveAttribute=True
            #Проверка допустимого ключевого слова
            if (
                lItemKey == "class_name" or
                lItemKey == "class_name_re" or
                lItemKey == "parent" or
                lItemKey == "process" or
                lItemKey == "title" or
                lItemKey == "title_re" or
                lItemKey == "top_level_only" or
                lItemKey == "visible_only" or
                lItemKey == "enabled_only" or
                lItemKey == "best_match" or
                lItemKey == "handle" or
                lItemKey == "ctrl_index" or
                lItemKey == "found_index" or
                lItemKey == "predicate_func" or
                lItemKey == "active_only" or
                lItemKey == "control_id" or
                lItemKey == "control_type" or
                lItemKey == "auto_id" or
                lItemKey == "framework_id" or
                lItemKey == "backend"):
                True == True
            else:
                lFlagRemoveAttribute=True

                
            #############################
            #Конструкция по удалению ключа из словаря
            if lFlagRemoveAttribute:
                lSpecificationItemNew.pop(lItemKey)
        #Проверит наличие ctrl_index - если он есть, то удалить control_id и control_type из-за того, что они мешают друг другу
        if 'ctrl_index' in lSpecificationItemNew:
            if "control_id" in lSpecificationItemNew:
                lSpecificationItemNew.pop("control_id")
            if "control_type" in lSpecificationItemNew:
                lSpecificationItemNew.pop("control_type")
        #Проверить наличие handle - если он есть, то удалить process, control_id и control_type из-за того, что они мешают друг другу
        if 'handle' in lSpecificationItemNew:
            if "control_id" in lSpecificationItemNew:
                lSpecificationItemNew.pop("control_id")
            if "control_type" in lSpecificationItemNew:
                lSpecificationItemNew.pop("control_type")
            if "process" in lSpecificationItemNew:
                lSpecificationItemNew.pop("process")
        #Иначе Проверить наличие process - если он есть, то удалить тк он нужен только при подключении к процессу
        if 'process' in lSpecificationItemNew:
            lSpecificationItemNew.pop("process")
        #Добавить строку в результирующий массив
        lResult.append(lSpecificationItemNew)
    #Вернуть результат
    return lResult

#old name 1 - ElementSpecificationArraySearchPrepare
#old name 2 - ElementSpecificationListNormalize
def UIOSelector_SearchProcessNormalize_UIOSelector (inControlSpecificationArray):
    """L-,W+: Нормализовать UIO селектор для дальнейшего использования в функциях поиска процесса, в котором находится искомый UIO объект. Если недопустимых атрибутов не присутствует, то оставить как есть.

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelectorDitry = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lDemoBaseUIOSelectorClean = UIDesktop.UIOSelector_SearchProcessNormalize_UIOSelector(lDemoBaseUIOSelectorDitry) # Очистить UIO селектор от недопустимых ключей для дальнейшего использования

    :param inControlSpecificationArray: UIO селектор, который определяет UIO объект, для которого будет представлен перечень доступных активностей.
    :type inControlSpecificationArray: list, обязательный
    :return: нормализованный UIO селектор
    """
    lResult=[]
    #Циклический обход
    for lSpecificationItem in inControlSpecificationArray:
        lSpecificationItemNew=lSpecificationItem.copy()
        #Перебор всех элементов
        for lItemKey,lItemValue in lSpecificationItem.items():
            #Флаг удаления атрибута
            lFlagRemoveAttribute=False
            #############################
            #Если является вложенным словарем - удалить
            if type(lItemValue) is dict:
                lFlagRemoveAttribute=True
            #Является типом None
            if lItemValue is None:
                lFlagRemoveAttribute=True
            #Проверка допустимого ключевого слова
            if (
                lItemKey == "class_name" or
                lItemKey == "class_name_re" or
                lItemKey == "parent" or
                lItemKey == "process" or
                lItemKey == "title" or
                lItemKey == "title_re" or
                lItemKey == "top_level_only" or
                lItemKey == "visible_only" or
                lItemKey == "enabled_only" or
                lItemKey == "best_match" or
                lItemKey == "handle" or
                lItemKey == "ctrl_index" or
                lItemKey == "found_index" or
                lItemKey == "predicate_func" or
                lItemKey == "active_only" or
                lItemKey == "control_id" or
                lItemKey == "control_type" or
                lItemKey == "auto_id" or
                lItemKey == "framework_id" or
                lItemKey == "backend"):
                True == True
            else:
                lFlagRemoveAttribute=True

                
            #############################
            #Конструкция по удалению ключа из словаря
            if lFlagRemoveAttribute:
                lSpecificationItemNew.pop(lItemKey)
        #Проверит наличие ctrl_index - если он есть, то удалить control_id и control_type из-за того, что они мешают друг другу
        if 'ctrl_index' in lSpecificationItemNew:
            if "control_id" in lSpecificationItemNew:
                lSpecificationItemNew.pop("control_id")
            if "control_type" in lSpecificationItemNew:
                lSpecificationItemNew.pop("control_type")
        #Проверить наличие handle - если он есть, то удалить process, control_id и control_type из-за того, что они мешают друг другу
        if 'handle' in lSpecificationItemNew:
            if "control_id" in lSpecificationItemNew:
                lSpecificationItemNew.pop("control_id")
            if "control_type" in lSpecificationItemNew:
                lSpecificationItemNew.pop("control_type")
            if "process" in lSpecificationItemNew:
                lSpecificationItemNew.pop("process")
        #Иначе Проверить наличие process - если он есть, то удалить title, control_id и control_type из-за того, что они мешают друг другу
        elif 'process' in lSpecificationItemNew:
            if "control_id" in lSpecificationItemNew:
                lSpecificationItemNew.pop("control_id")
            if "control_type" in lSpecificationItemNew:
                lSpecificationItemNew.pop("control_type")
            if "title" in lSpecificationItemNew:
                lSpecificationItemNew.pop("title")
        #Добавить строку в результирующий массив
        lResult.append(lSpecificationItemNew)
    #Вернуть результат
    return lResult

#old: - ElementInfoExportObject
def UIOEI_Convert_UIOInfo(inElementInfo):
    """L-,W+: Техническая функция: Дообогащение словаря с параметрами UIO объекта по заданному UIO.element_info

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lUIO = UIDesktop.UIOSelector_Get_UIO(lDemoBaseUIOSelector) # Получить UIO объект по UIO селектору.
        lUIOProcessInfoDict = UIDesktop.UIOEI_Convert_UIOInfo(lUIO.element_info)

    :param inElementInfo: экземпляр класса UIO.element_info, для которого требуется дообогатить словарь с параметрами (в дальнейшем можно использовать как элемент UIO селектора).
    :type inElementInfo: object, обязательный
    :return: dict, пример: {"title":None,"rich_text":None,"process_id":None,"process":None,"handle":None,"class_name":None,"control_type":None,"control_id":None,"rectangle":{"left":None,"top":None,"right":None,"bottom":None}, 'runtime_id':None}
    """
    #Подготовить выходную структуру данных
    lResult = {"title":None,"rich_text":None,"process_id":None,"process":None,"handle":None,"class_name":None,"control_type":None,"control_id":None,"rectangle":{"left":None,"top":None,"right":None,"bottom":None}, 'runtime_id':None}
    #Проверка name
    try:
        lResult['title']=inElementInfo.name
    except Exception as e:
        True == False
    #Проверка rich_text
    try:
        lResult['rich_text']=inElementInfo.rich_text
    except Exception as e:
        True == False
    #Проверка process_id
    try:
        lResult['process_id']=inElementInfo.process_id
        lResult['process']=inElementInfo.process_id
    except Exception as e:
        True == False
    #Проверка handle
    try:
        lResult['handle']=inElementInfo.handle
    except Exception as e:
        True == False
    #Проверка class_name
    try:
        lResult['class_name']=inElementInfo.class_name
    except Exception as e:
        True == False
    #Проверка control_type
    try:
        lResult['control_type']=inElementInfo.control_type
    except Exception as e:
        True == False
    #Проверка control_id
    try:
        if inElementInfo.control_id!=0:
            lResult['control_id']=inElementInfo.control_id
    except Exception as e:
        True == False
    #Проверка rectangle left
    try:
        lResult['rectangle']['left']=inElementInfo.rectangle.left
    except Exception as e:
        True == False
    #Проверка rectangle right
    try:
        lResult['rectangle']['right']=inElementInfo.rectangle.right
    except Exception as e:
        True == False
    #Проверка rectangle top
    try:
        lResult['rectangle']['top']=inElementInfo.rectangle.top
    except Exception as e:
        True == False
    #Проверка rectangle bottom
    try:
        lResult['rectangle']['bottom']=inElementInfo.rectangle.bottom
    except Exception as e:
        True == False
    #Проверка runtime_id
    try:
        lResult['runtime_id']=inElementInfo.runtime_id
    except Exception as e:
        True == False
    #Вернуть результат
    return lResult

#old: - GetRootElementList
def BackendStr_GetTopLevelList_UIOInfo(inBackend=mDefaultPywinautoBackend):
    """L-,W+: Получить список UIOInfo словарей - процессы, которые запущены в рабочей сессии и готовы для взаимодействия с роботом через backend inBackend

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        lAppList = UIDesktop.BackendStr_GetTopLevelList_UIOInfo() # Очистить UIO селектор от недопустимых ключей для дальнейшего использования

    :param inBackend: вид backend, который планируется использовать для взаимодействия с UIO объектами
    :type inBackend: list, обязательный
    :return: список UIOInfo словарей
    """
    #Получить список объектов
    lResultList=pywinauto.findwindows.find_elements(top_level_only=True,backend=inBackend)    
    lResultList2=[]
    for lI in lResultList:
        lTempObjectInfo=lI
        lResultList2.append(UIOEI_Convert_UIOInfo(lI))
    return lResultList2

#old: - ElementDrawOutlineNew
def UIOSelector_Highlight(inUIOSelector):
    """L-,W+: Подсветить на несколько секунд на экране зеленой рамкой UIO объект, который соответствует входящему UIO селектору inUIOSelector

    !ВНИМАНИЕ! ДАННАЯ ФУНКЦИОНАЛЬНОСТЬ В АВТОМАТИЧЕСКОМ РЕЖИМЕ ПОДДЕРЖИВАЕТ ВСЕ РАЗРЯДНОСТИ ПРИЛОЖЕНИЙ (32|64), КОТОРЫЕ ЗАПУЩЕНЫ В СЕСИИ. PYTHON x64 ИМЕЕТ ВОЗМОЖНОСТЬ ВЗЗАИМОДЕЙСТВИЯ С x32 UIO ОБЪЕКТАМИ, НО МЫ РЕКОМЕНДУЕМ ДОПОЛНИТЕЛЬНО ИСПОЛЬЗОВАТЬ ИНТЕРПРЕТАТОР PYTHON x32 (ПОДРОБНЕЕ СМ. ФУНКЦИЮ Configure())

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        UIDesktop.UIOSelector_Highlight(lDemoBaseUIOSelector) # Подсветить UIO объект по UIO селектору

    :param inUIOSelector: UIO селектор, который определяет UIO объект, для которого будет представлен перечень доступных активностей.
    :type inUIOSelector: list, обязательный
    """
    #Check the bitness
    lSafeOtherProcess = UIOSelector_SafeOtherGet_Process(inUIOSelector)
    if lSafeOtherProcess is None:
        UIO_Highlight(UIOSelector_Get_UIO(inUIOSelector))
    else:
        # Run function from other process with help of PIPE
        lPIPEResuestDict = {"ModuleName": "UIDesktop", "ActivityName": "UIOSelector_Highlight",
                            "ArgumentList": [inUIOSelector],
                            "ArgumentDict": {}}
        # Отправить запрос в дочерний процесс, который отвечает за работу с Windows окнами
        ProcessCommunicator.ProcessChildSendObject(lSafeOtherProcess, lPIPEResuestDict)
        # Get answer from child process
        lPIPEResponseDict = ProcessCommunicator.ProcessChildReadWaitObject(lSafeOtherProcess)
        if lPIPEResponseDict["ErrorFlag"]:
            raise Exception(
                f"Exception was occured in child process (message): {lPIPEResponseDict['ErrorMessage']}, (traceback): {lPIPEResponseDict['ErrorTraceback']}")
        else:
            return lPIPEResponseDict["Result"]
    return True
#old: - ElementDrawOutlineNewFocus
def UIOSelector_FocusHighlight(inUIOSelector):
    """L-,W+: Установить фокус и подсветить на несколько секунд на экране зеленой рамкой UIO объект, который соответствует входящему UIO селектору inUIOSelector

    !ВНИМАНИЕ! ДАННАЯ ФУНКЦИОНАЛЬНОСТЬ В АВТОМАТИЧЕСКОМ РЕЖИМЕ ПОДДЕРЖИВАЕТ ВСЕ РАЗРЯДНОСТИ ПРИЛОЖЕНИЙ (32|64), КОТОРЫЕ ЗАПУЩЕНЫ В СЕСИИ. PYTHON x64 ИМЕЕТ ВОЗМОЖНОСТЬ ВЗЗАИМОДЕЙСТВИЯ С x32 UIO ОБЪЕКТАМИ, НО МЫ РЕКОМЕНДУЕМ ДОПОЛНИТЕЛЬНО ИСПОЛЬЗОВАТЬ ИНТЕРПРЕТАТОР PYTHON x32 (ПОДРОБНЕЕ СМ. ФУНКЦИЮ Configure())

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        UIDesktop.UIOSelector_FocusHighlight(lDemoBaseUIOSelector) # Установить фокус и подсветить UIO объект по UIO селектору

    :param inUIOSelector: UIO селектор, который определяет UIO объект, для которого будет представлен перечень доступных активностей.
    :type inUIOSelector: list, обязательный
    """

    #Check the bitness
    lSafeOtherProcess = UIOSelector_SafeOtherGet_Process(inUIOSelector)
    if lSafeOtherProcess is None:
        UIO_FocusHighlight(UIOSelector_Get_UIO(inUIOSelector))
    else:
        # Run function from other process with help of PIPE
        lPIPEResuestDict = {"ModuleName": "UIDesktop", "ActivityName": "UIOSelector_FocusHighlight",
                            "ArgumentList": [inUIOSelector],
                            "ArgumentDict": {}}
        # Отправить запрос в дочерний процесс, который отвечает за работу с Windows окнами
        ProcessCommunicator.ProcessChildSendObject(lSafeOtherProcess, lPIPEResuestDict)
        # Get answer from child process
        lPIPEResponseDict = ProcessCommunicator.ProcessChildReadWaitObject(lSafeOtherProcess)
        if lPIPEResponseDict["ErrorFlag"]:
            raise Exception(
                f"Exception was occured in child process (message): {lPIPEResponseDict['ErrorMessage']}, (traceback): {lPIPEResponseDict['ErrorTraceback']}")
        else:
            return lPIPEResponseDict["Result"]
    return True

#old: - draw_outline_new
def UIO_Highlight(lWrapperObject,colour='green',thickness=2,fill=None,rect=None,inFlagSetFocus=False):
    """L-,W+: Выполнить подсветку UIO объекта на экране

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lUIO = UIDesktop.UIOSelector_Get_UIO(lDemoBaseUIOSelector) # Получить UIO объект по UIO селектору
        UIDesktop.UIO_Highlight(lUIO) # Подсветить UIO объект по UIO селектору зеленым цветом с толщиной подсветки 2 px.

    :param lWrapperObject: UIO объект, который будет подсвечен
    :type lWrapperObject: object UIO, обязательный
    :param colour: цвет подсветки UIO объекта. Варианты: 'red', 'green', 'blue'. По умолчанию 'green'
    :type colour: str, необязательный
    :param thickness: толщина подсветки UIO объекта. По умолчанию 2
    :type thickness: int, необязательный
    :param inFlagSetFocus: признак установки фокуса на UIO объект перед подсветкой. По умолчанию False
    :type inFlagSetFocus: bool, необязательный
    """
    if fill is None: fill = win32defines.BS_NULL
    if lWrapperObject is not None:
        """
        Draw an outline around the window.
        * **colour** can be either an integer or one of 'red', 'green', 'blue'
        (default 'green')
        * **thickness** thickness of rectangle (default 2)
        * **fill** how to fill in the rectangle (default BS_NULL)
        * **rect** the coordinates of the rectangle to draw (defaults to
          the rectangle of the control)
        """
        if inFlagSetFocus:
            #Установить фокус на объект, чтобы было видно выделение
            lWrapperObject.set_focus()
            time.sleep(0.5)
        # don't draw if dialog is not visible
        #if not lWrapperObject.is_visible():
        #    return
        colours = {
            "green": 0x00ff00,
            "blue": 0xff0000,
            "red": 0x0000ff,
        }
        # if it's a known colour
        if colour in colours:
            colour = colours[colour]
        if rect is None:
            rect = lWrapperObject.rectangle()
        # create the pen(outline)
        pen_handle = win32functions.CreatePen(
                win32defines.PS_SOLID, thickness, colour)
        # create the brush (inside)
        brush = win32structures.LOGBRUSH()
        brush.lbStyle = fill
        brush.lbHatch = win32defines.HS_DIAGCROSS
        brush_handle = win32functions.CreateBrushIndirect(ctypes.byref(brush))
        # get the Device Context
        dc = win32functions.CreateDC("DISPLAY", None, None, None )
        # push our objects into it
        win32functions.SelectObject(dc, brush_handle)
        win32functions.SelectObject(dc, pen_handle)
        # draw the rectangle to the DC
        win32functions.Rectangle(
            dc, rect.left, rect.top, rect.right, rect.bottom)
        # Delete the brush and pen we created
        win32functions.DeleteObject(brush_handle)
        win32functions.DeleteObject(pen_handle)
        # delete the Display context that we created
        win32functions.DeleteDC(dc)

#old: - draw_outline_new_focus
def UIO_FocusHighlight(lWrapperObject,colour='green',thickness=2,fill=None,rect=None):
    """L-,W+: Установить фокус и выполнить подсветку UIO объекта на экране

    .. code-block:: python

        # UIDesktop: Взаимодействие с UI объектами приложений
        from pyOpenRPA.Robot import UIDesktop
        # 1С: UIO Селектор выбора базы
        lDemoBaseUIOSelector = [{"title":"Запуск 1С:Предприятия","class_name":"V8TopLevelFrameTaxiStarter","backend":"uia"}]		
        lUIO = UIDesktop.UIOSelector_Get_UIO(lDemoBaseUIOSelector) # Получить UIO объект по UIO селектору
        UIDesktop.UIO_FocusHighlight(lUIO) # Установить фокус и подсветить UIO объект по UIO селектору зеленым цветом с толщиной подсветки 2 px.

    :param lWrapperObject: UIO объект, который будет подсвечен
    :type lWrapperObject: object UIO, обязательный
    :param colour: цвет подсветки UIO объекта. Варианты: 'red', 'green', 'blue'. По умолчанию 'green'
    :type colour: str, необязательный
    :param thickness: толщина подсветки UIO объекта. По умолчанию 2
    :type thickness: int, необязательный
    """
    if fill is None: fill = win32defines.BS_NULL
    UIO_Highlight(lWrapperObject,'green',2,fill,None,True)

#Определить разрядность процесса
lProcessBitnessStr = str(struct.calcsize("P") * 8)
Usage.Process(inComponentStr="Robot")
License.ConsoleVerify()

