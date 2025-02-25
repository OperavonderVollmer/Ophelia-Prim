from abc import ABC, abstractmethod
from functions.opheliaMouth import opheliaSpeak
from functions.opheliaHears import opheliaHears
import opheliaNeurals as opheNeu
#from functions.opheliaDiscord import waitInput

class opheliaPlugin(ABC):
    def __init__(self, name: str, prompt: str= "", description: str="", needsArgs: bool = False, modes = [], helpText = "", operaOnly: bool = False):
        self.name = name
        self.desc = description
        self.prompt = prompt
        self.needsArgs = needsArgs
        self.modes = modes
        self.helpText = helpText
        self.operaOnly = operaOnly
        
    def getName(self): return self.name
    def getDesc(self): return self.desc
    def getPrompt(self): return self.prompt
    def getOperaOnly(self): return self.operaOnly
    def getHelpText(self): return self.helpText
    def getNeedsArgs(self): return self.needsArgs

    def prepExecute(self):
        if self.prompt != "": opheliaSpeak(self.prompt)
# only has a return if needsArgs
        if self.needsArgs: 
            target = opheliaHears(3)
            if self.modes:
                for mode in self.modes:
                    if target.__contains__(mode): 
                        find = target.replace(mode, "").replace(" ", "")
                        target = [find, mode]
                        break
                else: return "Query cancelled"
            opheNeu.debug_log(f"Sending parameters {target} from {self.name}")
            return target
        pass
    def execute(self):
        # enter code here
        pass
    def cheatResult(self):

        pass