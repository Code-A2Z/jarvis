import streamlit as st

from src.helpers.structPages import structPages

def application():
  pages = {
    "": [
      st.Page("src/apps/public/home.py", title="Home", icon=":material/home:"),
      st.Page("src/apps/public/youtubePlaylist.py", title="Jarvis Videos", icon=":material/ondemand_video:"),
    ],
    "Account": [
      st.Page("src/apps/auth/auth.py", title="Authentication", icon=":material/lock_open:"),
    ],
  }
  if st.user and st.user.is_logged_in:
    MAIN_DIR = "src/apps/pages"
    pages.update({
      "Programs": structPages(f'{MAIN_DIR}/programs'),
      "Models": structPages(f'{MAIN_DIR}/models'),
      "Automations": structPages(f'{MAIN_DIR}/automations'),
    })
  if st.user.email == st.secrets["general"]["ADMIN_EMAIL"] and st.user.given_name == st.secrets["general"]["ADMIN_NAME"]:
    pages.update({
      "Admin": [
        st.Page("src/apps/auth/env.py", title="Environment Variables", icon=":material/security:"),
      ]
    })
  return st.navigation(pages)

application().run()
