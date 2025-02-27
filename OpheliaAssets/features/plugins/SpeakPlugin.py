from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu

class plugin(opheliaPlugin):
    def __init__(self):
        from opheliaDialogue import dialogue
        super().__init__(name="Speak", prompt="Which category would you like Ophelia to speak from?", description= "Ophelia shall speak a random voice line", needsArgs=True, modes=list(dialogue.keys()), operaOnly=True)

    def getModes(self):
        return self.modes
# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead
    def getDialogue(self, t="general"):
        try:
            return opheNeu.getRandomDialogue(t)
        except: return f"Ophelia does not have that category {opheNeu.getRandomDialogue('errors')}" 
        
    def execute(self):
        target = self.prepExecute()
        return self.getDialogue(target)

    def cheatResult(self, **kwargs):
        return self.getDialogue(kwargs["command"])
    
def get_plugin():
    return plugin()

