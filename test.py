import opheliaNeurals as opheNeu
import opheliaMainFunctions as opheMf
import opheliaAuxilliary as opheAux

def opheliaListen (duration, commandMap):
    while opheNeu.opheliaRequired:
        opheliaHeard = opheliaHears(duration, opheNeu.recognizer)
        if opheliaHeard != "":
            print(f"Detected Input: {opheliaHeard}")
            opheliaHeard = opheliaHeard.lower()
            if opheliaHeard.__contains__("ophelia") or opheliaHeard.__contains__("command"):
                opheMf.opheliaObey(opheliaHeard,commandMap)
            else:
                print("Rambling...")  
            if "cancel" in opheliaHeard:
                opheNeu.opheliaRequired = False      

def opheliaHears(duration, currRecognizer): 
    with opheNeu.sr.Microphone() as source:
        audio = currRecognizer.listen(source, timeout=None if duration <= 0 else duration)
        opheliaHeard = ""
        try:
            opheliaHeard = currRecognizer.recognize_google(audio)
        except opheNeu.sr.RequestError:
            try:
                opheliaHeard = currRecognizer.recognize_sphinx(audio)
            except opheNeu.sr.UnknownValueError:
                opheliaHeard = ("Sorry, Ophelia could not understand the audio.")
            except opheNeu.sr.RequestError as e:
                opheliaHeard = (f"PocketSphinx error; {e}")
        finally:
            return opheliaHeard
        

opheliaListen(0,opheAux.commandMap)
