import pywhatkit
import streamlit as st


# TODO: Explore the pywhatkit library and implement the youtube function or use any other library to implement the youtube function
def youtube():
  st.title("YouTube Search App")
  term = st.text_input("Enter the term you want to search on YouTube")
  if st.button("Search") and term != "":
    pywhatkit.playonyt(term)
