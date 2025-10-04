import time

import streamlit as st


def timer():
  st.info("This is a simple timer application.", icon="⏳")

  col1, col2, col3 = st.columns(3)
  with col1:
    hour = st.number_input("Hour", min_value=0, max_value=23, value=0)
  with col2:
    minute = st.number_input("Minute", min_value=0, max_value=59, value=0)
  with col3:
    second = st.number_input("Second", min_value=0, max_value=59, value=0)

  if st.button("Start Timer"):
    countdown_time = hour * 3600 + minute * 60 + second

    timer_message = st.empty()
    timer_message.info(f"Timer set for {hour} hours, {minute} minutes, and {second} seconds.", icon="🕒")

    while countdown_time:
      min, sec = divmod(countdown_time, 60)
      hour, min = divmod(min, 60)
      timer_message.info(f"Timer set for {hour} hours, {min} minutes, and {sec} seconds.", icon="🕒")
      countdown_time -= 1
      time.sleep(1)

    st.balloons()
    timer_message.success("Time's up!", icon="🎉")
