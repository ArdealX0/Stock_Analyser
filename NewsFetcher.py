import requests
from datetime import datetime, timedelta
import os
import json

class NewsFetcher:

    def __init__(self, api_key=None):

        self.api_key = api_key or os.environ.get('NEWSAPI_KEY')
        if not self.api_key:
            raise ValueError("NewsAPI key must be provided or set as NEWSAPI_KEY environment variable")
        
        self.base_url = "https://newsapi.org/v2/everything"
    
    def fetch_news(self, ticker, days=30, language="en", sort_by="publishedAt", page_size=100):
        
        # Calculate date range (from 30 days ago to today)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Format dates for NewsAPI
        from_date = start_date.strftime('%Y-%m-%d')
        to_date = end_date.strftime('%Y-%m-%d')
        
        # Build query for financial news
        query = f"{ticker} AND (stock OR investor OR market OR financial OR earnings OR share OR trading)"
        
        # Set up parameters for the API request
        params = {
            'q': query,
            'from': from_date,
            'to': to_date,
            'language': language,
            'sortBy': sort_by,
            'pageSize': page_size,
            'apiKey': self.api_key
        }
        
        # Make the request
        response = requests.get(self.base_url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            api_response = response.json()
            articles = api_response.get('articles', [])
            
            # Process articles into a format suitable for sentiment analysis
            processed_articles = []
            for article in articles:
                processed_article = {
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'content': article.get('content', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'published_at': article.get('publishedAt', ''),
                    'sentiment': None  # To be filled by sentiment analyzer
                }
                processed_articles.append(processed_article)
            
            return processed_articles
        else:
            error_message = f"Error fetching news. Status code: {response.status_code}"
            try:
                error_details = response.json()
                error_message += f", Details: {error_details['message']}"
            except:
                error_message += f", Response: {response.text}"
            
            raise Exception(error_message)
    
    def clear_existing_files(self, ticker):

        filename = f"{ticker.upper()}_news.json"
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Removed existing file: {filename}")
    
    def save_to_file(self, ticker, articles):
        
        # Create a standard filename based on the ticker
        filename = f"{ticker.upper()}_news.json"
        
        # Create the json output structure
        output_data = {
            'ticker': ticker.upper(),
            'fetch_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'article_count': len(articles),
            'articles': articles
        }
        
        # Write to file (will overwrite if exists)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        return filename
 
def main():

    # REPLACE THESE VALUES WITH YOUR OWN
    api_key = "fb9c35a1127340a6bd373bd7194e2d26"  
    ticker = "AAPL" 
    days = 30  
    
    try:
        # Initialize the NewsFetcher with hardcoded API key
        fetcher = NewsFetcher(api_key=api_key)
        
        # Clear any existing files for this ticker
        fetcher.clear_existing_files(ticker)
        
        # Fetch the news for hardcoded ticker
        print(f"Fetching news for {ticker} from the past {days} days...")
        articles = fetcher.fetch_news(ticker, days=days)
        
        # Save to file
        output_file = fetcher.save_to_file(ticker, articles)
        print(f"Saved {len(articles)} articles to {output_file}")
            
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()