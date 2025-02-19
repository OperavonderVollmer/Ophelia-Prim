import opheliaNeurals as opheNeu
import opheliaAuxilliary as opheAux
import opheliaBridge as opheBri
import opheliaTrayIcon as opheIcon
from functions import opheliaMouth, opheliaHears

def onStart():
    if not opheNeu.ctypes.windll.shell32.IsUserAnAdmin():
        opheNeu.ctypes.windll.shell32.ShellExecuteW(None, "runas", opheNeu.sys.executable, " ".join(opheNeu.sys.argv), None, 1)
        print(f"Requested elevation: {opheNeu.sys.executable} {opheNeu.sys.argv[0]}")
        opheNeu.sys.exit(0)
    else: pass

def opheliaBegin(onStartBool, quickstart=False):
    opheBri.bridgeIconStart(opheIcon)
    print("Ophelia Prime Booting...")
    if onStartBool: 
        onStart()
    if not quickstart:
        opheliaMouth.opheliaSpeak(opheNeu.getRandomDialogue("greetings"))
        with opheNeu.sr.Microphone(device_index=1) as source:
            opheNeu.recognizer.adjust_for_ambient_noise(source)
            opheNeu.recognizer.energy_threshold *= 0.75
            print(f"Adjusted energy threshold: {opheNeu.recognizer.energy_threshold}")
        weatherReport = opheAux.getWeather(False)
        try:        
            opheliaMouth.opheliaSpeak(f"Would you like to hear today's weather report?")
            if opheliaHears.opheliaHears(6).__contains__("yes"): print("Getting Weather Report..."); opheliaMouth.opheliaSpeak(weatherReport)
            else: print("Weather report rejected..."); pass
        except: pass
        opheliaMouth.opheliaSpeak(opheNeu.getRandomDialogue("ready"))
    opheAux.postureCheckWrapped()
    opheBri.opheliaStartMainLoop()
    
