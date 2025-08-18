import streamlit as st
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences


# ---------------------------
# Load model & tokenizer
# ---------------------------
@st.cache_resource
def load_model_and_tokenizer():
    try:
        model = tf.keras.models.load_model("spam_classifier.h5")
        with open("tokenizer.pkl", "rb") as f:
            tokenizer = pickle.load(f)
        return model, tokenizer
    except Exception as e:
        st.error(f"Could not load model/tokenizer: {e}")
        st.stop()

model, tokenizer = load_model_and_tokenizer()


# ---------------------------
# Prediction function
# ---------------------------
def predict_message(message, model, tokenizer, max_len=100):
    seq = tokenizer.texts_to_sequences([message])
    padded = pad_sequences(seq, maxlen=max_len, padding="post", truncating="post")
    prob = float(model.predict(padded)[0][0])
    return prob


# ---------------------------
# Streamlit UI
# ---------------------------
def spam_app():
    st.title("Spam Message Detector")

    message = st.text_area("Enter a message:")

    if st.button("Predict") and message.strip():
        prob = predict_message(message, model, tokenizer)

        if prob > 0.5:
            st.error(f"Spam detected! (Confidence: {prob:.2f})")
        else:
            st.success(f"Ham (Not Spam) (Confidence: {1-prob:.2f})")
    elif st.button("Predict"):
        st.warning("Please enter a message before predicting.")


# ---------------------------
# Run app
# ---------------------------
spam_app()
