from functions import opheliaObey
from functions.opheliaHears import opheliaHears
import opheliaNeurals as opheNeu

def opheliaListens(timeout=None, commandMap=None):
    opheNeu.debug_log("Ophelia is now listening...")
    while opheNeu.opheliaRequired:
        opheliaHeard = opheliaHears(timeout)
        if opheliaHeard:
            if "ophelia" in opheliaHeard or "command" in opheliaHeard:
                opheNeu.debug_log(f"Ophelia has heard {opheliaHeard}")
                #opheliaObey.opheliaDo(opheliaHeard, commandMap)
                opheliaObey.opheliaDo(opheliaHeard)
            else: print("Rambling... " + opheNeu.random.choice(opheNeu.misc["emojis"])) 