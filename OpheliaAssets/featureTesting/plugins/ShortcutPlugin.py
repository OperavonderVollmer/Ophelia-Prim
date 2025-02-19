from featureTesting.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__("Shortcut", "What app would you like Ophelia to open?", needsArgs=True)

    def execute(self):
        target = self.prepExecute()
        root_dir = opheNeu.os.path.dirname(opheNeu.os.path.abspath(__file__)) 
        shortcutDir = opheNeu.os.path.join(root_dir, "..", "..", "assets/shortcuts")  
        shortcutPath = opheNeu.os.path.join(shortcutDir, target)
        shortcutPath += ".lnk"
        for app in opheNeu.os.listdir(shortcutDir):
            if app.lower() == target+".lnk":
                try:
                    opheNeu.subprocess.Popen([shortcutPath], shell=True)  
                    return(f"Opening {target}...")
                except Exception as e: print(f"An error occurred: {str(e)}")
        else:
            return(f"Shortcut '{target}' not found. Is the {target} shortcut in shortcuts folder?")   

def get_plugin():
    return plugin()
