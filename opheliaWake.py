import opheliaNeurals as opheNeu
import opheliaMainFunctions as opheMf
import opheliaAuxilliary as opheAux
import opheliaBridge as opheBri

def onStart():
    if not opheNeu.ctypes.windll.shell32.IsUserAnAdmin():
        opheNeu.ctypes.windll.shell32.ShellExecuteW(None, "runas", opheNeu.sys.executable, " ".join(opheNeu.sys.argv), None, 1)
        print(f"Requested elevation: {opheNeu.sys.executable} {opheNeu.sys.argv[0]}")
        opheNeu.sys.exit(0)

def opheliaBegin(onStartBool):
    print("Ophelia Prime Booting...")
    if onStartBool: 
        onStart()
    opheMf.opheliaSpeak(f"Welcome, Master. Ophelia has been humbly waiting for you.")
    with opheNeu.sr.Microphone(device_index=1) as source:
        opheNeu.recognizer.adjust_for_ambient_noise(source)
        opheNeu.recognizer.energy_threshold *= 0.75
        print(f"Adjusted energy threshold: {opheNeu.recognizer.energy_threshold}")
    weatherReport = opheAux.getWeather(False)
    try:        
        opheMf.opheliaSpeak(f"Would you like to hear today's weather report?")
        if opheMf.opheliaHears(6).__contains__("yes"): print("Getting Weather Report..."); opheMf.opheliaSpeak(weatherReport)
        else: print("Weather report rejected..."); pass
    except: pass
    opheMf.opheliaSpeak("How may Ophelia assist you today?")
    opheBri.opheliaStartMainLoop()
