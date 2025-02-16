import opheliaMainFunctions as opheMf
import opheliaAuxilliary as opheAux

# command recognized > speak "what is query" > listen query > getSummary > speak "summary"

def opheliaStartMainLoop():
    opheMf.opheliaListen(0, commandMap)

def followUp(command_type):
    prompts = {
        "query": "What would you like Ophelia to look up?",
        "shortcut": "What app would you like Ophelia to open?",
        "transmission": "What would you like Ophelia to say or play?"
    }
    actions = {
        "query": opheAux.getWikipediaSummary,
        "shortcut": opheAux.openApp,
        "transmission": opheAux.audioThroughMic
    }

    opheMf.opheliaSpeak(prompts[command_type])    
    try:
        target = opheMf.opheliaHears(0)
        if command_type == "transmission":
            if target.__contains__("play"): isTTS = False
            elif target.__contains__("say"): isTTS = True
            else: return "Query cancelled"
            if target.lower().startswith("say "):
                target = target[4:]
            elif target.lower().startswith("play "):
                target = target[5:]
            target = target.replace(" ", "")
            return actions[command_type](target, isTTS=isTTS)
        opheMf.opheliaSpeak(f"Locating {target}...")
        return actions[command_type](target)
    except Exception as e:
        print(e)
        return "Query cancelled"

commandMap = {
"hello": opheAux.greeting,
"stat": opheAux.getCPUStats,
"crush his balls": lambda: "Now crushing his balls",
"sleep": opheAux.opheliaSleep,
"weather": opheAux.getWeather,
"query": followUp,
"shortcut": followUp,
"transmission": followUp
}