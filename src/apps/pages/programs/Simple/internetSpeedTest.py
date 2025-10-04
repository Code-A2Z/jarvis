import speedtest
import streamlit as st


def internetSpeedTest():
  if st.button("🏃‍➡️ Run Speed Test"):
    sp_test = speedtest.Speedtest()
    sp_test.get_best_server()
    download_speed = sp_test.download() / 1000000
    upload_speed = sp_test.upload() / 1000000
    ping = sp_test.results.ping

    col1, col2, col3 = st.columns(3)
    with col1:
      st.metric(label="Download Speed", value=f"{download_speed:.2f} Mbps")
    with col2:
      st.metric(label="Upload Speed", value=f"{upload_speed:.2f} Mbps")
    with col3:
      st.metric(label="Ping", value=f"{ping:.2f} ms")
    st.toast("Speed Test Completed!", icon="✅")
