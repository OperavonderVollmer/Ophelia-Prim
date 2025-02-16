import speech_recognition as sr
import pyttsx3
import threading

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Function to handle speech recognition in the background
def listen_for_cancel():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for 'cancel' command...")
        while True:
            try:
                audio = recognizer.listen(source, timeout=1)
                command = recognizer.recognize_google(audio).lower()
                if "cancel" in command:
                    print("'Cancel' command detected.")
                    try:
                        tts_engine.endLoop()
                    except: pass  # Stop speech immediately                    
                    break
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                break

# Function to speak the provided text
def speak_text(text):
    tts_engine.say(text)
    tts_engine.startLoop()  # Start the event loop
    try:
        tts_engine.endLoop()
    except: pass

# Main function to manage speaking and listening
def speak_with_cancel(text):
    # Start the listening thread
    listener_thread = threading.Thread(target=listen_for_cancel)
    listener_thread.start()
    print(tts_engine.isBusy())
    # Speak the text
    speak_text(text)
    print("This code reached")
    print(tts_engine.isBusy())
    # Wait for the listener thread to finish
    listener_thread.join()

# Example usage

testMessage = "This is a test script. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog."
speak_with_cancel(testMessage)
speak_with_cancel(testMessage)


