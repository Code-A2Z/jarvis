import os
import sys
from pathlib import Path
from zipfile import ZipFile

import cv2
import numpy as np
import streamlit as st
import tensorflow as tf
from deepface import DeepFace
from dotenv import load_dotenv
from PIL import Image

# Initialize environment variables
load_dotenv()

# Configuration
MODEL_FOLDER = Path("src/apps/pages/models/ImageProcessing/model_files")
MODEL_FILENAME = "best_emotion_model.keras"
MODEL_PATH = MODEL_FOLDER / MODEL_FILENAME

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../"))
if PROJECT_ROOT not in sys.path:
  sys.path.append(PROJECT_ROOT)

EMOTION_LABELS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

# GPU setup
try:
  gpus = tf.config.experimental.list_physical_devices("GPU")
  if gpus:
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
except Exception:
  pass


@st.cache_resource
def load_custom_model():
  """Load custom model with compatibility fallback"""
  try:
    return tf.keras.models.load_model(MODEL_PATH, safe_mode=False)
  except TypeError as e:
    if "batch_shape" in str(e):
      custom_objects = {"InputLayer": lambda **kwargs: tf.keras.layers.InputLayer(**{k: v for k, v in kwargs.items() if k != "batch_shape"})}
      return tf.keras.models.load_model(MODEL_PATH, custom_objects=custom_objects, safe_mode=False)
    raise


def ensure_model():
  """Ensure model is available locally"""
  if not MODEL_PATH.exists():
    from src.helpers.kaggle import downloadNotebookOutput

    st.warning("Downloading model from Kaggle...")
    MODEL_FOLDER.mkdir(parents=True, exist_ok=True)

    downloadNotebookOutput(os.getenv("KAGGLE_USERNAME"), os.getenv("KAGGLE_NOTEBOOK"), str(MODEL_FOLDER))

    # Extract if zip file was downloaded
    for zip_file in MODEL_FOLDER.glob("*.zip"):
      with ZipFile(zip_file) as z:
        z.extractall(MODEL_FOLDER)
      zip_file.unlink()


def preprocess_image(img):
  """Prepare image for custom model"""
  img = np.array(img) if isinstance(img, Image.Image) else img
  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img_resized = cv2.resize(img_gray, (48, 48))
  return (img_resized / 255.0).reshape(1, 48, 48, 1)


def predict_with_custom_model(model, img):
  """Predict emotion using custom model"""
  processed = preprocess_image(img)
  prediction = model.predict(processed, verbose=0)
  emotion = EMOTION_LABELS[np.argmax(prediction)]
  confidence = float(np.max(prediction))
  return emotion, confidence


def predict_with_deepface(img):
  """Predict emotion using DeepFace"""
  img = np.array(img) if isinstance(img, Image.Image) else img
  result = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)
  return result[0]["dominant_emotion"], result[0]["emotion"]


# ---- Jarvis entry function ----
def emotionRecognitionModel():
  st.title("Emotion Recognition from Facial Expressions")

  option = st.radio("Method:", ("DeepFace (Pretrained)", "Custom Keras Model"))
  capture = st.radio("Input:", ("Upload Image", "Use Webcam"))

  image = None
  if capture == "Upload Image":
    uploaded = st.file_uploader("Choose image", type=["jpg", "jpeg", "png"])
    if uploaded:
      image = Image.open(uploaded)
  else:
    picture = st.camera_input("Take a picture")
    if picture:
      image = Image.open(picture)

  if image:
    st.image(image, use_column_width=True)

    if option == "DeepFace (Pretrained)":
      with st.spinner("Analyzing with DeepFace..."):
        emotion, scores = predict_with_deepface(image)
        st.success(f"Predicted Emotion: {emotion}")
        st.json(scores)
    else:
      ensure_model()
      with st.spinner("Predicting with custom model..."):
        model = load_custom_model()
        emotion, confidence = predict_with_custom_model(model, image)
        st.success(f"Predicted Emotion: {emotion} ({confidence:.2%})")

  st.caption("This page supports both DeepFace and custom-trained models with Kaggle integration.")


emotionRecognitionModel()
