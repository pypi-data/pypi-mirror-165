from setuptools import setup, find_packages
import Version
import os
def LongDescriptionRead():
    with open('pyOpenRPA/README.md', "r", encoding="utf-8") as f:
        return f.read()

#Do pyOpenRPA package __init__ __version__ update
Version.pyOpenRPAVersionUpdate("..","pyOpenRPA/__init__.py")

datadir = "pyOpenRPA\\Resources"
datafiles = []
for d, folders, files in os.walk(datadir): 
    for f in files: 
        datafiles.append(os.path.join(d,f))
datadir = "pyOpenRPA\\Orchestrator\\Web"
for d, folders, files in os.walk(datadir): 
    for f in files: 
        datafiles.append(os.path.join(d,f))
datadir = "pyOpenRPA\\Studio\\Web"
for d, folders, files in os.walk(datadir): 
    for f in files: 
        datafiles.append(os.path.join(d,f))
datafile = "pyOpenRPA\\Tools\\RobotRDPActive\\Template.rdp"
datafiles = datafiles + [datafile]
datafile = "pyOpenRPA\\Tools\\RobotScreenActive\\ConsoleStart.bat"
datafiles = datafiles + [datafile]
datafile = "pyOpenRPA\\LICENSE.pdf"
datafiles = datafiles + [datafile]
setup(name='pyOpenRPA',
      version=Version.Get(".."),
      description='The powerful open source RPA platform for business',
      long_description=LongDescriptionRead(),
      long_description_content_type='text/markdown',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
		'License :: Free For Educational Use',
		'License :: Free For Home Use',
		'License :: Free for non-commercial use',
        'Intended Audience :: Developers',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
		'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Home Automation'
      ],
      keywords='pyOpenRPA OpenRPA RPA Robot Automation Robotization OpenSource IT4Business',
      url='https://pyopenrpa.ru/',
      author='Ivan Maslov',
      author_email='Ivan.Maslov@pyopenrpa.ru',
      license='Текст лицензии см. в файле: LICENSE.PDF (в корне) или по адресу: https://pyopenrpa.ru/license/oferta.pdf',
      packages=find_packages(),
      install_requires=[
          'pillow>=6.0.0',
		  'keyboard>=0.13.3',
		  'pyautogui<=0.9.52',
		  'psutil>=5.6.2'
		  'crypto>=1.4.1', 
		  'schedule>=1.1.0', 
		  'Jinja2>=2.2.11.2', 
		  'selenium>=3.141.0'
      ],
	  extras_require={
        ':sys_platform == "win32"': [
            'pywin32>=224', 'WMI>=1.4.9', 'pywinauto>=0.6.8'
        ],
        ':"linux" in sys_platform': [
            'simplepam>=0.1.5', 'pyclip>=0.6.0'
        ]
	},
      include_package_data=True,
      #data_files = datafiles,
      #package_data = {"pyOpenRPA": datafiles},
      zip_safe=False)
