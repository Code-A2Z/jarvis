import requests
import streamlit as st


def advice():
  res = requests.get("https://api.adviceslip.com/advice").json()
  advice_text = res["slip"]["advice"]
  st.markdown(f"#### 💡 **{advice_text}**")

  if st.button("🔄 Reload Advice"):
    st.session_state["reload_advice"] = not st.session_state.get("reload_advice", False)
