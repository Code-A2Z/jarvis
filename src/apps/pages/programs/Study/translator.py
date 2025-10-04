import streamlit as st
from deep_translator import GoogleTranslator

langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)

# TODO: Detect the input text language
# TODO: Convert the whole file into the target language
# TODO: Create a copy button to copy the translated text
# TODO: Add more different types of translators like Microsoft, Deepl, ChatGPT, etc.


def translator():
  st.toast("This is a simple translator that can translate text from one language to another.", icon="ℹ️")
  to_lang = st.selectbox("To Language", list(langs_dict.keys()))
  text = st.text_area("Enter Text to Translate")
  if st.button("Translate") and text:
    my_translator = GoogleTranslator(source="auto", target=to_lang)
    result = my_translator.translate(text)
    st.code(result)
