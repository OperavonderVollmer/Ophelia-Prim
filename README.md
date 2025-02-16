# **Ophelia AI**

The successor to my ["Oper4sTools"](https://github.com/FacundoDayne/Oper4sTools), Ophelia is an Artificial <sub>almost</sub> Intelligence —a voice-controlled assistant designed to provide a seamless and responsive experience. While not a true AI, Ophelia <sub>sort of</sub> intelligently processes voice commands, executes tasks, and integrates with various system functions to assist users efficiently.

## Features

**Speech Recognition:** Uses Google Speech Recognition and PocketSphinx as a fallback for offline use.

**Text-to-Speech:** Communicates responses using pyttsx3 (or an AI-generated voice model in the future).

**System Monitoring:** Retrieves CPU usage, temperature, RAM usage, and disk activity.

**Application Launcher:** Opens programs based on shortcuts placed in a designated folder.

**Wikipedia Integration:** Provides summarized information from Wikipedia.

**Weather Reports:** Retrieves and reports the current weather and upcoming forecasts.

**Reminders & Alarms (Planned):** Future integration with Google Calendar.

**Audio Output Through Virtual Mic:** Routes Ophelia's speech through both speakers and a virtual microphone for external communication, allowing Ophelia to talk and play sounds to the mic. **_REQUIRES VBCABLE OR EQUIVALENT_**

## Config File

In `OpheliaAssets` there is a config file containing some things that need setup (will refine in the future)

## How to Use Ophelia

Ophelia will listen in the background for `command` following a keyword

Commands should be spoken with a `command <command>` format. (example: `command stats`)

# Command List

-   hello
    > Returns a greeting
-   stat
    > Returns the cpu and ram stats (gpu and drive stats planned)
-   weather
    > Returns the weather forecast for next 12 hours for the city stated in config
-   query
    > Asks a follow up question about the search query, then returns the information via wikipedia
-   shortcut
    > Asks a follow up question about the shortcut name, then returns a message about the shortcut after attempting to open it
-   transmission
    > Asks a follow up question about the nature of the transmission. If keyword **"say"** is heard, assume tts. if keyword **play** is heard, assume its wav file. Then will return a message about the state of the transmission after attempting to play the tranmission
-   sleep
    > Gracefully powers down Ophelia

## Installation & Setup

Ensure you have Python installed (version 3.9+ recommended).

Install dependencies using:
`pip install -r requirements.txt`

Run `Ophelia-prim.bat` to start Ophelia.

Ophelia will run in the background and is accessible through a tray icon

## Notes

Ophelia operates in the background, waiting for trigger words to activate.

It is optimized for speed and efficiency, avoiding excessive resource usage.

Future expansions may introduce more AI-driven interactions.
