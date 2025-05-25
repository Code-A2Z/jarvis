import streamlit as st
import requests

def get_quote():
  response = requests.get("https://zenquotes.io/api/today")
  if response.status_code == 200:
    return response.json()[0]
  else:
    return None

def quote():
  st.markdown("## 🗣️ Quote of the Day")
  quote = get_quote()
  if quote:
    st.markdown(f"#### 💭 **{quote['q']}**")
    st.markdown(f"> #### **{quote['a']}**")
  else:
    st.error("Couldn't fetch a quote at this moment. Please try again later.", icon="🚨")
