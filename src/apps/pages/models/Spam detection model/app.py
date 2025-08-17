import streamlit as st
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load model
model = tf.keras.models.load_model("spam_classifier.h5")



# Load tokenizer
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Max sequence length (should be same as used in training)
MAX_LEN = 100  

st.title("📧 Spam Message Detector")

# User input
message = st.text_area("Enter a message:")

if st.button("Predict"):
    if message.strip() != "":
        # Convert message to sequence
        seq = tokenizer.texts_to_sequences([message])
        padded = pad_sequences(seq, maxlen=MAX_LEN, padding="post", truncating="post")

        # Predict
        prediction = model.predict(padded)
        prob = float(prediction[0][0])

        if prob > 0.5:
            st.error(f"🚨 Spam detected! (Confidence: {prob:.2f})")
        else:
            st.success(f"✅ Ham (Not Spam) (Confidence: {1-prob:.2f})")
    else:
        st.warning("Please enter a message before predicting.")


# In[ ]:




