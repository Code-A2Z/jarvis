import streamlit as st
from groq import Groq
import os

from src.helpers.displayInstructions import showInstructions
from src.helpers.checkKeyExist import isKeyExist

api_guide = """
    ### How to get your Groq API Key:
    1. Visit [Groq Console](https://console.groq.com/keys).
    2. Sign up or log in with your account.
    3. Navigate to the **API Keys** section.
    4. Click on **+ Create Key** to generate a new API key.
    5. Copy the key and paste it in the input field below.
"""

@st.cache_resource(show_spinner=True)
def load_summarizer():
    """Initialize Groq client - replaces the transformers pipeline"""
    exists = isKeyExist("GROQ_API_KEY", "api_key")
    if not exists["GROQ_API_KEY"]:
        showInstructions(markdown_text=api_guide, fields="GROQ_API_KEY")
        st.stop()

    api_key = (os.environ.get("GROQ_API_KEY") or st.secrets['api_key']["GROQ_API_KEY"])
    return Groq(api_key=api_key)

def textSummarization():
    user_input = st.text_area("Enter the text you'd like to summarize (minimum 50 words)", height=200, placeholder="Type or paste your text here...")
    if st.button("Summarize"):
        summarizer = load_summarizer()
        if len(user_input.split()) < 50:
            st.toast("Please enter at least 50 words for summarization.", icon="⚠️")
        else:
            with st.spinner("Summarizing..."):
                # Use Groq API instead of transformers pipeline.
                chat_completion = summarizer.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are a helpful assistant that summarizes text. Return only the content"
                        },
                        {
                            "role": "user",
                            "content": f"Please provide a concise and short summary of the following text\n\n{user_input}"
                        }
                    ],
                    model="llama-3.1-8b-instant",  # Fast and efficient model
                    max_tokens=150,
                    temperature=0.3
                )
                
                summary_text = chat_completion.choices[0].message.content
                st.subheader("Summary:")
                st.write(summary_text)
