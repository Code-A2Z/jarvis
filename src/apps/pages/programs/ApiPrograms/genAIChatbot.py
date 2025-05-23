import google.generativeai as genai
import streamlit as st
import os

from src.helpers.displayInstructions import showInstructions
from src.helpers.checkKeyExist import isKeyExist

api_guide = """
Obtain an API key from [Google](https://ai.google.dev/gemini-api) and Enter it here.
"""

if "messages" not in st.session_state:
  st.session_state.messages = []

def geminiINIT():
  model = genai.GenerativeModel("gemini-1.5-flash")
  chat = model.start_chat(history=[])
  return chat

def generateResponse(chat_instance: genai.ChatSession, prompt: str):
  with st.chat_message("ai"):
    response = chat_instance.send_message(prompt, stream=True)
    for chunk in response:
      try:
        yield str(chunk.text)
      except ValueError as e:
        st.error("ValueError: You are not allowed to ask that kind of a prompt!")
  st.session_state.messages.append({"role": "ai", "content": response.text})

def displayHistory():
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.write(message["content"])

def genAIChatbot():
  exists = isKeyExist("GEMINI_API_KEY", "api_key")
  if not exists["GEMINI_API_KEY"]:
    showInstructions(markdown_text=api_guide, fields="GEMINI_API_KEY")
    prompt = None
    st.stop()

  GEMINI_API_KEY = (st.secrets['api_key']["GEMINI_API_KEY"] or os.environ["GEMINI_API_KEY"])
  genai.configure(api_key=GEMINI_API_KEY)
  prompt = st.chat_input("Let's chat!")
  msg = st.chat_message("ai")
  st.write("Hi! How can I help you today?")

  chat_instance = geminiINIT()
  displayHistory()

  if prompt != "" and prompt is not None:
    user_message = st.chat_message("user")
    st.session_state.messages.append({"role": "user", "content": prompt})
    user_message.write(prompt)
    response = generateResponse(chat_instance, prompt)
    st.write_stream(response)
