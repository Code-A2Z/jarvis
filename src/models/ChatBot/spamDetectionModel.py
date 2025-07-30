import streamlit as st
import pickle
import os

def load_spam_model():
    model_path = 'src/models/ChatBot/spam_model.pkl'
    vectorizer_path = 'src/models/ChatBot/spam_vectorizer.pkl'
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        return model, vectorizer
    except Exception as e:
        st.error(f"Model or vectorizer could not be loaded: {e}", icon="🚨")
        st.stop()

def spamDetectionModel():
    model, vectorizer = load_spam_model()
    st.title("Spam Detection")
    st.write("Enter a message to check if it is spam or not.")
    user_input = st.text_area("Message")
    if st.button("Predict"):
        if not user_input:
            st.warning("Please enter a message.")
        else:
            X = vectorizer.transform([user_input])
            prediction = model.predict(X)[0]
            label = "Spam" if prediction == 1 or prediction == "spam" else "Not Spam"
            if label == "Spam":
                st.error(f"This message is: {label}\n\n{user_input}")
            else:
                st.success(f"This message is: {label}\n\n{user_input}")
    st.toast("This model uses a Naive Bayes classifier.", icon="ℹ️")

if __name__ == "__main__":
    import streamlit as st
    spamDetectionModel()