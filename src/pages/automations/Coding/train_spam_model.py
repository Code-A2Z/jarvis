# Spam Detection Model Training Script
# This script downloads the SMS Spam Collection dataset, preprocesses it, trains a Naive Bayes model, and saves the model and vectorizer.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import pickle
import os
import urllib.request

# Download dataset if not present
dataset_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip'
dataset_path = 'src/pages/automations/Coding/smsspamcollection.zip'
extracted_path = 'src/pages/automations/Coding/SMSSpamCollection'

if not os.path.exists(extracted_path):
    print('Downloading dataset...')
    urllib.request.urlretrieve(dataset_url, dataset_path)
    import zipfile
    with zipfile.ZipFile(dataset_path, 'r') as zip_ref:
        zip_ref.extractall('src/pages/automations/Coding/')

# Load dataset
data = pd.read_csv(extracted_path, sep='\t', header=None, names=['label', 'message'])

# Preprocessing
from collections import Counter
from sklearn.utils import resample
from sklearn.metrics import confusion_matrix, classification_report

X = data['message']
y = data['label'].map({'ham': 0, 'spam': 1})

# Print class distribution
print('Class distribution before balancing:', Counter(y))

# Combine X and y for upsampling
df = pd.DataFrame({'message': X, 'label': y})
df_majority = df[df.label == 0]
df_minority = df[df.label == 1]

# Upsample minority class
df_minority_upsampled = resample(df_minority, 
                                 replace=True,     # sample with replacement
                                 n_samples=len(df_majority),    # to match majority class
                                 random_state=42) # reproducible results

df_balanced = pd.concat([df_majority, df_minority_upsampled])

# Shuffle the dataset
df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

print('Class distribution after balancing:', Counter(df_balanced.label))

X = df_balanced['message']
y = df_balanced['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorization
vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Model training
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Evaluation
preds = model.predict(X_test_vec)
acc = accuracy_score(y_test, preds)
cm = confusion_matrix(y_test, preds)
print(f'Accuracy: {acc:.4f}')
print('Confusion Matrix:')
print(cm)
print('Classification Report:')
print(classification_report(y_test, preds, target_names=["Not Spam", "Spam"]))

# Save model and vectorizer
with open('src/pages/automations/Coding/spam_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('src/pages/automations/Coding/spam_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print('Model and vectorizer saved successfully!')
