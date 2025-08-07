import streamlit as st
import re

def preprocess_text(text):
    """Clean and preprocess text for spam detection"""
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    return text

def get_spam_keywords():
    """Get comprehensive list of spam indicators"""
    return {
        'urgent_words': ['urgent', 'immediate', 'act now', 'limited time', 'expires', 'deadline', 'hurry'],
        'money_words': ['free', 'money', 'cash', 'prize', 'win', 'won', 'winner', 'lottery', 'jackpot', 'bonus', 'discount'],
        'action_words': ['click', 'call now', 'buy now', 'order now', 'subscribe', 'download', 'install', 'claim'],
        'suspicious_words': ['congratulations', 'selected', 'approved', 'guaranteed', 'risk free', 'no cost', 'special offer'],
        'medical_words': ['lose weight', 'diet', 'pills', 'medication', 'cure', 'treatment', 'miracle'],
        'financial_words': ['loan', 'credit', 'debt', 'mortgage', 'investment', 'income', 'profit', 'preapproved'],
        'adult_words': ['hot', 'sexy', 'singles', 'dating', 'meet', 'lonely', 'romance'],
        'scam_indicators': ['verify account', 'suspend', 'security alert', 'confirm identity', 'update payment', 'locked account']
    }

@st.cache_data
def create_spam_detector():
    """Create a rule-based spam detector that works without external files"""
    keywords = get_spam_keywords()
    
    # Weight different categories based on spam likelihood
    weights = {
        'urgent_words': 3.0,
        'money_words': 2.5,
        'action_words': 2.0,
        'suspicious_words': 2.5,
        'medical_words': 1.5,
        'financial_words': 2.0,
        'adult_words': 3.0,
        'scam_indicators': 4.0
    }
    
    return keywords, weights

def calculate_spam_score(text, keywords, weights):
    """Calculate spam score based on keyword matching and patterns"""
    processed_text = preprocess_text(text)
    
    if not processed_text.strip():
        return 0.0, []
    
    total_score = 0.0
    found_indicators = []
    
    # Check for spam keywords
    for category, word_list in keywords.items():
        for keyword in word_list:
            if keyword in processed_text:
                total_score += weights[category]
                found_indicators.append(f"{keyword} ({category.replace('_', ' ').title()})")
    
    # Additional heuristics
    exclamation_count = text.count('!')
    if exclamation_count > 2:
        total_score += exclamation_count * 0.5
        found_indicators.append(f"Multiple exclamations ({exclamation_count})")
    
    # Check for excessive capitals
    caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
    if caps_ratio > 0.3:
        total_score += 2.0
        found_indicators.append(f"Excessive capitals ({caps_ratio:.1%})")
    
    # Check for suspicious patterns
    if '$' in text and any(word in processed_text for word in ['free', 'win', 'prize']):
        total_score += 1.5
        found_indicators.append("Money symbol with promotional words")
    
    # Normalize score to percentage (0-100)
    max_possible_score = 20.0
    confidence = min(100, (total_score / max_possible_score) * 100)
    
    return confidence, found_indicators

def predict_spam(message):
    """Predict if a message is spam with confidence score"""
    keywords, weights = create_spam_detector()
    confidence, indicators = calculate_spam_score(message, keywords, weights)
    
    # Threshold for spam classification
    spam_threshold = 30.0
    
    if confidence >= spam_threshold:
        prediction = "spam"
    else:
        prediction = "ham"
    
    return prediction, confidence, indicators

def spam_detection():
    """Main spam detection interface"""
    st.title("📧 Spam Detection System")
    st.markdown("*Rule-based spam detection with no external dependencies*")
    st.markdown("---")
    
    # Input section
    st.subheader("🔍 Message Analysis")
    message = st.text_area(
        "Enter message to analyze:",
        placeholder="Type or paste your message here...",
        height=120,
        help="Enter any text message to check if it's spam or legitimate"
    )
    
    # Threshold adjustment
    threshold = st.slider(
        "Spam Detection Threshold (%)",
        min_value=10,
        max_value=80,
        value=30,
        help="Minimum score required to classify as spam"
    )
    
    # Analysis section
    if st.button("🔎 Analyze Message", type="primary"):
        if message and message.strip():
            with st.spinner("Analyzing message..."):
                prediction, confidence, indicators = predict_spam(message)
                
                # Display results
                st.markdown("### 📊 Analysis Results")
                
                if confidence >= threshold:
                    st.error(f"🚨 **SPAM DETECTED** - {confidence:.1f}% spam score")
                    st.markdown("⚠️ This message shows characteristics of spam/phishing")
                else:
                    st.success(f"✅ **LEGITIMATE MESSAGE** - {confidence:.1f}% spam score")
                    st.markdown("👍 This appears to be a normal, legitimate message")
                
                # Show detected indicators
                if indicators:
                    with st.expander(f"🔍 Detected Spam Indicators ({len(indicators)})"):
                        for indicator in indicators:
                            st.write(f"• {indicator}")
                else:
                    st.info("ℹ️ No spam indicators detected")
                
                # Technical details
                with st.expander("🔬 Technical Details"):
                    st.write(f"**Classification:** {prediction.upper()}")
                    st.write(f"**Spam Score:** {confidence:.2f}%")
                    st.write(f"**Threshold:** {threshold}%")
                    st.write(f"**Processed Text:** `{preprocess_text(message)}`")
                    st.write(f"**Message Length:** {len(message)} characters")
                    st.write(f"**Indicators Found:** {len(indicators)}")
        else:
            st.warning("⚠️ Please enter a message to analyze")
    
    # Sample testing section
    st.markdown("---")
    st.subheader("🧪 Test with Sample Messages")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🚨 Spam Examples:**")
        spam_samples = [
            "FREE MONEY! Click now to claim $1000! Act immediately!",
            "URGENT! Your account will be suspended! Verify now!",
            "Congratulations! You won the lottery! Call to claim your prize!"
        ]
        for i, sample in enumerate(spam_samples, 1):
            if st.button(f"Test Spam {i}", key=f"spam_{i}", use_container_width=True):
                pred, conf, inds = predict_spam(sample)
                st.text_area("Sample:", sample, height=60, key=f"spam_text_{i}")
                if conf >= threshold:
                    st.error(f"Result: SPAM ({conf:.1f}% score)")
                else:
                    st.success(f"Result: LEGITIMATE ({conf:.1f}% score)")
    
    with col2:
        st.markdown("**✅ Legitimate Examples:**")
        ham_samples = [
            "Hi! How are you doing today?",
            "Meeting scheduled for tomorrow at 3 PM",
            "Thanks for sending the project documents"
        ]
        for i, sample in enumerate(ham_samples, 1):
            if st.button(f"Test Ham {i}", key=f"ham_{i}", use_container_width=True):
                pred, conf, inds = predict_spam(sample)
                st.text_area("Sample:", sample, height=60, key=f"ham_text_{i}")
                if conf >= threshold:
                    st.error(f"Result: SPAM ({conf:.1f}% score)")
                else:
                    st.success(f"Result: LEGITIMATE ({conf:.1f}% score)")
    
    # Sidebar information
    with st.sidebar:
        st.markdown("### 📊 Detection Method")
        st.info("""
        **Rule-Based Detection:**
        - Keyword analysis
        - Pattern recognition  
        - Heuristic scoring
        - No external files needed
        """)
        
        st.markdown("### 🎯 Detection Categories")
        keywords = get_spam_keywords()
        for category, words in keywords.items():
            category_name = category.replace('_', ' ').title()
            with st.expander(f"{category_name} ({len(words)} words)"):
                st.write(", ".join(words))
        
        st.markdown("---")
        st.markdown("### ℹ️ How It Works")
        st.markdown("""
        1. **Text Processing:** Clean and normalize input
        2. **Keyword Matching:** Check against spam vocabulary
        3. **Pattern Analysis:** Detect suspicious structures
        4. **Scoring:** Calculate weighted spam probability
        5. **Classification:** Apply threshold for final decision
        """)

# Entry point for Jarvis integration
def main():
    """Main function called by Jarvis"""
    spam_detection()

if __name__ == "__main__":
    main()
