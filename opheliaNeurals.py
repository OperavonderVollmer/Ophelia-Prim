import pyttsx3, pyaudio, psutil, wmi, ctypes, sys, os
import speech_recognition as sr
import threading as thr
import time, random, requests
from datetime import datetime
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
import wikipediaapi
import wikipedia


opheliaRequired = True
opheliaInterrupted = False
recognizer = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
computer = wmi.WMI(namespace="root\\wmi")