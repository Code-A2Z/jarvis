import os
import sys
import cv2
import numpy as np
import streamlit as st
from PIL import Image
from deepface import DeepFace
import tensorflow as tf

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# ---- Local imports for Kaggle download ----
from src.helpers.kaggle import downloadNotebookOutput

# ---- Constants ----
MODEL_FOLDER = "src/apps/pages/models/ImageProcessing/model_files"
MODEL_FILENAME = "best_emotion_model.keras"
MODEL_PATH = os.path.join(MODEL_FOLDER, MODEL_FILENAME)

# Kaggle Notebook Info (Replace with your actual notebook info)
KAGGLE_USERNAME = "your-kaggle-username"
KAGGLE_NOTEBOOK = "your-emotion-model-notebook"

# ---- Ensure model is available ----
def ensure_model():
    if not os.path.exists(MODEL_PATH):
        st.warning("Model not found locally. Downloading from Kaggle...")
        os.makedirs(MODEL_FOLDER, exist_ok=True)
        downloadNotebookOutput(KAGGLE_USERNAME, KAGGLE_NOTEBOOK, MODEL_FOLDER)
        if not os.path.exists(MODEL_PATH):
            st.error("Model download failed. Please check Kaggle credentials and notebook output.")
            st.stop()
    return MODEL_PATH

# ---- Lazy-load custom model ----
@st.cache_resource
def load_custom_model():
    model_path = ensure_model()
    return tf.keras.models.load_model(model_path)

# ---- Preprocess for custom Keras model ----
def preprocess_image(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_resized = cv2.resize(img_gray, (48, 48))
    img_normalized = img_resized / 255.0
    return img_normalized.reshape(1, 48, 48, 1)

# ---- Labels based on training dataset ----
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

def predict_with_custom_model(model, img):
    processed = preprocess_image(img)
    prediction = model.predict(processed)
    emotion = emotion_labels[np.argmax(prediction)]
    confidence = np.max(prediction)
    return emotion, confidence

def predict_with_deepface(img):
    # Convert PIL or webcam to numpy array (RGB)
    if isinstance(img, Image.Image):
        img = np.array(img)
    elif not isinstance(img, np.ndarray):
        raise ValueError("Unsupported image type for DeepFace")
    
    result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
    dominant_emotion = result[0]['dominant_emotion']
    return dominant_emotion, result[0]['emotion']

# ---- Streamlit UI ----
st.title("Emotion Recognition from Facial Expressions")

option = st.radio("Choose Detection Method:", ("DeepFace (Pretrained)", "Custom Keras Model"))
capture_method = st.radio("Input Method:", ("Upload Image", "Use Webcam"))

def handle_prediction(img):
    if option == "DeepFace (Pretrained)":
        with st.spinner("Analyzing with DeepFace..."):
            emotion, all_scores = predict_with_deepface(img)
            st.success(f"Predicted Emotion: {emotion}")
            st.json(all_scores)
    else:
        with st.spinner("Predicting with Custom Model..."):
            model = load_custom_model()
            emotion, confidence = predict_with_custom_model(model, np.array(img))
            st.success(f"Predicted Emotion: {emotion} ({confidence:.2f})")

if capture_method == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        handle_prediction(image)
else:
    picture = st.camera_input("Capture an Image")
    if picture:
        image = Image.open(picture)
        st.image(image, caption="Captured Image", use_container_width=True)
        handle_prediction(image)

st.caption("This page supports both DeepFace and custom-trained models with Kaggle model integration.")
