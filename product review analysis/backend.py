from flask import Flask, render_template, request, jsonify
import pickle
import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import sklearn
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

# Download required NLTK data
try:
    stopwords_set = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stopwords_set = set(stopwords.words('english'))

emoticon_pattern = re.compile(r'(?::|;|=)(?:-)?(?:\)|\(|D|P)')

app = Flask(__name__)

with open('models/clf.pkl', 'rb') as f:
    clf = pickle.load(f)
with open('models/tfidf.pkl', 'rb') as f:
    tfidf = pickle.load(f)


def preprocessing(text):
    text = re.sub('<[^>]*>', '', text)
    emojis = emoticon_pattern.findall(text)
    text = re.sub(r'[\W+]', ' ', text.lower()) + ' '.join(emojis).replace('-', '')
    prter = PorterStemmer()
    text = [prter.stem(word) for word in text.split() if word not in stopwords_set]
    return " ".join(text)


def scrape_amazon_reviews(url, max_reviews=50):
    """Scrape reviews from Amazon product page"""
    reviews = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        # If it's a product page, try to get the reviews page
        if '/dp/' in url or '/product/' in url:
            # Extract ASIN
            import re
            asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
            if not asin_match:
                asin_match = re.search(r'/product/([A-Z0-9]{10})', url)
            
            if asin_match:
                asin = asin_match.group(1)
                # Try to get reviews page
                domain = 'amazon.com' if 'amazon.com' in url else 'amazon.in'
                reviews_url = f'https://www.{domain}/product-reviews/{asin}'
                print(f"Trying reviews URL: {reviews_url}")
                response = requests.get(reviews_url, headers=headers, timeout=15)
            else:
                response = requests.get(url, headers=headers, timeout=15)
        else:
            response = requests.get(url, headers=headers, timeout=15)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        print(f"Response status: {response.status_code}")
        
        # Try multiple Amazon review selectors
        selectors = [
            ('span', {'data-hook': 'review-body'}),
            ('div', {'data-hook': 'review-body'}),
            ('div', {'class': 'review-text-content'}),
            ('div', {'class': 'a-expander-content reviewText review-text-content'}),
            ('span', {'class': 'review-text-content'}),
        ]
        
        for tag, attrs in selectors:
            review_elements = soup.find_all(tag, attrs)
            if review_elements:
                print(f"Found {len(review_elements)} reviews with selector: {tag} {attrs}")
                for element in review_elements[:max_reviews]:
                    review_text = element.get_text(strip=True)
                    # Clean up common Amazon text
                    review_text = review_text.replace('Read more', '').strip()
                    if review_text and len(review_text) > 15:
                        reviews.append(review_text)
                if reviews:
                    break
        
        # Also get review titles
        title_selectors = [
            ('a', {'data-hook': 'review-title'}),
            ('span', {'data-hook': 'review-title'}),
            ('div', {'data-hook': 'review-title'}),
        ]
        
        for tag, attrs in title_selectors:
            title_elements = soup.find_all(tag, attrs)
            if title_elements:
                print(f"Found {len(title_elements)} titles with selector: {tag} {attrs}")
                for element in title_elements[:max_reviews]:
                    title_text = element.get_text(strip=True)
                    # Remove star ratings from titles
                    title_text = re.sub(r'^\d+\.\d+\s+out of \d+ stars\s*', '', title_text)
                    if title_text and len(title_text) > 5 and title_text not in reviews:
                        reviews.append(title_text)
                if len(reviews) >= 10:
                    break
        
        print(f"Total reviews scraped: {len(reviews)}")
                
    except Exception as e:
        print(f"Error scraping Amazon: {e}")
        import traceback
        traceback.print_exc()
    
    return reviews


def scrape_generic_reviews(url, max_reviews=50):
    """Generic scraper for other websites"""
    reviews = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(f"Generic scraper - Response status: {response.status_code}")
        
        # Look for common review patterns
        possible_selectors = [
            {'class': re.compile(r'review', re.I)},
            {'class': re.compile(r'comment', re.I)},
            {'class': re.compile(r'feedback', re.I)},
            {'itemprop': 'reviewBody'},
            {'itemprop': 'description'},
            {'data-hook': re.compile(r'review', re.I)},
        ]
        
        for selector in possible_selectors:
            elements = soup.find_all(['p', 'div', 'span'], selector)
            print(f"Found {len(elements)} elements with selector: {selector}")
            for element in elements[:max_reviews]:
                text = element.get_text(strip=True)
                if text and 20 < len(text) < 500 and text not in reviews:
                    reviews.append(text)
            
            if len(reviews) >= 10:
                break
        
        print(f"Generic scraper found {len(reviews)} reviews")
                
    except Exception as e:
        print(f"Error scraping: {e}")
        import traceback
        traceback.print_exc()
    
    return reviews[:max_reviews]


def scrape_reviews_from_url(url, max_reviews=50):
    """Main function to scrape reviews based on URL"""
    domain = urlparse(url).netloc.lower()
    
    if 'amazon' in domain:
        return scrape_amazon_reviews(url, max_reviews)
    else:
        return scrape_generic_reviews(url, max_reviews)


def analyze_reviews(reviews):
    """Analyze a list of reviews and return sentiment stats"""
    if not reviews:
        return None
    
    # Preprocess reviews
    processed_reviews = [preprocessing(r) for r in reviews]
    
    # Vectorize
    vectors = tfidf.transform(processed_reviews)
    
    # Predict
    predictions = clf.predict(vectors)
    
    # Calculate stats
    positive_count = int(list(predictions).count(1))
    negative_count = int(list(predictions).count(0))
    total = positive_count + negative_count
    
    if total == 0:
        return None
    
    positive_percentage = (positive_count / total) * 100
    
    if positive_count > negative_count:
        sentiment = "POSITIVE"
    elif negative_count > positive_count:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"
    
    return {
        'sentiment': sentiment,
        'positive': positive_count,
        'negative': negative_count,
        'total': total,
        'positive_percentage': round(positive_percentage, 1),
        'negative_percentage': round(100 - positive_percentage, 1)
    }

@app.route('/', methods=['GET', 'POST'])
def analyze_sentiment():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')

        if uploaded_file:
            # Read CSV
            df = pd.read_csv(uploaded_file)

            # Expect column name "review_title"
            reviews = df['review_title'].astype(str).tolist()

            # Preprocess all reviews
            processed_reviews = [preprocessing(r) for r in reviews]

            # Vectorize all reviews
            vectors = tfidf.transform(processed_reviews)

            # Predict sentiments
            predictions = clf.predict(vectors)

            # Count positive/negative
            positive_count = list(predictions).count(1)
            negative_count = list(predictions).count(0)

            # Majority sentiment
            if positive_count > negative_count:
                final_sentiment = "Overall Sentiment: POSITIVE"
            elif negative_count > positive_count:
                final_sentiment = "Overall Sentiment: NEGATIVE"
            else:
                final_sentiment = "Both sentiments are equal."

            return render_template('frontend.html',
                                   sentiment=final_sentiment,
                                   positive=positive_count,
                                   negative=negative_count)

    return render_template('frontend.html')


@app.route('/compare', methods=['GET', 'POST'])
def compare_products():
    if request.method == 'POST':
        url1 = request.form.get('url1', '').strip()
        url2 = request.form.get('url2', '').strip()
        
        if not url1 or not url2:
            return render_template('compare.html', error="Please provide both URLs")
        
        # Scrape reviews from both URLs
        print(f"Scraping reviews from URL 1: {url1}")
        reviews1 = scrape_reviews_from_url(url1)
        
        print(f"Scraping reviews from URL 2: {url2}")
        reviews2 = scrape_reviews_from_url(url2)
        
        if not reviews1 or len(reviews1) < 3:
            return render_template('compare.html', 
                                 error="Could not find enough reviews from Product 1. Try a different URL or use CSV upload.")
        
        if not reviews2 or len(reviews2) < 3:
            return render_template('compare.html', 
                                 error="Could not find enough reviews from Product 2. Try a different URL or use CSV upload.")
        
        # Analyze both products
        result1 = analyze_reviews(reviews1)
        result2 = analyze_reviews(reviews2)
        
        # Determine winner
        if result1['positive_percentage'] > result2['positive_percentage']:
            winner = "product1"
            winner_text = "Product 1 has better reviews!"
        elif result2['positive_percentage'] > result1['positive_percentage']:
            winner = "product2"
            winner_text = "Product 2 has better reviews!"
        else:
            winner = "tie"
            winner_text = "Both products have similar reviews!"
        
        return render_template('compare.html',
                             url1=url1,
                             url2=url2,
                             result1=result1,
                             result2=result2,
                             winner=winner,
                             winner_text=winner_text)
    
    return render_template('compare.html')


if __name__ == '__main__':
    app.run(debug=True)
