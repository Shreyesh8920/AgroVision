import requests
from datetime import date, timedelta

def get_soil(lat: float, lon: float):
    """
    Fetch environmental data (soil moisture, soil temperature, humidity, precipitation) from Open-Meteo.
    Returns a structured dictionary with soil moisture, soil temperature, humidity, and average rainfall.
    """
    def fetch_open_meteo(lat, lon):
        url = "https://api.open-meteo.com/v1/forecast"
        today = date.today()
        start_date = today - timedelta(days=7)
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "soil_moisture_0_to_7cm,soil_temperature_0cm,relative_humidity_2m,precipitation",
            "timezone": "UTC",
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": today.strftime("%Y-%m-%d")
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    try:
        # Fetch Open-Meteo data
        try:
            meteo_data = fetch_open_meteo(lat, lon)
            hourly = meteo_data.get("hourly", {})
            soil_moisture_list = hourly.get("soil_moisture_0_to_7cm", [])
            soil_temperature_list = hourly.get("soil_temperature_0cm", [])
            humidity_list = hourly.get("relative_humidity_2m", [])
            precipitation_list = hourly.get("precipitation", [])

            soil_moisture_values = [float(x) for x in soil_moisture_list if x is not None]
            soil_temperature_values = [float(x) for x in soil_temperature_list if x is not None]
            humidity_values = [float(x) for x in humidity_list if x is not None]
            precipitation_values = [float(x) for x in precipitation_list if x is not None]

            if not soil_moisture_values:
                raise ValueError("Missing soil moisture data from Open-Meteo")
            if not soil_temperature_values:
                raise ValueError("Missing soil temperature data from Open-Meteo")
            if not humidity_values:
                raise ValueError("Missing humidity data from Open-Meteo")
            if not precipitation_values:
                raise ValueError("Missing precipitation data from Open-Meteo")

            avg_soil_moisture = sum(soil_moisture_values) / len(soil_moisture_values)
            avg_soil_temperature = sum(soil_temperature_values) / len(soil_temperature_values)
            avg_humidity = sum(humidity_values) / len(humidity_values)
            avg_precipitation = sum(precipitation_values) / len(precipitation_values)
        except Exception as e:
            return {"error": f"Failed to fetch Open-Meteo data: {str(e)}"}

        return {
            "soil_moisture": round(avg_soil_moisture, 3),
            "soil_temperature": round(avg_soil_temperature, 2),
            "humidity": round(avg_humidity, 2),
            "avg_rainfall": round(avg_precipitation, 3)
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}