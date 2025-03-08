import opheliaNeurals as opheNeu
import opheliaPlugins as ophePlu
import opheliaBridge as opheBri
import opheliaTrayIcon as opheIcon
from functions import opheliaMouth, opheliaHears, opheliaDiscord as opheDisc

def onStart():
    if not opheNeu.ctypes.windll.shell32.IsUserAnAdmin():
        opheNeu.ctypes.windll.shell32.ShellExecuteW(None, "runas", opheNeu.sys.executable, " ".join(opheNeu.sys.argv), None, 1)
        print(f"Requested elevation: {opheNeu.sys.executable} {opheNeu.sys.argv[0]}")
        opheNeu.sys.exit(0)
    else: pass

def startDiscord():
    opheDisc.discordLoop = opheDisc.wakeOpheliaDiscord()
    opheNeu.discordLoop = opheDisc.discordLoop
    opheNeu.thr.Thread(target=opheDisc.discordLoop.run_forever, daemon=True).start()

def opheliaBegin(onStartBool, quickstart=False, discord=True):
    print("Ophelia Prime Booting...")
    opheNeu.thr.Thread(target=opheNeu.monitorThreads, daemon=True).start()
    opheBri.bridgeIconStart(opheIcon)
    opheNeu.debug_log("Ophelia Prime Booting...")
    if onStartBool: onStart()
    if discord: startDiscord()
    if not quickstart:
        opheliaMouth.opheliaSpeak(opheNeu.getRandomDialogue("greetings"))
        with opheNeu.sr.Microphone(device_index=1) as source:
            opheNeu.recognizer.adjust_for_ambient_noise(source)
            opheNeu.recognizer.energy_threshold *= 0.75
            print(f"Adjusted energy threshold: {opheNeu.recognizer.energy_threshold}")
        weatherReport = ophePlu.plugins["Weather"].execute(showLogs=False)
        try:        
            opheliaMouth.opheliaSpeak(f"Would you like to hear today's weather report?")
            if opheliaHears.opheliaHears(8, timed=True).__contains__("yes"): 
                print("Getting Weather Report..."); 
                opheliaMouth.opheliaSpeak(weatherReport)
            else: print("Weather report rejected..."); pass
        except: pass
        opheliaMouth.opheliaSpeak(opheNeu.getRandomDialogue("ready"))
    
    opheliaMouth.opheliaSpeak(f"There are currently {ophePlu.plugins['Ticket'].startQuestManager()} daily quests completed.")
    ophePlu.plugins["Posture"].postureCheckWrapped()
    opheBri.opheliaStartMainLoop()
    
