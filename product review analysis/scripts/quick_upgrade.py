"""
Quick Model Upgrade - Retrain with sample data to fix version warnings
"""

import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegressionCV
import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

# Download NLTK data
try:
    stopwords_set = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stopwords_set = set(stopwords.words('english'))

emoticon_pattern = re.compile(r'(?::|;|=)(?:-)?(?:\)|\(|D|P)')

def preprocessing(text):
    text = re.sub('<[^>]*>', '', text)
    emojis = emoticon_pattern.findall(text)
    text = re.sub(r'[\W+]', ' ', text.lower()) + ' '.join(emojis).replace('-', '')
    prter = PorterStemmer()
    text = [prter.stem(word) for word in text.split() if word not in stopwords_set]
    return " ".join(text)

# Sample training data
reviews = [
    'This product is amazing! Love it!', 'Terrible quality, waste of money',
    'Best purchase ever, highly recommend', 'Disappointed with the product',
    'Excellent service and great product', 'Poor quality, broke after one use',
    'Fantastic! Exceeded my expectations', 'Not worth the price, very bad',
    'Outstanding quality and fast delivery', 'Horrible experience, do not buy',
    'Perfect! Exactly what I needed', 'Cheap material, very disappointed',
    'Absolutely love this product!', 'Worst purchase I have ever made',
    'Great value for money', 'Defective product, requesting refund',
    'Superb quality, will buy again', 'Useless product, total waste',
    'Highly satisfied with my purchase', 'Terrible customer service',
    'Good product, works well', 'Bad experience, not recommended',
    'Awesome quality!', 'Very poor service', 'Highly recommend this!',
    'Complete waste of money', 'Love everything about it', 'Disappointed',
    'Excellent product', 'Terrible', 'Great!', 'Awful', 'Perfect', 'Horrible'
]

labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
          1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

print("🔄 Preprocessing reviews...")
processed_reviews = [preprocessing(r) for r in reviews]

print("🔤 Training TF-IDF Vectorizer...")
tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X = tfidf.fit_transform(processed_reviews)

print("🤖 Training Logistic Regression model...")
clf = LogisticRegressionCV(cv=3, random_state=42, max_iter=1000)
clf.fit(X, labels)

print("💾 Saving upgraded models...")
with open('models/clf.pkl', 'wb') as f:
    pickle.dump(clf, f)
print("✅ Saved models/clf.pkl")

with open('models/tfidf.pkl', 'wb') as f:
    pickle.dump(tfidf, f)
print("✅ Saved models/tfidf.pkl")

print("\n🎉 Models upgraded successfully!")
print("⚠️  Note: These are trained on sample data. For production, use upgrade_model.py with your real data.")
