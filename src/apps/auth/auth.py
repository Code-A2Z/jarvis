from datetime import datetime
import streamlit as st
from time import sleep
import pytz

from src.utils.greeting import GreetUser

def unix_to_ist(timestamp):
    india_tz = pytz.timezone('Asia/Kolkata')
    format_str = '%I:%M:%S %p IST'
    return datetime.fromtimestamp(timestamp, pytz.utc).astimezone(india_tz).strftime(format_str)

def auth():
    if st.user and not st.user.is_logged_in:
        st.title("🔐 Login Required")
        st.write("Please authenticate to access your profile.")

        provider = st.selectbox("Choose login provider", ["Google", "GitHub"])
        login_btn = st.button("🔓 Authenticate")

        if login_btn:
            if provider == "Google":
                st.login("google")
            elif provider == "GitHub":
                st.login("github")

    else:
        # Attribute fallbacks to prevent crashes
        given_name = getattr(st.user, "given_name", None) or getattr(st.user, "name", "User")
        full_name = getattr(st.user, "name", given_name)
        picture = getattr(st.user, "picture", None)
        email = getattr(st.user, "email", "N/A")

        st.title(f"🙏 {GreetUser(given_name)}")
        st.success("Welcome to Jarvis AI Assistant!", icon="🤝")

        if picture:
            st.image(picture, caption=full_name)
        st.write("Email:", email)

        if st.button("Log out"):
            st.toast(f"Goodbye, {full_name}! See you soon!", icon="🚪")
            sleep(2)
            st.logout()

auth()
