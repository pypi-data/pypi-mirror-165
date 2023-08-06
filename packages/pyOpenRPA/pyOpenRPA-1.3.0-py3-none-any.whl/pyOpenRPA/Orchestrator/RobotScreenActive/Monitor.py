import time #lib to create delay
from pyOpenRPA.Tools import CrossOS
from . import Screen # module to detect screen exists
#Check screen every 1 second
def CheckScreen(inIntervalSeconds=1):
    if CrossOS.IS_WINDOWS_BOOL:
        while True:
            #Check if screen exist
            if not Screen.Exists():
                #Send os command to create console version (base screen)
                Screen.ConsoleScreenBase()
                #Delay to create console screen
                time.sleep(15)
            #Delay
            time.sleep(inIntervalSeconds)
        return None