import io
import pickle
import sys
import os
import numpy as np
from PIL import Image

import streamlit as st
import torch
from torch import nn
from torchvision import models, transforms
from src.helpers.kaggle import downloadNotebookOutput

# Fix module path for src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../..")))


# APP HEADER
st.title("Arabic Dates Classification 🍂")
st.markdown(
    "This pretrained model classifies an image of **Arabic Dates** "
    "into one of the 9 varieties commonly found in the Arabian region."
)

# LOAD MODEL
@st.cache_resource
def load_model_data():
    try:
        downloadNotebookOutput("supratikbhowal", "arabic-dates-classification", "notebook")

        MODEL_PKL_PATH = "notebook/arabic_dates_model.pkl"
        with open(MODEL_PKL_PATH, "rb") as f:
            model_data = pickle.load(f)

        if isinstance(model_data, dict) and "model" in model_data and "class_names" in model_data:
            model = model_data["model"]
            class_names = model_data["class_names"]
        else:
            model = model_data
            CLASSES_PATH = "notebook/arabic_dates_classnames.pkl"
            with open(CLASSES_PATH, "rb") as f:
                class_names = pickle.load(f)

        model.eval()
        return model, class_names

    except Exception as e:
        st.error(f"🚨 Failed to load model or data: {e}")
        st.stop()


model, CLASS_NAMES = load_model_data()
st.success("✅ Model and class names loaded successfully!")


# IMAGE PREPROCESSING
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

def preprocess_image(image: Image.Image):
    image = image.convert("RGB")
    return transform(image).unsqueeze(0)

def predict(model, image_tensor, class_names):
    with torch.no_grad():
        outputs = model(image_tensor)
        probs = torch.nn.functional.softmax(outputs[0], dim=0)
    probs = probs.numpy()
    sorted_indices = np.argsort(probs)[::-1]
    sorted_probs = probs[sorted_indices]
    sorted_labels = [class_names[i] for i in sorted_indices]
    return sorted_labels, sorted_probs

# FILE UPLOAD
uploaded_file = st.file_uploader("📸 Upload an image of Arabic Dates", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image_data = uploaded_file.read()
    image = Image.open(io.BytesIO(image_data))
    st.image(image, caption="Uploaded Image", width=400)
    st.write("🔍 Analyzing...")

    image_tensor = preprocess_image(image)
    labels, probs = predict(model, image_tensor, CLASS_NAMES)

    top_class = labels[0]
    top_prob = probs[0] * 100

    st.markdown(f"### ✅ Predicted Class: **{top_class}** ({top_prob:.2f}% confidence)")

    prob_dict = {labels[i]: float(probs[i] * 100) for i in range(len(labels))}
    st.write("#### 📊 Probability Distribution:")
    st.bar_chart(prob_dict)

else:
    st.info("👆 Upload a clear image of dates to classify.")

# FOOTER
st.caption("Trained with ResNet50 on the Arabian Dates Dataset — 9 classes")