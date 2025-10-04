import random
import string

import streamlit as st


def generate_password(length, upper, lower, digits, special):
  chars = (
    (string.ascii_uppercase if upper else "")
    + (string.ascii_lowercase if lower else "")
    + (string.digits if digits else "")
    + (string.punctuation if special else "")
  )
  if not chars:
    st.error("Please select at least one character type!", icon="🚨")
    return ""
  return "".join(random.choice(chars) for _ in range(length))


def passwordGenerator():
  length = st.slider("Password length", min_value=4, max_value=30, value=8)

  col1, col2 = st.columns(2)
  with col1:
    upper = st.checkbox("Include capital A-Z letters", True)
  with col2:
    lower = st.checkbox("Include small a-z letters", True)

  col3, col4 = st.columns(2)
  with col3:
    digits = st.checkbox("Include 0-9 numbers", True)
  with col4:
    special = st.checkbox("Include special characters", True)

  pwd = ""
  if st.button("Generate Password", key="generate_password"):
    pwd = generate_password(length, upper, lower, digits, special)

  if pwd:
    st.code(pwd, language="text")
    st.toast("Password generated successfully!", icon="✅")
