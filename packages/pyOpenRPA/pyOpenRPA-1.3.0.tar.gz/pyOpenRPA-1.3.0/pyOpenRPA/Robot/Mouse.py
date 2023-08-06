from pyautogui import *
import time

WAIT_AFTER_SEC_FLOAT = 0.4 # Настройка модуля Mouse: Время, которое ожидать после выполнения любой операции модуля Mouse. Настройка является единой для всех участов кода, использующих модуль Mouse. Если для некоторой функции требуется изменить данное время ожидания, то в отношении этой функции можно применить соответсвующий аргумент.

def Click(inXInt:int=None, inYInt:int=None, inClickCountInt:int=1, inIntervalSecFloat:float=0.0, inButtonStr:str='left', inMoveDurationSecFloat:float=0.0, inWaitAfterSecFloat:float=WAIT_AFTER_SEC_FLOAT):
    """L+,W+: Нажатие (вниз) кнопки мыши и затем немедленно выпуск (вверх) её. Допускается следующая параметризация. Если не указаны inXInt и inYInt - клик производится по месту нахождения указателя мыши.

    !ВНИМАНИЕ! Отсчет координат inXInt, inYInt начинается с левого верхнего края рабочей области (экрана).
    
    .. code-block:: python

        # Mouse: Взаимодействие с мышью
        from pyOpenRPA.Robot import Mouse
        Mouse.Click(100,150) #Выполнить нажатие левой клавиши мыши на экране по координатам: X(гор) 100px, Y(вер) 150px.

    :param inXInt: Целевая позиция указателя мыши по оси X (горизонтальная ось). 
    :type inXInt: int, опциональный
    :param inYInt: Целевая позиция указателя мыши по оси Y (вертикальная ось). 
    :type inYInt: int, опциональный
    :param inClickCountInt: Количество нажатий (вниз и вверх) кнопкой мыши, По умолчанию 1
    :type inClickCountInt: int, опциональный
    :param inIntervalSecFloat: Интервал ожидания в секундах между нажатиями, По умолчанию 0.0
    :type inIntervalSecFloat: float, опциональный 
    :param inButtonStr: Номер кнопки, которую требуется нажать. Возможные варианты: 'left', 'middle', 'right' или 1, 2, 3. В остальных случаях инициирует исключение ValueError. По умолчанию 'left'
    :type inButtonStr: str, опциональный
    :param inMoveDurationSecFloat: Время перемещения указателя мыши, По умолчанию 0.0 (моментальное перемещение)
    :type inMoveDurationSecFloat: float, опциональный
    :param inWaitAfterSecFloat: Количество секунд, которые ожидать после выполнения операции. По умолчанию установлено в настройках модуля Mouse (базовое значение 0.4)
    :type inWaitAfterSecFloat: float, опциональный
    """
    if inWaitAfterSecFloat == None: inWaitAfterSecFloat = WAIT_AFTER_SEC_FLOAT
    click(x=inXInt, y=inYInt, clicks=inClickCountInt, interval=inIntervalSecFloat, button=inButtonStr, duration=inMoveDurationSecFloat)
    time.sleep(inWaitAfterSecFloat)

def ClickDouble(inXInt:int=None, inYInt:int=None, inWaitAfterSecFloat:float=WAIT_AFTER_SEC_FLOAT):
    """L+,W+: Двойное нажатие левой клавиши мыши. Данное действие аналогично вызову функции (см. ниже).
    
    !ВНИМАНИЕ! Отсчет координат inXInt, inYInt начинается с левого верхнего края рабочей области (экрана).

    .. code-block:: python

        # Mouse: Взаимодействие с мышью
        from pyOpenRPA.Robot import Mouse
        Mouse.ClickDouble(100,150) #Выполнить двойное нажатие левой клавиши мыши на экране по координатам: X(гор) 100px, Y(вер) 150px.

    :param inXInt: Целевая позиция указателя мыши по оси X (горизонтальная ось). 
    :type inXInt: int, опциональный
    :param inYInt: Целевая позиция указателя мыши по оси Y (вертикальная ось). 
    :type inYInt: int, опциональный
    :param inWaitAfterSecFloat: Количество секунд, которые ожидать после выполнения операции. По умолчанию установлено в настройках модуля Mouse (базовое значение 0.4)
    :type inWaitAfterSecFloat: float, опциональный
    """
    if inWaitAfterSecFloat == None: inWaitAfterSecFloat = WAIT_AFTER_SEC_FLOAT
    doubleClick(x=inXInt, y=inYInt)
    time.sleep(inWaitAfterSecFloat)

def Down(inXInt:int=None, inYInt:int=None, inButtonStr:str='left', inWaitAfterSecFloat:float=WAIT_AFTER_SEC_FLOAT):
    """L+,W+: Переместить указатель по координатам inXInt, inYInt, после чего нажать (вниз) клавишу мыши и не отпускать до выполнения соответсвующей команды (см. Up). Если координаты inXInt, inYInt не переданы - нажатие происходит на тех координатах X/Y, на которых указатель мыши находится.

    !ВНИМАНИЕ! Отсчет координат inXInt, inYInt начинается с левого верхнего края рабочей области (экрана).

    .. code-block:: python

        # Mouse: Взаимодействие с мышью
        from pyOpenRPA.Robot import Mouse
        Mouse.Down() #Опустить левую клавишу мыши

    :param inXInt: Целевая позиция указателя мыши по оси X (горизонтальная ось). 
    :type inXInt: int, опциональный
    :param inYInt: Целевая позиция указателя мыши по оси Y (вертикальная ось). 
    :type inYInt: int, опциональный
    :param inButtonStr: Номер кнопки, которую требуется нажать. Возможные варианты: 'left', 'middle', 'right' или 1, 2, 3. В остальных случаях инициирует исключение ValueError. По умолчанию 'left'
    :type inButtonStr: str, опциональный
    :param inWaitAfterSecFloat: Количество секунд, которые ожидать после выполнения операции. По умолчанию установлено в настройках модуля Mouse (базовое значение 0.4)
    :type inWaitAfterSecFloat: float, опциональный
    """
    if inWaitAfterSecFloat == None: inWaitAfterSecFloat = WAIT_AFTER_SEC_FLOAT
    mouseDown(x=inXInt, y=inYInt, button = inButtonStr)
    time.sleep(inWaitAfterSecFloat)

def Up(inXInt:int=None, inYInt:int=None, inButtonStr:str='left', inWaitAfterSecFloat:float=WAIT_AFTER_SEC_FLOAT):
    """L+,W+: Отпустить (вверх) клавишу мыши. Если координаты inXInt, inYInt не переданы - нажатие происходит на тех координатах X/Y, на которых указатель мыши находится.

    !ВНИМАНИЕ! Отсчет координат inXInt, inYInt начинается с левого верхнего края рабочей области.

    .. code-block:: python

        # Mouse: Взаимодействие с мышью
        from pyOpenRPA.Robot import Mouse
        Mouse.Up(inButtonStr:str='right') #Поднять правую клавишу мыши

    :param inXInt: Целевая позиция указателя мыши по оси X (горизонтальная ось). 
    :type inXInt: int, опциональный
    :param inYInt: Целевая позиция указателя мыши по оси Y (вертикальная ось). 
    :type inYInt: int, опциональный
    :param inButtonStr: Номер кнопки, которую требуется поднять. Возможные варианты: 'left', 'middle', 'right' или 1, 2, 3. В остальных случаях инициирует исключение ValueError. По умолчанию 'left'
    :type inButtonStr: str, опциональный
    :param inWaitAfterSecFloat: Количество секунд, которые ожидать после выполнения операции. По умолчанию установлено в настройках модуля Mouse (базовое значение 0.4)
    :type inWaitAfterSecFloat: float, опциональный
    """
    if inWaitAfterSecFloat == None: inWaitAfterSecFloat = WAIT_AFTER_SEC_FLOAT
    mouseUp(x=inXInt, y=inYInt, button = inButtonStr)
    time.sleep(inWaitAfterSecFloat)

def MoveTo(inXInt=None, inYInt=None, inMoveDurationSecFloat:float=0.0, inWaitAfterSecFloat:float=WAIT_AFTER_SEC_FLOAT):
    """L+,W+: Переместить указатель мыши на позицию inXInt, inYInt за время inMoveDurationSecFloat.

    !ВНИМАНИЕ! Отсчет координат inXInt, inYInt начинается с левого верхнего края рабочей области (экрана).

    .. code-block:: python

        # Mouse: Взаимодействие с мышью
        from pyOpenRPA.Robot import Mouse
        Mouse.MoveTo(inXInt=100, inYInt=200) #Переместить указатель мыши по координатам: X(гор) 100, Y(вер) 200

    :param inXInt: Целевая позиция указателя мыши по оси X (горизонтальная ось). 
    :type inXInt: int, опциональный
    :param inYInt: Целевая позиция указателя мыши по оси Y (вертикальная ось). 
    :type inYInt: int, опциональный
    :param inMoveDurationSecFloat: Время перемещения указателя мыши, По умолчанию 0.0 (моментальное перемещение)
    :type inMoveDurationSecFloat: float, опциональный
    :param inWaitAfterSecFloat: Количество секунд, которые ожидать после выполнения операции. По умолчанию установлено в настройках модуля Mouse (базовое значение 0.4)
    :type inWaitAfterSecFloat: float, опциональный
    """
    if inWaitAfterSecFloat == None: inWaitAfterSecFloat = WAIT_AFTER_SEC_FLOAT
    moveTo(x=inXInt, y=inYInt, duration=inMoveDurationSecFloat)
    time.sleep(inWaitAfterSecFloat)
    
def ScrollVertical(inScrollClickCountInt, inXInt=None, inYInt=None, inWaitAfterSecFloat:float=WAIT_AFTER_SEC_FLOAT):
    """L+,W+: Переместить указатель мыши на позицию inXInt, inYInt и выполнить вертикальную прокрутку (скроллинг) колесом мыши на количество щелчков inScrollClickCountInt.

    !ВНИМАНИЕ! Отсчет координат inXInt, inYInt начинается с левого верхнего края рабочей области (экрана).

    .. code-block:: python

        # Mouse: Взаимодействие с мышью
        from pyOpenRPA.Robot import Mouse
        Mouse.ScrollVertical(100, inXInt=100, inYInt=200) #Крутить колесо мыши вниз на 100 кликов по координатам: X(гор) 100, Y(вер) 200
        Mouse.ScrollVertical(-100) #Крутить колесо мыши вверх на 100 кликов по текущим координатам указателя мыши.

    :param inScrollClickCountInt: Количество щелчок колеса мыши, которое требуется !вертикально! прокрутить. Аргумент может принимать как положительное (прокрутка вниз), так и отрицательное (прокрутка вверх) значения
    :type inScrollClickCountInt: int, обязательный
    :param inXInt: Целевая позиция указателя мыши по оси X (горизонтальная ось). 
    :type inXInt: int, опциональный
    :param inYInt: Целевая позиция указателя мыши по оси Y (вертикальная ось). 
    :type inYInt: int, опциональный
    :param inWaitAfterSecFloat: Количество секунд, которые ожидать после выполнения операции. По умолчанию установлено в настройках модуля Mouse (базовое значение 0.4)
    :type inWaitAfterSecFloat: float, опциональный
    """
    if inWaitAfterSecFloat == None: inWaitAfterSecFloat = WAIT_AFTER_SEC_FLOAT
    inScrollClickCountInt = inScrollClickCountInt*-1
    vscroll(inScrollClickCountInt, x=inXInt, y=inYInt)
    time.sleep(inWaitAfterSecFloat)
    
def ScrollHorizontal(inScrollClickCountInt, inXInt=None, inYInt=None, inWaitAfterSecFloat:float=WAIT_AFTER_SEC_FLOAT):
    """L+,W-: Переместить указатель мыши на позицию inXInt, inYInt и выполнить горизонтальную прокрутку (скроллинг) виртуальным колесом мыши на количество щелчков inScrollClickCountInt.

    !ВНИМАНИЕ! Отсчет координат inXInt, inYInt начинается с левого верхнего края рабочей области (экрана).

    .. code-block:: python

        # Mouse: Взаимодействие с мышью
        from pyOpenRPA.Robot import Mouse
        Mouse.ScrollHorizontal(100, inXInt=100, inYInt=200) #Крутить колесо мыши вниз на 100 кликов по координатам: X(гор) 100, Y(вер) 200
        Mouse.ScrollHorizontal(-100) #Крутить колесо мыши вверх на 100 кликов по текущим координатам указателя мыши.

    :param inScrollClickCountInt: Количество щелчок колеса мыши, которое требуется !горизонтально! прокрутить. Аргумент может принимать как положительное (прокрутка вправо), так и отрицательное (прокрутка влево) значения
    :type inScrollClickCountInt: int, обязательный
    :param inXInt: Целевая позиция указателя мыши по оси X (горизонтальная ось). 
    :type inXInt: int, опциональный
    :param inYInt: Целевая позиция указателя мыши по оси Y (вертикальная ось). 
    :type inYInt: int, опциональный
    :param inWaitAfterSecFloat: Количество секунд, которые ожидать после выполнения операции. По умолчанию установлено в настройках модуля Mouse (базовое значение 0.4)
    :type inWaitAfterSecFloat: float, опциональный
    """
    if inWaitAfterSecFloat == None: inWaitAfterSecFloat = WAIT_AFTER_SEC_FLOAT
    hscroll(inScrollClickCountInt, x=inXInt, y=inYInt)
    time.sleep(inWaitAfterSecFloat)
