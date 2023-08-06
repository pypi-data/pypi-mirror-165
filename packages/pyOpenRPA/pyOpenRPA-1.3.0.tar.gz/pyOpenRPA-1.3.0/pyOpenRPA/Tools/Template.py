from pyOpenRPA import Orchestrator
from . import CrossOS
import jinja2
import os
from inspect import signature # For detect count of def args
import operator
import math
import copy

class Template():
    """
    Шаблон генерации строки. Использует Jinja2

    .. code-block:: python

        from pyOpenRPA.Tools import Template
        # ПРИМЕР:
        lTemplate = Template.Template(
            inPathStr="ControlPanel\\test.html", 
            inRefreshBool = True)
        lStr = lTemplate.GenerateStr() # Сформировать текст по шаблону
        
    Контектст, который формируется по умолчанию:
    ControlPanelInstance: self,
    OrchestratorModule: Orchestrator,
    EnumerateDef: enumerate,
    OperatorModule: operator,
    MathModule: math

    Вы можете дополнить стандартный словарь контекста с помощью функции ContextDictSet() 

    .. code-block:: html
    
        Hello my control panel!
        You can use any def from Orchestrator module here in Jinja2 HTML template:
        Example: OrchestratorModule.OSCMD(inCMDStr="notepad")
        {{MathModule.pi}}

    """
    # Jinja2 consolidated
    mJinja2TemplateRefreshBool = None
    mJinja2ContextDict = None
    mJinja2TemplatePathStr = None
    mJinja2TemplateFileNameStr = None
    mJinja2Loader = None
    mJinja2Env = None
    mJinja2Template = None
    mLogger = None

    def __init__(self, inPathStr = None, inRefreshBool = False, inLogger = None):
        """
        Конструктор шаблона для генерации

        :param inPathStr: Путь к шаблону. Поддерживает специфику разлных ОС. 'path/to/file' и 'path\\to\\file'
        :param inRefreshBool: True - читать шаблон из файловой системы при каждом обращении на формирование строки (GenerateStr)
        """
        self.PathSet(inPathStr = inPathStr)
        self.mJinja2TemplateRefreshBool = inRefreshBool
        self.mLogger = inLogger

    def ContextDictSet(self, inContextDict):
        """
        Установить дополнительный контекст для генерации строки.

        :param inContextDict: Дополнительный контекст, который будет использоваться при формировании строки
        """
        self.mJinja2ContextDict = inContextDict

    def PathSet(self, inPathStr):
        """
        Установить путь к шаблону для генерации (движок Jinja2)

        :param inPathStr: Путь к шаблону для генерации
        """
        try:
            if inPathStr is not None:
                lSystemLoaderPathStr = "/".join(CrossOS.PathSplitList(inPathStr=inPathStr)[0:-1])
                lTemplateFileNameStr = CrossOS.PathSplitList(inPathStr=inPathStr)[-1]
                self.mJinja2TemplateFileNameStr = lTemplateFileNameStr
                self.mJinja2Loader = jinja2.FileSystemLoader(lSystemLoaderPathStr)
                self.mJinja2Env = jinja2.Environment(loader=self.mJinja2Loader, trim_blocks=True)
                self.mJinja2Template = self.mJinja2Env.get_template(lTemplateFileNameStr)
        except Exception as e:
            if self.mLogger: self.mLogger.exception("EXCEPTION WHEN INIT JINJA2")
            raise e

    def GenerateStr(self, inContextDict=None):
        """
        Сформировать строку с помощью шаблонизатора Jinja2. Передать контекст для формирования inContextDict. 
        
        По умолчанию доступны следующие атрибуты контекста:
        {
            "TemplateInstance":self,
            "OrchestratorModule":Orchestrator,
            "EnumerateDef": enumerate,
            "OperatorModule": operator,
            "MathModule": math
        }
        
        :param inContextDict: Дополнительный контекст для генерации строки. 
        :return: Сформированная строка
        :rtype: str
        """
        if inContextDict is None: inContextDict = {}
        if self.mJinja2TemplateRefreshBool == True:
            self.mJinja2Template = self.mJinja2Env.get_template(self.mJinja2TemplateFileNameStr)
        lContextDict = self.ContextGenerateDict()
        lContextDict.update(inContextDict)
        lStr = self.mJinja2Template.render(**lContextDict) # Render the template into str
        return lStr

    def ContextGenerateDict(self):
        """
        Техническая функция. Сформировать преднастроенный словарь контекста для дальнейшего дообогащения
        :return:
        """
        lData = {
            "TemplateInstance":self,
            "OrchestratorModule":Orchestrator,
            "EnumerateDef": enumerate,
            "OperatorModule": operator,
            "MathModule": math
        }
        # Checkj Jinja2ContextDict
        if self.mJinja2ContextDict is not None:
            lData.update(self.mJinja2ContextDict)
        return lData