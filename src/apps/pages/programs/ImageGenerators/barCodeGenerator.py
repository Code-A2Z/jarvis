import io

import streamlit as st
from barcode import EAN8, EAN13, UPCA
from barcode.writer import ImageWriter

BARCODE_TYPE = {"EAN-13": [13, EAN13], "EAN-8": [8, EAN8], "UPCA": [12, UPCA]}


def generate(num, option):
  if BARCODE_TYPE[option][0] != len(num):
    st.warning(f"Please enter a {BARCODE_TYPE[option][0]} digits long barcode number", icon="⚠️")
    st.stop()

  output = io.BytesIO()
  my_code = BARCODE_TYPE[option][1](num, writer=ImageWriter())
  my_code.write(output)
  output.seek(0)

  st.image(output, caption=f"Generated Barcode - {num}")
  st.download_button(label="Download Image", data=output, file_name=num + ".png", mime="image/png")


def barCodeGenerator():
  option = st.radio("Select type of Barcode", ["EAN-13", "EAN-8", "UPCA"], horizontal=True)
  num = st.number_input(
    "Enter barcode number",
    format="%d",
    min_value=10 ** (BARCODE_TYPE[option][0] - 1),
    max_value=10 ** BARCODE_TYPE[option][0] - 1,
    placeholder=f"Enter {BARCODE_TYPE[option][0]} digits long barcode number",
  )

  if st.button("Generate barcode"):
    generate(str(num), option)
