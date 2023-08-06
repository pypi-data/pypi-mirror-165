import platform
"""
Специфические команды, которые надо выполнять только на ОС семейства Linux: if OS.IS_LINUX_BOOL:

Специфические команды, которые надо выполнять только на ОС семейства Windows: if OS.IS_WINDOWS_BOOL:

"""
IS_LINUX_BOOL = (platform.system().upper()=="LINUX" or platform.system().upper()=="LINUX2")
IS_WINDOWS_BOOL = (platform.system()=="Windows")

def PathStr(inPathStr:str) -> str:
    """Преобразование строк, который содержат путь к каталогу или файлу. В зависимости от операционной системы поддерживаются разные форматы.

    Для Windows ОС: path\\to\\file
    Для Linux ОС: path/to/file

    .. code-block:: python

        from pyOpenRPA.Tools import CrossOS
        lPathStr = CrossOS.PathStr(inPathStr = 'path/to\\file')
        # WINDOWS: lPathStr == 'path\\to\\file' 
        # LINUX: lPathStr == 'path/to/file' 

    :param inPathStr: Строка, которую обработать в зависимости от ОС, на которой происходит выполнение
    :type inPathStr: str
    :return: Обработанная строка с учетом используемой ОС
    :rtype: str
    """
    if inPathStr is None: return None
    if IS_WINDOWS_BOOL:
        return inPathStr.replace("/","\\")
    if IS_LINUX_BOOL:
        return inPathStr.replace("\\","/")

def PathSplitList(inPathStr:str) -> list:
    """Парсинг строки пути на элементы. Учитывает специфику формирования путей в разных ОС (Windows, Linux)

    Для Windows ОС: path\\to\\file
    Для Linux ОС: path/to/file

    .. code-block:: python

        from pyOpenRPA.Tools import CrossOS
        lPathList = CrossOS.PathSplitList(inPathStr = 'path/to\\file')
        # WINDOWS: lPathList == ['path', 'to', 'file'] 
        # LINUX: lPathList == ['path', 'to', 'file']  

    :param inPathStr: Строка, которую обработать в зависимости от ОС, на которой происходит выполнение
    :type inPathStr: str
    :return: Массив элементов пути. Пример: ['path', 'to', 'file'] 
    :rtype: list
    """
    inPathStr = inPathStr.replace("\\","/")
    return inPathStr.split("/")


def PathJoinList(inList: list) ->str:
    """Слияние элементов списка в строку. Учитывает специфику формирования путей в разных ОС (Windows, Linux)

    Для Windows ОС: path\\to\\file
    Для Linux ОС: path/to/file

    .. code-block:: python

        from pyOpenRPA.Tools import CrossOS
        lPathStr = CrossOS.PathJoinList(inList = ['path', 'to', 'file'] )
        # WINDOWS: lPathStr == 'path\\to\\file' 
        # LINUX: lPathStr == 'path/to/file'  

    :param inList: Строка, которую обработать в зависимости от ОС, на которой происходит выполнение
    :type inList: str
    :return: Массив элементов пути. Пример: ['path', 'to', 'file'] 
    :rtype: list
    """
    if IS_LINUX_BOOL: return "/".join(inList)
    elif IS_WINDOWS_BOOL: return "\\".join(inList)