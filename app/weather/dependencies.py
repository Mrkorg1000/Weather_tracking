from fastapi import HTTPException
import requests
from app.config import settings


COORDS_KEY = settings.GEO_KEY

async def get_coords(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"

    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Please type a valid city name"
        )
    data = response.json()
    try:
        if city.lower() == data['results'][0]['name'].lower():
            latitude = data["results"][0]["latitude"]
            longitude = data["results"][0]["longitude"]
            return latitude, longitude
        
    except KeyError:
        return "Please type a valid city name"


async def get_weather_data(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"

    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Please type a valid city name"
        )
    else:
        weather_data = response.json()
        temperature = weather_data["current_weather"]["temperature"]
        windspeed = weather_data["current_weather"]["windspeed"]
        return temperature, windspeed
