from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__(name="Wikipedia", prompt="What would you like Ophelia to look up?", description="Ophelia shall read out a wikipedia article for Master", needsArgs=True, modes=False)

# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead

    def getWikipediaSummary(self, t, sentences=4):
        topic = t
        wiki = opheNeu.wikipediaapi.Wikipedia(user_agent="Opera operavgxgamer@gmail.com", language="en")  # English Wikipedia API

        def summarize(text, sentences):
            parser = opheNeu.PlaintextParser.from_string(text, opheNeu.Tokenizer("english"))
            summarizer = opheNeu.LuhnSummarizer()
            summary = summarizer(parser.document, sentences)
            return " ".join([str(sentence) for sentence in summary])

        try:
            # Try getting the page directly
            page = wiki.page(topic)
            if page.exists(): return summarize(page.summary, sentences)
            # If page doesn't exist, fall back to search results
            search_results = opheNeu.wikipedia.search(topic)
            if search_results:
                best_match = search_results[0]  # Take the first search result
                page = wiki.page(best_match)
                if page.exists():
                    print(page)
                    return f"I found multiple results. Here's information about {best_match}: " + summarize(page.text, sentences)
                else:
                    return "I couldn't find anything on Wikipedia about that topic."

        except opheNeu.wikipedia.exceptions.DisambiguationError as e:
            options = e.options[:5]  # Show only the first 5 options
            return f"'{topic}' is ambiguous. Did you mean: {', '.join(options)}?"
        except opheNeu.wikipedia.exceptions.PageError:
            return "I couldn't find anything on Wikipedia about that topic."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def execute(self):
        target = self.prepExecute()        
        return self.getWikipediaSummary(target)
    
    def cheatResult(self, **kwargs):
        return self.getWikipediaSummary(kwargs["command"])

def get_plugin():
    return plugin()


