import pyttsx3, pyaudio, psutil, wmi, ctypes, sys, os
import speech_recognition as sr
import opheliaAuxilliary as opheAux
import opheliaNeurals as opheNeu

def opheliaListen(duration):    
    if opheNeu.opheliaRequired:
        print("Awaiting Input...")
        with sr.Microphone() as source:
            if duration < 1:
                audio = opheNeu.recognizer.listen(source)
            else:
                audio = opheNeu.recognizer.listen(source, timeout=duration)
            text = ""

            try:
                text = opheNeu.recognizer.recognize_google(audio)
            except sr.RequestError:
                try:
                    text = opheNeu.recognizer.recognize_sphinx(audio)
                except sr.UnknownValueError:
                    text = ("Sorry, Ophelia could not understand the audio.")
                except sr.RequestError as e:
                    text = (f"PocketSphinx error; {e}")
            finally:
                print(f"Detected Input: {text}")
                text = text.lower()
                if text.__contains__("ophelia") or text.__contains__("command"):
                    opheliaSpeak(recognizeCommand(text))                
                opheliaListen(0)
                return text
def recognizeCommand(command):
    if command.__contains__("command"):
        try:
            for keyword, response in commandMap.items():
                if keyword in command:
                    print(f"Command Recognized: {str(keyword)}")
                    opheliaSpeak(f"Command Recognized")
                    return response() if callable(response) else response
        except Exception as e:
            print(e)
            return(f"Command cannot be executed")
    else:
        opheAux.opheliaCareKit()
def opheliaSpeak(text):    
    opheNeu.engine.say(text=text)
    opheNeu.engine.runAndWait()
def opheliaStop():
    opheNeu.opheliaRequired = False
    opheliaSpeak("Ophelia has been instructed to stop, Ophelia wishes you an excellent day")
    opheNeu.engine.stop()
#--------------------------------------------------------#
commandMap = {
    "stat": opheAux.getCPUStats,
    "balls": lambda: "Now crushing his balls",
    "stop": opheliaStop,
    }
#--------------------------------------------------------#
def onStart():
    if ctypes.windll.shell32.IsUserAnAdmin():
        # Already running as admin, proceed with the operation
        opheliaSpeak(f"Welcome, Master. Ophelia has been humbly waiting for you")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        print(f"Requested elevation: {sys.executable} {sys.argv[0]}")
        sys.exit(0)
#--------------------------------------------------------#
def opheliaBegin ():
    with sr.Microphone() as source:
        opheNeu.recognizer.adjust_for_ambient_noise(source)
        print(f"Adjusted energy threshold: {opheNeu.recognizer.energy_threshold}")
    opheliaSpeak(opheliaListen(0))
opheliaBegin()
try:
    opheAux.getCPUStats()
except Exception as e:
    print(e)


input("Press Enter to continue...")