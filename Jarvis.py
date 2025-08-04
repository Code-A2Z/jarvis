import streamlit as st

from src.helpers.structPages import structPages
from src.helpers.getFolders import getFolders

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

  # For development - always show all pages (remove this for production)
  # In production, uncomment the authentication check below
  
  MAIN_DIR = "src/apps/pages"
  folders = getFolders(MAIN_DIR)
  if folders:
    for folder_name, folder_dir in folders.items():
      pages[folder_name.title()] = structPages(f"{MAIN_DIR}/{folder_dir}")

  # Production authentication (commented out for development)
  # if st.session_state.get('logged_in', False):
  #   MAIN_DIR = "src/apps/pages"
  #   folders = getFolders(MAIN_DIR)
  #   if folders:
  #     for folder_name, folder_dir in folders.items():
  #       pages[folder_name.title()] = structPages(f"{MAIN_DIR}/{folder_dir}")
  #
  #   # Check admin privileges
  #   user_email = st.session_state.get('user_email', '')
  #   user_name = st.session_state.get('user_name', '')
  #   
  #   try:
  #     admin_email = st.secrets["general"]["ADMIN_EMAIL"]
  #     admin_name = st.secrets["general"]["ADMIN_NAME"]
  #     
  #     if user_email == admin_email and user_name == admin_name:
  #       pages.update({
  #         "Admin": [
  #           st.Page("src/apps/auth/env.py", title="Environment Variables", icon=":material/security:"),
  #         ]
  #       })
  #   except KeyError:
  #     # Skip admin section if secrets not configured
  #     pass

  return st.navigation(pages)

application().run()

