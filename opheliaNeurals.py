import pyttsx3, pyaudio, psutil, wmi, ctypes, sys, os
import speech_recognition as sr

opheliaRequired = True
recognizer = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
computer = wmi.WMI(namespace="root\\wmi")