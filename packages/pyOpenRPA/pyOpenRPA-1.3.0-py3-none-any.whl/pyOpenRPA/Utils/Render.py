import jinja2
from pyOpenRPA.Tools import CrossOS

class Render():
    """L+,W+: Класс генерации текста по шаблонам Jinja2

    .. code-block:: python

        # Пример использования
        from pyOpenRPA.Utils.Render import Render
        lRender = Render(inTemplatePathStr="test.txt", inTemplateRefreshBool = True)
        lRender.Generate()

    .. code-block:: html
    
        Hello my control panel!
        You can use any def from Orchestrator module here in Jinja2 HTML template:
        Example: OrchestratorModule.OSCMD(inCMDStr="notepad")
        {{MathModule.pi}} # Обратиться к переменной 
        {% if UserInfoDict['UserNameUpperStr']=="ND" %}
        YES - IT IS ND
        {% endif %}

        {% include 'test2.txt' %} # Добавить содержимого другого файла. Подняться выше нельзя через .. 

    """
    # Jinja2 consolidated
    mTemplateRefreshBool = None
    mDataDict = None

    # RefreshHTML block
    mTemplatePathStr = None
    mTemplateFileNameStr = None
    mLoader = None
    mEnv = None
    mTemplate = None
    mLogger = None

    def __init__(self, inTemplatePathStr = None, inTemplateRefreshBool = False, inLogger = None):
        """L+,W+: Инициализация объекта генерации текста из шаблона Jinja2

        .. code-block:: python

            # Пример использования
            from pyOpenRPA.Utils.Render import Render
            lRender = Render(inTemplatePathStr="test.txt", inTemplateRefreshBool = True)

        :param inTemplatePathStr: Путь к шаблону в формате Jinja2
        :type inTemplatePathStr: str
        :param inTemplateRefreshBool: True - читать шаблон Jinja2 при каждом выхове функции Generate()
        :type inTemplateRefreshBool: bool
        :param inLogger: Экземпляр логгера
        :type inLogger: logging.Logger
        :return: self
        :rtype: pyOpenRPA.Utils.Render.Render
        """
        self.mLogger = inLogger
        self.TemplatePathSet(inTemplatePathStr = inTemplatePathStr)
        self.mTemplateRefreshBool = inTemplateRefreshBool

    def DataSet(self, inDataDict):
        """L+,W+: Установить словарь данных, передаваемый в шаблонизатор. Функция полезна для фиксации тех данных, которые не изменяются при каждом вызове функции Generate. Если такие данные изменяются каждый раз, то передавать их можно через функцию Generate

        .. code-block:: python

            # Пример использования
            from pyOpenRPA.Utils.Render import Render
            lRender = Render(inTemplatePathStr="test.txt", inTemplateRefreshBool = True)
            lRender.DataSet(inDataDict={"key1":"value1"})
            lRender.Generate()

        :param inDataDict: Словарь данных, который отправляется в шаблон Jinja2 при генерации
        :type inDataDict: str
        :return: None
        """
        self.mDataDict = inDataDict
        
    def TemplatePathSet(self, inTemplatePathStr, inLogger = None):
        """L+,W+: Установить шаблон формата Jinja2, из которого формировать готовый текст

        .. code-block:: python

            # Пример использования
            from pyOpenRPA.Utils.Render import Render
            lRender = Render(inTemplatePathStr="test.txt")
            lRender.TemplatePathSet(inDataDict={"key1":"value1"})
            lRender.Generate()

        :param inTemplatePathStr: Путь к шаблону в формате Jinja2
        :type inTemplatePathStr: str
        :param inLogger: Экземпляр логгера
        :type inLogger: logging.Logger
        :return:
        """
        try:
            if inTemplatePathStr is not None:
                lSystemLoaderPathStr = "/".join(CrossOS.PathSplitList(inPathStr=inTemplatePathStr)[0:-1])
                lTemplateFileNameStr = CrossOS.PathSplitList(inPathStr=inTemplatePathStr)[-1]
                self.mTemplateFileNameStr = lTemplateFileNameStr
                self.mLoader = jinja2.FileSystemLoader(lSystemLoaderPathStr)
                self.mEnv = jinja2.Environment(loader=self.mLoader, trim_blocks=True)
                self.mTemplate = self.mEnv.get_template(lTemplateFileNameStr)
        except Exception as e:
            self._LogException(inStr = "ОШИБКА ПРИ УСТАНОВКЕ ШАБЛОНА JINJA2", inLogger = inLogger, inException=e)

    def Generate(self, inDataDict=None, inLogger = None) -> str:
        """L+,W+: Сформировать текст из шаблона Jinja2. Pass the context inDataDict
        
        .. code-block:: python

            # Пример использования
            from pyOpenRPA.Utils.Render import Render
            lRender = Render(inTemplatePathStr="test.txt", inTemplateRefreshBool = True)
            lRender.Generate()

        :param inDataDict: Словарь для передачи в шаблонизатор
        :type inDataDict: dict
        :param inLogger: Экземпляр логгера
        :type inLogger: logging.Logger
        :return: Текст, сформированный шаблонизатором Jinja2
        :rtype: str
        """
        try:
            if self.mTemplateRefreshBool == True:
                self.mTemplate = self.mEnv.get_template(self.mTemplateFileNameStr)
            if self.mDataDict is not None: lDataDict = self.mDataDict
            elif inDataDict is not None: lDataDict = inDataDict
            else: lDataDict = {}
            if self.mDataDict is not None and inDataDict is not None: lDataDict.update(inDataDict)
            lStr = self.mTemplate.render(**lDataDict) # Render the template into str
            return lStr
        except Exception as e:
            self._LogException(inStr="ОШИБКА ПРИ ГЕНЕРАЦИИ ТЕКСТА ИЗ ШАБЛОНА JINJA2", inLogger=inLogger)

    # LOGGING HANDLERS
    def _LogException(self, inStr, inLogger = None, inException = None):
        if inLogger is not None: inLogger.exception(inStr)
        elif self.mLogger is not None: self.mLogger.exception(inStr)
        else: raise inException