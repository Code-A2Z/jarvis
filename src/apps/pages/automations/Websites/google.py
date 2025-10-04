import pywhatkit
import streamlit as st
from pywikihow import search_wikihow


# TODO: Implement the google function which will search the query on google and display the first result from google.
def google():
  query = st.text_input("Enter your query")
  if query and st.button("Search"):
    pywhatkit.search(query)
    result = search_wikihow(query=query, max_results=1)
    st.write(result[0].summary)
