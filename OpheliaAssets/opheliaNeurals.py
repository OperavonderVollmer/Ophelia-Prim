# APIs
import os
import sys
import time
import random
import ctypes
import subprocess
import threading as thr
import tempfile
import wave
import numpy as np
import scipy.signal as sps
import librosa
import requests
import wikipedia
import wikipediaapi
import pyttsx3
import pyaudio
import psutil
import wmi
import sounddevice as sd
import speech_recognition as sr
import PIL.Image as pilImg
import pystray
import re

from word2number import w2n
from datetime import datetime
from pydub import AudioSegment
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

# Importing from project
import config
from opheliaDialogue import dialogue , misc


city = config.city
micIndex = config.micIndex
speakerIndex = config.speakerIndex
opheliaRequired = True
opheliaInterrupted = False
recognizer = sr.Recognizer()
mic = sr.Microphone()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 
computer = wmi.WMI(namespace="root\\wmi")
debugMode = config.debugMode 
deepDebugMode = config.deepDebugMode
cheatWord = None

postureCheckFileName = "rock"
postureCheckPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))
postureCheckFile = os.path.join(postureCheckPath, postureCheckFileName) 
postureCheckActive = os.path.exists(postureCheckFile)
defaultPostureInterval = "10"
postureLooping = False


def debug_log(message): 
    if debugMode: print(f"[DEBUG]--------------------------------------------------------[DEBUG] {message}")

def getRandomDialogue(category):
    return random.choice(dialogue[category])

BLACKLISTED_KEYWORDS = [r"\bimport\b", r"\bexec\b", r"\beval\b", r"\bsystem\b", r"\bos\b",r"\bsubprocess\b",r"\brm\b",r"\bdel\b",r"\bopen\b",r"\bfile\b"]
def checkText(text):
    with re:
        for keyword in BLACKLISTED_KEYWORDS:
            if re.search(keyword, text, re.IGNORECASE):
                debug_log(f"Blocked potentially dangerous input: {text}")
                return None  # Return None to indicate blocked input
        else: return text