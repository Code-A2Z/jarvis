import streamlit as st
import requests

def advice():
  res = requests.get("https://api.adviceslip.com/advice").json()
  advice_text = res['slip']['advice']
  st.markdown(f"#### 💡 **{advice_text}**")
