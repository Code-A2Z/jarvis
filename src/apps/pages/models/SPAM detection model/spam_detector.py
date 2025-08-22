import os
import streamlit as st
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ---------------------------
# Download model/tokenizer from Kaggle Kernel
# ---------------------------
@st.cache_resource
def download_from_kaggle(output_dir="kaggle_models"):
    try:
        os.makedirs(output_dir, exist_ok=True)
        kernel_ref = "smritipandey02/spam-detection"  # Hardcoded username + notebook
        
        # Download kernel outputs
        os.system(f"kaggle kernels output {kernel_ref} -p {output_dir}")
        
        st.success(f"Downloaded model/tokenizer from Kaggle Kernel: {kernel_ref}")
        return output_dir
    except Exception as e:
        st.error(f"Could not download from Kaggle: {e}")
        st.stop()

# ---------------------------
# Load model & tokenizer
# ---------------------------
@st.cache_resource
def load_model_and_tokenizer():
    try:
        model_dir = download_from_kaggle()
        
        model = tf.keras.models.load_model(os.path.join(model_dir, "spam_classifier.h5"))
        with open(os.path.join(model_dir, "tokenizer.pkl"), "rb") as f:
            tokenizer = pickle.load(f)
        
        return model, tokenizer
    except Exception as e:
        st.error(f"Could not load model/tokenizer: {e}")
        st.stop()

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

    # Load Model button
    if st.button("Load Model", key="load_btn"):
        with st.spinner("Loading model & tokenizer..."):
            model, tokenizer = load_model_and_tokenizer()
            st.session_state["model"] = model
            st.session_state["tokenizer"] = tokenizer
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
