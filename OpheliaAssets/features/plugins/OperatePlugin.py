from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu
from functions.sanitize import sanitizeText

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__(name="Operate", prompt="Which command would you like to execute? Currently, only shutdown is supported", needsArgs=True)

# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead 

    def operate(self, target):
        # shutdown10hours
        def getSpecial(sp):
            if "minutes" in sp:
                sp = sp.replace("minutes", "")
                return f" /s /t {60 * int(sp)}"
            elif "hours" in sp:
                sp = sp.replace("hours", "")
                return f" /s /t {3600 * int(sp)}"
            return args.get(sp, "")
            
        args = { "now": " /s /t 0", "abort": " /a", "restart": " /r" }

        if sanitizeText(target) == None : return opheNeu.getRandomDialogue("dirty_messages")
        for mode in ["shutdown"]:
            if target.__contains__(mode): command = str(mode)    
            else: return f"{target} is Invalid or unimplemented mode"
        target = target.replace(command, "")
        special = getSpecial(target)
        command = str(mode) + special
        try:
            output = opheNeu.subprocess.run(command, shell=True, check=True)
        except: output = f"Failed to execute command. Error Code: {str(output.returncode)}"
        return f"Executed command '{command}. Output: '{output}'"

    def execute(self):
        target = self.prepExecute()
        target = target.replace(" ", "")
        return self.operate(target)


    def cheatResult(self, target):
        target = target.replace(" ", "")
        return self.operate(target)

def get_plugin():
    return plugin()
