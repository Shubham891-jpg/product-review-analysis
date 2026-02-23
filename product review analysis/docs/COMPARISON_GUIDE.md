# 🆚 Product Comparison Feature Guide

## 🎉 New Feature Added!

Your sentiment analysis app now supports comparing reviews from two different products!

## 🌐 How to Use

### Option 1: Compare Products by URL

1. **Open your browser** and go to: http://127.0.0.1:5000/compare
2. **Enter two product URLs** (Amazon, Flipkart, or any e-commerce site)
3. **Click "Compare Now!"**
4. **See the comparison** with:
   - Side-by-side sentiment analysis
   - Winner highlighted with 🏆
   - Visual progress bars
   - Detailed statistics

### Option 2: Single Product Analysis (CSV)

1. Go to: http://127.0.0.1:5000
2. Upload CSV file with reviews
3. Get detailed sentiment analysis

## 📊 What You'll See

### Comparison Results Include:
- **Sentiment Score** for each product (Positive/Negative/Neutral)
- **Review Counts** (positive, negative, total)
- **Percentage Breakdown** with visual progress bars
- **Winner Declaration** 🏆
- **Emoji Indicators** (😊 for positive, 😔 for negative)

## 🔗 Supported Websites

The scraper works best with:
- ✅ Amazon (all regions)
- ✅ Flipkart
- ✅ Most e-commerce sites with reviews
- ⚠️ Some sites may block scraping (use CSV upload instead)

## 📝 Example URLs to Try

### Amazon:
```
https://www.amazon.com/dp/PRODUCT_ID
https://www.amazon.in/product-name/dp/PRODUCT_ID
```

### Flipkart:
```
https://www.flipkart.com/product-name/p/PRODUCT_ID
```

## ⚠️ Important Notes

1. **Scraping Time**: May take 10-30 seconds per product
2. **Review Limit**: Scrapes up to 50 reviews per product
3. **Rate Limiting**: Some sites may block too many requests
4. **Fallback**: If scraping fails, use CSV upload method

## 🎯 Tips for Best Results

1. **Use direct product pages** with reviews visible
2. **Ensure URLs are complete** (include https://)
3. **Compare similar products** for meaningful results
4. **Check review count** - more reviews = better accuracy

## 🚀 Navigation

- **📊 Single Analysis**: http://127.0.0.1:5000
- **🆚 Compare Products**: http://127.0.0.1:5000/compare

Use the navigation pills at the top to switch between modes!

## 🛠️ Technical Details

### Web Scraping Features:
- Automatic site detection (Amazon, generic)
- Multiple selector patterns for compatibility
- User-agent rotation to avoid blocks
- Error handling and fallbacks

### Analysis Features:
- Same ML model used for both methods
- Consistent preprocessing pipeline
- Real-time sentiment calculation
- Percentage-based comparison

## 🐛 Troubleshooting

**"Could not find enough reviews" error:**
- Try a different product URL
- Use the CSV upload method instead
- Check if the page has visible reviews

**Scraping takes too long:**
- Normal for some sites (up to 30 seconds)
- Check your internet connection
- Try a different product page

**Comparison seems inaccurate:**
- Ensure both products have enough reviews
- Check if reviews were properly scraped
- Consider using CSV upload for better control

## 📈 Future Enhancements

Potential improvements:
- Support for more e-commerce sites
- Bulk comparison (3+ products)
- Review text display
- Export comparison results
- Historical tracking
