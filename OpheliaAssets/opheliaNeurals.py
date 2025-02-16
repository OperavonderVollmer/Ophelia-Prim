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
from datetime import datetime
from pydub import AudioSegment
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

micIndex = 10
speakerIndex = 17 
opheliaRequired = True
opheliaInterrupted = False
recognizer = sr.Recognizer()
mic = sr.Microphone()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
computer = wmi.WMI(namespace="root\\wmi")
debugMode = False

def debug_log(message): 
    if debugMode: print(f"[DEBUG] {message}")