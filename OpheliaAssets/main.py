#import opheliaWake as opheWake
#import opheliaBridge as opheBri
#from opheliaPlugins import plugins


#--------------------------------------------------------#
#opheWake.opheliaBegin(not opheNeu.debugMode)
#opheWake.opheliaBegin(onStartBool=False)
#opheWake.opheliaBegin(onStartBool=True)
#opheWake.opheliaBegin(onStartBool=False, quickstart=True)

#--------------------------------------------------------#


import subprocess


def stream_youtube_audio(url: str):
    """
    Streams audio from a YouTube URL using yt-dlp and ffplay.
    
    :param url: The YouTube video URL
    """
    try:
        process = subprocess.Popen(
            ["yt-dlp", "--ignore-config", "-f", "bestaudio", "-o", "-", url],
            stdout=subprocess.PIPE,
        )        
        ffplay_process = subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "-"],
            stdin=process.stdout,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        
        ffplay_process.wait()
    except FileNotFoundError:
        print("Error: Make sure yt-dlp and ffplay are installed and in your system's PATH.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    video_url = input("Enter YouTube URL: ")
    stream_youtube_audio(video_url)

