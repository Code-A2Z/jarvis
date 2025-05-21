from requests import get
from json import loads
import streamlit as st

def fact():
  response = get('https://uselessfacts.jsph.pl/api/v2/facts/random')
  fact = loads(response.text)['text'].title()
  st.markdown(f"#### 🤔 **{fact}**")

  if st.button("🔄 Reload Fact"):
    st.session_state['reload_fact'] = not st.session_state.get('reload_fact', False)
