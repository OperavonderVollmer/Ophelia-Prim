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
import logging

from word2number import w2n
from datetime import datetime
from pydub import AudioSegment
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

# Importing from project
import config
from opheliaDialogue import dialogue , misc
from functions import opheliaAsync as asy
import opheliaLogging as opheLog

city = config.city
micIndex = config.micIndex
speakerIndex = config.speakerIndex
opheliaRequired = True
opheliaInterrupted = False
opheliaLocal = True
recognizer = sr.Recognizer()
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

discordLoop = None

def debug_log(message, deepLog=False, speakLog=False): 
    output = f"[DEBUG]--------------------------------------------------------[DEBUG] {message}" if speakLog is not "speakLogChannel" else message
    try:
        if discordLoop is not None: discordLog(output, 
                                               "deepLogChannel" if deepLog else 
                                               "speakLogChannel" if speakLog else 
                                               "logChannel" )
    except ImportError: print("Discord implementation cannot be located")
    except RuntimeError: print("Discord loop is not running")
    except Exception as e: output = e 
    opheLog.logging.debug(output + " - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if debugMode: 
        if deepLog and not deepDebugMode: return
        print(output)

def discordLog(message, selectedChannel):
    from functions import opheliaDiscord as opheDisc
    try:
        asy.async_to_sync(opheDisc.sendChannel(message, selectedChannel), discordLoop)
    except RuntimeWarning: print("Didn't await")

def killDiscord ():
    if discordLoop is None: return
    from functions import opheliaDiscord as opheDisc
    try: 
        asy.async_to_sync(opheDisc.stopOpheliaDiscord(), discordLoop)
    except RuntimeWarning: print("Didn't await")

def playSong(name):
    from functions import opheliaDiscord as opheDisc
    try:
        asy.async_to_sync(opheDisc.startMusicStream(name), discordLoop)
    except RuntimeWarning: print("Didn't await")

def getRandomDialogue(category):
    return random.choice(dialogue[category])

def normalizeNumber(t):
    try:
        if isinstance(t, str):
            t = t.strip().lower()
            if t.isdigit():
                return int(t)
            return w2n.word_to_num(t)
        else: return t        
    except ValueError: raise

def copyToClipboard(t):
    subprocess.run("clip", text=True, input=t, shell=True)

def isRequired():
    try:
        return opheliaRequired  # Normal check
    except NameError:  # If opheliaNeurals is gone, assume shutdown
        return False
    except AttributeError:  # If opheliaRequired is missing, assume shutdown
        return False

def monitorThreads():
    def mon():
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:                
                if not isRequired():
                    return
                threadCount = len(thr.enumerate())
                warningMessage = "SOFT WARNING: MORE THAN 50 THREADS LIVE." if threadCount > 50 else "HARD WARNING: MORE THAN 100 THREADS LIVE." if threadCount > 100 else ""
                p = f"{warningMessage} There are currently {threadCount} threads running."
                print(p)
                opheLog.logging.debug(f"{p} - {timestamp}")
                debug_log(p)
                time.sleep(30)
            except (NameError, AttributeError): # If opheliaNeurals is gone, assume shutdown
                return
            except Exception as e: 
                opheLog.logging.debug(f"{e} - {timestamp}")
                print("Monitor Thread failed, restarting in 5 seconds...")
                time.sleep(5)
                thr.Thread(target=monitorThreads, daemon=True).start()
                return
    thr.Thread(target=mon, daemon=True).start()