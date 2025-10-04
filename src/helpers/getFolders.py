import os

import streamlit as st

from src.helpers.camelToReadable import camelToReadable


def getFolders(MODULE_FOLDER_PATH):
  try:
    files = [f for f in os.listdir(MODULE_FOLDER_PATH) if os.path.isdir(os.path.join(MODULE_FOLDER_PATH, f)) and not f.startswith("__")]
  except FileNotFoundError:
    st.error("The specified directory does not exist.")
    return {}

  folders = {}
  for folder in files:
    readable_name = camelToReadable(folder)
    folders[readable_name] = folder
  return folders
