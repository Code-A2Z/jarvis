import re

import nltk
import streamlit as st
from nltk.corpus import words
from nltk.metrics.distance import edit_distance
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Download NLTK words corpus if not already present
try:
  nltk.data.find("corpora/words")
except LookupError:
  st.info("Downloading NLTK words corpus...")
  nltk.download("words")


# Load word list for fallback
word_list = set(words.words())


# Custom dictionary for common misspellings
custom_dict = {
  "hav": "have",
  "problm": "problem",
  "speling": "spelling",
  "grammer": "grammar",
  "teh": "the",
  "recieve": "receive",
  "wierd": "weird",
  "definately": "definitely",
  "dont": "don't",
  "cant": "can't",
  "wont": "won't",
  "thier": "their",
  "alot": "a lot",
  "seperate": "separate",
  "occured": "occurred",
  "untill": "until",
  "freind": "friend",
  "accomodate": "accommodate",
  "begining": "beginning",
  "judgement": "judgment",
}


# Initialize T5 model and tokenizer
@st.cache_resource
def loadModel():
  model = T5ForConditionalGeneration.from_pretrained("vennify/t5-base-grammar-correction")
  tokenizer = T5Tokenizer.from_pretrained("vennify/t5-base-grammar-correction")
  return model, tokenizer


# Fallback spell correction using Levenshtein distance
def correctWordFallback(word, max_distance=3):
  """Correct a single word using edit distance with higher threshold."""
  if word.lower() in word_list:
    return word
  # Check custom dictionary first
  if word.lower() in custom_dict:
    return custom_dict[word.lower()]
  # Find candidates with Levenshtein distance
  candidates = [w for w in word_list if edit_distance(word.lower(), w, max_distance) <= max_distance]
  # Sort by edit distance to prioritize closer matches
  candidates.sort(key=lambda w: edit_distance(word.lower(), w, max_distance))
  return candidates[0] if candidates else word


# Spell and grammar correction using T5
def correctSpelling(text, model, tokenizer):
  """Correct spelling and grammar using T5 model with custom dictionary."""
  # Step 1: Apply custom dictionary corrections
  corrected_text = text
  for wrong, correct in custom_dict.items():
    corrected_text = re.sub(r"\b" + re.escape(wrong) + r"\b", correct, corrected_text, flags=re.IGNORECASE)
  # Step 2: Use T5 for grammar and spelling correction
  input_text = f"correct: {corrected_text}"
  inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
  # Generate corrected text with refined parameters
  outputs = model.generate(
    inputs["input_ids"],
    max_length=512,
    num_beams=5,  # Increase beams for better accuracy
    length_penalty=1.0,
    early_stopping=True,
  )
  corrected = tokenizer.decode(outputs[0], skip_special_tokens=True)
  # Step 3: Fallback for any uncorrected words
  tokens = re.findall(r"\b\w+\b", corrected)
  corrected_tokens = []
  for token in tokens:
    is_capitalized = token[0].isupper() if token else False
    is_all_caps = token.isupper() if token else False
    corrected_token = correctWordFallback(token.lower())
    if is_all_caps:
      corrected_token = corrected_token.upper()
    elif is_capitalized:
      corrected_token = corrected_token.capitalize()
    corrected_tokens.append(corrected_token)
  # Reconstruct text
  corrected_text = []
  token_idx = 0
  word_pattern = re.compile(r"\b\w+\b")
  last_end = 0
  for match in word_pattern.finditer(corrected):
    corrected_text.append(corrected[last_end : match.start()])
    if token_idx < len(corrected_tokens):
      corrected_text.append(corrected_tokens[token_idx])
      token_idx += 1
    last_end = match.end()
  corrected_text.append(corrected[last_end:])
  return "".join(corrected_text)


# Streamlit UI
def spellingCorrectorModel():
  # st.title("Spell Checker")
  st.write("Enter text below to correct spelling and grammar. Select the corrected text and press Ctrl+C to copy.")
  # Input text area
  input_text = st.text_area("Enter Text:", height=150, placeholder="e.g., I hav a problm with speling")
  # Correct button
  if st.button("Correct Spelling"):
    if input_text.strip():
      model, tokenizer = loadModel()
      with st.spinner("Correcting text..."):
        corrected = correctSpelling(input_text, model, tokenizer)
      st.session_state["corrected_text"] = corrected  # Store in session state
      st.text_area("Corrected Text (select and press Ctrl+C to copy):", value=corrected, height=150, disabled=False, key="corrected_text_area")
    else:
      st.warning("Please enter some text to correct.")
