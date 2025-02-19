from featureTesting.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu
import opheliaPlugins as ophePlu

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__(name="Sleep")

# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead

    def opheliaSleep(self):    
        ophePlu.plugins["Transmission"].audioThroughMic(opheNeu.getRandomDialogue("farewells"), True, False)
        opheNeu.opheliaRequired = False
        return ""

    def execute(self):
        return self.opheliaSleep()

def get_plugin():
    return plugin()

