# OpenRPA
First open source RPA platform for business is released!

# How to run
Studio
Double click to Studio\StudioRun_32.cmd or Studio\StudioRun_64.cmd

# Robot how to debug
Robot\PythonDebug_64.cmd
import Robot
Robot.ActivityRun(
	{
	   ModuleName: <"GUI"|..., str>,
	   ActivityName: <Function or procedure name in module, str>,
	   ArgumentList: [<Argument 1, any type>, ...] - optional,
	   ArgumentDict: {<Argument 1 name, str>:<Argument 1 value, any type>, ...} - optional
	}
)

# Robot example script:
Robot\Examples\GetFolderList\Python_32_Script_Run.cmd

# Python 32 bit
Resources\WPy32-3720\python-3.7.2\python.exe

# Python 64 bit
Resources\WPy64-3720\python-3.7.2.amd64\python.exe

# Module GUI activity List:
############################
Новая версия
############################
Получить список элементов, который удовлетворяет условиям через расширенный движок поиска
[
   {
       "index":<Позиция элемента в родительском объекте>,
       "depth_start" - глубина, с которой начинается поиск (по умолчанию 1)
       "depth_end" - глубина, до которой ведется поиск (по умолчанию 1)
       "class_name" - наименование класса, который требуется искать
       "title" - наименование заголовка
       "rich_text" - наименование rich_text
   }
]



Created by pyOpenRPA LLC (Ivan Maslov)