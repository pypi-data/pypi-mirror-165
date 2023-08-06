import requests, time, json
from . import Processor
# O2A - Data flow Orchestrator to Agent

# f"{lProtocolStr}://{lHostStr}:{lPortInt}/pyOpenRPA/Agent/O2A"
# Request BODY:
# { "HostNameUpperStr": "", "UserUpperStr": "" }
# Response BODY:
# QUEUE ITEM
#                 # {
#                 #    "Def":"DefAliasTest", # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
#                 #    "ArgList":[1,2,3], # Args list
#                 #    "ArgDict":{"ttt":1,"222":2,"dsd":3} # Args dictionary
#                 #    "ArgGSettings": # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
#                 #    "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
#                 # },

def O2A_Loop(inGSettings):
    lL = inGSettings["Logger"]
    lActivityLastGUIDStr = "" # Init empty ActivityLastGUIDStr
    while inGSettings["O2ADict"]["IsOnlineBool"]:
        # Send request to the orchestrator server
        lRequestBody = None
        # ConnectionError - CE
        lCEPhaseFastTimeLastGoodFloat = time.time()
        lCEPhaseFastDurationSecFloat = inGSettings['O2ADict']['ConnectionTimeoutSecFloat']
        lCEPhaseFastRetrySecFloat = inGSettings['O2ADict']['RetryTimeoutSecFloat']/5.0
        lCEPhaseLongRetrySecFloat = inGSettings['O2ADict']['RetryTimeoutSecFloat']*12.0
        try:
            lProtocolStr= "https" if inGSettings["OrchestratorDict"]["IsHTTPSBool"] else "http"
            lHostStr = inGSettings["OrchestratorDict"]["HostStr"]
            lPortInt = inGSettings["OrchestratorDict"]["PortInt"]
            lURLStr=f"{lProtocolStr}://{lHostStr}:{lPortInt}/pyOpenRPA/Agent/O2A"
            lDataDict = { "HostNameUpperStr": inGSettings["AgentDict"]["HostNameUpperStr"], "UserUpperStr": inGSettings["AgentDict"]["UserUpperStr"], "ActivityLastGUIDStr": lActivityLastGUIDStr}
            lResponse = requests.post(url= lURLStr, cookies = {"AuthToken":inGSettings["OrchestratorDict"]["SuperTokenStr"]}, json=lDataDict, timeout=inGSettings["O2ADict"]["ConnectionTimeoutSecFloat"])
            lCEPhaseFastTimeLastGoodFloat = time.time()
            if lResponse.status_code != 200:
                if lL: lL.warning(f"Agent can not connect to Orchestrator. Below the response from the orchestrator:{lResponse}")
                time.sleep(inGSettings["O2ADict"]["RetryTimeoutSecFloat"])
            else:
                lRequestBody = lResponse.text
                lBodyLenInt = len(lRequestBody)
                if lBodyLenInt != 0: # CHeck if not empty result when close the connection from orch
                    lQueueList = lResponse.json() # Try to get JSON
                    for lQueueItem in lQueueList:
                        # Append QUEUE item in ProcessorDict > ActivityList
                        lActivityLastGUIDStr = lQueueItem["GUIDStr"]
                        # Check if ActivityItem ["ThreadBool"] = False > go sync mode in processor queue; Else: New thread
                        if lQueueItem.get("ThreadBool",False) == False:
                            inGSettings["ProcessorDict"]["ActivityList"].append(lQueueItem)
                        else:
                            Processor.ProcessorRunAsync(inGSettings=inGSettings,inActivityList=[lQueueItem])
                        # Log full version if bytes size is less than limit . else short
                        lAgentLimitLogSizeBytesInt = 500
                        if lBodyLenInt <= lAgentLimitLogSizeBytesInt:
                            if lL: lL.info(f"Словарь ActivityItem, полученный от оркестратора: {lQueueItem}")
                        else:
                            if lL: lL.info(f"Словарь ActivityItem, полученный от оркестратора: содержимое свернуто из-за большого размера ({lBodyLenInt} байт")
                else:
                    if lL: lL.debug(f"Поступил пустой ответ от оркестратора - цикл попытается обновить соединение между оркестратором и агентом");
        except requests.exceptions.ConnectionError as e:
            if time.time() - lCEPhaseFastTimeLastGoodFloat <= lCEPhaseFastDurationSecFloat:
                if lL: lL.error(f"О2А Ошибка соединения - оркестратор недоступен. Повторить попытку через {lCEPhaseFastRetrySecFloat} с.")
                time.sleep(lCEPhaseFastRetrySecFloat)
            else:
                if lL: lL.error(f"О2А Ошибка соединения - оркестратор недоступен. Повторить попытку через {lCEPhaseLongRetrySecFloat} с.")
                time.sleep(lCEPhaseLongRetrySecFloat)
        except ConnectionResetError as e:
            if lL: lL.error(f"О2А Ошибка сброса соединения - оркестратор недоступен. Повторить попытку через {inGSettings['O2ADict']['RetryTimeoutSecFloat']} с.")
            time.sleep(inGSettings["O2ADict"]["RetryTimeoutSecFloat"])
        except json.decoder.JSONDecodeError as e:
            if lL: lL.error(f"О2А Ошибка декодирования JSON - далее представлено содержимое, которое поступило на обработку: {lRequestBody}")
            time.sleep(inGSettings["O2ADict"]["RetryTimeoutSecFloat"])
        except requests.exceptions.Timeout as e:
            if lL: lL.exception(f"О2А Ошибка соединения (превышено время ожидания). Повторить попытку через {inGSettings['O2ADict']['RetryTimeoutSecFloat']} с.")
            time.sleep(inGSettings["O2ADict"]["RetryTimeoutSecFloat"])
        except Exception as e:
            if lL: lL.exception(f"О2А Общая ошибка. Повторить попытку через {inGSettings['O2ADict']['RetryTimeoutSecFloat']} с.")
            time.sleep(inGSettings["O2ADict"]["RetryTimeoutSecFloat"])