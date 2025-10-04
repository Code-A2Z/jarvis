from json import loads

import streamlit as st
from requests import get


def joke():
  response = get("https://official-joke-api.appspot.com/random_joke")
  joke_question = loads(response.text)["setup"].title()
  joke_response = loads(response.text)["punchline"].title()
  st.markdown(f"#### 🤔 **{joke_question}**")
  st.markdown(f"> #### **{joke_response}**")

  if st.button("🔄 Reload Joke"):
    st.session_state["reload_joke"] = not st.session_state.get("reload_joke", False)
