import os, pystray, time, threading
import PIL.Image as pilImg
import opheliaNeurals as opheNeu
import opheliaPlugins as ophePlu

path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, "assets", "op.png")
image = pilImg.open(path)

def getIcon(commandMap=ophePlu.plugins):
    def onClicked(icon, item):
        for key in commandMap:
            item = str(item).lower()
            if key == item:
                opheNeu.cheatWord = f"command {key}"
                print(f"Printing {key}...")
                break

    return pystray.Icon("Ophelia", image, "Ophelia", menu=pystray.Menu(
        *[pystray.MenuItem(key.capitalize(), onClicked) for key in commandMap if key != "Sleep"],
        pystray.MenuItem("Sleep", onClicked)
    ))

tray_icon = None

def startIcon():
    def iconLogic():
        opheNeu.debug_log("Starting Icon...")
        global tray_icon
        tray_icon = getIcon()
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
        if opheNeu.deepDebugMode: opheNeu.debug_log("Icon monitoring Loop, ticking...")
    opheNeu.debug_log("Stopping Icon...")
    tray_icon.visible = False
    tray_icon.stop()