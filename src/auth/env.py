import streamlit as st

def displayStreamlitSecrets(data, prefix=""):
  for key, value in data.items():
    full_key = f"{prefix}{key}"
    if isinstance(value, dict):
      st.divider()
      st.markdown(f"**{full_key}/**")
      displayStreamlitSecrets(value, prefix=full_key + "/")
    else:
      st.text_input(label=key, value=str(value), disabled=True, key=full_key)

def env():
  st.title("Environment Variables")
  st.markdown(
    """
    This page displays the environment variables used in the application. 
    The values are hidden for security reasons.
    """
  )
  if st.user.email == st.secrets["general"]["ADMIN_EMAIL"] and st.user.given_name == st.secrets["general"]["ADMIN_NAME"]:
    st.success("You are logged in as an admin.", icon="✅")
    displayStreamlitSecrets(st.secrets)
  else:
    st.warning("You are not authorized to view the environment variables.", icon="⚠️")

env()
