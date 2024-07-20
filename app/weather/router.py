from fastapi import APIRouter, Depends, HTTPException, status
from app.config import settings
from app.user.dependencies import get_current_user
from app.user.models import User
from app.weather.dao import WeatherDAO
from app.weather.dependencies import get_weather_data, get_coords
from app.weather.schemas import SchemaWeatherBase, SchemaWeatherCreate, SchemaWeatherDB


router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)


@router.post("") 
async def get_weather(city_name: SchemaWeatherBase, current_user: User = Depends(get_current_user)):

    try:
        latitude, longitude = await get_coords(city_name.city)
        temperature, windspeed = await get_weather_data(latitude, longitude)
        if temperature and windspeed:

            weather_obj = SchemaWeatherCreate(
                user_id=current_user.id,
                city=city_name.city,
                temperature=temperature,
                wind_speed=windspeed,
            )
    except Exception:
        return "Please type a valid city name"
    
    else:
        await WeatherDAO.add(weather_obj)

        return (
            f"Погода в {weather_obj.city}:  "
            f"Температура {weather_obj.temperature}°С "
            f"скорость ветра {weather_obj.wind_speed}"
        )
