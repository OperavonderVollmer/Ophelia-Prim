from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu
from functions.sanitize import sanitizeText

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__(name="Operate", prompt="Which command would you like to execute? Currently, only shutdown is supported", needsArgs=True, modes=["shutdown"])

# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead 

    def operate(self, target):
        # ["shutdown", "5 minutes"]
        def getSpecial(sp):
            if "minutes" in sp:
                return f" /s /t {60 * int(sp.split()[0])}"
            elif "hours" in sp:
                return f" /s /t {3600 * int(sp.split()[0])}"
            return args.get(sp, "")
            
        args = {
            "now": " /s /t 0",
            "abort": " /a",
            "restart": " /r"
        }        
        mode = sanitizeText(target[0])
        if mode not in self.modes: return "Invalid or unimplemented mode"
        special = getSpecial(sanitizeText(target[1]))
        command = str(mode) + special
        try:
            output = opheNeu.subprocess.run(command, shell=True, check=True)
        except: pass
        return f"Executed command '{command}. Output: '{output}'"

    def execute(self):
        target = self.prepExecute()
        return self.operate(target)

    def cheatResult(self, target):
        target = target.split(maxsplit=1)
        return self.operate(target)

def get_plugin():
    return plugin()
