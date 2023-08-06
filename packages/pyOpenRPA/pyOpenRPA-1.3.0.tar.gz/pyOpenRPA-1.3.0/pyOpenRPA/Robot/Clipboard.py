from pyOpenRPA.Tools import CrossOS
if CrossOS.IS_WINDOWS_BOOL: import win32clipboard #CrossOS
if CrossOS.IS_LINUX_BOOL: import pyclip #CrossOS
####################################
#Info: Clipboard module of the Robot app (OpenRPA - Robot)
####################################
# GUI Module - interaction with Windows clipboard

def Get():
    """L+,W+: Получить текстовое содержимое буфера обмена.

    .. code-block:: python

        # Clipboard: Взаимодействие с буфером
        from pyOpenRPA.Robot import Clipboard
        lClipStr = Clipboard.Get()

    :return: Текстовое содержимое буфера обмена
    :rtype: str
    """
    return ClipboardGet()

def Set(inTextStr:str):
    """L+,W+: Установить текстовое содержимое в буфер обмена.

    .. code-block:: python

        # Clipboard: Взаимодействие с буфером
        from pyOpenRPA.Robot import Clipboard
        lClipStr = Clipboard.Set(inTextStr="HELLO WORLD")

    :param inTextStr: Текстовое содержимое для установки в буфера обмена
    :type inTextStr: str
    """
    ClipboardSet(inText=inTextStr)

def ClipboardGet():
    if CrossOS.IS_WINDOWS_BOOL:
        win32clipboard.OpenClipboard()
        lResult = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
    if CrossOS.IS_LINUX_BOOL:
        lResult = pyclip.paste(text=True)
    return lResult

def ClipboardSet(inText):
    if CrossOS.IS_WINDOWS_BOOL:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT,inText)
        win32clipboard.CloseClipboard()
    if CrossOS.IS_LINUX_BOOL:
        pyclip.copy(inText) # copy data to the clipboard

