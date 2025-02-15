from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
import wikipediaapi
import wikipedia

def get_wikipedia_summary(topic, sentences=2):
    wiki = wikipediaapi.Wikipedia(user_agent="Opera operavgxgamer@gmail.com", language="en")  # English Wikipedia API

    def summarize(text, sentences):
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LuhnSummarizer()
        summary = summarizer(parser.document, sentences)
        return " ".join([str(sentence) for sentence in summary])

    try:
        # Try getting the page directly
        page = wiki.page(topic)
        if page.exists():
            return summarize(page.summary, sentences)
        
        # If page doesn't exist, fall back to search results
        search_results = wikipedia.search(topic)
        if search_results:
            best_match = search_results[0]  # Take the first search result
            page = wiki.page(best_match)
            if page.exists():
                return f"I found multiple results. Here's information about {best_match}: " + summarize(page.summary, sentences)
            else:
                return "I couldn't find anything on Wikipedia about that topic."

    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:5]  # Show only the first 5 options
        return f"'{topic}' is ambiguous. Did you mean: {', '.join(options)}?"
    except wikipedia.exceptions.PageError:
        return "I couldn't find anything on Wikipedia about that topic."
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Example usage
topic = "Black hole"  # Could refer to an animal, car, software, etc.
summary = get_wikipedia_summary(topic)
print(summary)
