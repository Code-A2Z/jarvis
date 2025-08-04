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
  # Initialize session state
  if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
  
  if not st.session_state.logged_in:
    st.title("🔐 Login Required")
    st.write("Please authenticate to access your profile.")
    
    # Simple authentication (you can replace with actual OAuth)
    with st.form("login_form"):
      username = st.text_input("Username")
      password = st.text_input("Password", type="password")
      submit = st.form_submit_button("Login")
      
      if submit and username and password:
        # Simple check (replace with actual authentication)
        if username == "admin" and password == "admin123":
          st.session_state.logged_in = True
          st.session_state.user_name = "Admin User"
          st.session_state.user_email = "admin@jarvis.ai"
          st.rerun()
        else:
          st.error("Invalid credentials")

  else:
    user_name = st.session_state.get('user_name', 'User')
    user_email = st.session_state.get('user_email', 'unknown@email.com')
    
    st.title(f"🙏 {GreetUser(user_name)}")
    st.success("Welcome to Jarvis AI Assistant!", icon="🤝")
    st.write("Name:", user_name)
    st.write("Email:", user_email)

    if st.button("Log out"):
      st.toast(f"Goodbye, {user_name}! See you soon!", icon="🚪")
      st.session_state.logged_in = False
      st.session_state.pop('user_name', None)
      st.session_state.pop('user_email', None)
      sleep(2)
      st.rerun()

auth()
