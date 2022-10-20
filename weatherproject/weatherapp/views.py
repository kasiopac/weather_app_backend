from django.shortcuts import render, redirect
import requests
import datetime
from geopy.geocoders import Nominatim
from .models import MyCity
from .forms import SetMyCity
from django.http import HttpResponseRedirect


def get_forecast(city):

    geolocator = Nominatim(user_agent="kasiopac")
    location = geolocator.geocode(city)
    lat = location.raw["lat"]
    lon = location.raw["lon"]

    api_key = "d4bdffc8670b3d66754f5b03909a2453"
    lang = "pl"
    URL = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&lang={lang}&appid={api_key}"
    today_raw = datetime.date.today()
    today = today_raw.isoformat()
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
    hourly_forecast = []

    for hour in range(3, 47, 4):
        hourly_description = hourly[hour]["weather"][0]["description"]
        try:
            hourly_rain = hourly[hour]["rain"]["1h"]
        except KeyError:
            hourly_rain = 0
        hourly_temp = int(hourly[hour]["temp"])
        hourly_forecast.append(
            f"pogoda za {hour + 1} h: {hourly_description}, {hourly_temp} stopni, opady: {hourly_rain} mm"
        )

    daily_forecast = []
    for day in range(1, 5):
        daily_description = daily[day]["weather"][0]["description"]
        try:
            daily_rain = daily[day]["rain"]
        except KeyError:
            daily_rain = 0
        daily_temp_min = int(daily[day]["temp"]["min"])
        daily_temp_max = int(daily[day]["temp"]["max"])

        daily_forecast.append(
            f"pogoda dnia {today_raw + datetime.timedelta(days=day)}: {daily_description}, od {daily_temp_min} do {daily_temp_max} stopni, opady: {daily_rain} mm"
        )

    return {
        "current_description": current_description,
        "current_icon": current_icon,
        "current_rain": current_rain,
        "current_temp": current_temp,
        "city": city,
        "today": today,
        "hourly_forecast": hourly_forecast,
        "daily_forecast": daily_forecast,
    }


def index(request):
    if request.user.is_authenticated:
        try:
            city = MyCity.objects.get(user=request.user)
        except:
            city = None
        if city:
            weather_data = get_forecast(city=city)
            return render(request, "weatherapp/index.html", weather_data)

    elif "city" in request.POST:
        city = request.POST["city"]
        weather_data = get_forecast(city=city)
        return render(request, "weatherapp/index.html", weather_data)

    else:
        return render(
            request,
            "weatherapp/index.html",
            {"description": None, "icon": None, "temp": None, "city": None, "today": None},
        )


def mycity(response):

    city = MyCity.objects.filter(user=response.user)
    if city:
        return redirect("/")

    if response.method == "POST":
        form = SetMyCity(response.POST)
        if form.is_valid():
            city_name = form.cleaned_data["name"]
            cn = MyCity(name=city_name)
            cn.save()
            response.user.mycity.add(cn)

            return HttpResponseRedirect("/")

    else:
        form = SetMyCity()

    return render(response, "weatherapp/mycity.html", {"form": form})
