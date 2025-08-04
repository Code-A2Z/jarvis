import sys
import os
import pandas as pd
import pickle
sys.path.append('.')

print("🔍 Debugging Spam Detection Model...")

try:
    # Load the model files directly
    data_dir = os.path.join('src/apps/pages/models/SpamDetection', 'data')
    models_dir = os.path.join('src/apps/pages/models/SpamDetection', 'models')
    
    print(f"📁 Data directory: {data_dir}")
    print(f"📁 Models directory: {models_dir}")
    
    # Check files exist
    dataset_path = os.path.join(data_dir, 'spam_dataset.pkl')
    vectorizer_path = os.path.join(models_dir, 'vectorizer.pkl')
    model_path = os.path.join(models_dir, 'spam_model.pkl')
    
    print(f"📄 Dataset exists: {os.path.exists(dataset_path)}")
    print(f"📄 Vectorizer exists: {os.path.exists(vectorizer_path)}")
    print(f"📄 Model exists: {os.path.exists(model_path)}")
    
    # Load and inspect dataset
    if os.path.exists(dataset_path):
        spam_data = pd.read_pickle(dataset_path)
        print(f"📊 Dataset shape: {spam_data.shape}")
        print(f"📊 Dataset columns: {spam_data.columns.tolist()}")
        if 'label' in spam_data.columns:
            print(f"📊 Label distribution:")
            print(spam_data['label'].value_counts())
        print(f"📊 First few rows:")
        print(spam_data.head(3))
    
    # Load and test vectorizer
    if os.path.exists(vectorizer_path):
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        print(f"🔤 Vectorizer type: {type(vectorizer)}")
        print(f"🔤 Vectorizer vocabulary size: {len(vectorizer.vocabulary_) if hasattr(vectorizer, 'vocabulary_') else 'N/A'}")
        
        # Test vectorizer
        test_text = "Free money now!"
        vector = vectorizer.transform([test_text])
        print(f"🔤 Test vector shape: {vector.shape}")
        print(f"🔤 Test vector non-zero elements: {vector.nnz}")
    
    # Load and test model
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print(f"🤖 Model type: {type(model)}")
        print(f"🤖 Model classes: {model.classes_ if hasattr(model, 'classes_') else 'N/A'}")
        
        # Test prediction
        if os.path.exists(vectorizer_path):
            test_messages = [
                "Free money now!",
                "Hi, how are you?",
                "URGENT! Click here to claim prize!",
                "Meeting at 3pm tomorrow"
            ]
            
            for msg in test_messages:
                vector = vectorizer.transform([msg])
                prediction = model.predict(vector)[0]
                probabilities = model.predict_proba(vector)[0]
                confidence = max(probabilities) * 100
                print(f"🧪 '{msg}' -> {prediction} ({confidence:.1f}%)")
                print(f"    Probabilities: {dict(zip(model.classes_, probabilities))}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
