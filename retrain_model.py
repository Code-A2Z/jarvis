import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import re

def retrain_spam_model():
    """Retrain the spam detection model with better generalization"""
    
    # Load the dataset
    data_dir = 'src/apps/pages/models/SpamDetection/data'
    models_dir = 'src/apps/pages/models/SpamDetection/models'
    
    spam_data = pd.read_pickle(os.path.join(data_dir, 'spam_dataset.pkl'))
    print(f"📊 Original dataset: {spam_data.shape}")
    print(spam_data['label'].value_counts())
    
    # Preprocess function
    def preprocess_text(text):
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = ' '.join(text.split())
        return text
    
    # Clean the data
    spam_data['text'] = spam_data['text'].apply(preprocess_text)
    
    # Remove duplicates to prevent overfitting
    spam_data = spam_data.drop_duplicates(subset=['text'])
    print(f"📊 After deduplication: {spam_data.shape}")
    
    # Split the data
    X = spam_data['text']
    y = spam_data['label']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Create TF-IDF vectorizer with better parameters for generalization
    vectorizer = TfidfVectorizer(
        max_features=3000,  # Reduced from 5000 to prevent overfitting
        min_df=2,          # Words must appear at least 2 times
        max_df=0.95,       # Ignore words that appear in 95%+ of documents
        stop_words='english',
        ngram_range=(1, 2), # Include bigrams for better context
        sublinear_tf=True   # Use sublinear scaling
    )
    
    # Transform the data
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Train Naive Bayes with smoothing
    model = MultinomialNB(alpha=0.1)  # Reduced alpha for less smoothing
    model.fit(X_train_vec, y_train)
    
    # Evaluate
    train_accuracy = model.score(X_train_vec, y_train)
    test_accuracy = model.score(X_test_vec, y_test)
    
    print(f"🎯 Training accuracy: {train_accuracy:.3f}")
    print(f"🎯 Test accuracy: {test_accuracy:.3f}")
    
    # Check for overfitting
    if train_accuracy - test_accuracy > 0.05:
        print("⚠️ Warning: Model might be overfitting!")
    
    # Detailed classification report
    y_pred = model.predict(X_test_vec)
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Test on new examples
    new_test_cases = [
        "Free money! Click here now!",
        "Hello, how are you doing?",
        "URGENT: Account suspended!",
        "Meeting at 3pm tomorrow",
        "Win cash prizes today!",
        "Thanks for the documents"
    ]
    
    print("\n🧪 Testing on new examples:")
    for text in new_test_cases:
        processed = preprocess_text(text)
        vector = vectorizer.transform([processed])
        prediction = model.predict(vector)[0]
        probabilities = model.predict_proba(vector)[0]
        confidence = max(probabilities) * 100
        
        print(f"'{text}' -> {prediction} ({confidence:.1f}%)")
    
    # Save the improved model
    print("\n💾 Saving improved model...")
    
    with open(os.path.join(models_dir, 'vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)
    
    with open(os.path.join(models_dir, 'spam_model.pkl'), 'wb') as f:
        pickle.dump(model, f)
    
    # Update model info
    model_info = {
        'total_messages': len(spam_data),
        'spam_count': (spam_data['label'] == 'spam').sum(),
        'ham_count': (spam_data['label'] == 'ham').sum(),
        'features': X_train_vec.shape[1],
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'model_type': 'MultinomialNB',
        'vectorizer_params': {
            'max_features': vectorizer.max_features,
            'min_df': vectorizer.min_df,
            'max_df': vectorizer.max_df,
            'ngram_range': vectorizer.ngram_range
        }
    }
    
    with open(os.path.join(data_dir, 'model_info.pkl'), 'wb') as f:
        pickle.dump(model_info, f)
    
    print("✅ Model retrained and saved successfully!")
    print(f"📊 Final stats: {model_info['total_messages']} messages, {model_info['features']} features")

if __name__ == "__main__":
    retrain_spam_model()
