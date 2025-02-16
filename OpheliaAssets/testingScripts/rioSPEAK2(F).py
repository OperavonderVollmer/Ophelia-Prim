from TTS.tts.configs.shared_configs import BaseTTSConfig
from TTS.tts.models import setup_model
import torch
import simpleaudio as sa
import os

# Path to your extracted model files
model_path = "./RioVoice/model.pth"

def load_model():
    config = BaseTTSConfig().load_json("./RioVoice/model.json")
    model = setup_model(config, model_path)
    #model.load_checkpoint(config, checkpoint_path=model_path, eval=True)
    model.to(torch.device("cpu"))  # Change to "cuda" if using GPU
    return model

def speak(text):
    model = load_model()
    output_wav = "output.wav"

    # Generate speech
    model.synthesize(text, output_wav)

    # Play the generated audio
    wave_obj = sa.WaveObject.from_wave_file(output_wav)
    wave_obj.play().wait_done()

speak("Hello, I am Ophelia.")
