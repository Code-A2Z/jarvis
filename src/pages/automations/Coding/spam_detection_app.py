st.title('Spam Detection App')
st.write('Enter a message below to check if it is spam or not.')
st.title('Spam Detection App')
st.write('Enter a message below to check if it is spam or not.')
import streamlit as st
import sys
import os
sys.path.append(os.path.abspath('src/models/ChatBot'))
from spamDetectionModel import SpamDetectionModel

st.title('Spam Detection App')
st.write('Enter a message below to check if it is spam or not.')

try:
    spam_model = SpamDetectionModel()
except Exception as e:
    st.error(str(e))
    spam_model = None

user_input = st.text_area('Message:', '')

if st.button('Predict'):
    if not user_input:
        st.warning('Please enter a message.')
    elif spam_model is None:
        st.error('Model or vectorizer not loaded.')
    else:
        prediction = spam_model.predict(user_input)
        is_spam = prediction == 1 or prediction == 'spam'
        label = 'Spam' if is_spam else 'Not Spam'
        if is_spam:
            st.error(f'This message is: {label}\n\n{user_input}')
        else:
            st.success(f'This message is: {label}\n\n{user_input}')
