# 🧪 Testing Guide

## ✅ Improvements Made

The web scraper has been enhanced with:
- Better Amazon review detection (multiple selectors)
- Automatic ASIN extraction and reviews page navigation
- Improved headers to avoid blocking
- Better error logging for debugging
- Support for both product pages and review pages

## 🔗 How to Get Working URLs

### For Amazon:

1. **Go to Amazon** (amazon.com or amazon.in)
2. **Search for a product** (e.g., "wireless mouse")
3. **Click on a product**
4. **Copy the URL** - Should look like:
   ```
   https://www.amazon.com/Product-Name/dp/B08XXXXXXXXX
   ```
5. **Or use the reviews page directly:**
   ```
   https://www.amazon.com/product-reviews/B08XXXXXXXXX
   ```

### Example Working URLs:

```
https://www.amazon.com/dp/B08N5WRWNW
https://www.amazon.in/dp/B08N5WRWNW
```

## 📊 Testing Steps

### Test 1: Compare Two Products

1. Go to: http://127.0.0.1:5000/compare
2. Enter two Amazon product URLs
3. Click "Compare Now!"
4. Wait 10-30 seconds
5. Check the console/logs for debugging info

### Test 2: CSV Upload

1. Create a CSV file with this format:
   ```csv
   review_title
   "Great product! Love it!"
   "Terrible quality"
   "Best purchase ever"
   "Disappointed with this"
   "Excellent service"
   ```

2. Go to: http://127.0.0.1:5000
3. Upload the CSV
4. Click "Analyze Sentiments Now!"

## 🐛 Debugging

### Check Server Logs

The server now prints detailed debugging information:
- Response status codes
- Number of reviews found
- Which selectors worked
- Any errors encountered

### View Logs in Real-Time

Run this command in a separate terminal:
```bash
# The logs will show in the terminal where you ran python backend.py
```

Or check the process output to see what's happening.

## ⚠️ Common Issues

### "Could not find enough reviews"

**Possible causes:**
1. Amazon is blocking the request
2. The URL doesn't have reviews
3. The page structure changed

**Solutions:**
- Try the direct reviews page URL: `https://www.amazon.com/product-reviews/ASIN`
- Use a product with many reviews (100+)
- Try a different product
- Use CSV upload as fallback

### Scraping Takes Too Long

- Normal for some sites (10-30 seconds)
- Check your internet connection
- Try a simpler product page

### No Reviews Scraped

- Check if the product page actually has reviews
- Try opening the URL in your browser first
- Look at the server logs for error messages

## 🎯 Best Practices

1. **Use popular products** with many reviews (50+)
2. **Test with Amazon first** (best supported)
3. **Check the URL** works in your browser
4. **Wait patiently** - scraping takes time
5. **Check server logs** for debugging info

## 📝 Sample Test Products

Try these Amazon products (they usually have many reviews):

```
Electronics:
https://www.amazon.com/dp/B08N5WRWNW (Echo Dot)
https://www.amazon.com/dp/B07XJ8C8F5 (Fire TV Stick)

Books:
https://www.amazon.com/dp/0735219095
https://www.amazon.com/dp/1501110365
```

## 🔍 Monitoring

Watch the server output for messages like:
```
Trying reviews URL: https://www.amazon.com/product-reviews/B08N5WRWNW
Response status: 200
Found 10 reviews with selector: span {'data-hook': 'review-body'}
Found 10 titles with selector: a {'data-hook': 'review-title'}
Total reviews scraped: 20
```

This tells you the scraping is working!

## 💡 Tips

- **Amazon.com** usually works better than regional sites
- **Product pages with 100+ reviews** are more reliable
- **Direct review URLs** work better than product pages
- **CSV upload** is always the most reliable method
