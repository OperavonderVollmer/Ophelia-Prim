import opheliaNeurals as opheNeu

# I haven't figured this part out
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
                # opheliaCancelCommand()
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

def opheliaSpeak(text, engine=opheNeu.engine, wait=True):
    p = f"Ophelia says: {text}"
    print(p)
    opheNeu.debug_log(p, speakLog = True)
    if text: 
        engine.say(text=text)
        if wait: 
            engine.runAndWait()
            engine.stop()
        else: 
            engine.startLoop()
            engine.iterate()