import opheliaNeurals as opheNeu

def opheliaHears(timeout=None, currRecognizer=opheNeu.recognizer, timed=False):
    opheliaHeard = None    
    def callback(recognizer, audio):
        nonlocal opheliaHeard
        try:
            opheliaHeard = recognizer.recognize_google(audio).lower()
        except opheNeu.sr.UnknownValueError:             
            try:
                opheliaHeard = recognizer.recognize_sphinx(audio).lower()
            except opheNeu.sr.UnknownValueError:
                opheliaHeard = None
                opheNeu.debug_log("Could not understand audio, didn't return anything to prevent confusion")
            except opheNeu.sr.RequestError:
                pass
        except opheNeu.sr.RequestError as e:
            opheliaHeard = None
            opheNeu.debug_log(f"Recognition error: {e}, didn't return anything to prevent confusion")
    opheNeu.debug_log("Listening for user input...")

    mic = opheNeu.sr.Microphone()

    print("Started Listening")
    if timed:
        with mic as source:
            opheliaHeard = currRecognizer.listen(source, timeout=timeout)
            return opheliaHeard if opheliaHeard else None
        
    stop_listening = currRecognizer.listen_in_background(mic, callback, phrase_time_limit=timeout)
    while not opheliaHeard and opheNeu.opheliaRequired:
        opheNeu.time.sleep(0.05)
        if opheNeu.cheatWord: opheliaHeard = opheNeu.cheatWord; opheNeu.cheatWord = None
            
    stop_listening(wait_for_stop=False) 
    print("Stopped Listening")
    return opheliaHeard