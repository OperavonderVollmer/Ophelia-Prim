from features.opheliaPluginTemplate import opheliaPlugin
from functions.opheliaMouth import opheliaSpeak

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__(name="Print Stream", prompt="This will print Stream")

    def execute(self):
        return ("Stream")

def get_plugin():
    return plugin()

