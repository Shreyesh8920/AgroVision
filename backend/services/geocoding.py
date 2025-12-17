# backend/services/geocoding.py
import requests

def geocode(location=None, lat=None, lon=None):
    """
    Geocode a location string or reverse-geocode latitude/longitude coordinates.
    Returns (lat, lon, {"district": ..., "state": ..., "city": ...})
    """
    headers = {"User-Agent": "CropRecoApp/1.0 (student project)"}
    try:
        if location is not None:
            # Forward geocoding
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": location,
                "format": "json",
                "addressdetails": 1,
                "limit": 1
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if not data:
                return None, None, {"district": None, "state": None, "city": None}
            lat_val = float(data[0]["lat"])
            lon_val = float(data[0]["lon"])
            address = data[0].get("address", {})
        elif lat is not None and lon is not None:
            # Reverse geocoding using Google Maps Geocoding API restricted to India
            url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                "latlng": f"{lat},{lon}",
                "key": "YOUR_GOOGLE_API_KEY",
                "result_type": "locality|administrative_area_level_2|administrative_area_level_1",
                "language": "en",
                "components": "country:IN"
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("status") != "OK" or not data.get("results"):
                return None, None, {"district": None, "state": None, "city": None, "location_name": "Unknown Location"}

            # Parse address components
            components = {}
            for component in data["results"][0]["address_components"]:
                types = component.get("types", [])
                if "administrative_area_level_2" in types:
                    components["district"] = component.get("long_name")
                if "administrative_area_level_1" in types:
                    components["state"] = component.get("long_name")
                if "locality" in types:
                    components["city"] = component.get("long_name")
                if "sublocality" in types and "city" not in components:
                    components["city"] = component.get("long_name")
                if "postal_town" in types and "city" not in components:
                    components["city"] = component.get("long_name")

            # Confirm that location is in India by checking country component
            country_found = False
            for component in data["results"][0]["address_components"]:
                if "country" in component.get("types", []) and component.get("short_name") == "IN":
                    country_found = True
                    break
            if not country_found:
                return None, None, {"district": None, "state": None, "city": None, "location_name": "Unknown Location"}

            lat_val = float(lat)
            lon_val = float(lon)
            district = components.get("district")
            state = components.get("state")
            city = components.get("city") or district or state

            # Updated location_name fallback order for reverse geocoding
            location_name = city or district or state or "Unknown Location"

            address = {
                "district": district,
                "state": state,
                "city": city,
                "location_name": location_name
            }
        else:
            return None, None, {"error": "Either location or lat/lon must be provided."}

        if location is not None:
            district = (
                address.get("county") or
                address.get("state_district") or
                address.get("region")
            )
            state = address.get("state")
            # Updated city fallback order
            city = (address.get("city") or address.get("town") or address.get("village") or
                    address.get("suburb") or district or state)

            # Updated location_name fallback order for forward geocoding
            location_name = (address.get("city") or address.get("town") or address.get("village") or
                             address.get("suburb") or district or state or "Unknown Location")

            return lat_val, lon_val, {
                "district": district,
                "state": state,
                "city": city,
                "location_name": location_name
            }
        else:
            return lat_val, lon_val, address
    except Exception as e:
        return None, None, {"error": str(e)}