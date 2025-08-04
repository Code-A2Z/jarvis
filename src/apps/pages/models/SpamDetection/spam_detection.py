import streamlit as st
import pandas as pd
import pickle
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

def preprocess_text(text):
    """Clean and preprocess text for spam detection"""
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    return text

@st.cache_data(show_spinner=False)
def load_spam_model():
    """Load the spam detection model with proper error handling"""
    try:
        # Get the directory of this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, 'data')
        models_dir = os.path.join(current_dir, 'models')
        
        # Load the dataset
        dataset_path = os.path.join(data_dir, 'spam_dataset.pkl')
        vectorizer_path = os.path.join(models_dir, 'vectorizer.pkl')
        model_path = os.path.join(models_dir, 'spam_model.pkl')
        
        if all(os.path.exists(p) for p in [dataset_path, vectorizer_path, model_path]):
            # Load the trained model
            spam_data = pd.read_pickle(dataset_path)
            
            with open(vectorizer_path, 'rb') as f:
                vectorizer = pickle.load(f)
            
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            # Load model info if available
            model_info = None
            try:
                info_path = os.path.join(data_dir, 'model_info.pkl')
                if os.path.exists(info_path):
                    with open(info_path, 'rb') as f:
                        model_info = pickle.load(f)
            except:
                pass
            
            return spam_data, vectorizer, model, model_info, True
        else:
            # Fallback to sample model
            return create_sample_model()
    
    except Exception:
        # Fallback to sample model if anything fails
        return create_sample_model()

def create_sample_model():
    """Create a robust sample spam detection model"""
    # Expanded sample data for better training
    spam_messages = [
        "FREE! Win money now! Click here immediately!",
        "URGENT! Your account suspended! Verify now!",
        "Congratulations! You won $10000! Claim prize!",
        "Limited time offer! Buy now 90% discount!",
        "Hot singles near you! Meet tonight!",
        "Make money fast! Work from home!",
        "ALERT! Suspicious activity! Click to secure!",
        "You're pre-approved! Get loan now!",
        "Casino bonus! Play now win big!",
        "Lose weight fast! Miracle pills!"
    ]
    
    ham_messages = [
        "Hi there, how was your day today?",
        "Let's schedule our meeting for tomorrow afternoon.",
        "Thanks for sending the project documents.",
        "Happy birthday! Hope you have a wonderful day.",
        "Can you review this report when you have time?",
        "The presentation went well, thanks for your help.",
        "I'll be running a few minutes late to our call.",
        "Please find the attached files for your review.",
        "Looking forward to our collaboration on this project.",
        "Hope you're doing well and staying safe."
    ]
    
    # Create balanced dataset
    texts = spam_messages + ham_messages
    labels = ['spam'] * len(spam_messages) + ['ham'] * len(ham_messages)
    
    df = pd.DataFrame({'text': texts, 'label': labels})
    
    # Preprocess texts
    df['text'] = df['text'].apply(preprocess_text)
    
    # Create vectorizer with optimized parameters
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.9
    )
    
    # Fit vectorizer and train model
    X = vectorizer.fit_transform(df['text'])
    y = df['label']
    
    # Train with balanced parameters
    model = MultinomialNB(alpha=0.5)
    model.fit(X, y)
    
    # Create model info
    model_info = {
        'total_messages': len(df),
        'spam_count': len(spam_messages),
        'ham_count': len(ham_messages),
        'features': X.shape[1],
        'model_type': 'Sample MultinomialNB'
    }
    
    return df, vectorizer, model, model_info, False

def predict_spam(message, vectorizer, model):
    """Predict if a message is spam with confidence score"""
    try:
        processed_message = preprocess_text(message)
        if not processed_message.strip():
            return "unknown", 0.0
        
        message_vector = vectorizer.transform([processed_message])
        prediction = model.predict(message_vector)[0]
        probabilities = model.predict_proba(message_vector)[0]
        
        # Get confidence as the maximum probability
        confidence = max(probabilities) * 100
        
        return prediction, confidence
    
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        return "unknown", 0.0

def spam_detection():
    """Main spam detection interface"""
    st.title("📧 Spam Detection System")
    st.markdown("---")
    
    # Load model data
    spam_data, vectorizer, model, model_info, is_full_model = load_spam_model()
    
    # Display model information
    if model_info:
        if is_full_model:
            st.success(f"✅ Using trained model with {model_info['total_messages']:,} messages")
        else:
            st.info(f"ℹ️ Using sample model with {model_info['total_messages']} messages")
    
    # Clear cache button
    if st.button("🔄 Refresh Model", help="Reload the spam detection model"):
        load_spam_model.clear()
        st.rerun()
    
    st.markdown("---")
    
    # Input section
    st.subheader("🔍 Message Analysis")
    message = st.text_area(
        "Enter message to analyze:",
        placeholder="Type or paste your message here...",
        height=120,
        help="Enter any text message to check if it's spam or legitimate"
    )
    
    # Confidence threshold
    threshold = st.slider(
        "Confidence Threshold (%)",
        min_value=50,
        max_value=95,
        value=75,
        help="Minimum confidence required for classification"
    )
    
    # Analysis button
    if st.button("🔎 Analyze Message", type="primary"):
        if message and message.strip():
            with st.spinner("Analyzing message..."):
                prediction, confidence = predict_spam(message, vectorizer, model)
                
                # Display results
                st.markdown("### 📊 Analysis Results")
                
                if prediction == "spam":
                    if confidence >= threshold:
                        st.error(f"🚨 **SPAM DETECTED** - {confidence:.1f}% confidence")
                        st.markdown("⚠️ This message shows characteristics of spam/phishing")
                    else:
                        st.warning(f"⚠️ **Possible Spam** - {confidence:.1f}% confidence (below threshold)")
                        st.markdown("🤔 Message has some spam-like features but confidence is low")
                else:
                    if confidence >= threshold:
                        st.success(f"✅ **LEGITIMATE MESSAGE** - {confidence:.1f}% confidence")
                        st.markdown("👍 This appears to be a normal, legitimate message")
                    else:
                        st.info(f"ℹ️ **Likely Legitimate** - {confidence:.1f}% confidence (low confidence)")
                        st.markdown("🤷 Classification uncertain due to low confidence")
                
                # Technical details
                with st.expander("🔬 Technical Details"):
                    st.write(f"**Prediction:** {prediction}")
                    st.write(f"**Confidence Score:** {confidence:.2f}%")
                    st.write(f"**Processed Text:** {preprocess_text(message)}")
                    st.write(f"**Original Length:** {len(message)} characters")
                    st.write(f"**Cleaned Length:** {len(preprocess_text(message))} characters")
        else:
            st.warning("⚠️ Please enter a message to analyze")
    
    # Sample messages section
    st.markdown("---")
    st.subheader("🧪 Try Sample Messages")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🚨 Spam Examples:**")
        spam_samples = [
            "FREE MONEY! Click now to claim $1000!",
            "URGENT! Account suspended! Verify immediately!",
            "You won a lottery! Call to claim prize!"
        ]
        for i, sample in enumerate(spam_samples):
            if st.button(f"Test Spam {i+1}", key=f"spam_{i}"):
                st.text_area("Sample message:", sample, key=f"spam_display_{i}")
    
    with col2:
        st.markdown("**✅ Legitimate Examples:**")
        ham_samples = [
            "Hi! How are you doing today?",
            "Meeting scheduled for tomorrow at 3 PM",
            "Thanks for the project documents"
        ]
        for i, sample in enumerate(ham_samples):
            if st.button(f"Test Ham {i+1}", key=f"ham_{i}"):
                st.text_area("Sample message:", sample, key=f"ham_display_{i}")
    
    # Model statistics in sidebar
    with st.sidebar:
        st.markdown("### 📊 Model Statistics")
        if model_info:
            st.metric("Dataset Size", f"{model_info['total_messages']:,}")
            st.metric("Spam Messages", f"{model_info['spam_count']:,}")
            st.metric("Ham Messages", f"{model_info['ham_count']:,}")
            st.metric("Features", f"{model_info['features']:,}")
            
            if 'test_accuracy' in model_info:
                st.metric("Test Accuracy", f"{model_info['test_accuracy']:.1%}")
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This spam detection system uses:
        - **TF-IDF Vectorization** for text features
        - **Multinomial Naive Bayes** for classification
        - **N-gram analysis** for context understanding
        - **Confidence scoring** for reliable predictions
        """)

# Main function for the module
def spamDetectionModel():
    """Wrapper function to maintain compatibility"""
    return spam_detection()

if __name__ == "__main__":
    spam_detection()
