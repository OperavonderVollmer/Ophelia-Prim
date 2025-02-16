import pyttsx3
import pyaudio
import numpy as np

def opheliaSpeaksThroughMic(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    
    # Find the virtual audio cable output device
    p = pyaudio.PyAudio()
    selectedMic = "CABLE Input (VB-Audio Virtual Cable)"
    selectedSpeaker = "SteelSeries Sonar - Gaming (SteelSeries Sonar Virtual Audio Device)"
    virtualMicIndex = None
    virtualSpeakerIndex = None
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        if selectedMic in dev_info["name"]:  # Adjust based on your actual device name
            virtualMicIndex = i
        if selectedSpeaker in dev_info["name"]:  # Adjust based on your actual device name
            virtualSpeakerIndex = i
    # Open an audio stream
    virtualMic = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=48000,
                    output=True,
                    output_device_index=virtualMicIndex)
    
    virtualSpeaker = p.open(format=pyaudio.paInt16,
                     channels=8,
                     rate=96000,
                     output=True,
                     output_device_index=virtualSpeakerIndex)
    
    def on_word(name, location, length):
        audio = engine.iterate()
        for chunk in audio:
            audio_data = np.frombuffer(chunk, dtype=np.int16)
            virtualMic.write(audio_data.tobytes())
            #virtualSpeaker.write(audio_data.tobytes())
    
    engine.connect('started-word', on_word)
    engine.say(text)
    engine.runAndWait()
    
    virtualMic.stop_stream()
    virtualMic.close()
    virtualSpeaker.stop_stream()
    virtualSpeaker.close()
    p.terminate()
    
# Example usage
opheliaSpeaksThroughMic("Hello, I am Ophelia.")