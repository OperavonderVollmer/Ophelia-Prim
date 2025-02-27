import subprocess, time, os, psutil, json, random, threading, uuid
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, IAudioSessionManager2, IAudioSessionControl
from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu
from functions.opheliaAsync import async_to_sync, async_to_sync_params

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__("Jukebox", "Which jukebox command?", description="Ophelia will play music for Master", needsArgs=True, modes=[
            "start", "stop", "pause", "volume", "add", "peep", "next", "previous", "repeat", "shuffle", "linecut", "pulltheplug", "discord", "search"
            ])
        self.isRunning = False
        self.isPlaying = False
        self.isRepeat = 0 #isRepeat 0 = no repeat, 1 = repeat playlist, 2 = repeat song 
        self.currentSongIndex = 0
        self.currentPlaybackID = None
        self.volume = 100
        self.jukebox = []
        self.process = None
        self.ffplay_process = None
        self.isDiscord = True

    def getModes(self):
        return self.modes
    
    def getOptions(self, dir=False):
        valid = ["start", "stop", "pause", "next", "previous", "repeat", "shuffle", "pulltheplug"]
        return valid 

    def getSongInfo(self, url: str):
        def formatTime(seconds):
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes}:{seconds:02d}"

        try:
            result = subprocess.run(
                ["yt-dlp", "--ignore-config", "--dump-json", url],
                capture_output=True,
                text=True
            )
            video_info = json.loads(result.stdout)
            return {
                "title": video_info.get("title", "Unknown Title"),
                "uploader": video_info.get("artist", video_info.get("uploader", "Unknown Uploader")),
                "duration": formatTime(video_info.get("duration", 0)),
                "url": url,
            }
        except Exception as e:
            print(f"Error fetching video info: {e}")
            return None

    def playSong(self, **kwargs):
        song = kwargs["command"]
        senderInfo = kwargs.get("senderInfo", None)
        print(f"Trying to play {song['title']}")
        o = (f"Playing: {song['title']} by {song['uploader']} ({song['duration']})")
        print("IN WE GOOOOOO")
        if self.isDiscord:                
            try:
                from functions.opheliaDiscord import discordLoop
                from functions.opheliaDiscordJukebox import startMusicStream

                if senderInfo is not None and senderInfo["vcChannel"] == None: return "You need to be in a voice channel to use this command."
                print("I KNOW IM BAD")
                async_to_sync_params(startMusicStream, discordLoop, senderInfo=senderInfo, song=song["url"], outputMessage=o)
                print("GIVE IT SOME TIME")
                return o
            except Exception as e: return (f"Error occured trying to play through discord: {e}")
        def _monitorPlayback(playbackID = None, senderInfo = None):
            """Waits for the song to finish playing, then calls nextSong()."""
            try:
                while self.ffplay_process.poll() is None:
                    if not self.isRunning: return
                    if playbackID != self.currentPlaybackID: return
                    time.sleep(1)
                if playbackID == self.currentPlaybackID:
                    self.nextSong(senderInfo=senderInfo)
            except AttributeError: print("Song stopped.")

        if not self.isRunning:
            return ("The jukebox isn't running.")
        if self.isPlaying: self.stopSong(command=False)
        try:
            self.isPlaying = True
            newID = uuid.uuid4()
            self.currentPlaybackID = newID  # Generate a unique ID for this playback session

            self.process = subprocess.Popen(
                ["yt-dlp", "--ignore-config", "-f", "bestaudio", "-o", "-", song["url"]],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL
            )
            '"-volume", str(self.volume),'
            self.ffplay_process = subprocess.Popen(
                ["ffplay", "-nodisp", "-autoexit",  "-"],
                stdin=self.process.stdout,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # Start a separate thread to monitor song completion
            threading.Thread(target=_monitorPlayback, kwargs={"playbackID":newID, "senderInfo":senderInfo}, daemon=True).start()
            return(o)

        except FileNotFoundError:
            print("Error: Make sure yt-dlp and ffplay are installed.")
        except Exception as e:
            return(f"An error occurred trying to play locally: {e}")
        

    

    def pauseSong(self, **kwargs):
        from functions.opheliaDiscordJukebox import pauseMusicStream
        from functions.opheliaDiscord import discordLoop
        if self.isDiscord:
            async_to_sync_params(pauseMusicStream, discordLoop, senderInfo = kwargs["senderInfo"])
            return "Pausing/unpausing song..."

        if not self.isRunning:
            return("The jukebox isn't playing anything.")
        
        if self.ffplay_process and self.isPlaying:
            try:
                p = psutil.Process(self.ffplay_process.pid)
                p.suspend()
                self.isPlaying = False
            except Exception as e:
                print(f"Error pausing: {e}")
            return("Pausing song...")
        elif self.ffplay_process and not self.isPlaying:
            try:
                p = psutil.Process(self.ffplay_process.pid)
                p.resume()
                self.isPlaying = True
            except Exception as e:
                print(f"Error resuming: {e}")
            return("Unpausing song...")

    def stopSong(self, **kwargs):
        fullStop = bool(kwargs["command"])
        if self.isDiscord:
            from functions.opheliaDiscordJukebox import stopMusicStream
            from functions.opheliaDiscord import discordLoop
            async_to_sync_params(stopMusicStream, discordLoop, senderInfo = kwargs["senderInfo"])
            return "Stopping song..."
        
        if not self.isPlaying: return ("No song is playing.")

        for attr in ["process", "ffplay_process"]:  
            p = getattr(self, attr)
            if p:
                p.terminate()
                try:
                    p.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    p.kill()
                setattr(self, attr, None) 
        self.isPlaying = False
        if fullStop: self.isRunning = False; self.currentSongIndex = 0
        return("Song stopped.")

    def volumeControl(self, **kwargs):
        if self.isDiscord:
            return "Jukebox on discord doesn't support volume control."
        try:
            newVolume = int(kwargs["command"])
            if newVolume < 0 or newVolume > 100: raise ValueError
        except (ValueError, TypeError):
            return ("Volume must be an integer between 0 and 100")         
        if not self.isRunning:
            return("Jukebox is not playing")
        try:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                if session.Process and session.Process.name() == "ffplay.exe":
                    volume = session.SimpleAudioVolume
                    volume.SetMasterVolume(newVolume / 100.0, None)
                    return(f"Volume for ffplay.exe set to {newVolume}%")
            return("Could not find ffplay.exe in the volume mixer.")
        except Exception as e:
            return(f"Error adjusting volume: {e}")

    def nextSong(self, **kwargs):
        print("Playing next song...")
        self.currentSongIndex += 1
        if self.currentSongIndex >= len(self.jukebox):
            if self.isRepeat == 1:
                self.currentSongIndex = 0
            elif self.isRepeat == 0:
                self.stopSong(command=True, senderInfo = kwargs.get("senderInfo", None))
                return  ("Reached the end of the playlist")
        if 0 <= self.currentSongIndex < len(self.jukebox): 
            x = self.playSong(command = self.jukebox[self.currentSongIndex], senderInfo = kwargs.get("senderInfo", None))
            if kwargs.get("end", False): return
            else : return x
    
    def previousSong(self, **kwargs):
        if self.currentSongIndex > 0: self.currentSongIndex -= 1
        if 0 <= self.currentSongIndex < len(self.jukebox): return self.playSong(command = self.jukebox[self.currentSongIndex], senderInfo = kwargs.get("senderInfo", None))

    def repeatSong(self, **kwargs):
        if self.isRepeat == 2: self.isRepeat = 0
        else: self.isRepeat += 1
        repeat = {0: "No repeat", 1: "Repeat playlist", 2: "Repeat song"}
        return (f"Repeat mode set to {repeat[self.isRepeat]}")

    def dropTheNeedle(self, **kwargs):
        self.isRunning = True
        self.currentSongIndex = 0
        if len(self.jukebox) > 0:
            currentSong = self.jukebox[self.currentSongIndex]
            return self.playSong(command = currentSong, senderInfo = kwargs["senderInfo"])
        else: return("Jukebox is empty")

    def insertCoin(self, **kwargs):
        """Adds a single video or an entire playlist to the jukebox."""
        
        # Detect if the URL is a playlist
        url = str(kwargs["command"])
        print(f"Adding {url} to jukebox...")
        try:
            result = subprocess.run(
                ["yt-dlp", "--flat-playlist", "--print", "url", url],
                capture_output=True,
                text=True,
                check=True
            )
            video_urls = result.stdout.strip().split("\n")
            outputMessage = []
            if len(video_urls) > 1:
                print(f"Adding {len(video_urls)} songs from playlist to jukebox...")
                for video_url in video_urls:
                    song = self.getSongInfo(video_url)
                    if song:
                        self.jukebox.append(song)
                        o = (f"Added '{song['title']}' to jukebox")
                        print (o)
                        outputMessage.append(o)
            else:
                song = self.getSongInfo(url)
                if song:
                    self.jukebox.append(song)
                    outputMessage = f"Added '{song['title']}' to jukebox"

        except Exception as e:
            return(f"Error adding playlist: {e}")
        peep = self.peepJukebox(**kwargs)
        if isinstance(outputMessage, list): return('\n'.join(outputMessage) + "\n" + peep)
        return(outputMessage + "\n" + peep)

    def peepJukebox(self, **kwargs):
        if len(self.jukebox) == 0: return "Jukebox is empty"
        peep = []
        for i, song in enumerate(self.jukebox, 0):
            star = "* " if i == self.currentSongIndex else ""
            peep.append(f"{star}Song #{i + 1}. '{song['title']}' by {song['uploader']} ({song['duration']})")

        if kwargs["command"] == "secret": return peep
        return "Jukebox:\n-------------------------------\n" + "\n".join(peep)
    
    def pullThePlug(self,**kwargs):
        self.jukebox = []
        self.stopSong(command=True, senderInfo = kwargs["senderInfo"])
        return "Jukebox has been emptied and turned off"

    def shuffleCards(self, **kwargs):
        if len(self.jukebox) < 1: return ("Jukebox is empty")

        current_song = self.jukebox[self.currentSongIndex]  # Keep track of the current song
        random.shuffle(self.jukebox)  # Shuffle the list
        new_index = self.jukebox.index(current_song)
        self.currentSongIndex = new_index
        return("Shuffled Jukebox:\n" + self.peepJukebox())

    def lineCut(self, **kwargs):      # LineCut is a command to cut a song in the playlist and start a new playlist from that song.

        try:
            index = int(kwargs["command"]) - 1
            if 0 <= index < len(self.jukebox):
                self.currentSongIndex = index
                return self.playSong(command = self.jukebox[self.currentSongIndex], senderInfo = kwargs["senderInfo"])
            else: return("Index out of range")
        except (ValueError, TypeError, IndexError):
            return (f"Index must be an integer between 1 and {len(self.jukebox)}") 
        
    def songBook(self, **kwargs): 
        searchSong = kwargs["command"]
        try:
            result = subprocess.run(
                ["yt-dlp", "--flat-playlist", "--print", "%(title)s %(webpage_url)s", "ytsearch:" + searchSong],
                capture_output=True,
                text=True,
                check=True
            )
            song = self.getSongInfo(result.stdout.split()[-1])
            if song:
                self.jukebox.append(song)
                return(f"Added '{song['title']}' to jukebox")
        except Exception as e:
            return(f"Error adding song: {e}")

    def discordOn(self, **kwargs):
        self.isDiscord = not self.isDiscord
        return (f"Discord use is now {self.isDiscord}")

# voice commands
# command jukebox control start, stop, stop, pause, volume, next, previous, repeat, shuffle, peep, linecut, pull the plug,
# non voice command
# all and add

# uses an array as parameter
# [target,mode]
# should be able to take null target as param
    def jukeboxControls(self, **kwargs):
        controls = {
            "start": self.dropTheNeedle,
            "stop": self.stopSong,
            "pause": self.pauseSong,
            "volume": self.volumeControl,
            "next": self.nextSong,
            "previous": self.previousSong,
            "repeat": self.repeatSong,
            "shuffle": self.shuffleCards,
            "peep": self.peepJukebox,
            "linecut": self.lineCut,
            "add": self.insertCoin,
            "pulltheplug": self.pullThePlug,
            "discord": self.discordOn,
            "search": self.songBook
        }
        #try:
        if kwargs["mode"] == "help": raise Exception
        print(kwargs["mode"] + " " + kwargs["command"])
        return controls[kwargs["mode"]](command = kwargs["command"], senderInfo = kwargs["senderInfo"])
        """except Exception as e:
            opheNeu.debug_log(f"Jukebox Error {e}")
            return(f"Jukebox command not recognized. Available commands: {', '.join(controls.keys())}.")"""


    def execute(self):
        t = self.prepExecute()
        opheNeu.debug_log(f"Target is '{t[1]}' and mode is '{t[0]}'")
        if "add" in t: return "Add song is not supported for voice commands, please insert using Discord"
        return self.jukeboxControls(command = t[0], mode = t[1])

    def cheatResult(self, **kwargs):    
        t = kwargs["command"]    
        for mode in self.modes:
            if t.__contains__(mode):
                t = t.replace(mode, "").replace(" ", "")
                opheNeu.debug_log(f"Target is '{t}' and mode is '{mode}'")
                return self.jukeboxControls(command = t, mode = mode, senderInfo = kwargs["senderInfo"])
        return self.jukeboxControls([t, "help"])

def get_plugin():
    print("Initializing Jukebox...")
    return plugin()

