import os
import sys
import json
from pathlib import Path
from zipfile import ZipFile

import cv2
import h5py
import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image
from dotenv import load_dotenv
from deepface import DeepFace

# load .env if present
load_dotenv()

# ----------------------------
# Config / Defaults
# ----------------------------
DEFAULT_IMG_SIZE = (48, 48)  # width, height
HAAR_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Default model location (you can change)
MODEL_FOLDER = Path("src/apps/pages/models/ImageProcessing/model_files")
MODEL_FILENAME = "best_emotion_model.keras"  # original keras file (kept for backwards compatibility)
MODEL_PATH = MODEL_FOLDER / MODEL_FILENAME

# Default fallback label set (if your model doesn't include embedded labels)
DEFAULT_EMOTION_LABELS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# ----------------------------
# GPU setup (optional)
# ----------------------------
def enable_gpu_memory_growth():
    try:
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            for g in gpus:
                tf.config.experimental.set_memory_growth(g, True)
    except Exception:
        pass

enable_gpu_memory_growth()

# ----------------------------
# Utility: Face detection & preprocessing
# ----------------------------
def detect_face_and_crop(img_bgr, cascade_path=HAAR_CASCADE_PATH):
    """
    Input: BGR image (numpy array)
    Output: cropped BGR image of the largest detected face, or center-crop fallback
    """
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cascade_path)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
    if len(faces) > 0:
        # choose largest face
        faces = sorted(faces, key=lambda r: r[2] * r[3], reverse=True)
        x, y, w, h = faces[0]
        pad = int(0.2 * max(w, h))
        x0 = max(0, x - pad)
        y0 = max(0, y - pad)
        x1 = min(img_bgr.shape[1], x + w + pad)
        y1 = min(img_bgr.shape[0], y + h + pad)
        return img_bgr[y0:y1, x0:x1]
    # fallback: center square crop
    h, w = img_bgr.shape[:2]
    side = min(h, w)
    cx, cy = w // 2, h // 2
    x0 = max(0, cx - side // 2)
    y0 = max(0, cy - side // 2)
    return img_bgr[y0:y0+side, x0:x0+side]

def preprocess_for_model(img, size=DEFAULT_IMG_SIZE, do_face_detect=True):
    """
    img: PIL.Image or numpy (RGB or BGR)
    Returns: (1, H, W, 1) float32 normalized [0,1]
    """
    # convert PIL to numpy BGR if needed
    if isinstance(img, Image.Image):
        img = np.array(img.convert("RGB"))[:, :, ::-1]  # RGB->BGR
    elif isinstance(img, np.ndarray):
        # assume either RGB or BGR. If shape last channel==3, assume BGR if values match typical cv2
        if img.ndim == 3 and img.shape[2] == 3:
            pass  # assume BGR already
    else:
        raise ValueError("Unsupported image type for preprocessing")

    if do_face_detect:
        face = detect_face_and_crop(img)
    else:
        # center square crop fallback
        h, w = img.shape[:2]
        side = min(h, w)
        cx, cy = w // 2, h // 2
        x0 = max(0, cx - side // 2)
        y0 = max(0, cy - side // 2)
        face = img[y0:y0+side, x0:x0+side]

    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (size[0], size[1]), interpolation=cv2.INTER_AREA)
    arr = resized.astype("float32") / 255.0
    arr = arr.reshape((1, size[1], size[0], 1))
    return arr

# ----------------------------
# Load / ensure default model is available
# ----------------------------
def ensure_model_download():
    """If the default MODEL_PATH doesn't exist you can optionally download from a configured notebook output.
       This tries to replicate your old behavior; it's optional — adjust or remove depending on your environment.
    """
    if MODEL_PATH.exists():
        return
    # If you have a helper to download from Kaggle (like your repo used), try calling it.
    try:
        from src.helpers.kaggle import downloadNotebookOutput
    except Exception:
        return
    st.warning("Default model not found locally; attempting to download from Kaggle output...")
    MODEL_FOLDER.mkdir(parents=True, exist_ok=True)
    try:
        downloadNotebookOutput(
            os.getenv("KAGGLE_USERNAME"),
            os.getenv("KAGGLE_NOTEBOOK"),
            str(MODEL_FOLDER)
        )
        for z in MODEL_FOLDER.glob("*.zip"):
            with ZipFile(z, "r") as zz:
                zz.extractall(MODEL_FOLDER)
            z.unlink()
    except Exception as e:
        st.error(f"Could not download model automatically: {e}")

# ----------------------------
# Model load helpers (cached)
# ----------------------------
@st.cache_resource
def load_keras_model_safe(path: str):
    """
    Load a Keras model. Catch common issues (InputLayer batch_shape problems).
    path: path to .keras, .h5 or saved model
    """
    try:
        model = tf.keras.models.load_model(path, compile=False)
        return model
    except TypeError as e:
        # Attempts to handle old saved InputLayer batch_shape bug
        if "batch_shape" in str(e):
            custom_objects = {
                "InputLayer": lambda **kwargs: tf.keras.layers.InputLayer(
                    **{k: v for k, v in kwargs.items() if k != "batch_shape"}
                )
            }
            model = tf.keras.models.load_model(path, custom_objects=custom_objects, compile=False)
            return model
        raise
    except Exception:
        # re-raise to be handled by caller
        raise

@st.cache_resource
def load_h5_model_and_labels(path: str):
    """
    Loads a model saved in HDF5 (.h5) and tries to read a 'labels' attribute from the file.
    Returns: (model, labels_list)
    """
    # load model (no compile)
    model = load_keras_model_safe(path)
    labels = None
    try:
        with h5py.File(path, "r") as f:
            # 'labels' attribute may be stored as JSON string; try to read it
            raw = f.attrs.get("labels", None)
            if raw is not None:
                try:
                    labels = json.loads(raw)
                except Exception:
                    # maybe it's already a list or byte-string
                    if isinstance(raw, (bytes, bytearray)):
                        try:
                            labels = json.loads(raw.decode("utf-8"))
                        except Exception:
                            labels = None
                    elif isinstance(raw, (list, tuple)):
                        labels = list(raw)
    except Exception:
        # ignore label reading issues (model loaded ok)
        labels = None

    if labels is None:
        labels = DEFAULT_EMOTION_LABELS.copy()
    return model, labels

# ----------------------------
# Model prediction wrappers
# ----------------------------
def predict_with_h5_model(model, labels, pil_image, do_face_detect=True):
    processed = preprocess_for_model(pil_image, do_face_detect=do_face_detect)
    preds = model.predict(processed, verbose=0)
    idx = int(np.argmax(preds, axis=-1)[0])
    score = float(np.max(preds))
    label = labels[idx] if idx < len(labels) else f"label_{idx}"
    # return label, confidence, full_scores dict
    score_dict = {labels[i] if i < len(labels) else f"label_{i}": float(preds[0, i]) for i in range(preds.shape[1])}
    return label, score, score_dict

def predict_with_custom_keras_kerasfile(model, pil_image):
    # for your old .keras style model - use same preprocessing
    processed = preprocess_for_model(pil_image)
    preds = model.predict(processed, verbose=0)
    idx = int(np.argmax(preds, axis=-1)[0])
    score = float(np.max(preds))
    label = DEFAULT_EMOTION_LABELS[idx] if idx < len(DEFAULT_EMOTION_LABELS) else f"label_{idx}"
    score_dict = {DEFAULT_EMOTION_LABELS[i] if i < len(DEFAULT_EMOTION_LABELS) else f"label_{i}": float(preds[0, i]) for i in range(preds.shape[1])}
    return label, score, score_dict

def predict_with_deepface(pil_image):
    img = np.array(pil_image.convert("RGB"))
    # DeepFace.analyze returns list/dict depending on version; ensure compatibility
    result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
    # Some versions return a dict containing 'dominant_emotion' and 'emotion' map
    if isinstance(result, dict):
        dom = result.get("dominant_emotion", None)
        scores = result.get("emotion", None)
        return dom, scores
    if isinstance(result, (list, tuple)):
        r = result[0]
        return r.get("dominant_emotion", None), r.get("emotion", None)
    return None, None

# ----------------------------
# Streamlit UI
# ----------------------------
def emotionRecognitionModel():
    st.title("Emotion Recognition from Facial Expressions")

    method = st.radio("Method", ("DeepFace (Pretrained)", "Single HDF5 (.h5) Model", "Legacy .keras Model"))
    input_mode = st.radio("Input", ("Upload Image", "Use Webcam"))

    # allow model upload for h5 or keras
    uploaded_model = None
    if method == "Single HDF5 (.h5) Model":
        st.markdown("**Model file**: you can either use the default bundled HDF5, or upload your own `.h5` file that contains an embedded `labels` attribute.")
        uploaded_model = st.file_uploader("Upload .h5 model (optional)", type=["h5"])
    elif method == "Legacy .keras Model":
        st.markdown("**Legacy**: this uses your .keras/savedmodel file referenced by `MODEL_PATH` or upload one.")
        uploaded_model = st.file_uploader("Upload .keras/.h5 model (optional)", type=["h5", "keras"])

    # image input
    pil_image = None
    if input_mode == "Upload Image":
        uploaded = st.file_uploader("Choose image", type=["jpg", "jpeg", "png"])
        if uploaded:
            pil_image = Image.open(uploaded).convert("RGB")
    else:
        picture = st.camera_input("Take a picture")
        if picture:
            pil_image = Image.open(picture).convert("RGB")

    if pil_image is None:
        st.info("Please upload an image or take a picture.")
        return

    st.image(pil_image, caption="Input Image", use_column_width=True)

    # Face detection toggle
    do_face_detect = st.checkbox("Use face detection (recommended)", value=True)

    if method == "DeepFace (Pretrained)":
        with st.spinner("Analyzing with DeepFace..."):
            try:
                dom, scores = predict_with_deepface(pil_image)
                st.success(f"Predicted Emotion: {dom}")
                if isinstance(scores, dict):
                    st.json(scores)
                else:
                    st.write(scores)
            except Exception as e:
                st.error(f"DeepFace error: {e}")

    elif method == "Single HDF5 (.h5) Model":
        # decide model path: either uploaded file or default
        if uploaded_model is not None:
            # save to a temp path and load
            temp_model_path = Path("tmp_uploaded_model.h5")
            with open(temp_model_path, "wb") as f:
                f.write(uploaded_model.getbuffer())
            model_path_to_load = str(temp_model_path)
        else:
            # fallback: try default .h5 in same folder as .keras file
            # If there is a .h5 with same name, prefer it
            candidate = MODEL_FOLDER / (MODEL_FILENAME.replace(".keras", ".h5"))
            if candidate.exists():
                model_path_to_load = str(candidate)
            else:
                # fallback to MODEL_PATH (legacy .keras) - not ideal but we attempt
                model_path_to_load = str(MODEL_PATH) if MODEL_PATH.exists() else None

        if model_path_to_load is None or not Path(model_path_to_load).exists():
            st.error("No model available. Please upload a .h5 model or ensure the default model is present.")
        else:
            with st.spinner("Loading model..."):
                try:
                    model, labels = load_h5_model_and_labels(model_path_to_load)
                except Exception as e:
                    st.error(f"Could not load model: {e}")
                    return
            with st.spinner("Predicting..."):
                try:
                    label, score, score_dict = predict_with_h5_model(model, labels, pil_image, do_face_detect=do_face_detect)
                    st.success(f"Predicted: {label} ({score:.2%})")
                    st.markdown("**Scores:**")
                    st.json(score_dict)
                except Exception as e:
                    st.error(f"Prediction failed: {e}")

    else:  # Legacy .keras Model
        # try uploaded file first
        model_to_use = None
        if uploaded_model is not None:
            tmp_path = Path("tmp_uploaded_legacy_model.h5")
            with open(tmp_path, "wb") as f:
                f.write(uploaded_model.getbuffer())
            try:
                model_to_use = load_keras_model_safe(str(tmp_path))
            except Exception as e:
                st.error(f"Failed to load uploaded model: {e}")
                model_to_use = None

        if model_to_use is None:
            # fallback to MODEL_PATH
            ensure_model_download()
            if MODEL_PATH.exists():
                try:
                    model_to_use = load_keras_model_safe(str(MODEL_PATH))
                except Exception as e:
                    st.error(f"Failed to load default model at {MODEL_PATH}: {e}")
                    model_to_use = None

        if model_to_use is None:
            st.error("No Keras model loaded. Upload a model or fix MODEL_PATH.")
        else:
            with st.spinner("Predicting with legacy model..."):
                try:
                    label, score, score_dict = predict_with_custom_keras_kerasfile(model_to_use, pil_image)
                    st.success(f"Predicted: {label} ({score:.2%})")
                    st.markdown("**Scores:**")
                    st.json(score_dict)
                except Exception as e:
                    st.error(f"Prediction failed: {e}")

    st.caption("This page supports DeepFace, single-file .h5 Keras models (with embedded labels) and legacy .keras models.")

if __name__ == "__main__":
    emotionRecognitionModel()
