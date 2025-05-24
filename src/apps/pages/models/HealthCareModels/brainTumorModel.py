import tensorflow as tf
import streamlit as st
import numpy as np
from PIL import Image
import gdown

@st.cache_resource
def load_model():
    gdown.download(f"https://drive.google.com/uc?id={st.secrets['brainTumorModel']['BRAIN_TUMOR_TEST']}", 'brain_tumor_test.keras', quiet=False)
    model = tf.keras.models.load_model("brain_tumor_test.keras")
    return model

def get_mri():
    img = st.file_uploader("Please Upload MRI Scan of Brain", type=["jpg", "jpeg"])
    codn = False
    data = []
    if img is not None:
        st.image(img, width=420, caption="Uploaded Img")
        data = Image.open(img).convert("RGB")
        data = data.resize((64, 64))
        data = np.asarray(data)
        data = np.expand_dims(data, axis=0)
        codn = True

    return codn, data

def do_test(img):
    model = load_model()
    res = np.argmax(model.predict(img))
    return res

def brainTumorModel():
    codn, img = get_mri()
    res = None

    if codn:
        res = do_test(img)

    if res is not None:
        if res == 0:
            st.error("Hi User, You are diagnosed with Glioma. Please consult a doctor.")
        elif res == 1:
            st.error("Hi User, You are diagnosed with Meningioma. Please consult a doctor.")
        elif res == 2:
            st.success("Congrats User, You are not diagnosed with a brain tumor.")
        elif res == 3:
            st.error("Hi User, You are diagnosed with Pituitary tumor. Please consult a doctor.")

    codn = False
