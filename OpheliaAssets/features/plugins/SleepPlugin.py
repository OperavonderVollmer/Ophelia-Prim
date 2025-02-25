from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu
import opheliaPlugins as ophePlu

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__(name="Sleep", description="Ophelia shall power down")

# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead

    def opheliaSleep(self):    
        opheNeu.debug_log("Ophelia Prime powering down")
        output = opheNeu.getRandomDialogue("farewells")
        def sayGoodbye():
            ophePlu.plugins["Transmission"].audioThroughMic(output, True, False)
            opheNeu.opheliaRequired = False
            print("Ophelia no longer required")
        if opheNeu.discordLoop: opheNeu.discordLoop.stop()
        opheNeu.thr.Thread(target=sayGoodbye).start()        
        return output

    def execute(self):
        return self.opheliaSleep()

    def cheatResult(self, t, sender=None):
        return self.execute()
def get_plugin():
    return plugin()

