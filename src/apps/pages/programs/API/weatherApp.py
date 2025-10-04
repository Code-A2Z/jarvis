import os

import requests
import streamlit as st

from src.helpers.checkKeyExist import isKeyExist
from src.helpers.displayInstructions import showInstructions

api_guide = """### How to get your API Key:
1. Visit [WeatherAPI.com](https://www.weatherapi.com/).
2. Sign up for a free account.
3. Generate an API key from your account dashboard.
4. Enter the API key in the input field.
"""


def getWeather(api_key, city):
  try:
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      weather = {
        "city": data["location"]["name"],
        "country": data["location"]["country"],
        "temperature": data["current"]["temp_c"],
        "humidity": data["current"]["humidity"],
        "pressure": data["current"]["pressure_mb"],
        "wind_speed": data["current"]["wind_kph"],
        "condition": data["current"]["condition"]["text"],
        "icon": data["current"]["condition"]["icon"],
        "feels_like": data["current"]["feelslike_c"],
        "last_updated": data["current"]["last_updated"],
      }
      return weather, None
    else:
      return None, data.get("error", {}).get("message", "Unknown error")
  except Exception as e:
    return None, str(e)


def weatherApp():
  exists = isKeyExist("WEATHER_API_KEY", "api_key")
  if not exists["WEATHER_API_KEY"]:
    showInstructions(markdown_text=api_guide, fields="WEATHER_API_KEY")
    st.stop()

  api_key = os.environ.get("WEATHER_API_KEY") or st.secrets["api_key"]["WEATHER_API_KEY"]
  city = st.text_input("Enter City Name")

  if st.button("Get Weather") and city:
    weather, error = getWeather(api_key, city)
    if weather:
      st.subheader(f"Weather in {weather['city']}, {weather['country']}")
      col1, col2 = st.columns(2)
      with col1:
        st.image(f"http:{weather['icon']}")
        st.write(f"**{weather['condition']}**")
      with col2:
        st.write(f"**Temperature:** {weather['temperature']} °C")
        st.write(f"**Feels Like:** {weather['feels_like']} °C")
        st.write(f"**Humidity:** {weather['humidity']} %")
        st.write(f"**Pressure:** {weather['pressure']} hPa")
        st.write(f"**Wind Speed:** {weather['wind_speed']} kph")
      st.info(f"**Last Updated:** {weather['last_updated']}", icon="ℹ️")
    else:
      st.toast("Please provide both API Key and City Name.", icon="🚨")
      st.error(error, icon="🚨")
