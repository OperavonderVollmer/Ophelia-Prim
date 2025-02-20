from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__("Shortcut", "What app would you like Ophelia to open?", needsArgs=True)
        

    def getOptions(self, dir=False):
        root_dir = opheNeu.os.path.dirname(opheNeu.os.path.abspath(__file__)) 
        shortcutDir = opheNeu.os.path.join(root_dir, "..", "..", "assets/shortcuts")
        if dir: return shortcutDir
        valid = []
        for file in opheNeu.os.listdir(shortcutDir):
            filep = opheNeu.os.path.join(shortcutDir, file)
            if filep.endswith(".lnk"): valid.append(file[:-4])
        return valid 
   
    
    def openApp(self, target):
        shortcutDir = self.getOptions()       
        for app in shortcutDir:
            print(f"Comparing target {target} with app {app}")
            if app.lower() == str(target).lower():
                shortcutPath = opheNeu.os.path.join(self.getOptions(dir=True), app + ".lnk")
                print(shortcutPath)
                try:
                    opheNeu.subprocess.Popen([shortcutPath], shell=True)  
                    return(f"Opening {target}...")
                except Exception as e: print(f"An error occurred: {str(e)}")
        else:
            return(f"Shortcut '{target}' not found. Is the {target} shortcut in shortcuts folder?")   

    def execute(self):
        target = self.prepExecute()
        self.openApp(target)
    # target
    def cheatResult(self, target): 
        return self.openApp(target)

def get_plugin():
    return plugin()
