import streamlit as st
import requests
from bs4 import BeautifulSoup

def horoscope():
    def get_horoscope_by_day(zodiac_sign: int, day: str):
        try:
            if not "-" in day:
                res = requests.get(f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-{day}.aspx?sign={zodiac_sign}")
            else:
                day = day.replace("-", "")
                res = requests.get(f"https://www.horoscope.com/us/horoscopes/general/horoscope-archive.aspx?sign={zodiac_sign}&laDate={day}")
            
            soup = BeautifulSoup(res.content, 'html.parser')
            data = soup.find('div', attrs={'class': 'main-horoscope'})
            return data.p.text, None
        except Exception as e:
            return None, str(e)

    zodiac_signs = {
        "Aries": 1, "Taurus": 2, "Gemini": 3, "Cancer": 4, "Leo": 5, "Virgo": 6, "Libra": 7, "Scorpio": 8, "Sagittarius": 9, "Capricorn": 10, "Aquarius": 11, "Pisces": 12
        }

    st.title("Daily Horoscope")

    sign = st.selectbox("Select your Zodiac sign", options=list(zodiac_signs.keys()))
    day = st.selectbox("Select the day", options=["today", "yesterday", "tomorrow"])
    convert_button = st.button(label="Get Horoscope")

    if convert_button:
        zodiac_sign = zodiac_signs[sign]
        horoscope_text, error = get_horoscope_by_day(zodiac_sign, day)
        if horoscope_text:
            st.success(horoscope_text)
        else:
            st.error(f"Could not retrieve horoscope data: {error}")