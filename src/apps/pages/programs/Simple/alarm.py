import datetime
import time

import streamlit as st


def alarm():
  col1, col2, col3 = st.columns(3)
  with col1:
    hour = st.number_input("Hour", min_value=0, max_value=23, key="hour")
  with col2:
    minute = st.number_input("Minute", min_value=0, max_value=59, key="minute")
  with col3:
    second = st.number_input("Second", min_value=0, max_value=59, key="second")

  alarm_time = f"{hour:02d}:{minute:02d}:{second:02d}"

  col4, col5 = st.columns(2)
  with col4:
    message_option = st.radio("Choose Alarm Message Option", ("Predefined Message", "Custom Message"), key="msg_opt")
    if message_option == "Predefined Message":
      predefined_messages = ["Time's up!", "Wake up!", "Meeting time!", "Take a break!"]
      alarm_message = st.selectbox("Choose a predefined message", predefined_messages, key="predef_msg")
    else:
      alarm_message = st.text_area("Enter your custom message", "Time's up!", key="custom_msg")

  with col5:
    note_option = st.radio("Choose Note/Link Option", ("None", "Custom Note/Link"), key="note_opt")
    alarm_note = st.text_area("Enter your link or note here", "", key="custom_note") if note_option == "Custom Note/Link" else "No note or link"

  if st.button("Set Alarm"):
    now = datetime.datetime.now()
    alarm_dt = now.replace(hour=int(hour), minute=int(minute), second=int(second), microsecond=0)
    if alarm_dt <= now:
      st.toast(f"(> {datetime.datetime.now().strftime('%H:%M:%S')}) Alarm time must be in the future.", icon="⚠️")
    elif (alarm_dt - now).total_seconds() > 3600:
      st.toast("Alarm time must be within the next hour.", icon="⚠️")
    else:
      st.success(f"Alarm set for {alarm_time}.", icon="⏰")
      st.toast("Waiting for alarm...", icon="⏰")
      while True:
        current_time = datetime.datetime.now()
        if current_time >= alarm_dt:
          st.balloons()
          st.warning(alarm_message, icon="⚠️")
          st.info(f"Note/Link: {alarm_note}", icon="ℹ️")
          st.toast("Alarm triggered!", icon="🔔")
          break
        time.sleep(1)
