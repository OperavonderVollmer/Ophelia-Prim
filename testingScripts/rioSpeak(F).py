import torch
from TTS.api import TTS
import gradio as gr

#unused for now
# rioVoice = TTS(model_name='TokiBotan/TsukatsukiRio_RVCV2')

#checks if GPU is cuda compatible
device = "cuda" if torch.cuda.is_available() else "cpu"

def speak(speak="Hello, I am Ophelia."):
    tts = TTS(model_name='tts_models/it/mai_female/vits').to(device)
    tts.tts_to_file(text=speak,file_path='../output/output.wav')
    return '../output/output.wav' 

print(speak())