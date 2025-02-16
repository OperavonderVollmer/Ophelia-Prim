def get_weather_forecast(city="Taguig"):
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        current_time = datetime.now().hour * 100  # Get current hour in 24-hour format (e.g., 3 AM -> 300)

        forecast = data["weather"][0]["hourly"]
        upcoming_forecast = [
            hour for hour in forecast if int(hour["time"]) >= current_time
        ][:4]  # Get the next 12 hours (4 forecasts, as data is in 3-hour intervals)

        forecast_strings = []
        for hour in upcoming_forecast:
            time_str = f"{int(hour['time']) // 100}:00"  # Convert 2400 format to readable format
            description = hour["weatherDesc"][0]["value"]
            temperature = hour["tempC"]
            forecast_strings.append(f"At {time_str}, it will be {description} with a temperature of {temperature}°C.")
        current_date = datetime.now().strftime("%B %d, %Y")
        return f"The day is currently {current_date}. In {city}, here is the 12-hour forecast:\n" + "\n".join(forecast_strings)

    else:
        return "Unfortunately, Could not fetch weather data."
