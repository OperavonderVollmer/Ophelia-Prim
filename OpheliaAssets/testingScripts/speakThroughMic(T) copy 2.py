import pyttsx3
import pyaudio
import sounddevice as sd
import numpy as np
import wave
import os

def opheliaSpeaksThroughMic(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    p = pyaudio.PyAudio()

    # Find devices (more robust)
    mic_index = None
    speaker_index = None
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        if "CABLE Input (VB-Audio Virtual Cable)" in dev_info["name"] and dev_info["maxOutputChannels"] > 0:
            mic_index = i
        if "SteelSeries Sonar - Gaming (SteelSeries Sonar Virtual Audio Device)" in dev_info["name"] and dev_info["maxOutputChannels"] > 0: # Check the actual name!
            speaker_index = i

    if mic_index is None or speaker_index is None:
        print("Virtual Cable or Speaker not found!")
        return

    # Consistent audio parameters (crucial!)
    sample_rate = 48000  # Or 48000, but be consistent!
    channels = 1        # Mono for simplicity (start with mono)

    # 1. Generate speech audio (using WAV file)
    engine.save_to_file(text, "temp.wav")
    engine.runAndWait()

    wf = wave.open("temp.wav", 'rb')
    n_frames = wf.getnframes()
    speech_audio = wf.readframes(n_frames)
    speech_data = np.frombuffer(speech_audio, dtype=np.int16)
    wf.close()
    os.remove("temp.wav")

    # 2. Microphone stream (using sounddevice)
    #try:
    with sd.InputStream(samplerate=sample_rate, channels=channels, dtype='int16') as mic_stream:  # Use sounddevice
        # 3. Output stream (using pyaudio)
        with p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    output=True,
                    output_device_index=mic_index) as out_stream:

            # 4. Mixing loop (read from mic, mix with speech, write to output)
            speech_index = 0
            chunk_size = 1024  # Adjust as needed

            for _ in range(0, int(n_frames / chunk_size) + 1):  # Loop through speech chunks
                mic_data, overflowed = mic_stream.read(chunk_size)  # Read from microphone (sounddevice)

                if overflowed:
                    print("Mic input overflowed!") # Handle overflow if needed

                if speech_index < len(speech_data):  # Check if there's speech data left
                    speech_chunk = speech_data[speech_index:speech_index + chunk_size]
                    speech_index += chunk_size
                else:
                    speech_chunk = np.zeros(chunk_size, dtype=np.int16)  # Pad with zeros if speech is finished

                # Mix the audio (adjust volume as needed)
                mixed_data = mic_data + speech_chunk * 0.5  # Adjust 0.5 for speech volume

                out_stream.write(mixed_data.tobytes())  # Write mixed data to output stream

    #except Exception as e:
        #print(f"Error: {e}")

    p.terminate()

# Example usage
opheliaSpeaksThroughMic("Hello, I am Ophelia.")