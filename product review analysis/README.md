# 🎯 Product Review Sentiment Analysis & Comparison

A beautiful Flask web application that analyzes and compares product reviews using AI-powered sentiment detection.

## ✨ Features

- 📊 **Single Product Analysis** - Upload CSV files with reviews
- 🆚 **Product Comparison** - Compare two products by URL
- 🕷️ **Web Scraping** - Automatically scrape reviews from Amazon, Flipkart, etc.
- 🎨 **Dynamic UI** - Animated gradients, emojis, and interactive elements
- 📈 **Visual Analytics** - Progress bars, charts, and statistics
- 🏆 **Winner Detection** - Automatically highlights the better product
- 🤖 **ML-Powered** - Uses Logistic Regression and TF-IDF for accurate predictions

## 🚀 Quick Start

1. **Activate the virtual environment:**
   ```bash
   .venv\Scripts\activate
   ```

2. **Run the application:**
   ```bash
   python backend.py
   ```

3. **Open your browser:**
   - Single Analysis: http://127.0.0.1:5000
   - Compare Products: http://127.0.0.1:5000/compare

## 📖 Usage

### Option 1: CSV Upload (Single Product)
1. Go to http://127.0.0.1:5000
2. Upload a CSV file with a `review_title` column
3. Click "Analyze Sentiments Now!"
4. View results with emojis and statistics

### Option 2: URL Comparison (Two Products)
1. Go to http://127.0.0.1:5000/compare
2. Enter two product URLs (Amazon, Flipkart, etc.)
3. Click "Compare Now!"
4. See side-by-side comparison with winner 🏆

## 📁 Project Structure

```
product-review-analysis/
├── backend.py              # Flask application (main entry point)
├── templates/              # HTML templates
│   ├── frontend.html       # Single analysis page
│   └── compare.html        # Comparison page
├── models/                 # ML models
│   ├── clf.pkl            # Trained classifier
│   └── tfidf.pkl          # TF-IDF vectorizer
├── scripts/               # Utility scripts
│   ├── upgrade_model.py   # Full model retraining
│   └── quick_upgrade.py   # Quick model upgrade
├── docs/                  # Documentation
│   ├── COMPARISON_GUIDE.md
│   ├── MODEL_UPGRADE_GUIDE.md
│   └── TESTING_GUIDE.md
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Requirements

- Python 3.12+
- Flask
- scikit-learn
- pandas
- nltk
- beautifulsoup4
- requests

Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎓 Model Upgrade

If you see scikit-learn version warnings, upgrade the models:

```bash
python scripts/quick_upgrade.py
```

For detailed model training with your own data:
```bash
python scripts/upgrade_model.py
```

See `docs/MODEL_UPGRADE_GUIDE.md` for more details.

## 📊 CSV Format

Your CSV file should have a `review_title` column:

```csv
review_title
"Great product! Love it!"
"Terrible quality, waste of money"
"Best purchase ever"
```

## 🌐 Supported Websites

- ✅ Amazon (all regions)
- ✅ Flipkart
- ✅ Most e-commerce sites with reviews

## 🎨 UI Features

- Animated gradient backgrounds
- Emoji indicators (😊 😔 🎉)
- Progress bars with percentages
- Interactive hover effects
- Loading animations
- Glassmorphism design
- Responsive layout

## 📚 Documentation

- `docs/COMPARISON_GUIDE.md` - Product comparison feature guide
- `docs/MODEL_UPGRADE_GUIDE.md` - Model training and upgrade guide
- `docs/TESTING_GUIDE.md` - Testing and debugging guide

## 🐛 Troubleshooting

**Scraping fails:**
- Use CSV upload instead
- Try different product URLs
- Check internet connection

**Model warnings:**
- Run `python quick_upgrade.py`
- Restart the Flask app

**No reviews found:**
- Ensure URL has visible reviews
- Try Amazon product pages
- Use CSV upload as fallback

## 🎯 Future Enhancements

- [ ] Support for more e-commerce sites
- [ ] Bulk comparison (3+ products)
- [ ] Export results to PDF/CSV
- [ ] Historical tracking
- [ ] API endpoints
- [ ] Docker support

## 📝 License

This project is for educational purposes.

## 🤝 Contributing

Feel free to fork, improve, and submit pull requests!

---

Made with ❤️ using Flask, scikit-learn, and lots of emojis! 🎉
