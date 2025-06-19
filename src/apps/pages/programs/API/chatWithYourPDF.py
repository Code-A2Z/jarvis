import streamlit as st
import os
import tempfile
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

from src.helpers.displayInstructions import showInstructions
from src.helpers.checkKeyExist import isKeyExist

# --- API Key Instructions ---
api_guide = """
### How to get your Groq API Key:
1. Visit [Groq Console](https://console.groq.com/keys).
2. Sign up or log in with your account.
3. Navigate to the **API Keys** section.
4. Click on **+ Create Key** to generate a new API key.

#### How to get your Google API Key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey).
2. Generate an API key for Generative AI access.
"""

@st.cache_resource(show_spinner=True)
def load_model():
    try:
        api_key = (os.environ.get("GROQ_API_KEY") or st.secrets['api_key']["GROQ_API_KEY"])
        return ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=api_key
        )
    except KeyError:
        st.error("❌ GROQ_API_KEY not found in environment variables!")
        st.markdown(api_guide)
        st.stop()

def chatWithYourPDF():
    st.title("📄 Chat With Your PDF")
    
    exists = isKeyExist("GROQ_API_KEY", "api_key")
    if not exists["GROQ_API_KEY"]:
        showInstructions(markdown_text=api_guide, fields="GROQ_API_KEY")
        st.stop()
    exists = isKeyExist("GOOGLE_API_KEY", "api_key")
    if not exists["GOOGLE_API_KEY"]:
        showInstructions(markdown_text=api_guide, fields="GOOGLE_API_KEY")
        st.stop()

    if "retriever" not in st.session_state:
        st.session_state.retriever = None

    file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if file and file.type == "application/pdf":
        with st.spinner("Processing your PDF..."):
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

                GOOGLE_API_KEY = (os.environ.get("GOOGLE_API_KEY") or st.secrets['api_key']["GOOGLE_API_KEY"])
                embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07", google_api_key=GOOGLE_API_KEY)
                vector_store = FAISS.from_documents(documents=documents, embedding=embeddings)
                st.session_state.retriever = vector_store.as_retriever(
                    search_type="mmr", search_kwargs={"k": 2}
                )

                st.success("✅ PDF processed successfully. You can now start chatting.")
                
                # Clean up temp file
                os.unlink(tmp_path)
                
            except Exception as e:
                st.error(f"❌ Error processing PDF: {str(e)}")

    elif file and file.type != "application/pdf":
        st.error("Please upload a valid PDF file.")

    if st.session_state.retriever:
        query = st.text_input("Ask something about the PDF...")
        if query:
            with st.spinner("Thinking..."):
                try:
                    context = st.session_state.retriever.invoke(query)
                    prompt_template = ChatPromptTemplate.from_messages([
                        ("system", "You are a helpful assistant. Use the following context to answer the user's query: {context}"),
                        ("user", "{query}")
                    ])
                    prompt = prompt_template.invoke({"context": context, "query": query})
                    llm = load_model()
                    response = llm.invoke(prompt)
                    ai_message = response.content
                    st.markdown("#### 📌 Response")
                    st.write(ai_message)
                except Exception as e:
                    st.error(f"❌ Error generating response: {str(e)}")