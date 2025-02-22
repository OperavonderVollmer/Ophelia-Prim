from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu
from freedictionaryapi.clients.sync_client import DictionaryApiClient

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__(name="Definition", prompt="What word would you like Ophelia to look up?", needsArgs=True, modes=False)

# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead

    def getDefinition(self, t):
        try:
            t = t.lower()
            with DictionaryApiClient() as client:
                parser = client.fetch_parser(t)
            word = parser.word
            i = 1
            stack = []
            for meaning in word.meanings:
                for definition in meaning.definitions:
                    add = "Definition " + str(i) + ": " + definition.definition
                    if definition.example: add += " Example: " + definition.example
                    add +="\n"
                    stack.append(add)
                    i += 1
            if len(stack) == 0: raise Exception
            else: return f"There are {len(stack)} definitions for {t}\n" + "".join(stack)
        except Exception: return f"Could not find a definition for {t}"


    def execute(self):
        t = self.prepExecute()
        return self.getDefinition(t)

    def cheatResult(self, target):
        return self.getDefinition(target)

def get_plugin():
    return plugin()

