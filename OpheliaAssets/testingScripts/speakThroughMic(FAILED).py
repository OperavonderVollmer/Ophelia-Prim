import pyttsx3
import pyaudio
import wave

def speak(text):
    engine = pyttsx3.init()

    # Set audio output to virtual cable
    engine.setProperty('voice', 'default')  # Use your preferred voice
    engine.setProperty('rate', 150)  # Adjust speed

    # Speak and save to file simultaneously
    engine.save_to_file(text, "output.wav")
    engine.runAndWait()

    # Play the file through both speakers and virtual mic
    play_audio("output.wav")

def play_audio(file_path):
    # Open the WAV file
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()

    # Open a PyAudio stream for real speakers
    # stream_speaker = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=wf.getframerate(), output=True)

    # Open a PyAudio stream for the virtual microphone
    stream_mic = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)  # No device index
                         # Adjust this if needed

    data = wf.readframes(1024)
    while data:
        #stream_speaker.write(data)  # Send to speakers
        stream_mic.write(data)      # Send to virtual mic
        data = wf.readframes(1024)

    #stream_speaker.stop_stream()
    #stream_speaker.close()
    stream_mic.stop_stream()
    stream_mic.close()
    p.terminate()

speak("Hello, I am Ophelia.")
input("Press Enter to continue...")