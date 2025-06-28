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
        st.write("Please authenticate using your preferred account to access your profile.")

        # Dual login options: Google and GitHub
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔓 Login with Google"):
                st.login("google")

        with col2:
            if st.button("🐱 Login with GitHub"):
                st.login("github")

    else:
        st.title(f"🙏 {GreetUser(st.user.given_name)}")
        st.success("Welcome to Jarvis AI Assistant!", icon="🤝")
        st.image(st.user.picture, caption=st.user.name)
        st.write("Email:", st.user.email)

        if st.button("Log out"):
            st.toast(f"Goodbye, {st.user.name}! See you soon!", icon="🚪")
            sleep(2)
            st.logout()

auth()
