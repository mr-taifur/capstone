import os
import requests
import dotenv

# Load environment variables
dotenv.load_dotenv()

OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")

# Climate-accurate simulated weather profiles for Bangladesh districts to serve as fallback
BANGLADESH_SIMULATED_WEATHER = {
    "dhaka": {
        "temp": 30.5,
        "humidity": 75,
        "rain_prob": 20,
        "description": "Scattered clouds"
    },
    "rajshahi": {
        "temp": 36.2,
        "humidity": 45,
        "rain_prob": 5,
        "description": "Sunny and hot"
    },
    "sylhet": {
        "temp": 27.8,
        "humidity": 92,
        "rain_prob": 85,
        "description": "Heavy monsoon showers"
    },
    "rangpur": {
        "temp": 23.4,
        "humidity": 87,
        "rain_prob": 60,
        "description": "Overcast and drizzling"
    },
    "mymensingh": {
        "temp": 17.5,
        "humidity": 89,
        "rain_prob": 50,
        "description": "Cool morning fog"
    },
    "chittagong": {
        "temp": 31.0,
        "humidity": 82,
        "rain_prob": 40,
        "description": "Breezy and humid"
    }
}

def get_weather(location: str) -> dict:
    """
    Fetches real-time weather data for a given district in Bangladesh.
    If the API call fails or no API key is set, it falls back to high-fidelity simulated climate profiles.
    
    Returns a dictionary with:
    - temp: Temperature in Celsius
    - humidity: Relative humidity in %
    - rain_prob: Estimated rain probability (0 to 100)%
    - description: Weather condition string
    - source: 'live' or 'simulated'
    """
    loc_clean = location.strip().lower()
    
    # 1. Attempt Live OpenWeather API query if key exists
    if OPENWEATHER_API_KEY:
        try:
            # Query standard API
            # OpenWeather uses city names. Append ',BD' for Bangladesh
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location},BD&appid={OPENWEATHER_API_KEY}&units=metric"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                description = data["weather"][0]["description"].capitalize()
                
                # OpenWeather 2.5 standard call doesn't always provide direct rain probability,
                # so we estimate it based on cloud cover or rain keys
                clouds = data.get("clouds", {}).get("all", 0)
                rain_data = data.get("rain", {})
                if rain_data:
                    rain_prob = 90
                else:
                    rain_prob = min(100, max(0, int(clouds * 0.8)))
                    
                return {
                    "temp": temp,
                    "humidity": humidity,
                    "rain_prob": rain_prob,
                    "description": description,
                    "source": "live"
                }
        except Exception as e:
            print(f"OpenWeather API call failed: {e}. Falling back to simulation.")
            
    # 2. Fallback to high-fidelity simulated weather for Bangladesh
    for district, profile in BANGLADESH_SIMULATED_WEATHER.items():
        if district in loc_clean:
            return {
                "temp": profile["temp"],
                "humidity": profile["humidity"],
                "rain_prob": profile["rain_prob"],
                "description": profile["description"],
                "source": "simulated"
            }
            
    # Default fallback profile (Dhaka average)
    return {
        "temp": 29.0,
        "humidity": 78,
        "rain_prob": 30,
        "description": "Partly cloudy",
        "source": "simulated_default"
    }
