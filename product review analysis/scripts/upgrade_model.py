"""
Model Upgrade Script for Sentiment Analysis
This script helps you retrain your model with the current scikit-learn version (1.7.2)
"""

import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

# Download required NLTK data
try:
    stopwords_set = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stopwords_set = set(stopwords.words('english'))

emoticon_pattern = re.compile(r'(?::|;|=)(?:-)?(?:\)|\(|D|P)')


def preprocessing(text):
    """Preprocess text for sentiment analysis"""
    text = re.sub('<[^>]*>', '', text)
    emojis = emoticon_pattern.findall(text)
    text = re.sub(r'[\W+]', ' ', text.lower()) + ' '.join(emojis).replace('-', '')
    prter = PorterStemmer()
    text = [prter.stem(word) for word in text.split() if word not in stopwords_set]
    return " ".join(text)


def train_model_from_csv(csv_path, review_column='review_title', label_column='sentiment'):
    """
    Train a new model from your CSV data
    
    Parameters:
    - csv_path: Path to your training CSV file
    - review_column: Name of the column containing reviews
    - label_column: Name of the column containing labels (0=negative, 1=positive)
    """
    print("📊 Loading training data...")
    df = pd.read_csv(csv_path)
    
    print(f"✅ Loaded {len(df)} reviews")
    print(f"📝 Columns: {df.columns.tolist()}")
    
    # Check if label column exists
    if label_column not in df.columns:
        print(f"⚠️  Label column '{label_column}' not found!")
        print("Available columns:", df.columns.tolist())
        return None, None
    
    # Preprocess reviews
    print("🔄 Preprocessing reviews...")
    df['processed'] = df[review_column].astype(str).apply(preprocessing)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['processed'], 
        df[label_column], 
        test_size=0.2, 
        random_state=42
    )
    
    print(f"📚 Training set: {len(X_train)} reviews")
    print(f"🧪 Test set: {len(X_test)} reviews")
    
    # Train TF-IDF Vectorizer
    print("🔤 Training TF-IDF Vectorizer...")
    tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)
    
    # Train Logistic Regression model
    print("🤖 Training Logistic Regression model...")
    clf = LogisticRegressionCV(cv=5, random_state=42, max_iter=1000, n_jobs=-1)
    clf.fit(X_train_tfidf, y_train)
    
    # Evaluate model
    print("\n📈 Model Evaluation:")
    y_pred = clf.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"✅ Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Negative', 'Positive']))
    
    print("\n🎯 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Save models
    print("\n💾 Saving upgraded models...")
    with open('models/clf.pkl', 'wb') as f:
        pickle.dump(clf, f)
    print("✅ Saved models/clf.pkl")
    
    with open('models/tfidf.pkl', 'wb') as f:
        pickle.dump(tfidf, f)
    print("✅ Saved models/tfidf.pkl")
    
    print("\n🎉 Model upgrade complete!")
    return clf, tfidf


def create_sample_dataset():
    """Create a sample dataset for demonstration"""
    print("📝 Creating sample dataset...")
    
    sample_data = {
        'review_title': [
            'This product is amazing! Love it!',
            'Terrible quality, waste of money',
            'Best purchase ever, highly recommend',
            'Disappointed with the product',
            'Excellent service and great product',
            'Poor quality, broke after one use',
            'Fantastic! Exceeded my expectations',
            'Not worth the price, very bad',
            'Outstanding quality and fast delivery',
            'Horrible experience, do not buy',
            'Perfect! Exactly what I needed',
            'Cheap material, very disappointed',
            'Absolutely love this product!',
            'Worst purchase I have ever made',
            'Great value for money',
            'Defective product, requesting refund',
            'Superb quality, will buy again',
            'Useless product, total waste',
            'Highly satisfied with my purchase',
            'Terrible customer service'
        ],
        'sentiment': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv('sample_training_data.csv', index=False)
    print("✅ Created sample_training_data.csv")
    return 'sample_training_data.csv'


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Sentiment Analysis Model Upgrade Tool")
    print("=" * 60)
    print()
    
    print("Choose an option:")
    print("1. Train with your own CSV file")
    print("2. Train with sample data (demo)")
    print()
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == '1':
        csv_path = input("Enter path to your CSV file: ").strip()
        review_col = input("Enter review column name (default: review_title): ").strip() or 'review_title'
        label_col = input("Enter label column name (default: sentiment): ").strip() or 'sentiment'
        
        print()
        train_model_from_csv(csv_path, review_col, label_col)
        
    elif choice == '2':
        print()
        csv_path = create_sample_dataset()
        print()
        train_model_from_csv(csv_path, 'review_title', 'sentiment')
        
    else:
        print("❌ Invalid choice!")
