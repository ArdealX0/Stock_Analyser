import requests
from datetime import datetime, timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

class NewsFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
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
            
            # Process articles to include title and content when available
            processed_articles = []
            for article in articles:
                processed_article = {
                    'title': article.get('title', ''),
                    'content': article.get('description', '')  # Use description as content
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


class SentimentAnalyzer:
    def __init__(self):
        try:
            nltk.data.find('vader_lexicon')
        except LookupError:
            nltk.download('vader_lexicon')
        
        # Initialize VADER sentiment analyzer
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, articles, ticker):
        """
        Analyzes sentiment of a list of articles using NLTK's VADER.
        """
        results = []
        for article in articles:
            title = article['title']
            content = article['content']
            
            # Combine title and content for better sentiment analysis
            text = f"{title}. {content}"
            
            # Get sentiment scores
            scores = self.analyzer.polarity_scores(text)
            
            # Determine sentiment label based on compound score
            sentiment_label = self._get_sentiment_label(scores['compound'])
            
            result = {
                'title': title,
                'sentiment_score': scores['compound'],
                'sentiment_label': sentiment_label,
                'ticker': ticker.upper(),
            }
            results.append(result)
        
        return results
    
    def _get_sentiment_label(self, score):
        if score > 0.05:
            return "positive"
        elif score < -0.05:
            return "negative"
        else:
            return "neutral"


def analyze_sentiment(ticker, news_api_key="4e84117fe7c64dd4848bdc3c5834eadf", days=30):
    """
    Fetches news for a given ticker, analyzes sentiment using NLTK's VADER, and returns the results as a dictionary.
    """
    try:
        # Initialize the NewsFetcher
        news_fetcher = NewsFetcher(api_key=news_api_key)

        # Fetch the news for the ticker
        articles = news_fetcher.fetch_news(ticker, days=days)

        # Initialize the SentimentAnalyzer
        sentiment_analyzer = SentimentAnalyzer()

        # Analyze sentiment
        sentiment_results = sentiment_analyzer.analyze_sentiment(articles, ticker)

        # Return sentiment results summary as a dictionary
        positive = sum(1 for result in sentiment_results if result['sentiment_label'] == 'positive')
        neutral = sum(1 for result in sentiment_results if result['sentiment_label'] == 'neutral')
        negative = sum(1 for result in sentiment_results if result['sentiment_label'] == 'negative')
        
        total = len(sentiment_results)
        
        # Handle case where no articles were found
        if total == 0:
            return {
                'positive': 0,
                'neutral': 0,
                'negative': 0,
                'positive_percentage': 0,
                'neutral_percentage': 0,
                'negative_percentage': 0,
                'article_count': 0,
                'message': 'No articles found for analysis'
            }

        sentiment_summary = {
            'positive': positive,
            'neutral': neutral,
            'negative': negative,
            'positive_percentage': positive / total * 100,
            'neutral_percentage': neutral / total * 100,
            'negative_percentage': negative / total * 100,
            'article_count': total
        }

        return sentiment_summary

    except Exception as e:
        print(f"Error: {e}")
        return None