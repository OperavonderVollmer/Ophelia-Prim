from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu
from dotenv import load_dotenv
import os, re, requests, pandas
from functions.opheliaHears import opheliaHears
import opheliaPlugins as ophePlu

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__(name="Search", prompt="What would you like Ophelia to search for?", description="Ophelia shall provide you with the results and links to your query", needsArgs=True, modes=False)

# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead

    def googleSearch(self, t, isCheat=False):

        def buildPayload(query: str, startIndex=1, endIndex=5, **params) :
            """
                Builds a payload for the Google Custom Search API
                
            """
            payload = {
                'key': searchToken,
                'cx': searchEngineID,
                'q': query,
                'start': startIndex,
                'num': endIndex,
            }
            payload.update(params)
            return payload        
        def makeRequest(payload):
            try:
                response = requests.get('https://www.googleapis.com/customsearch/v1', params=payload)
                response.raise_for_status()  # Raises an HTTPError if status != 200
                data = response.json()
                if "items" not in data:
                    return {"error": "No results found"}
                return data
            except requests.RequestException as e:
                return {"error": f"Request failed: {e}"}
            
        def messageResults(resultDict, isCheat=isCheat):
            """
                Makes the message readable
                Use this link for more info: https://developers.google.com/custom-search/v1/reference/rest/v1/Search
                Also strips the link if not called from discord to ensure its not too cluttered
            """
            text = ""
            i = 1
            for result in resultDict:
                text += "Result: " + resultDict[result]['title'] + "\n"
                if isCheat:
                    text += "Link: " + resultDict[result]['link'] + "\n"
                text += "Snippet: " + resultDict[result]['snippet'] + "\n"
                text += f"That was result number: {str(i)}\n\n"
                i += 1
            return text

        def interpretResults(message):
            """
                After reading the message, asks the user if they want to copy any of the links
                Copies the link to clipboard if so
            """
            ophePlu.plugins["Transmission"].audioThroughMic(message + ". Would you like to copy any of the links? Say Result followed by the index.", isTTS=True, playThroughMic=False)
            print("Now listening for input...")
            index = opheliaHears()
            index = opheNeu.normalizeNumber(index.replace("result", ""))
            index = "result"+str(index)
            if index.startswith("result"):
                opheNeu.copyToClipboard(resultDict[index]['link'])
                return f"Copied {resultDict[index]['title']} link to clipboard"
            return "Result not found"
        
        load_dotenv()
        searchToken = str(os.getenv("searchToken"))
        searchEngineID = str(os.getenv("searchEngineID"))
        payload = buildPayload(t)
        response = makeRequest(payload)
        resultDict = {}
        for result in response['items']:
            resultDict["result"+str(len(resultDict)+1)] = {
                "title": result['title'],
                "link": result['link'],
                "snippet": result['snippet'],
            }
        mess = messageResults(resultDict)
        if isCheat: return mess
        return interpretResults(mess)
   
    def execute(self):
        t = self.prepExecute()
        return self.googleSearch(t)

    def cheatResult(self, target, sender=None):
        return self.googleSearch(target, isCheat=True)

def get_plugin():
    return plugin()

