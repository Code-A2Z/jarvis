import requests
import streamlit as st


def fetch_location_from_ip(ip_address):
  url = f"http://ip-api.com/json/{ip_address}"
  response = requests.get(url)
  data = response.json()

  if data.get("status") == "success":
    return {
      "City": data.get("city", "N/A"),
      "Region": data.get("regionName", "N/A"),
      "Country": data.get("country", "N/A"),
      "Latitude": data.get("lat", "N/A"),
      "Longitude": data.get("lon", "N/A"),
      "ORG": data.get("org", "N/A"),
      "ZIP": data.get("zip", "N/A"),
      "Timezone": data.get("timezone", "N/A"),
    }
  return None


def locationSearch():
  st.info("Enter an IP address to find its location.", icon="ℹ️")
  ip_address = st.text_input("Enter an IP address", placeholder="e.g., 54.49.176.72")

  if st.button("Find Location") and ip_address:
    with st.spinner("Fetching Location..."):
      location_info = fetch_location_from_ip(ip_address.strip())

    if location_info:
      col1, col2 = st.columns(2)
      with col1:
        st.metric(label="City", value=location_info["City"])
        st.metric(label="Region", value=location_info["Region"])
        st.metric(label="Country", value=location_info["Country"])
        st.metric(label="ZIP", value=location_info["ZIP"])
      with col2:
        st.metric(label="Timezone", value=location_info["Timezone"])
        st.metric(label="Latitude", value=location_info["Latitude"])
        st.metric(label="Longitude", value=location_info["Longitude"])
        st.metric(label="Organization", value=location_info["ORG"])
    else:
      st.error("Could not fetch location. Try another IP!", icon="❌")
