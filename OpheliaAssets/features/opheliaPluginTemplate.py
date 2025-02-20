from abc import ABC, abstractmethod
from functions.opheliaMouth import opheliaSpeak
from functions.opheliaHears import opheliaHears
#from functions.opheliaDiscord import waitInput

class opheliaPlugin(ABC):
    def __init__(self, name: str, prompt: str= "", needsArgs: bool = False, modes = []):
        self.name = name
        self.prompt = prompt
        self.needsArgs = needsArgs
        self.modes = modes
        pass
    def getName(self): return self.name
    def prepExecute(self):
        if self.prompt != "": opheliaSpeak(self.prompt)
# only has a return if needsArgs
        if self.needsArgs: 
            target = opheliaHears(3)
            if self.modes:
                for mode in self.modes:
                    if target.__contains__(mode): 
                        target = target.lower().replace(mode, "").replace(" ", "")
                        return [target, mode]
                else: return "Query cancelled"
            else: return target
        pass
    def execute(self):
        # enter code here
        pass
    def cheatResult(self):

        pass