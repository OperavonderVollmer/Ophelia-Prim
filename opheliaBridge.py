import opheliaMainFunctions as opheMf
import opheliaAuxilliary as opheAux

# command recognized > speak "what is query" > listen query > getSummary > speak "summary"

def opheliaStartMainLoop():
    opheMf.opheliaListen(0, commandMap)

def getQuery():
    opheMf.opheliaSpeak("What would you like Ophelia to look up?")
    try:
        target = opheMf.opheliaHears(5)
        opheMf.opheliaSpeak(f"Looking up {target}...")
        return (opheAux.getWikipediaSummary(target) + ". This concludes the summary.")
    except Exception as e:
        print(e)
        return "Query cancelled"

commandMap = {
"hello": opheAux.greeting,
"stat": opheAux.getCPUStats,
"crush his balls": lambda: "Now crushing his balls",
"sleep": opheAux.opheliaSleep,
"weather": opheAux.getWeather,
"query": getQuery
}