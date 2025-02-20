from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__(name="Weather")

# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead

    def getWeather(self, showLogs=True, city=opheNeu.city):
        url = f"https://wttr.in/{city}?format=j1"
        response = opheNeu.requests.get(url)

        if response.status_code == 200:
            data = response.json()
            current_time = opheNeu.datetime.now().hour * 100  # Current hour in 24-hour format
            forecast = data["weather"][0]["hourly"]

            # Get the next 12 hours of forecasts, wrapping around to the next day if needed
            upcoming_forecast = []
            hours_needed = 4  # We want 4 forecasts (12 hours)

            for i in range(hours_needed):
                index = (forecast.index([h for h in forecast if int(h["time"]) >= current_time][0]) + i) % len(forecast)
                upcoming_forecast.append(forecast[index])

            forecast_strings = []
            for hour in upcoming_forecast:
                time_str = f"{int(hour['time']) // 100:02d}:00"  # Format with leading zero
                description = hour["weatherDesc"][0]["value"]
                temperature = hour["tempC"]
                forecast_strings.append(f"At {time_str}, it will be {description} with a temperature of {temperature}°C.")

            current_date = opheNeu.datetime.now().strftime("%B %d, %Y")
            output = f"The day is currently {current_date}. This is the weather forecast for {city} for the next 12 hours:\n" + "\n".join(forecast_strings) + "\nThis concludes the weather forecast."

            if showLogs:
                print(output)
            return output
        else:
            return "Unfortunately, Could not fetch weather data."
    def execute(self):
        return self.getWeather()

    def cheatResult(self):
        return self.execute()
def get_plugin():
    return plugin()

