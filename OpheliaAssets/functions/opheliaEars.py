import opheliaNeurals as opheNeu

def opheliaListens(timeout=None):
    while opheNeu.opheliaRequired:
        opheliaHeard = opheliaHears(timeout)
        if opheliaHeard:
            opheNeu.debug_log(f"Detected Input: {opheliaHeard}")
            if "ophelia" in opheliaHeard or "command" in opheliaHeard:
                # opheliaObey(opheliaHeard, commandMap)
                print("Ophelia has heard a command")
            else:
                print("Rambling...")

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
    
    while not opheliaHeard:
        opheNeu.time.sleep(0.1)
    
    stop_listening(wait_for_stop=True) 
    return opheliaHeard

def testFunction():
    print("What would you like to eat?")
    selection = opheliaHears()
    print("You selected: " + selection)

opheNeu.debug_log("opheliaListens test")
opheliaListens()
