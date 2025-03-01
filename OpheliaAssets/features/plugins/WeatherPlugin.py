from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__(name="Weather", description="Ophelia shall provide you a rundown of the weather")

# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead

    def getWeather(self, showLogs=True, city=opheNeu.city):
        url = f"https://wttr.in/{city}?format=j1"
        response = opheNeu.requests.get(url)

        if response.status_code != 200:
            return "Unfortunately, could not fetch weather data."

        data = response.json()
        current_time = opheNeu.datetime.now().hour * 100  # Current hour in 24-hour format

        # Ensure weather data exists
        if "weather" not in data or not data["weather"]:
            return "Weather data is missing from the response."
        
        today_forecast = data["weather"][0]["hourly"]  # Today's forecast
        tomorrow_forecast = data["weather"][1]["hourly"] if len(data["weather"]) > 1 else []  # Tomorrow's forecast

        # Get forecasts after the current time
        future_forecasts = [h for h in today_forecast if int(h["time"]) >= current_time]

        # If no forecasts are left today, use tomorrow's data
        if not future_forecasts:
            future_forecasts = tomorrow_forecast  

        # Prevent index error if there's still no forecast
        if not future_forecasts:
            return "No forecast data available for the next 12 hours."

        # Get the starting forecast index
        start_index = today_forecast.index(future_forecasts[0]) if future_forecasts[0] in today_forecast else 0

        upcoming_forecast = []
        hours_needed = 4  # We want 4 forecasts (12 hours)

        for i in range(hours_needed):
            index = (start_index + i) % len(today_forecast)  # Wrap around properly
            if index == 0 and len(tomorrow_forecast) > 0:  # If reaching the end, switch to tomorrow
                upcoming_forecast.extend(tomorrow_forecast[:hours_needed - len(upcoming_forecast)])
                break
            upcoming_forecast.append(today_forecast[index])

        # Generate readable forecast messages
        forecast_strings = []
        for hour in upcoming_forecast:
            time_str = f"{int(hour['time']) // 100:02d}:00"
            description = hour["weatherDesc"][0]["value"]
            temperature = hour["tempC"]
            forecast_strings.append(f"At {time_str}, it will be {description} with a temperature of {temperature}°C.")

        current_date = opheNeu.datetime.now().strftime("%B %d, %Y")
        output = f"The day is currently {current_date}. This is the weather forecast for {city} for the next 12 hours:\n" + "\n".join(forecast_strings) + "\nThis concludes the weather forecast."

        if showLogs:
            print(output)
        return output


    def execute(self, showLogs=True):
        return self.getWeather(showLogs)

    def cheatResult(self, **kwargs):
        return self.execute()
def get_plugin():
    return plugin()

