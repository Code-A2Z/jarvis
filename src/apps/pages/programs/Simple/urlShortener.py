import streamlit as st
import pyshorteners
import pyperclip

def shorten_url(input_url):
  shortener = pyshorteners.Shortener()
  short_url = shortener.tinyurl.short(input_url)
  return short_url

def urlShortener():
  input_url = st.text_input("Enter URL to be shortened", "")
  if st.button("✨ Shorten URL"):
    if input_url:  
      try:
        short_url = shorten_url(input_url)
        pyperclip.copy(short_url)
        st.success(f"**Shortened URL:** {short_url} and saved to your clipboard!", icon="✅")
      except Exception as e:
        st.error(f"Error occurred: {e}", icon="🚨")
    else:
      st.error("Please enter a valid URL.", icon="🚨")
