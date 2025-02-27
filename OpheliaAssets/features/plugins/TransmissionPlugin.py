from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__(name="Transmission", prompt="What would you like Ophelia to say or play?", description="Ophelia shall speak Master's message or play the stated sound bite" ,needsArgs=True, modes=["say", "play"])

# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead

    def getModes(self):
        return self.modes

    def getOptions(self, dir=False):
        root_dir = opheNeu.os.path.dirname(opheNeu.os.path.abspath(__file__)) 
        audioDir = opheNeu.os.path.join(root_dir, "..", "..", "assets/sound_bites")  
        if dir: return audioDir
        valid = []
        for file in opheNeu.os.listdir(audioDir):
            filep = opheNeu.os.path.join(audioDir, file)
            if filep.endswith(".wav"): valid.append(file[:-4])
        return valid 

    def audioThroughMic(self, text, isTTS=True, playThroughMic=True, mic_index=opheNeu.micIndex, speaker_index=opheNeu.speakerIndex):
        def playAudio(audio, sample_rate, device):
            opheNeu.sd.play(audio, samplerate=sample_rate, device=device)
            opheNeu.sd.wait() 
        try:
            text = text.lower()
            if isTTS:
                with opheNeu.tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as temp_wav:
                    fileName = temp_wav.name
                opheNeu.engine.save_to_file(text, fileName)
                opheNeu.engine.runAndWait() 
                opheNeu.engine.stop()
                opheNeu.time.sleep(.1)
            else:
                target = text.replace(" ", "")
                audioDir = self.getOptions(dir=True)
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
        except FileNotFoundError: return False
        return True

    def execute(self):
        target = self.prepExecute()
        print(f"Target: {target}")
        self.audioThroughMic(target[0], isTTS=(target[1] == "say"))

    def cheatResult(self, **kwargs): 
        target = kwargs["command"]
        isTTS = target.startswith("say")
        target = target[4:] if isTTS else target[5:] if target.startswith("play") else target
        print(f"Target: {target}")
        output = self.audioThroughMic(target, isTTS=isTTS)
        if not output: return f"Requested {target} not found, please select one of the following: {', '.join(self.getOptions())}. You can also add new .wav files to the assets/sound_bites folder."
        else: return "556036"
def get_plugin():
    return plugin()


