from TTS.api import TTS


# Replace with the paths to your model and config files
model_path = "./RioVoice/model.pth"

# Initialize the TTS model
tts = TTS(model_name=model_path)
text = "Hello, this is a test using my custom model."

# Synthesize speech and save to a file
tts.synthesize(text=text, output_path='./output/output.wav')
