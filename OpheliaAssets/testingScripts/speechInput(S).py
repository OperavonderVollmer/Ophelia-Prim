import speech_recognition as sr

recognizer = sr.Recognizer()

def inquiry():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = recognizer.listen(source)
        text = ""
        try:
            text = recognizer.recognize_google(audio)
        except sr.RequestError:
            try:
                text = recognizer.recognize_sphinx(audio)
            except sr.UnknownValueError:
                text = ("Sorry, Ophelia could not understand the audio.")
            except sr.RequestError as e:
                text = (f"PocketSphinx error; {e}")
        finally:
            return(text)


print(inquiry())