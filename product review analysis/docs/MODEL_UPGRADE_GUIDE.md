# 🚀 Model Upgrade Guide

Your current models were trained with scikit-learn 1.0.2, but you're using version 1.7.2. This causes compatibility warnings. Here's how to upgrade:

## 📋 Options

### Option 1: Quick Upgrade (Sample Data) ⚡
**Use this if:** You just want to eliminate warnings quickly for testing

```bash
python quick_upgrade.py
```

This will:
- Train new models with sample data
- Save them in the current scikit-learn version (1.7.2)
- Remove all version warnings
- ⚠️ Note: Models will be less accurate (trained on only 34 samples)

### Option 2: Full Upgrade (Your Data) 🎯
**Use this if:** You have your original training data and want accurate models

```bash
python upgrade_model.py
```

Then follow the prompts:
1. Choose option 1 (train with your own CSV)
2. Provide path to your training CSV file
3. Specify column names:
   - Review column (e.g., "review_title", "review", "text")
   - Label column (e.g., "sentiment", "label") - should contain 0 (negative) or 1 (positive)

**CSV Format Example:**
```csv
review_title,sentiment
"Great product!",1
"Terrible quality",0
"Love it!",1
```

### Option 3: Demo with Sample Data 📝
**Use this if:** You want to see how it works first

```bash
python upgrade_model.py
```

Then choose option 2 - this will:
- Create a sample CSV file
- Train models on it
- Show you the process

## 🔍 What Gets Upgraded?

Both scripts will create new versions of:
- `clf.pkl` - Logistic Regression classifier
- `tfidf.pkl` - TF-IDF vectorizer

## 📊 Model Performance

After upgrading with your own data, you'll see:
- ✅ Accuracy score
- 📊 Classification report (precision, recall, F1-score)
- 🎯 Confusion matrix

## ⚠️ Important Notes

1. **Backup your current models** before upgrading:
   ```bash
   copy clf.pkl clf_backup.pkl
   copy tfidf.pkl tfidf_backup.pkl
   ```

2. **Training data requirements:**
   - CSV format
   - At least 100+ reviews recommended
   - Balanced classes (similar number of positive/negative)
   - Labels: 0 = negative, 1 = positive

3. **After upgrading:**
   - Restart your Flask app
   - Test with sample CSV files
   - Compare results with old model

## 🎓 Training Your Own Model from Scratch

If you want to collect and train on new data:

1. Collect product reviews with labels
2. Create CSV with columns: `review_title`, `sentiment`
3. Run: `python upgrade_model.py`
4. Choose option 1 and provide your CSV path

## 🆘 Troubleshooting

**"Column not found" error:**
- Check your CSV column names
- Provide correct column names when prompted

**Low accuracy:**
- Need more training data (500+ reviews recommended)
- Balance positive/negative samples
- Clean your data (remove duplicates, empty reviews)

**Memory errors:**
- Reduce `max_features` in TfidfVectorizer
- Use smaller training dataset

## 📚 Next Steps

After upgrading:
1. Test the app with sample reviews
2. Monitor prediction accuracy
3. Collect more data if needed
4. Retrain periodically with new reviews
