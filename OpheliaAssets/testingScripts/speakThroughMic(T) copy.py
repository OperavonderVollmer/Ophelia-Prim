import pyaudio
import pyttsx3
import time

# Initialize pyttsx3
engine = pyttsx3.init()

# Get available audio devices and find your virtual cable
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

virtual_cable_index = None

for i in range(0, numdevices):
    print(p.get_device_info_by_index(i).get('name'))
    if (p.get_device_info_by_index(i).get('name').startswith("CABLE Input (VB-Audio Virtual C")):
        virtual_cable_index = i
        print(f"Found Virtual Cable at index: {i}")
        break

if virtual_cable_index is None:
    print("Virtual Cable not found. Please make sure it's installed and configured correctly.")
    exit()


# Configure audio stream for output to the virtual cable
CHUNK = 1024  # Adjust chunk size if needed
FORMAT = pyaudio.paInt16  # Adjust format if needed
CHANNELS = 1 # Adjust if your virtual cable is stereo
RATE = 48000  # Adjust sample rate if needed

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK,
                output_device_index=virtual_cable_index) # crucial: specify the output device


def speak_and_stream(text):
    """Speaks the given text and streams the audio to the virtual cable."""

    # Generate speech audio using pyttsx3.  Crucially, get the audio data
    engine.save_to_file(text, "temp.wav") # Save to a temporary file
    engine.runAndWait()  # Needed to ensure the file is completely written


    import wave
    wf = wave.open("temp.wav", 'rb') # Open the file to read
    data = wf.readframes(CHUNK)

    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    wf.close()
    import os
    os.remove("temp.wav") # Clean up

# Example usage:
text_to_speak = "Hello, this is a test message being sent through the virtual cable."
speak_and_stream(text_to_speak)

# Clean up
stream.stop_stream()
stream.close()
p.terminate()

print("Speech streamed to virtual cable successfully.")