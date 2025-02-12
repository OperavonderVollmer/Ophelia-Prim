import pyttsx3
import speech_recognition as sr
import opheliaAuxilliary as oa


def opheliaBegin ():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print(f"Adjusted energy threshold: {recognizer.energy_threshold}")
    #opheliaListen(0, opheliaRequired)


def opheliaStop():
    global opheliaRequired
    opheliaRequired = False
    command = "Command recognized: Ophelia has been instructed to stop, Ophelia wishes you an excellent day"
    return command

def opheliaSpeak(text):    
    engine.say(text=text)
    engine.runAndWait()

def opheliaListen(duration, opheliaRequired):  
    try:  
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
                        opheliaSpeak(recognizeCommand(text))                    
                        opheliaListen(0, opheliaRequired)
                    else:
                        opheliaListen(0, opheliaRequired)
    except Exception as e:
        print(e)
        opheliaListen(0, opheliaRequired)
def recognizeCommand(command):
    if command.__contains__("command"):
        try:
            for keyword, response in commandMap.items():
                if keyword in command:
                    print(f"Command Recognized: {str(keyword)}")
                    opheliaSpeak(response() if callable(response) else response)
        except Exception as e:
            print(e)
            return(f"Command cannot be executed")
    else:
        oa.opheliaCareKit()

commandMap = {
    "stat": oa.getCPUStats,
    "balls": lambda: "Command Recognized: Now crushing his balls",
    "stop": opheliaStop,
    }
recognizer = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)