import opheliaAuxilliary as opheAux
from functions import opheliaMouth, opheliaEars

# command recognized > speak "what is query" > listen query > getSummary > speak "summary"

def opheliaStartMainLoop(opheIcon):
    opheIcon.startIcon(commandMap)
    opheliaEars.opheliaListens(0, commandMap)

def followUp(command_type):
    prompts = {
        "query": "What would you like Ophelia to look up?",
        "shortcut": "What app would you like Ophelia to open?",
        "transmission": "What would you like Ophelia to say or play?",
        "posture": "How many minutes would you like Ophelia to check your posture? Say 0 or False to deactivate",
        "voice": "Which category would you like Ophelia to speak from?"
  
    }
    actions = {
        "query": opheAux.getWikipediaSummary,
        "shortcut": opheAux.openApp,
        "transmission": opheAux.audioThroughMic,
        "posture": opheAux.postureCheckSetup,
        "voice": opheAux.speakDialogue
    }
    changeables ={
        "transmission": ["say", "play"],
    }

    opheliaMouth.opheliaSpeak(prompts[command_type])    
    try:
        target = opheliaEars.opheliaHears(0)
        for keyword, configs in changeables.items():
            if command_type == keyword:
                # 2nd prompt asks for mode + target
                if target is configs[0]: mode = False
                elif target is configs[1]: mode = True
                else: return "Query cancelled"
                # remove mode from target and remove spaces
                if target.lower().startswith(configs[0]):
                    target = target[len(configs[0]):]
                elif target.lower().startswith(configs[1]):
                    target = target[len(configs[1]):]
                target = target.replace(" ", "")
                return actions[command_type](target, mode)
            
        opheliaMouth.opheliaSpeak(f"Received {target}...")
        return actions[command_type](target)
    except Exception as e:
        print(e)
        return "Query cancelled"

commandMap = {
"stat": opheAux.getCPUStats,
"crush his balls": lambda: "Now crushing his balls",
"weather": opheAux.getWeather,
"query": followUp,
"shortcut": followUp,
"transmission": followUp,
"posture": followUp,
"voice": followUp,



"sleep": opheAux.opheliaSleep,
}
