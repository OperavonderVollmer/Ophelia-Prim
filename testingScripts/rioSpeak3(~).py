import os
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts


model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'RioVoice'))
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'RioVoice', 'model.json'))
output_dir = "./output/"
output_path = "./output/output.wav"

print("Loading model...")
config = XttsConfig()
config.load_json(model_path + "/model.json")
model = Xtts.init_from_config(config)
#model.load_checkpoint(config, checkpoint_dir=model_path, use_deepspeed=False)
model.cpu()

print("Computing speaker latents...")
gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=[model_path + "/Rio - Night Dancer.wav"])

print("Inference...")
out = model.inference(
    "It took me quite a long time to develop a voice and now that I have it I am not going to be silent.",
    "en",
    gpt_cond_latent,
    speaker_embedding,
    temperature=0.7, # Add custom parameters here
)
torchaudio.save("xtts.wav", torch.tensor(out["wav"]).unsqueeze(0), 24000)