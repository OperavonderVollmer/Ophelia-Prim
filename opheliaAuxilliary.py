import opheliaNeurals as opheNeu
import opheliaAuxilliary as opheAux

def getWikipediaSummary(topic, sentences=4):
    wiki = opheNeu.wikipediaapi.Wikipedia(user_agent="Opera operavgxgamer@gmail.com", language="en")  # English Wikipedia API

    def summarize(text, sentences):
        parser = opheNeu.PlaintextParser.from_string(text, opheNeu.Tokenizer("english"))
        summarizer = opheNeu.LuhnSummarizer()
        summary = summarizer(parser.document, sentences)
        return " ".join([str(sentence) for sentence in summary])

    try:
        # Try getting the page directly
        page = wiki.page(topic)
        if page.exists():
            return summarize(page.summary, sentences)
        
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
def getWeather(showLogs="True", city="Taguig"):
    url = f"https://wttr.in/{city}?format=j1"
    response = opheNeu.requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        current_time = opheNeu.datetime.now().hour * 100  # Get current hour in 24-hour format (e.g., 3 AM -> 300)
        noOfForecasts = 4
        forecast = data["weather"][0]["hourly"]
        upcoming_forecast = [
            hour for hour in forecast if int(hour["time"]) >= current_time
        ][:noOfForecasts]  # Get the next 12 hours (4 forecasts, as data is in 3-hour intervals)
        
        forecast_strings = []
        for hour in upcoming_forecast:
            time_str = f"{int(hour['time']) // 100}:00"  # Convert 2400 format to readable format
            description = hour["weatherDesc"][0]["value"]
            temperature = hour["tempC"]
            forecast_strings.append(f"At {time_str}, it will be {description} with a temperature of {temperature}°C.")
        current_date = opheNeu.datetime.now().strftime("%B %d, %Y")
        output = f"The day is currently {current_date}. This is the weather forecast for {city} for the next 12 hours:\n" + "\n".join(forecast_strings) +"\nThis concludes the weather forecast."
        if showLogs: print(output) 
        return output
    else:
        return "Unfortunately, Could not fetch weather data."
def getCPUStats():    
    cpu_usage = opheNeu.psutil.cpu_percent(interval=1)
    ram = opheNeu.psutil.virtual_memory()
    ram_available = (f"{ram.available / (1024 ** 3):.2f} GB")
    ram_usage = (f"{ram.percent}%")
    try:
        cpu_temp = (f"{(opheNeu.computer.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature / 10) - 273.15:.2f}°C")
    except:
        cpu_temp = "Currently Unavailable"
    text = (f"CPU Usage: {cpu_usage}%\nRAM Usage: {ram_usage}\nRAM Available: {ram_available}\nCPU Temperature: {cpu_temp}")
    print(text)
    return text
def opheliaSleep():
    opheNeu.opheliaRequired = False
    return("Farewell, Master. Ophelia wishes you an excellent day")
def greeting():
    greetings = ["Hello", "Hi", "Greetings"]
    return opheNeu.random.choice(greetings)
def openApp(target):
    with opheNeu.os as os:
        root_dir = os.path.dirname(os.path.abspath(__file__)) 
        shortcutPath = os.path.join(root_dir, "shortcuts", target)  
        shortcutPath += ".lnk"
        if os.path.exists(shortcutPath): 
            try:
                os.startfile(shortcutPath)  
                return(f"Opening {target}...")
            except Exception as e: print(f"An error occurred: {str(e)}")
        else:
            return(f"Shortcut '{target}' not found.")