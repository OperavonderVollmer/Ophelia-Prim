from functions import opheliaObey
import opheliaNeurals as opheNeu

def opheliaListens(timeout=None, commandMap=None):
    opheNeu.debug_log("Ophelia is now listening...")
    while opheNeu.opheliaRequired:
        opheliaHeard = opheliaHears(timeout)
        if opheliaHeard:
            if "ophelia" in opheliaHeard or "command" in opheliaHeard:
                opheliaObey.opheliaDo(opheliaHeard, commandMap)
                opheNeu.debug_log("Ophelia has heard a command")
            else: print("Rambling... " + opheNeu.random.choice(opheNeu.misc["emojis"])) 
        

def opheliaHears(timeout=None, currRecognizer=opheNeu.recognizer):
    opheliaHeard = None    
    def callback(currRecognizer, audio):
        nonlocal opheliaHeard
        try:
            opheliaHeard = currRecognizer.recognize_google(audio).lower()
            opheNeu.debug_log(f"Detected Input: {opheliaHeard}")
        except opheNeu.sr.UnknownValueError:             
            try:
                opheliaHeard = currRecognizer.recognize_sphinx(audio).lower()
                opheNeu.debug_log(f"Detected Input: {opheliaHeard}")
            except opheNeu.sr.UnknownValueError:
                opheliaHeard = None
                opheNeu.debug_log("Could not understand audio, didn't return anything to prevent confusion")
            except opheNeu.sr.RequestError:
                pass
        except opheNeu.sr.RequestError as e:
            opheliaHeard = None
            opheNeu.debug_log(f"Recognition error: {e}, didn't return anything to prevent confusion")
    opheNeu.debug_log("Listening for user input...")
    stop_listening = currRecognizer.listen_in_background(opheNeu.mic, callback, phrase_time_limit=timeout)
    while not opheliaHeard and opheNeu.opheliaRequired:
        opheNeu.time.sleep(0.05)
        if opheNeu.cheatWord: opheliaHeard = opheNeu.cheatWord; opheNeu.cheatWord = None; pass
    stop_listening(wait_for_stop=True) 
    return opheliaHeard


#--------------------------------------------------------#

def depreciatedOpheliaEars():
    def opheliaListens (duration, commandMap):
        while opheNeu.opheliaRequired:
            opheliaHeard = opheliaHears(duration)
            if opheliaHeard != "":
                print(f"Detected Input: {opheliaHeard}")
                if opheliaHeard.__contains__("ophelia") or opheliaHeard.__contains__("command"):
                    # opheliaObey(opheliaHeard,commandMap)
                    pass
                else:
                    print("Rambling...")        

    def opheliaHears(duration, currRecognizer=opheNeu.recognizer): 
        with opheNeu.sr.Microphone(device_index=1) as source:
            audio = currRecognizer.listen(source, timeout=None if duration <= 0 else duration)
            opheliaHeard = ""
            try:
                opheliaHeard = currRecognizer.recognize_google(audio)
                return opheliaHeard
            except opheNeu.sr.RequestError:
                try:
                    opheliaHeard = currRecognizer.recognize_sphinx(audio)
                    return opheliaHeard
                except opheNeu.sr.UnknownValueError:
                    opheliaHeard = ""
                except opheNeu.sr.RequestError as e:
                    # opheliaSpeak(f"PocketSphinx error; {e}")  
                    pass   
            except opheNeu.sr.UnknownValueError:
                opheliaHeard = ""
            finally: return opheliaHeard   
