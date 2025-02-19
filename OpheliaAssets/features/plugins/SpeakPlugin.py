from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__(name="Speak", prompt="Which category would you like Ophelia to speak from?", needsArgs=True, modes=False)

# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead
    def getDialogue(self, t="general"):
        try:
            return opheNeu.getRandomDialogue(t)
        except: return f"Ophelia does not have that category {opheNeu.getRandomDialogue('errors')}" 
        
    def execute(self):
        target = self.prepExecute()
        return self.getDialogue(target)

def get_plugin():
    return plugin()

