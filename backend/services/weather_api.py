import requests
from datetime import datetime, timezone

def get_weather(lat, lon):
    """
    Fetch current weather details for given coordinates using Open-Meteo API.
    Includes temperature, humidity, wind speed, rainfall, UV index, sunrise, and sunset.
    """
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&current_weather=true"
            "&hourly=relative_humidity_2m,precipitation,uv_index"
            "&daily=sunrise,sunset"
            "&timezone=auto"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data.get("current_weather", {})
        hourly = data.get("hourly", {})
        daily = data.get("daily", {})
        humidity = None
        rainfall = None
        uv_index = None
        sunrise = None
        sunset = None

        if "time" in hourly and hourly["time"]:
            current_time_str = current.get("time")
            if current_time_str:
                # Parse current time and hourly times to datetime objects
                current_time = datetime.fromisoformat(current_time_str)
                hourly_times = [datetime.fromisoformat(t) for t in hourly["time"]]

                # Find index of nearest hourly time to current_time
                time_diffs = [abs((ht - current_time).total_seconds()) for ht in hourly_times]
                nearest_index = time_diffs.index(min(time_diffs))

                humidity_list = hourly.get("relative_humidity_2m", [])
                rainfall_list = hourly.get("precipitation", [])
                uv_index_list = hourly.get("uv_index", [])

                if nearest_index < len(humidity_list):
                    humidity = humidity_list[nearest_index]
                if nearest_index < len(rainfall_list):
                    rainfall = rainfall_list[nearest_index]
                if nearest_index < len(uv_index_list):
                    uv_index = uv_index_list[nearest_index]

        if "time" in daily and daily["time"]:
            current_date_str = current.get("time", "")[:10]
            if current_date_str in daily["time"]:
                idx = daily["time"].index(current_date_str)
                sunrise_list = daily.get("sunrise", [])
                sunset_list = daily.get("sunset", [])
                if idx < len(sunrise_list):
                    sunrise_iso = sunrise_list[idx]
                    sunrise_dt = datetime.fromisoformat(sunrise_iso)
                    sunrise = sunrise_dt.strftime("%I:%M %p").lstrip('0')
                if idx < len(sunset_list):
                    sunset_iso = sunset_list[idx]
                    sunset_dt = datetime.fromisoformat(sunset_iso)
                    sunset = sunset_dt.strftime("%I:%M %p").lstrip('0')

        return {
            "location": {"lat": lat, "lon": lon},
            "temperature": current.get("temperature"),
            "humidity": humidity,
            "wind_speed": current.get("windspeed"),
            "rainfall": rainfall,
            "uv_index": uv_index,
            "sunrise": sunrise,
            "sunset": sunset,
            "time": current.get("time")
        }

    except Exception as e:
        return {"error": str(e)}