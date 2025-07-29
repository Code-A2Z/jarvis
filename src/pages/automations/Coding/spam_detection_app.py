# Streamlit Spam Detection App
# This app loads a trained model and vectorizer, and predicts if a message is spam or not.

import streamlit as st
import pickle
import os

st.title('Spam Detection App')
st.write('Enter a message below to check if it is spam or not.')

# Load model and vectorizer
MODEL_PATH = 'src/pages/automations/Coding/spam_model.pkl'
VECTORIZER_PATH = 'src/pages/automations/Coding/spam_vectorizer.pkl'

model = None
vectorizer = None

if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
else:
    st.error('Model or vectorizer not found. Please train the model first.')

# User input
user_input = st.text_area('Message:', '')

if st.button('Predict'):
    if not user_input:
        st.warning('Please enter a message.')
    elif model is None or vectorizer is None:
        st.error('Model or vectorizer not loaded.')
    else:
        # Preprocess and predict
        X = vectorizer.transform([user_input])
        prediction = model.predict(X)[0]
        is_spam = prediction == 1 or prediction == 'spam'
        label = 'Spam' if is_spam else 'Not Spam'
        color = "#f40909" if is_spam else "#18ef18"
        st.markdown(f'<div style="background-color:{color};padding:20px;border-radius:8px;font-size:18px;font-weight:bold;text-align:center;">This message is: {label}<br><br>{user_input}</div>', unsafe_allow_html=True)
