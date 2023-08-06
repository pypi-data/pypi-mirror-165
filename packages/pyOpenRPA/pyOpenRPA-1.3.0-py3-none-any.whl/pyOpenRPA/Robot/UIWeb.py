from selenium import *
from selenium import webdriver, common
from selenium.webdriver.common.by import By
import os
import sys
from pyOpenRPA.Tools import CrossOS
import time

# XPATH CSS CHEAT CHEET: https://devhints.io/xpath
# XPATH CSS CHEAT CHEET: https://devhints.io/css

UIO_WAIT_SEC_FLOAT = 60
UIO_WAIT_INTERVAL_SEC_FLOAT = 1.0

gBrowser:webdriver.Chrome = None

def BrowserChromeStart(inDriverExePathStr:str = None, inChromeExePathStr:str = None, inExtensionPathList:list = None, inProfilePathStr:str=None) -> webdriver.Chrome:
    """L+,W+: Выполнить запуск браузера Chrome. Если вы скачали pyOpenRPA вместе с репозиторием, то будет использоваться встроенный браузер Google Chrome. Если установка pyOpenRPA производилась другим способом, то требуется указать расположение браузера Google Chrome и соответствующего WebDriver.

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.BrowserClose()
		
    :param inDriverExePathStr: Путь до компонента webdriver.exe, по умолчанию None (путь до webdriver.exe, который расположен в репозитории pyOpenRPA)
    :type inDriverExePathStr: str, опционально
    :param inChromeExePathStr:Путь до компонента chrome.exe, по умолчанию None (путь до chrome.exe, который расположен в репозитории pyOpenRPA)
    :type inChromeExePathStr: str, опционально
    :param inExtensionPathList: Список путей, по которым располагаются расширения Chrome, по умолчанию None
    :type inExtensionPathList: list, опционально
    :param inProfilePathStr: Путь, по которому выполнить сохранения профиля Chrome (история, куки и т.д.), по умолчанию None (профиль не сохраняется)
    :type inProfilePathStr: str, опционально
    :return: Объект браузера Google Chrome
    :rtype: webdriver.Chrome
    """
    global gBrowser
    inDriverExePathStr = CrossOS.PathStr(inPathStr=inDriverExePathStr)
    inChromeExePathStr = CrossOS.PathStr(inPathStr=inChromeExePathStr)
    lExtensionPathList = []
    if inExtensionPathList is not None:
        for lItemStr in inExtensionPathList:
            lExtensionPathList.append(CrossOS.PathStr(inPathStr=lItemStr))
    inExtensionPathList = lExtensionPathList
    inChromeExePathStr = CrossOS.PathStr(inPathStr=inChromeExePathStr)
    inProfilePathStr = CrossOS.PathStr(inPathStr=inProfilePathStr)
    lResourcePathStr = os.path.abspath(os.path.join(sys.executable, "..","..", ".."))
    # Путь по умолчанию к портативному браузеру и драйверу (если скачивался репозиторий pyOpenRPA
    if inDriverExePathStr == None: 
        if CrossOS.IS_WINDOWS_BOOL: inDriverExePathStr = os.path.join(lResourcePathStr, "SeleniumWebDrivers", "Chrome", "chromedriver_win32 v84.0.4147.30", "chromedriver.exe")
        elif CrossOS.IS_LINUX_BOOL: inDriverExePathStr = os.path.join(lResourcePathStr, "SeleniumWebDrivers", "Chrome", "chromedriver_lin64 v103.0.5060.53", "chromedriver")
    if inChromeExePathStr == None: 
        if CrossOS.IS_WINDOWS_BOOL: inChromeExePathStr = os.path.join(lResourcePathStr, "WChrome64-840414730", "App", "Chrome-bin", "chrome.exe")
        elif CrossOS.IS_LINUX_BOOL: inChromeExePathStr = os.path.join(lResourcePathStr, "LChrome64-10305060114", "data", "chrome")
    if inExtensionPathList == None: inExtensionPathList = []
    # Set full path to exe of the chrome
    lWebDriverChromeOptionsInstance = webdriver.ChromeOptions()
    lWebDriverChromeOptionsInstance.binary_location = inChromeExePathStr
    #lWebDriverChromeOptionsInstance2 = webdriver.ChromeOptions()
    if inProfilePathStr is not None:
        inProfilePathStr = os.path.abspath(inProfilePathStr)
        lWebDriverChromeOptionsInstance.add_argument(f"user-data-dir={os.path.abspath(inProfilePathStr)}")
    # Add extensions
    for lExtensionItemFullPath in inExtensionPathList:
        lWebDriverChromeOptionsInstance.add_extension (os.path.abspath(lExtensionItemFullPath))
    #if inDriverExePathStr == "built-in":
    # Run with specified web driver path
    gBrowser = webdriver.Chrome(executable_path = inDriverExePathStr, options=lWebDriverChromeOptionsInstance)
    #else:
    #    lWebDriverInstance = webdriver.Chrome(options = lWebDriverChromeOptionsInstance)
    return gBrowser

def BrowserChange(inBrowser):
    """L+,W+: Выполнить смену активного браузера (при необходимости).

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        lBrowser1 = UIWeb.BrowserChromeStart()
        UIWeb.BrowserChange(inBrowser=None)
        lBrowser2 = UIWeb.BrowserChromeStart()
        UIWeb.BrowserClose()
        UIWeb.BrowserChange(inBrowser=lBrowser1)
        UIWeb.BrowserClose()

    :param inBrowser: Объект браузера
    :type inBrowser: webdriver.Chrome
    """
    global gBrowser
    gBrowser = inBrowser

def PageOpen(inURLStr: str):
    """L+,W+: Открыть страницу inURLStr в браузере и дождаться ее загрузки.

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        UIWeb.BrowserClose()

    :param inURLStr: URL адрес страницы
    :type inURLStr: str
    """
    global gBrowser
    if gBrowser is not None: gBrowser.get(inURLStr)

def PageScrollTo(inVerticalPxInt=0, inHorizontalPxInt=0):
    """L+,W+: Выполнить прокрутку страницы (по вертикали или по горизонтали)

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        UIWeb.PageScrollTo(inVerticalPxInt=100)
        UIWeb.BrowserClose()

    :param inVerticalPxInt: Величина вертикальной прокрутки страницы в пикселях, по умолчанию 0
    :type inVerticalPxInt: int, опционально
    :param inHorizontalPxInt: Величина горизонтальной прокрутки страницы в пикселях, по умолчанию 0
    :type inHorizontalPxInt: int, опционально
    """
    PageJSExecute(inJSStr=f"scroll({inHorizontalPxInt},{inVerticalPxInt})")

def PageJSExecute(inJSStr, *inArgList):
    """L+,W+: Отправить на выполнение на сторону браузера код JavaScript.

    !ВНИМАНИЕ! Данная функция поддерживает передачу переменных в область кода JavaScript (*inArgList). Обратиться к переданным переменным из JavaScript можно с помощью ключевого слова: arguments[i], где i - это порядковый номер переданной переменной

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        UIWeb.PageJSExecute(alert('arguments[0]);", "hello world!")
        UIWeb.BrowserClose()

    :param inJSStr: Код JavaScript, отправляемый на сторону браузера
    :type inJSStr: str
    :param *inArgList: Перечисление аргументов, отправляемых на сторону браузера
    :type *inArgList: str
    :return: Результат отработки кода JavaScript, если он заканчивался оператором "return"
    :rtype: str | int | bool | float
    """
    # arguments[0], arguments[1] etc
    global gBrowser
    if gBrowser is not None: return gBrowser.execute_script(inJSStr, *inArgList)
    
def BrowserClose():
    """L+,W+: Закрыть браузер

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        UIWeb.BrowserClose()

    """
    global gBrowser
    if gBrowser is not None: gBrowser.quit()

def UIOSelectorList(inUIOSelectorStr, inUIO=None) -> list:
    """L+,W+: Получить список UIO объектов по UIO селектору.

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        lUIOSelectorStr = "//*[@id=\"grid\"]/div[2]/div[2]/div[3]/div[1]/ul/li[5]/div/a"
        lUIOList = UIOSelectorList(inUIOSelectorStr = lUIOSelectorStr)
        UIWeb.BrowserClose()

    :param inUIOSelectorStr: XPATH или CSS селектор UI объекта на web странице. Подсказки по CSS: https://devhints.io/css Подсказки по XPath: https://devhints.io/xpath 
    :type inUIOSelectorStr: str
    :param inUIO: Объект UIO, от которого выполнить поиск UIO объектов по селектору, по умолчанию None
    :type inUIO: WebElement, опционально
    :return: Список UIO объектов
    :rtype: list
    """
    lResultList = []
    if inUIO is None:
        global gBrowser
        if gBrowser is not None:
            if UIOSelectorDetect(inUIOSelectorStr=inUIOSelectorStr) == "CSS":
                lResultList = gBrowser.find_elements(By.CSS_SELECTOR, inUIOSelectorStr)
            else:
                lResultList = gBrowser.find_elements(By.XPATH,inUIOSelectorStr)
    else: 
        if UIOSelectorDetect(inUIOSelectorStr=inUIOSelectorStr) == "CSS":
            lResultList = inUIO.find_elements(By.CSS_SELECTOR, inUIOSelectorStr)
        else:
            lResultList = inUIO.find_elements(By.XPATH,inUIOSelectorStr)
    return lResultList

def UIOSelectorFirst(inUIOSelectorStr, inUIO=None) -> list:
    """L+,W+: Получить UIO объект по UIO селектору.

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        lUIOSelectorStr = "//*[@id=\"grid\"]/div[2]/div[2]/div[3]/div[1]/ul/li[5]/div/a"
        lUIO = UIOSelectorFirst(inUIOSelectorStr = lUIOSelectorStr)
        UIWeb.BrowserClose()

    :param inUIOSelectorStr: XPATH или CSS селектор UI объекта на web странице. Подсказки по CSS: https://devhints.io/css Подсказки по XPath: https://devhints.io/xpath 
    :type inUIOSelectorStr: str
    :param inUIO: Объект UIO, от которого выполнить поиск UIO объектов по селектору, по умолчанию None
    :type inUIO: WebElement, опционально
    :return: Первый подходящий UIO объект
    :rtype: UIO объект
    """
    lResult = None
    lUIOList = UIOSelectorList(inUIOSelectorStr=inUIOSelectorStr, inUIO=inUIO)
    if len(lUIOList) > 0: lResult = lUIOList[0]
    return lResult

def UIOTextGet(inUIO) -> str:
    """L+,W+: Получить текст UI элемента.

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        lUIOSelectorStr = "//*[@id=\"grid\"]/div[2]/div[2]/div[3]/div[1]/ul/li[5]/div/a"
        lUIO = UIOSelectorList(inUIOSelectorStr = lUIOSelectorStr)[0]
        lTextStr = UIWeb.UIOTextGet(inUIO=lUIO)
        UIWeb.BrowserClose()

    :param inUIO: UIO элемент. Получить его можно с помощью функций UIOSelectorList или UIOSelectorFirst
    :type inUIO: WebElement
    :return: Текст UI элемента
    :rtype: str
    """
    return inUIO.text

def UIOAttributeGet(inUIO, inAttributeStr) -> str:
    """L+,W+: Получить обычный (нестилевой) атрибут у UI элемента.

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        lUIOSelectorStr = "//*[@id=\"grid\"]/div[2]/div[2]/div[3]/div[1]/ul/li[5]/div/a"
        lUIO = UIOSelectorList(inUIOSelectorStr = lUIOSelectorStr)[0]
        UIWeb.UIOAttributeGet(inUIO=lUIO, inAttributeStr = "href")
        UIWeb.BrowserClose()

    :param inUIO: UIO элемент. Получить его можно с помощью функций UIOSelectorList или UIOSelectorFirst
    :type inUIO: WebElement
    :param inAttributeStr: Наименование обычного (нестилевого) атрибута
    :type inAttributeStr: str
    :return: Значение обычного (нестилевого) атрибута
    :rtype: str
    """
    return inUIO.get_attribute(inAttributeStr)

def UIOAttributeStyleGet(inUIO, inAttributeStr) -> str:
    """L+,W+: Получить стилевой атрибут у UI элемента.

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        lUIOSelectorStr = "//*[@id=\"grid\"]/div[2]/div[2]/div[3]/div[1]/ul/li[5]/div/a"
        lUIO = UIOSelectorList(inUIOSelectorStr = lUIOSelectorStr)[0]
        UIWeb.UIOAttributeStyleGet(inUIO=lUIO, inAttributeStr = "href")
        UIWeb.BrowserClose()

    :param inUIO: UIO элемент. Получить его можно с помощью функций UIOSelectorList или UIOSelectorFirst
    :type inUIO: WebElement
    :param inAttributeStr: Наименование стилевого атрибута
    :type inAttributeStr: str
    :return: Значение стилевого атрибута
    :rtype: str
    """
    return inUIO.value_of_css_property(inAttributeStr)

def UIOAttributeSet(inUIO, inAttributeStr, inValue):
    """L+,W+: Установить обычный (нестилевой) атрибут у UI элемента.

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        lUIOSelectorStr = "//*[@id=\"grid\"]/div[2]/div[2]/div[3]/div[1]/ul/li[5]/div/a"
        lUIO = UIOSelectorList(inUIOSelectorStr = lUIOSelectorStr)[0]
        UIWeb.UIOAttributeSet(inUIO=lUIO, inAttributeStr = "href", inValue = "https://mail.ru")
        UIWeb.BrowserClose()

    :param inUIO: UIO элемент. Получить его можно с помощью функций UIOSelectorList или UIOSelectorFirst
    :type inUIO: WebElement
    :param inAttributeStr: Наименование обычного (нестилевого) атрибута
    :type inAttributeStr: str
    :param inValue: Устанавливаемое значение обычного (нестилевого) атрибута
    :type inValue: str
    """
    lJSStr = \
        f"arguments[0].setAttribute(arguments[1], arguments[2]);"
    gBrowser.execute_script(lJSStr,inUIO, inAttributeStr, inValue)

def UIOAttributeRemove(inUIO, inAttributeStr):
    """L+,W+: Удалить обычный (нестилевой) атрибут у UI элемента.

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        lUIOSelectorStr = "//*[@id=\"grid\"]/div[2]/div[2]/div[3]/div[1]/ul/li[5]/div/a"
        lUIO = UIOSelectorList(inUIOSelectorStr = lUIOSelectorStr)[0]
        UIWeb.UIOAttributeRemove(lUIO, "href")
        UIWeb.BrowserClose()

    :param inUIO: UIO элемент. Получить его можно с помощью функций UIOSelectorList или UIOSelectorFirst
    :type inUIO: WebElement
    :param inAttributeStr: Наименование обычного (нестилевого) атрибута
    :type inAttributeStr: str
    """
    lJSStr = \
        f"arguments[0].removeAttribute(arguments[1]);"
    gBrowser.execute_script(lJSStr,inUIO, inAttributeStr)

def UIOAttributeStyleSet(inUIO, inAttributeStr, inValue):
    """L+,W+: Установить стилевой атрибут у UI элемента.

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        lUIOSelectorStr = "//*[@id=\"grid\"]/div[2]/div[2]/div[3]/div[1]/ul/li[5]/div/a"
        lUIO = UIOSelectorList(inUIOSelectorStr = lUIOSelectorStr)[0]
        UIWeb.UIOAttributeStyleSet(inUIO=lUIO, inAttributeStr = "color", inValue = "grey")
        UIWeb.BrowserClose()

    :param inUIO: UIO элемент. Получить его можно с помощью функций UIOSelectorList или UIOSelectorFirst
    :type inUIO: WebElement
    :param inAttributeStr: Наименование стилевого атрибута
    :type inAttributeStr: str
    :param inValue: Устанавливаемое значение стилевого атрибута
    :type inValue: str
    """
    lJSStr = \
        f"arguments[0].style[arguments[1]]=arguments[2];"
    gBrowser.execute_script(lJSStr,inUIO, inAttributeStr, inValue)

def UIOAttributeStyleRemove(inUIO, inAttributeStr:str):
    """L+,W+: Удалить стилевой атрибут у UI элемента.

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        lUIOSelectorStr = "//*[@id=\"grid\"]/div[2]/div[2]/div[3]/div[1]/ul/li[5]/div/a"
        lUIO = UIOSelectorList(inUIOSelectorStr = lUIOSelectorStr)[0]
        UIWeb.UIOAttributeStyleRemove(lUIO, "color")
        UIWeb.BrowserClose()

    :param inUIO: UIO элемент. Получить его можно с помощью функций UIOSelectorList или UIOSelectorFirst
    :type inUIO: WebElement
    :param inAttributeStr: Наименование стилевого атрибута
    :type inAttributeStr: str
    """
    lJSStr = \
        f"arguments[0].style[arguments[1]]=\"\";"
    gBrowser.execute_script(lJSStr,inUIO, inAttributeStr)

def UIOClick(inUIO):
    """L+,W+: Выполнить нажатие по элементу inUIO.

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        lUIOSelectorStr = "//*[@id=\"grid\"]/div[2]/div[2]/div[3]/div[1]/ul/li[5]/div/a"
        lUIO = UIOSelectorList(inUIOSelectorStr = lUIOSelectorStr)[0]
        UIOClick(inUIO = lUIO)
        UIWeb.BrowserClose()

    :param inUIO: UIO элемент. Получить его можно с помощью функций UIOSelectorList или UIOSelectorFirst
    :type inUIO: WebElement
    """
    inUIO.click()

def UIOSelectorHighlight(inUIOSelectorStr: str, inIsFirst:bool=False, inDurationSecFloat:float=3.0, inColorStr:str="green"):
    """L+,W+: Выполнить подсвечивание UI элемента с селектором inUIOSelectorStr.

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        lUIOSelectorStr = "//*[@id=\"grid\"]/div[2]/div[2]/div[3]/div[1]/ul/li[5]/div/a"
        UIOSelectorHighlight(inUIOSelectorStr = lUIOSelectorStr)
        UIWeb.BrowserClose()

    :param inUIOSelectorStr: XPATH или CSS селектор UI элемента на web странице. Подсказки по CSS: https://devhints.io/css Подсказки по XPath: https://devhints.io/xpath 
    :type inUIOSelectorStr: str
    :param inIsFirst: True - подсветить только первый элемент, который удовлетворяет селектору. По умолчанию False
    :type inIsFirst: bool, опционально
    :param inDurationSecFloat: Длительность подсвечивания. По умолчанию 3.0 сек.
    :type inDurationSecFloat: float, опционально
    :param inColorStr: Цвет подсвечания Варианты: "red", "blue", "grey", "yellow". По умолчанию "green" (зеленый)
    :type inColorStr: str, опционально
    """
    global gBrowser
    if inIsFirst == True:
        lUIOList = [UIOSelectorFirst(inUIOSelectorStr=inUIOSelectorStr)]
        lJSStr = \
            f"var lElementList = arguments[0];" \
            f"if (lElementList.length>0) {{ lElementList=[lElementList[0]]; }}" \
            f"for (var lIndexInt=0; lIndexInt<lElementList.length;lIndexInt++) {{" \
            f"  lElement=lElementList[lIndexInt];" \
            f"  lElement.ORPABackupStyleOutline = lElement.style[\"outline\"];" \
            f"  lElement.style[\"outline\"]=\"2px solid {inColorStr}\";" \
            f"}}" \
            f"window.ORPAOutlineList = lElementList;"
        PageJSExecute(lJSStr, lUIOList)
    else:
        lUIOList = UIOSelectorList(inUIOSelectorStr=inUIOSelectorStr)
        lJSStr = \
            f"var lElementList = arguments[0];" \
            f"for (var lIndexInt=0; lIndexInt<lElementList.length;lIndexInt++) {{" \
            f"  lElement=lElementList[lIndexInt];" \
            f"  lElement.ORPABackupStyleOutline = lElement.style[\"outline\"];" \
            f"  lElement.style[\"outline\"]=\"2px solid {inColorStr}\";" \
            f"}}" \
            f"window.ORPAOutlineList = lElementList;"
        PageJSExecute(lJSStr, lUIOList)
    time.sleep(inDurationSecFloat)
    lJSStr = \
        f"var lElementList = window.ORPAOutlineList;" \
        f"for (var lIndexInt=0; lIndexInt<lElementList.length;lIndexInt++) {{" \
        f"  lElement=lElementList[lIndexInt];" \
        f"  lElement.style[\"outline\"]=lElement.ORPABackupStyleOutline;" \
        f"}}" \
        f"delete window.ORPAOutlineList;"
    PageJSExecute(inJSStr=lJSStr)

def UIOSelectorClick(inUIOSelectorStr: str):
    """L+,W+: Выполнить нажатие по элементу с селектором inUIOSelectorStr.

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        lUIOSelectorStr = "//*[@id=\"grid\"]/div[2]/div[2]/div[3]/div[1]/ul/li[5]/div/a"
        UIOSelectorClick(inUIOSelectorStr = lUIOSelectorStr)
        UIWeb.BrowserClose()

    :param inUIOSelectorStr: XPATH или CSS селектор UI элемента на web странице. Подсказки по CSS: https://devhints.io/css Подсказки по XPath: https://devhints.io/xpath 
    :type inUIOSelectorStr: str
    """
    PageJSExecute(inJSStr=f"document.querySelector('{inUIOSelectorStr}').click()")

def UIOSelectorWaitAppear(inUIOSelectorStr:str, inWaitSecFloat:float=UIO_WAIT_SEC_FLOAT, inWaitIntervalSecFloat:float = UIO_WAIT_INTERVAL_SEC_FLOAT):
    """L+,W+: Ожидать появление UI элемента на веб странице (блокирует выполнение потока), заданного по UIO селектору inUIOSelectorStr. Выполнять ожидание на протяжении inWaitSecFloat (по умолчанию 60 сек.). Проверка производится с интервалом inWaitIntervalSecFloat (по умолчанию 1 сек.)

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        lUIOSelectorStr = "//*[@id=\"grid\"]/div[2]/div[2]/div[3]/div[1]/ul/li[5]/div/a"
        lAppearUIOList = UIOSelectorWaitAppear(inUIOSelectorStr = lUIOSelectorStr)
        UIWeb.BrowserClose()
    
    :param inUIOSelectorStr: XPATH или CSS селектор UI элемента на web странице. Подсказки по CSS: https://devhints.io/css Подсказки по XPath: https://devhints.io/xpath 
    :type inUIOSelectorStr: str
    :param inWaitSecFloat: Время ожидания на исчезновение UI элемента, по умолчанию UIO_WAIT_SEC_FLOAT (60 сек)
    :type inWaitSecFloat: float, опциональный
    :param inWaitIntervalSecFloat: Интервал проверки исчезновения, по умолчанию UIO_WAIT_INTERVAL_SEC_FLOAT (1 сек)
    :type inWaitIntervalSecFloat: float, опциональный
    :raises Exception: Время ожидания превышено
    :return: Список UI элементов, которые удовлетворяют селектору и появились на странице
    :rtype: list
    """
    lStartSecFloat = time.time()
    lResultList=[]
    while time.time() - lStartSecFloat < inWaitSecFloat:
        lResultList = UIOSelectorList(inUIOSelectorStr=inUIOSelectorStr)
        if len(lResultList)>0: break
        time.sleep(inWaitIntervalSecFloat)
    if time.time() - lStartSecFloat > inWaitSecFloat: raise Exception(f"Wait time is over. No element has been appear")
    return lResultList

def UIOSelectorWaitDisappear(inUIOSelectorStr:str, inWaitSecFloat:float=UIO_WAIT_SEC_FLOAT, inWaitIntervalSecFloat:float = UIO_WAIT_INTERVAL_SEC_FLOAT):
    """L+,W+: Ожидать исчезновение UI элемента с веб страницы (блокирует выполнение потока), заданного по UIO селектору inUIOSelectorStr. Выполнять ожидание на протяжении inWaitSecFloat (по умолчанию 60 сек.). Проверка производится с интервалом inWaitIntervalSecFloat (по умолчанию 1 сек.)

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        lUIOSelectorStr = "//*[@id=\"grid\"]/div[2]/div[2]/div[3]/div[1]/ul/li[5]/div/a"
        UIOSelectorWaitDisappear(inUIOSelectorStr = lUIOSelectorStr)
        UIWeb.BrowserClose()
        
    :param inUIOSelectorStr: XPATH или CSS селектор UI элемента на web странице. Подсказки по CSS: https://devhints.io/css Подсказки по XPath: https://devhints.io/xpath 
    :type inUIOSelectorStr: str
    :param inWaitSecFloat: Время ожидания на исчезновение UI элемента, по умолчанию UIO_WAIT_SEC_FLOAT (60 сек)
    :type inWaitSecFloat: float, опциональный
    :param inWaitIntervalSecFloat: Интервал проверки исчезновения, по умолчанию UIO_WAIT_INTERVAL_SEC_FLOAT (1 сек)
    :type inWaitIntervalSecFloat: float, опциональный
    :raises Exception: Время ожидания превышено
    """
    lStartSecFloat = time.time()
    while time.time() - lStartSecFloat < inWaitSecFloat:
        lResultList = UIOSelectorList(inUIOSelectorStr=inUIOSelectorStr)
        if len(lResultList)==0: break
        time.sleep(inWaitIntervalSecFloat)
    if time.time() - lStartSecFloat > inWaitSecFloat: raise Exception(f"Wait time is over. No element has been disappear")


from lxml import etree
from io import StringIO
gXML = etree.parse(StringIO('<foo><bar></bar></foo>'))

def UIOSelectorDetect(inUIOSelectorStr:str) -> str:
    """L+,W+: Идентифицировать стиль селектора (CSS или XPATH)

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        lUIOSelectorStr = "#grid > div.grid-middle > div.grid__main-col.svelte-2y66pa > div.grid_newscol.grid_newscol__more-pulse.svelte-1yvqfic > div.grid__ccol.svelte-1yvqfic > ul > li:nth-child(5) > div > a"
        lUIOSelectorStr = "//*[@id=\"grid\"]/div[2]/div[2]/div[3]/div[1]/ul/li[5]/div/a"
        lResultStr = UIOSelectorDetect(inUIOSelectorStr = lUIOSelectorStr)

    :param inUIOSelectorStr: XPATH или CSS селектор UI объекта на web странице. Подсказки по CSS: https://devhints.io/css Подсказки по XPath: https://devhints.io/xpath 
    :type inUIOSelectorStr: str
    :return: "CSS" или "XPATH"
    :rtype: str
    """
    global gXML
    lResultStr = "CSS"
    try:
        gXML.xpath(inUIOSelectorStr)
        lResultStr = "XPATH"
    except etree.XPathEvalError as e:
        lResultStr = "CSS"
    return lResultStr


def UIOMouseSearchInit():
    """L+,W+: Инициализирует процесс поиска UI элемента с помощью мыши. Для прекращения поиска необходимо использовать функцию: UIOMouseSearchReturn

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        import time
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        UIWeb.UIOMouseSearchInit()
        time.sleep(3)
        UIWeb.UIOMouseSearchReturn()
        UIWeb.BrowserClose()
    """    
    lJSStr = """

        document.ORPASearch = function(e){
            document.ORPAMouseXInt = e.clientX;
            document.ORPAMouseYInt = e.clientY;
        }

        document.addEventListener('mousemove', document.ORPASearch, {
            passive: true})
    """
    PageJSExecute(lJSStr)

def UIOMouseSearchReturn():
    """L+,W+: Возвращает UIO объект, над которым находится указатель мыши. Предварительно должна быть вызвана функция UIWeb.UIOMouseSearchInit

    .. code-block:: python

        # UIWeb: Взаимодействие с ui web
        from pyOpenRPA.Robot import UIWeb
        import time
        UIWeb.BrowserChromeStart()
        UIWeb.PageOpen("https://mail.ru")
        UIWeb.UIOMouseSearchInit()
        time.sleep(3)
        UIWeb.UIOMouseSearchReturn()
        UIWeb.BrowserClose()

    :return: UIO объект
    :rtype: webelement
    """    
    lJSStr = """
        document.removeEventListener('mousemove', document.ORPASearch);    
        return document.elementFromPoint(document.ORPAMouseXInt,document.ORPAMouseYInt);
    """
    return PageJSExecute(lJSStr)
    