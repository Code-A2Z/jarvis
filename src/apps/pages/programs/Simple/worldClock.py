from datetime import datetime

import pytz
import streamlit as st

cities = {
  "Auckland": "Pacific/Auckland",
  "Sydney": "Australia/Sydney",
  "Tokyo": "Asia/Tokyo",
  "Seoul": "Asia/Seoul",
  "Hong Kong": "Asia/Hong_Kong",
  "Beijing": "Asia/Shanghai",
  "Singapore": "Asia/Singapore",
  "Bangkok": "Asia/Bangkok",
  "Jakarta": "Asia/Jakarta",
  "Delhi": "Asia/Kolkata",
  "Dubai": "Asia/Dubai",
  "Moscow": "Europe/Moscow",
  "Istanbul": "Europe/Istanbul",
  "Jerusalem": "Asia/Jerusalem",
  "Cairo": "Africa/Cairo",
  "Johannesburg": "Africa/Johannesburg",
  "Paris": "Europe/Paris",
  "Berlin": "Europe/Berlin",
  "Rome": "Europe/Rome",
  "London": "Europe/London",
  "Lisbon": "Europe/Lisbon",
  "Reykjavik": "Atlantic/Reykjavik",
  "Sao Paulo": "America/Sao_Paulo",
  "Buenos Aires": "America/Argentina/Buenos_Aires",
  "New York": "America/New_York",
  "Toronto": "America/Toronto",
  "Chicago": "America/Chicago",
  "Mexico City": "America/Mexico_City",
  "Denver": "America/Denver",
  "Los Angeles": "America/Los_Angeles",
  "San Francisco": "America/Los_Angeles",
  "Vancouver": "America/Vancouver",
}


def get_city_time(timezone):
  tz = pytz.timezone(timezone)
  city_time = datetime.now(tz)
  return city_time.strftime("%H:%M:%S"), city_time.strftime("%A, %Y-%m-%d")


def worldClock():
  cols = st.columns(2)
  for i, city in enumerate(cities.keys()):
    with cols[i % 2]:
      city_time, city_date = get_city_time(cities[city])
      st.markdown(f"### {city}")
      st.markdown(f"#### {city_time}")
      st.markdown(f"> #### {city_date}")
      st.divider()
