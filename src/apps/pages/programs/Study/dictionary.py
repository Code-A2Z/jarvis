import streamlit as st
from PyMultiDictionary import MultiDictionary

def dictionary():
  word = st.text_input("Enter the Word", placeholder="Type a word to get its meaning, synonym, or antonym")
  if st.button('Search dictionary') and word:
    dictionary = MultiDictionary()
    meaning = dictionary.meaning('en', word)
    synonyms = dictionary.synonym('en', word)
    antonyms = dictionary.antonym('en', word)
    with st.expander(word, expanded=True):
      st.write(f"**Meaning:** {meaning}")
      st.write(f"**Synonyms:** {synonyms}")
      st.write(f"**Antonyms:** {antonyms}")
