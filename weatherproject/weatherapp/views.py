from django.shortcuts import render
import requests
import datetime
from geopy.geocoders import Nominatim

# https://openweathermap.org/current
# https://www.youtube.com/watch?v=HCAWDqlfXUc&ab_channel=Pythonology   32:00


def index(request):

    if "city" in request.POST:  # or city in database
        city = request.POST["city"]

        geolocator = Nominatim(user_agent="kasiopac")
        location = geolocator.geocode(city)
        lat = location.raw["lat"]
        lon = location.raw["lon"]

        api_key = "d4bdffc8670b3d66754f5b03909a2453"
        lang = "pl"
        URL = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&lang={lang}&appid={api_key}"
        today = datetime.date.today().isoformat()
        try:
            forecast = requests.get(url=URL).json()
        except requests.exceptions.HTTPError:
            raise requests.exceptions.HTTPError("Błąd połączenia. Spróbuj ponownie")
        except requests.exceptions.ConnectionError:
            raise requests.exceptions.ConnectionError("Błąd połączenia. Spróbuj ponownie")
        try:
            current = forecast["current"]
            hourly = forecast["hourly"]
            daily = forecast["daily"]
        except KeyError:
            raise KeyError(forecast["message"])

        current_description = current["weather"][0]["description"]
        current_icon = current["weather"][0]["icon"]
        try:
            current_rain = current["rain"]["1h"]
        except KeyError:
            current_rain = 0
        current_temp = current["temp"]
        hourly_forecast = {}


        for hour in range(3, 47, 4):

            hourly_description = hourly[hour]["weather"][0]["description"]
            try:
                hourly_rain = hourly[hour]["rain"]["1h"]
            except KeyError:
                hourly_rain = 0
            hourly_temp = hourly[hour]["temp"]
            hourly_forecast[hour+1] = {"niebo":hourly_description, "temperatura": hourly_temp, "Opady": hourly_rain}

        daily_forecast = {}
        for day in range(1,5):
            daily_description = daily[day]["weather"][0]["description"]
            try:
                daily_rain = daily[day]["rain"]
            except KeyError:
                daily_rain = 0
            daily_temp = daily[day]["temp"]
            daily_forecast[day] = {"niebo":daily_description, "temperatura": daily_temp, "Opady": daily_rain}

        return render(
            request,
            "weatherapp/index.html",
            {
                "current_description": current_description,
                "current_icon": current_icon,
                "current_rain": current_rain,
                "current_temp": current_temp,
                "city": city,
                "today": today,
                "hourly_forecast": hourly_forecast,
                "daily_forecast": daily_forecast,
            },
        )

    else:
        return render(
            request,
            "weatherapp/index.html",
            {"description": None, "icon": None, "temp": None, "city": None, "today": None},
        )
