

import opheliaNeurals as opheNeu  
def opheliaConversation(text):  
    cancelRecognizer = opheNeu.sr.Recognizer()
    cancelRecognizer.energy_threshold = opheNeu.recognizer.energy_threshold
    mic = opheNeu.sr.Microphone(device_index=1)
    def callback(recognizer, audio):        
        print("[DEBUG] Callback Active")
        try:
            heard=""            
            heard = recognizer.recognize_google(audio)
            if heard.__contains__("cancel"):
                print("CancelMentioned")
                opheliaCancelCommand()
        except Exception: pass

    def opheliaInterrupt():
        opheNeu.opheliaInterrupted = False        
        print("\nOphelia Speaking...")
        print(opheNeu.opheliaInterrupted)
        stopListening = cancelRecognizer.listen_in_background(mic, callback)
        print(opheNeu.opheliaInterrupted)
        print("[DEBUG] Listening started")
        while not opheNeu.opheliaInterrupted:
            opheNeu.time.sleep(0.25)
            print("----Listening...")
            print(opheNeu.opheliaInterrupted)
        print("[DEBUG] Stopping listening")
        print(opheNeu.opheliaInterrupted)
        if opheNeu.opheliaInterrupted:
            stopListening(wait_for_stop=False)
        print("Killing Thread")

    cancelThread = opheNeu.thr.Thread(target=opheliaInterrupt)
    cancelThread.start()
    opheliaSpeak(text)
    
    opheNeu.opheliaInterrupted = True
    cancelThread.join()

def opheliaSpeak(text):
    opheNeu.engine.say(text=text)
    opheNeu.engine.runAndWait()

opheliaSpeak("Hello world")

def opheliaListen (duration, commandMap):
    while opheNeu.opheliaRequired:
        opheliaHeard = opheliaHears(duration)
        if opheliaHeard != "":
            print(f"Detected Input: {opheliaHeard}")
            if opheliaHeard.__contains__("ophelia") or opheliaHeard.__contains__("command"):
                opheliaObey(opheliaHeard,commandMap)
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
                opheliaSpeak(f"PocketSphinx error; {e}")     
        except opheNeu.sr.UnknownValueError:
            opheliaHeard = ""
        finally: return opheliaHeard   

def opheliaCareKit():
    return "Command Recognized: Unfortunately, this feature hasn't been implemented yet"

def opheliaObey(command, commandMap):
    if command.__contains__("command"):
        try:
            for keyword, response in commandMap.items():
                if keyword in command:
                    print(f"Command Recognized: {str(keyword)}")    
                    opheliaSpeak(f"{response(keyword) if callable(response) else response}")
        except Exception as e:
            print(e)
            return(f"Command cannot be executed")
    elif command.__contains__("ophelia"):
        opheliaSpeak(opheliaCareKit())
    
def opheliaCancelCommand():
    print("Cancelling command")
    opheNeu.opheliaInterrupted=True
    opheNeu.engine.stop()