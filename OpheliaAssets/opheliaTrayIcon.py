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
            key = key.lower()
            item = str(item).lower()
            if key == item:
                # forcefully gives ophelia a word, emulating a spoken command
                opheNeu.cheatWord = f"command {key}"
                print(f"Printing {key}...")
                break
    def hasOptions(key):
        return pystray.Menu(
            pystray.MenuItem("Open", onClicked),
            pystray.MenuItem("Options", onClicked)
        )
    
    def hasOptions(key):
        def onClicked(icon, item):
            item = str(item).replace(" Options", "").lower()
            # directly calls a plugin's cheatResult, bypassing the need for a spoken command
            print(f"Calling {item}...")
            ophePlu.plugins[key].cheatResult(command = f"{item}", senderInfo=None, isTray=True)
        options = ophePlu.plugins[key].getOptions()
        return pystray.Menu(
            *[pystray.MenuItem(key.capitalize(), onClicked) for key in options]
        )    
    return pystray.Icon("Ophelia", image, "Ophelia", menu=pystray.Menu(
        *[pystray.MenuItem(key.capitalize(), onClicked) for key in commandMap if key != "Sleep"],
        pystray.Menu.SEPARATOR,
        *[pystray.MenuItem(key.capitalize() + " Options", hasOptions(key)) for key in commandMap if key != "Sleep" and hasattr(commandMap[key],"getOptions")],
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Sleep", onClicked)
    ))

tray_icon = None

def startIcon():
    def iconLogic():
        print("Starting icon")
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
        time.sleep(10)
        opheNeu.debug_log("Icon monitoring Loop, ticking...", True)
    opheNeu.debug_log("Stopping Icon...")
    tray_icon.visible = False
    tray_icon.stop()