import pandas as pd
import streamlit as st


# TODO: Rectify the error in the sendMsg function
def sendMsg(phone_no, message):
  import time

  import pyautogui
  import pywhatkit

  pywhatkit.sendwhatmsg_instantly(phone_no, message)
  time.sleep(1)
  pyautogui.press("enter")
  time.sleep(1)
  pyautogui.hotkey("ctrl", "w")
  time.sleep(1)


def whatsApp():
  st.markdown("### WhatsApp Automation 📨")
  st.write("This app sends a WhatsApp message to all the contacts in the CSV file.")

  st.markdown("#### Upload a CSV file with phone numbers:")
  uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
  bottom = st.number_input("Enter the bottom range of phone numbers:", min_value=0, value=0)
  top = st.number_input("Enter the top range of phone numbers:", min_value=bottom + 1, value=bottom + 1)
  message = st.text_area("Enter the message to send:")

  if uploaded_file is not None:
    if st.button("Send WhatsApp Message"):
      if message == "":
        st.warning('Please upload a CSV file with a column named "Phone Number".', icon="⚠️")
        return

      df = pd.read_csv(uploaded_file)
      if top > len(df):
        st.warning("The top range of phone numbers exceeds the total number of phone numbers in the CSV file.", icon="⚠️")
        return

      if "phone_number" not in df.columns:
        st.warning('Please upload a CSV file with a column named "phone_number".', icon="⚠️")
        return

      for index, row in df.iterrows():
        if index >= bottom and index < top:
          try:
            sendMsg(row["phone_number"], message)
          except Exception as e:
            st.error(f"Message Sending Error: {e}")
            st.stop()

      st.write("All messages sent successfully!")
  else:
    st.info("Please upload a CSV file to send messages.", icon="ℹ️")
