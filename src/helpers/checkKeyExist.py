import os

import streamlit as st


def isKeyExist(keys, folder=None):
  """
  Check if one or more keys exist in Streamlit secrets or environment variables.

  Args:
    keys (str or list): A single key or a list of keys to check.
    folder (str, optional): Folder in st.secrets to look for keys.

  Returns:
    dict: A dictionary with keys as input and boolean values indicating existence.
  """
  if isinstance(keys, str):
    keys = [keys]
  secrets = st.secrets.get(folder, {}) if folder else st.secrets
  result = {}
  for key in keys:
    result[key] = bool(secrets.get(key) or os.environ.get(key))
  return result
