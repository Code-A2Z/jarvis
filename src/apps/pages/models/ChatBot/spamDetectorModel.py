import os
import streamlit as st
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ---------------------------
# Download & load model in one line (cached)
# ---------------------------
@st.cache_resource
def load_model_and_tokenizer(username="smritipandey02", notebook="spam-detection", out="kaggle_models"):
    os.makedirs(out, exist_ok=True)
    # Download from Kaggle if not already present
    os.system(f"kaggle kernels output {username}/{notebook} -p {out} --force")
    # Load model
    model = tf.keras.models.load_model(os.path.join(out, "spam_classifier.h5"))
    with open(os.path.join(out, "tokenizer.pkl"), "rb") as f:
        tokenizer = pickle.load(f)
    return model, tokenizer

# ---------------------------
# Prediction function
# ---------------------------
def predict_message(message, model, tokenizer, max_len=100):
    seq = tokenizer.texts_to_sequences([message])
    padded = pad_sequences(seq, maxlen=max_len, padding="post", truncating="post")
    prob = float(model.predict(padded, verbose=0)[0][0])
    return prob

# ---------------------------
# Streamlit UI
# ---------------------------
def spam_app():
    st.title("Spam Message Detector")

    # Load Model button
    if st.button("Load Model", key="load_btn"):
        with st.spinner("Downloading and loading model..."):
            st.session_state["model"], st.session_state["tokenizer"] = load_model_and_tokenizer()
        st.success("Model & Tokenizer Loaded Successfully!")

    # Input box
    message = st.text_area("Enter a message:", key="msg_input")

    # Predict button
    if st.button("Predict", key="predict_btn"):
        if not message.strip():
            st.warning("Please enter a message before predicting.")
        elif "model" not in st.session_state or "tokenizer" not in st.session_state:
            st.warning("Please load the model first.")
        else:
            prob = predict_message(message, 
                                   st.session_state["model"], 
                                   st.session_state["tokenizer"])
            if prob > 0.5:
                st.error(f"Spam detected! (Confidence: {prob:.2f})")
            else:
                st.success(f"Ham (Not Spam) (Confidence: {1-prob:.2f})")

# ---------------------------
# Run app
# ---------------------------
spam_app()
