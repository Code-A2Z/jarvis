import base64
import os

import google.generativeai as genai
import streamlit as st

from src.helpers.checkKeyExist import isKeyExist
from src.helpers.displayInstructions import showInstructions

api_guide = """
To get started, obtain an API key from [Google - Gemini Vision API](https://makersuite.google.com/app/apikey)
"""


def validate_file_size(file):
  return file is not None and file.size <= 20 * 1024 * 1024


def vision():
  exists = isKeyExist("VISION_API_KEY", "api_key")
  if not exists["VISION_API_KEY"]:
    showInstructions(markdown_text=api_guide, fields="VISION_API_KEY")
    st.stop()

  api_key = st.secrets["api_key"]["VISION_API_KEY"] or os.environ["VISION_API_KEY"]
  genai.configure(api_key=api_key)

  images = st.file_uploader("Upload Image Files", type=["jpg", "png", "webp", "heic", "heif"], accept_multiple_files=True)

  prompt = st.text_input("Enter your prompt", placeholder="Type your prompt here...")
  if st.button("Generate") and images and prompt:
    oversized_files = [image.name for image in images if not validate_file_size(image)]
    if oversized_files:
      st.error(f"The following files exceed the 20MB size limit: {', '.join(oversized_files)}")
      st.stop()

    try:
      encoded_images = [{"mime_type": "image/jpeg", "data": base64.b64encode(image.read()).decode("utf-8")} for image in images]
      model = genai.GenerativeModel(model_name="gemini-1.5-flash")
      response = model.generate_content(encoded_images + [prompt])
      st.subheader("Generated Response")
      st.text_area("Output", value=response.text, height=300)
    except Exception as e:
      st.error(f"An error occurred: {e}", icon="🚨")
