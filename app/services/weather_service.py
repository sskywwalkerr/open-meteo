from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.weather_models import CurrentWeather, HourlyForecast
from app.models.history_models import SearchHistory
import httpx


async def get_weather_data(city: str, db: AsyncSession, user):
    try:
        async with httpx.AsyncClient() as client:
            geocode_response = await client.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": city, "format": "json", "limit": 1},
                timeout=10.0
            )

            if geocode_response.status_code != 200:
                raise ValueError(f"Geocode API error: {geocode_response.status_code}")

            geocode_data = geocode_response.json()

            if not geocode_data:
                raise ValueError("Город не найден")

            lat, lon = geocode_data[0]["lat"], geocode_data[0]["lon"]

            weather_response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,wind_speed_10m",
                    "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
                    "timezone": "auto",
                    "forecast_days": 1
                },
                timeout=10.0
            )

            if weather_response.status_code != 200:
                raise ValueError(f"Weather API error: {weather_response.status_code}")

            data = weather_response.json()

        current_data = data.get("current")
        hourly_data = data.get("hourly")

        if not current_data or not hourly_data:
            raise ValueError("Некорректный ответ от погодного API")

        current = CurrentWeather(
            city=city,
            temperature_2m=current_data["temperature_2m"],
            wind_speed_10m=current_data["wind_speed_10m"],
            time=datetime.fromisoformat(current_data["time"])
        )
        db.add(current)
        await db.flush()

        time_list = hourly_data.get("time", [])[:24]
        temp_list = hourly_data.get("temperature_2m", [])[:24]
        hum_list = hourly_data.get("relative_humidity_2m", [])[:24]
        wind_list = hourly_data.get("wind_speed_10m", [])[:24]

        hourly = [
            HourlyForecast(
                current_weather_id=current.id,
                time=datetime.fromisoformat(time_str),
                temperature_2m=temp,
                relative_humidity_2m=hum,
                wind_speed_10m=wind
            )
            for time_str, temp, hum, wind in zip(time_list, temp_list, hum_list, wind_list)
        ]
        db.add_all(hourly)

        history = SearchHistory(city=city, user_id=user.id)
        db.add(history)

        await db.commit()
        await db.refresh(current)

        return {
            "current": current,
            "hourly": hourly,
            "history": history
        }

    except httpx.RequestError as e:
        raise ValueError(f"Ошибка сети: {str(e)}")
    except KeyError as e:
        raise ValueError(f"Отсутствует обязательное поле в ответе API: {e}")
    except Exception as e:
        raise ValueError(f"Неизвестная ошибка: {str(e)}")
