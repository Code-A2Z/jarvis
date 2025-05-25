import streamlit as st

def shift_char(c, s):
  if c.isupper():
    return chr((ord(c) - 65 + s) % 26 + 65)
  if c.islower():
    return chr((ord(c) - 97 + s) % 26 + 97)
  return c

def caeserCipher():
  col1, col2 = st.columns(2)
  with col1:
    text = st.text_input("Enter the word")
  with col2:
    direction = st.selectbox("Cipher direction", ['Encode', 'Decode'])
  shift = st.slider("Enter the shift amount", min_value=1, max_value=100, value=7, step=1)

  if st.button('Generate'):
    if text:
      s = shift if direction == 'Encode' else -shift
      result = ''.join(shift_char(c, s) for c in text)
      st.success(result, icon="✅")
    else:
      st.warning("You have not given any input", icon="⚠️")
