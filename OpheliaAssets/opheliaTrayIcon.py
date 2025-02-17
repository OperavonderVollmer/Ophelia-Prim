import os, pystray, time, threading
import PIL.Image as pilImg
from functions import opheliaMouth 
import opheliaNeurals as opheNeu
import opheliaAuxilliary as opheAux

path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, "assets", "op.png")
image = pilImg.open(path)

def getIcon(commandMap):
    def onClicked(icon, item):
        for key in commandMap.keys():
            item = str(item).lower()
            if key == item:
                opheNeu.cheatWord = f"command {key}"
                print(f"Printing {key}...")
                break

    return pystray.Icon("Ophelia", image, "Ophelia", menu=pystray.Menu(
        *[pystray.MenuItem(key.capitalize(), onClicked) for key in commandMap.keys()],
    ))

tray_icon = None

def startIcon(commandMap = {"stat": "opheAux.getCPUStats","crush his balls": lambda: "Now crushing his balls"}):
    def iconLogic():
        opheNeu.debug_log("Starting Icon...")
        global tray_icon
        tray_icon = getIcon(commandMap)
        trayThread = threading.Thread(target=tray_icon.run, daemon=True)
        trayThread.start()
        iconMonitoring()
    iconThread = threading.Thread(target=iconLogic, daemon=True)
    iconThread.start()

# start only if icon is not none and ophelia is required
# stop only if icon is not none and ophelia is not required
def iconMonitoring():
    while opheNeu.opheliaRequired: 
        time.sleep(5)
        opheNeu.debug_log("Icon monitoring Loop, ticking...")
    opheNeu.debug_log("Stopping Icon...")
    tray_icon.stop()