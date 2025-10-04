import os
import tempfile

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.helpers.checkKeyExist import isKeyExist
from src.helpers.displayInstructions import showInstructions

api_guide = """
| Get your Groq API Key | Get your Google API Key |
|-----------------------|-------------------------|
| 1. Visit [Groq Console](https://console.groq.com/keys). | 1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey). |
| 2. Sign up or log in with your account. | 2. Generate an API key for Generative AI access. |
| 3. Navigate to the **API Keys** section. | |
| 4. Click on **+ Create Key** to generate a new API key. | |
"""


def load_credentials():
  exists = isKeyExist(["GROQ_API_KEY", "GOOGLE_API_KEY"], "api_key")
  if not exists["GROQ_API_KEY"] or not exists["GOOGLE_API_KEY"]:
    showInstructions(markdown_text=api_guide, fields=["GROQ_API_KEY", "GOOGLE_API_KEY"])
    st.stop()


@st.cache_resource
def load_model():
  try:
    api_key = os.environ.get("GROQ_API_KEY") or st.secrets["api_key"]["GROQ_API_KEY"]
    return ChatGroq(model="llama-3.1-8b-instant", temperature=0, max_tokens=None, timeout=None, max_retries=2, api_key=api_key)
  except KeyError:
    st.toast("GROQ_API_KEY not found in environment variables!", icon="🚨")
    st.stop()


def chatWithYourPDF():
  load_credentials()
  GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") or st.secrets["api_key"]["GOOGLE_API_KEY"]

  file = st.file_uploader("Upload a PDF file", type=["pdf"])
  retriever = None
  if file:
    try:
      with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file.read())
        tmp_path = tmp_file.name

      loader = PyPDFLoader(tmp_path)
      pages = loader.load()
      raw_texts = [page.page_content for page in pages]
      text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
      )

      documents = text_splitter.create_documents(raw_texts)
      embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07", google_api_key=GOOGLE_API_KEY)
      vector_store = FAISS.from_documents(documents=documents, embedding=embeddings)
      retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 2})

      st.toast("PDF processed successfully. You can now start chatting.", icon="✅")
      os.unlink(tmp_path)
    except Exception as e:
      st.error(f"Error processing PDF: {str(e)}", icon="🚨")

    query = st.text_input("Ask a question about the PDF", placeholder="Type your question here...")
    if file and retriever and query:
      try:
        context = retriever.invoke(query)
        prompt_template = ChatPromptTemplate.from_messages(
          [("system", "You are a helpful assistant. Use the following context to answer the user's query: {context}"), ("user", "{query}")]
        )
        prompt = prompt_template.invoke({"context": context, "query": query})
        llm = load_model()
        response = llm.invoke(prompt)
        st.info(response.content, icon="💬")
      except Exception as e:
        st.error(f"Error generating response: {str(e)}", icon="🚨")
