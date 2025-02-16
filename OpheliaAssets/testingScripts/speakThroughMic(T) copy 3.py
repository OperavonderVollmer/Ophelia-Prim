import time
import pyttsx3
import numpy as np
import sounddevice as sd
import wave
import tempfile
import os

def speak_ophelia(text, mic_index, speaker_index):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    # Create a temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        temp_filename = temp_wav.name

    engine.save_to_file(text, temp_filename)
    engine.runAndWait()  # Ensure audio is saved before continuing

    # Read the saved WAV file
    with wave.open(temp_filename, 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        audio_data = np.frombuffer(wav_file.readframes(wav_file.getnframes()), dtype=np.int16)

    os.remove(temp_filename)  # Delete file after loading audio

    # Play audio on both Virtual Mic and Speaker
    sd.play(audio_data, samplerate=sample_rate, device=speaker_index)
    sd.play(audio_data, samplerate=sample_rate, device=mic_index)
    sd.wait()  # Ensure full playback before continuing

# Example usage
virtual_mic = 10  # Replace with your "CABLE Input" device index
speaker = 17  # Replace with your "SteelSeries Sonar Gaming" device index
speak_ophelia("Hello, I am Ophelia. How can I assist you?", virtual_mic, speaker)
