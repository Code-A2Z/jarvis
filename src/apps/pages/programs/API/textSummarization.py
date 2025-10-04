import os

import streamlit as st
from groq import Groq

from src.helpers.checkKeyExist import isKeyExist
from src.helpers.displayInstructions import showInstructions

api_guide = """
Get your Groq API Key
1. Visit [Groq Console](https://console.groq.com/keys).
2. Sign up or log in with your account.
3. Navigate to the **API Keys** section.
4. Click on **+ Create Key** to generate a new API key.
"""


def load_credentials():
  exists = isKeyExist("GROQ_API_KEY", "api_key")
  if not exists["GROQ_API_KEY"]:
    showInstructions(markdown_text=api_guide, fields="GROQ_API_KEY")
    st.stop()


@st.cache_resource
def load_summarizer():
  """Initialize Groq client - replaces the transformers pipeline"""
  api_key = os.environ.get("GROQ_API_KEY") or st.secrets["api_key"]["GROQ_API_KEY"]
  return Groq(api_key=api_key)


def textSummarization():
  load_credentials()
  user_input = st.text_area("Enter the text you'd like to summarize (minimum 50 words)", height=200)
  if st.button("Summarize") and len(user_input.split()) >= 50:
    summarizer = load_summarizer()
    with st.spinner("Summarizing..."):
      chat_completion = summarizer.chat.completions.create(
        messages=[
          {"role": "system", "content": "You are a helpful assistant that summarizes text. Return only the content"},
          {"role": "user", "content": f"Please provide a concise and short summary of the following text\n\n{user_input}"},
        ],
        model="llama-3.1-8b-instant",
        max_tokens=150,
        temperature=0.3,
      )

      summary_text = chat_completion.choices[0].message.content
      st.info(summary_text, icon="ℹ️")
