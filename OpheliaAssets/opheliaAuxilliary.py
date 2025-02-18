import opheliaNeurals as opheNeu

def getWikipediaSummary(t, sentences=4):
    topic = t
    wiki = opheNeu.wikipediaapi.Wikipedia(user_agent="Opera operavgxgamer@gmail.com", language="en")  # English Wikipedia API

    def summarize(text, sentences):
        parser = opheNeu.PlaintextParser.from_string(text, opheNeu.Tokenizer("english"))
        summarizer = opheNeu.LuhnSummarizer()
        summary = summarizer(parser.document, sentences)
        return " ".join([str(sentence) for sentence in summary])

    try:
        # Try getting the page directly
        page = wiki.page(topic)
        if page.exists(): return summarize(page.summary, sentences)
        # If page doesn't exist, fall back to search results
        search_results = opheNeu.wikipedia.search(topic)
        if search_results:
            best_match = search_results[0]  # Take the first search result
            page = wiki.page(best_match)
            if page.exists():
                print(page)
                return f"I found multiple results. Here's information about {best_match}: " + summarize(page.text, sentences)
            else:
                return "I couldn't find anything on Wikipedia about that topic."

    except opheNeu.wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:5]  # Show only the first 5 options
        return f"'{topic}' is ambiguous. Did you mean: {', '.join(options)}?"
    except opheNeu.wikipedia.exceptions.PageError:
        return "I couldn't find anything on Wikipedia about that topic."
    except Exception as e:
        return f"An error occurred: {str(e)}"
def getWeather(showLogs="True", city=opheNeu.city):
    url = f"https://wttr.in/{city}?format=j1"
    response = opheNeu.requests.get(url)
    if response.status_code == 200:
        data = response.json()
        current_time = opheNeu.datetime.now().hour * 100  # Get current hour in 24-hour format (e.g., 3 AM -> 300)
        noOfForecasts = 4
        forecast = data["weather"][0]["hourly"]
        upcoming_forecast = [
            hour for hour in forecast if int(hour["time"]) >= current_time
        ][:noOfForecasts]  # Get the next 12 hours (4 forecasts, as data is in 3-hour intervals)
        forecast_strings = []
        for hour in upcoming_forecast:
            time_str = f"{int(hour['time']) // 100}:00"  # Convert 2400 format to readable format
            description = hour["weatherDesc"][0]["value"]
            temperature = hour["tempC"]
            forecast_strings.append(f"At {time_str}, it will be {description} with a temperature of {temperature}°C.")
        current_date = opheNeu.datetime.now().strftime("%B %d, %Y")
        output = f"The day is currently {current_date}. This is the weather forecast for {city} for the next 12 hours:\n" + "\n".join(forecast_strings) +"\nThis concludes the weather forecast."
        if showLogs: print(output) 
        return output
    else: return "Unfortunately, Could not fetch weather data."
def getCPUStats(t):    
    cpu_usage = opheNeu.psutil.cpu_percent(interval=1)
    ram = opheNeu.psutil.virtual_memory()
    ram_available = (f"{ram.available / (1024 ** 3):.2f} GB")
    ram_usage = (f"{ram.percent}%")
    try:
        cpu_temp = (f"{(opheNeu.computer.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature / 10) - 273.15:.2f}°C")
    except:
        cpu_temp = "Currently Unavailable"
    text = (f"CPU Usage: {cpu_usage}%\nRAM Usage: {ram_usage}\nRAM Available: {ram_available}\nCPU Temperature: {cpu_temp}")
    print(text)
    return text
def opheliaSleep(t):    
    audioThroughMic(opheNeu.getRandomDialogue("farewells"), True, False)
    opheNeu.opheliaRequired = False
    return ""
def openApp(t):
    target = t
    root_dir = opheNeu.os.path.dirname(opheNeu.os.path.abspath(__file__)) 
    shortcutDir = opheNeu.os.path.join(root_dir, "assets/shortcuts")  
    shortcutPath = opheNeu.os.path.join(shortcutDir, target)
    shortcutPath += ".lnk"
    for app in opheNeu.os.listdir(shortcutDir):
        if app.lower() == target+".lnk":
            try:
                opheNeu.subprocess.Popen([shortcutPath], shell=True)  
                return(f"Opening {target}...")
            except Exception as e: print(f"An error occurred: {str(e)}")
    else:
        return(f"Shortcut '{target}' not found. Is the {target} shortcut in shortcuts folder?")   
def playAudio(audio, sample_rate, device):
        opheNeu.sd.play(audio, samplerate=sample_rate, device=device)
        opheNeu.sd.wait() 
def audioThroughMic(text, isTTS=True, playThroughMic=True, mic_index=opheNeu.micIndex, speaker_index=opheNeu.speakerIndex):
    if isTTS:
        with opheNeu.tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as temp_wav:
            fileName = temp_wav.name
        opheNeu.engine.save_to_file(text, fileName)
        opheNeu.engine.runAndWait() 
    else:
        target = text.replace(" ", "")
        root_dir = opheNeu.os.path.dirname(opheNeu.os.path.abspath(__file__)) 
        audioDir = opheNeu.os.path.join(root_dir, "assets/sound_bites")  
        audioPath = opheNeu.os.path.join(audioDir, target)
        fileName = audioPath + ".wav"
    with opheNeu.wave.open(fileName, 'rb') as wav_file:
            sample_rate = wav_file.getframerate()
            audio_data = opheNeu.np.frombuffer(wav_file.readframes(wav_file.getnframes()), dtype=opheNeu.np.int16)
    if not isTTS: 
        audio = opheNeu.AudioSegment.from_file(fileName)
        bitrate = (audio.frame_rate * audio.frame_width * 8)
        #bitrate_kbps = bitrate / 1000 
        #sample_rate = (bitrate_kbps * 96000) / 1536   # will change if it becomes a problem   
        sample_rate = (96000)                          # will change if it becomes a problem   
    #else: opheNeu.os.remove(fileName)     

    threads = [opheNeu.thr.Thread(target=playAudio, args=(audio_data, sample_rate, speaker_index))]
    if playThroughMic: threads.append(opheNeu.thr.Thread(target=playAudio, args=(audio_data, sample_rate, mic_index)))
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    return ""
def postureCheckSetup(t):
    try:
        def normalizeNumber(t):
            try:
                if isinstance(t, str):
                    t = t.strip().lower()
                    if t.isdigit():
                        return int(t)
                    return opheNeu.w2n.word_to_num(t)
                elif isinstance(t, bool): return opheNeu.defaultPostureInterval
                else: return t        
            except ValueError: raise
        t = normalizeNumber(t)
        if t:
            interval = t
            with open(opheNeu.postureCheckFile, "w") as postFile:
                postFile.write(str(interval))  
            opheNeu.postureCheckActive = True 
            postureCheckWrapped()         
            return f"Posture check is set to {interval} minutes."
        else:
            opheNeu.os.remove(opheNeu.postureCheckFile) if opheNeu.postureCheckActive else None
            opheNeu.postureCheckActive = False
            return "Posture check deactivated"
    except ValueError: return "Please provide a valid number of minutes"
def postureCheckWrapped():
    def postureCheck():
        def postureCheckLoopMethod():          
            opheNeu.postureLooping = True
            try:  
                with open(opheNeu.postureCheckFile, "r") as postFile:
                    interval = int(postFile.read())
                    print(f"interval {interval}")
            except FileNotFoundError: 
                return "Posture check is currently inactive"            
            opheNeu.debug_log("Posture check loop started")
            checks = 12
            sleep = 5                       # no of checks * sleep MUST equal 60    
            totalChecks = interval * checks   
            opheNeu.debug_log(f"Total Checks {totalChecks}")             
            while opheNeu.postureCheckActive:            
                c = 1
                for _ in range(totalChecks):
                    if not opheNeu.postureCheckActive or not opheNeu.opheliaRequired:
                        opheNeu.debug_log("Posture check deactivated due to posture check being deactivated")
                        return True
                    if opheNeu.deepDebugMode: opheNeu.debug_log(f"Debug message within the posture loop #{c}")
                    c+=1
                    opheNeu.time.sleep(sleep)
                    
                audioThroughMic(opheNeu.getRandomDialogue("posture"), True, False)
                print(f"Playing posture audio {opheNeu.datetime.now()}")
            opheNeu.debug_log("Posture check deactivated due to posture duration being over")

        if not opheNeu.postureLooping and opheNeu.postureCheckActive: 
            postureLoop = opheNeu.thr.Thread(target=postureCheckLoopMethod, daemon=True)
            postureLoop.start()
            postureLoop.join()
            return
        else: return "Posture check is already active"
    postureThread = opheNeu.thr.Thread(target=postureCheck)
    print(f"Posture check starting at {opheNeu.datetime.now()}...")
    postureThread.start()


def speakDialogue(t="general"):
    try:
        return opheNeu.getRandomDialogue(t)
    except: return f"Ophelia does not have that category {opheNeu.getRandomDialogue('errors')}" 

