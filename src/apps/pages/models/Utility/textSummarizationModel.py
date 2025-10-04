import streamlit as st
from transformers import pipeline


@st.cache_resource(show_spinner=True)
def load_summarizer():
  return pipeline("summarization", model="t5-small")


def textSummarizationModel():
  user_input = st.text_area("Enter the text you'd like to summarize (minimum 50 words)", height=200)
  if st.button("Summarize") and len(user_input.split()) >= 50:
    summarizer = load_summarizer()
    with st.spinner("Summarizing..."):
      summary = summarizer(user_input, max_length=150, min_length=30, do_sample=False)
      st.info(summary, icon="ℹ️")
