import io
import numpy as np
from PIL import Image
import streamlit as st
import torch
import torch.nn as nn
from torchvision import models, transforms


st.title("Arabic Dates Classification")
st.markdown(
    "This pretrained model will classify an image of **Arabic Dates** into one of the 9 date varieties from the Arabian region."
)

# MODEL LOADING
MODEL_PATH = "assets/arabic_dates_model.pth"
@st.cache_resource
def load_model():
    checkpoint = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
    class_names = checkpoint["classes"]

    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    model.fc = nn.Sequential(
        nn.Linear(model.fc.in_features, 512),
        nn.ReLU(),
        nn.Dropout(0.4),
        nn.Linear(512, len(class_names))
    )
    model.load_state_dict(checkpoint["model_state_dict"], strict=False)
    model.eval()
    return model, class_names

model, CLASS_NAMES = load_model()


# IMAGE PREPROCESSING & PREDICTION
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


# FILE UPLOAD SECTION
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
st.caption("Trained with ResNet50 on Arabian Dates Dataset — 9 classes")