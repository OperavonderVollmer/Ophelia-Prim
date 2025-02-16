import pyttsx3, pyaudio, psutil, wmi, ctypes, sys, os
import speech_recognition as sr


def inquiry(duration):    
    if opheliaRequired:
        print("Awaiting Input...")
        with sr.Microphone() as source:
            if duration < 1:
                audio = recognizer.listen(source)
            else:
                audio = recognizer.listen(source, timeout=duration)
            text = ""

            try:
                text = recognizer.recognize_google(audio)
            except sr.RequestError:
                try:
                    text = recognizer.recognize_sphinx(audio)
                except sr.UnknownValueError:
                    text = ("Sorry, Ophelia could not understand the audio.")
                except sr.RequestError as e:
                    text = (f"PocketSphinx error; {e}")
            finally:
                print(f"Detected Input: {text}")
                text = text.lower()
                if text.__contains__("ophelia") or text.__contains__("command"):
                    speak(recognizeCommand(text))                
                inquiry(0)
                return text
def recognizeCommand(command):
    if command.__contains__("command"):
        try:
            for keyword, response in commandMap.items():
                if keyword in command:
                    print(f"Command Recognized: {str(keyword)}")
                    return response() if callable(response) else response
        except Exception as e:
            print(e)
            return(f"Command cannot be executed")
    else:
        opheliaCareKit()
def speak(text):    
    engine.say(text=text)
    engine.runAndWait()
def opheliaStop():
    global opheliaRequired
    opheliaRequired = False
    speak("Command recognized: Ophelia has been instructed to stop, Ophelia wishes you an excellent day")
    engine.stop()
def getCPUStats():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_total = (f"{ram.total / (1024 ** 3):.2f} GB")
    ram_available = (f"{ram.available / (1024 ** 3):.2f} GB")
    ram_usage = (f"{ram.percent}%")
    try:
        cpu_temp = (f"{(computer.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature / 10) - 273.15:.2f}°C")
    except:
        cpu_temp = "Currently Unavailable"
    text = (f"CPU Usage: {cpu_usage}%\nRAM Usage: {ram_usage}\nRAM Total: {ram_total}\nRAM Available: {ram_available}\nCPU Temperature: {cpu_temp}")
    print(text)
    speak(text=text)
def opheliaCareKit():
    speak("Command Recognized: Unfortunately, this feature hasn't been implemented yet")
#--------------------------------------------------------#
opheliaRequired = True
recognizer = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
computer = wmi.WMI(namespace="root\\wmi")
commandMap = {
    "stat": getCPUStats,
    "balls": lambda: "Command Recognized: Now crushing his balls",
    "stop": opheliaStop,
    }
#--------------------------------------------------------#
def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        # Already running as admin, proceed with the operation
        speak(f"Welcome, Master. Ophelia has been humbly waiting for you")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        print(f"Requested elevation: {sys.executable} {sys.argv[0]}")
        sys.exit(0)
run_as_admin()
#--------------------------------------------------------#
with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)
    print(f"Adjusted energy threshold: {recognizer.energy_threshold}")
speak(inquiry(0))
