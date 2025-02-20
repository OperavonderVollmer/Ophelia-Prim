from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu
import opheliaPlugins as ophePlu

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__(name="Sleep")

# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead

    def opheliaSleep(self):    
        opheNeu.debug_log("Ophelia Prime powering down")
        output = opheNeu.getRandomDialogue("farewells")
        def sayGoodbye():
            ophePlu.plugins["Transmission"].audioThroughMic(output, True, False)
        opheNeu.thr.Thread(target=sayGoodbye).start()
        opheNeu.opheliaRequired = False
        return output

    def execute(self):
        return self.opheliaSleep()

    def cheatResult(self):
        return self.execute()
def get_plugin():
    return plugin()

