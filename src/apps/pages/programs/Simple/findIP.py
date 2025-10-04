import pyperclip
import requests
import streamlit as st


def get_ip(url):
  try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json().get("ip", "N/A")
  except Exception as e:
    return f"Error: {e}"


def findIP():
  st.title("🌏 Your Public IP Addresses")

  ipv4 = get_ip("https://api.ipify.org?format=json")
  ipv6 = get_ip("https://api64.ipify.org?format=json")

  col1, col2 = st.columns(2)
  with col1:
    st.metric(label="IPV4", value=ipv4)
    if st.button("Copy IPV4"):
      pyperclip.copy(ipv4)
      st.success("Copied IPV4 to clipboard!", icon="✅")

  with col2:
    st.metric(label="IPV6", value=ipv6)
    if st.button("Copy IPV6"):
      pyperclip.copy(ipv6)
      st.success("Copied IPV6 to clipboard!", icon="✅")
