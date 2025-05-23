import streamlit as st
import os

def showInstructions(markdown_text, fields):
  """
  Display instructions and input fields for one or more values.

  Args:
    markdown_text (str): Instructions to display.
    fields (list or str): Field name(s) to prompt for. Can be a string for a single field or a list of field names.
  """
  st.markdown(markdown_text)
  if isinstance(fields, str):
    fields = [fields]

  inputs = {}
  for field in fields:
    inputs[field] = st.text_input(f"Enter your {field.replace('_', ' ').capitalize()}", type="password")

  if st.button("Enter") and all(inputs[f] != "" for f in fields):
    for field in fields:
      os.environ[field] = inputs[field]
    st.rerun()
