import requests
from datetime import datetime, timedelta
import os

class NewsFetcher:
    def __init__(self, api_key):
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
    def __init__(self, market_aux_api_key = "QzdP3EF5tLroBWmmqFy5Wpap2eW0nB1z5JBqxewX"):
        self.market_aux_api_key = market_aux_api_key or os.environ.get('MARKET_AUX_API_KEY')

    def analyze_title_sentiment(self, titles, ticker):
        """
        Simulates sentiment of a list of article titles using keyword matching.
        """
        results = []
        for title in titles:
            result = self._simulate_sentiment_result(title, ticker)
            results.append(result)
        return results

    def _simulate_sentiment_result(self, title, ticker):
        score = self._simulate_sentiment(title)
        return {
            'title': title,
            'sentiment_score': score,
            'sentiment_label': self._get_sentiment_label(score),
            'ticker': ticker.upper(),
        }

    def _simulate_sentiment(self, text):
        positive_words = [
            'up', 'rise', 'growth', 'gain', 'profit', 'positive', 'bull', 'bullish', 'surge',
            'soar', 'boom', 'rally', 'strong', 'success', 'upgrade', 'beat', 'buy', 'increase',
            'record high', 'improved', 'outperform', 'resilient', 'favorable', 'expand', 'green',
            'tops', 'higher', 'solid', 'best', 'optimistic', 'momentum', 'breakout', 'support',
            'rebound', 'recovery', 'accelerate', 'bounce', 'stable', 'robust', 'milestone', 'buys',
            'confidence', 'exceed', 'gains', 'bull market', 'earnings beat', 'raised forecast',
            'guidance boost', 'growth outlook', 'dividend hike', 'cash flow', 'capital return',
            'buyback', 'record revenue', 'record earnings', 'all-time high', 'net profit',
            'margin expansion', 'upgraded', 'demand surge', 'price target increase', 'expansion',
            'strategic partnership', 'acquisition', 'launch', 'strong sales', 'increased guidance',
            'higher revenue', 'EPS beat', 'valuation boost', 'largest', 'boosted', 'added', 'lifted',
            'increased stake', 'upped holding', 'grew position', 'major stake', 'top holding',
            'largest position', 'raised position', 'new position', 'buying opportunity', 'bought'
        ]

        negative_words = [
            'down', 'fall', 'drop', 'loss', 'decline', 'negative', 'bear', 'bearish', 'crash',
            'plunge', 'bust', 'weak', 'poor', 'downgrade', 'miss', 'sell', 'decrease', 'record low',
            'underperform', 'volatile', 'concern', 'fear', 'worry', 'uncertain', 'layoff', 'cut',
            'slash', 'instability', 'recession', 'debt', 'losses', 'deteriorate', 'hit', 'struggle',
            'collapse', 'bankruptcy', 'lawsuit', 'shortfall', 'warning', 'scandal', 'slowdown', 'sells',
            'disappoint', 'headwind', 'pressure', 'profit miss', 'earnings miss', 'revenue miss',
            'guidance cut', 'downgraded', 'job cuts', 'lower outlook', 'suspension', 'selloff',
            'valuation drop', 'deficit', 'fraud', 'loss warning', 'missed expectations', 'sold',
            'dividend cut', 'SEC investigation', 'cost overrun', 'trading halt', 'penalty',
            'fine', 'market rout', 'default', 'net loss', 'credit downgrade', 'declining margins', 'smallest',
            'decreased stake', 'cut position', 'reduced stake', 'lowered position', 'trimmed holding',
            'sold off', 'stake cut', 'shares down', 'stock down', 'should you sell', 'pulling out', 'lowered', 
            'risks', 'turmoil', 'uncertainty', 'sell-off', 'bear market',
            'negative sentiment', 'negative outlook', 'poor performance', 'underperformance', 'disappointing', 
        ]

        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)

        total = pos_count + neg_count
        if total == 0:
            return 0

        return (pos_count - neg_count) / total

    def _get_sentiment_label(self, score):
        if score > 0.25:
            return "positive"
        elif score < -0.25:
            return "negative"
        else:
            return "neutral"


def analyze_sentiment(ticker, news_api_key = "4e84117fe7c64dd4848bdc3c5834eadf", days=30):
    """
    Fetches news for a given ticker, analyzes sentiment, and returns the results as a dictionary.
    """
    try:
        # Initialize the NewsFetcher
        news_fetcher = NewsFetcher(api_key=news_api_key)

        # Fetch the news for the ticker
        articles = news_fetcher.fetch_news(ticker, days=days)

        # Extract titles for sentiment analysis
        titles = [article['title'] for article in articles]

        # Initialize the SentimentAnalyzer
        sentiment_analyzer = SentimentAnalyzer()

        # Analyze sentiment
        sentiment_results = sentiment_analyzer.analyze_title_sentiment(titles, ticker)

        # Return sentiment results summary as a dictionary
        positive = sum(1 for result in sentiment_results if result['sentiment_label'] == 'positive')
        neutral = sum(1 for result in sentiment_results if result['sentiment_label'] == 'neutral')
        negative = sum(1 for result in sentiment_results if result['sentiment_label'] == 'negative')

        sentiment_summary = {
            'positive': positive,
            'neutral': neutral,
            'negative': negative,
            'positive_percentage': positive / len(sentiment_results) * 100,
            'neutral_percentage': neutral / len(sentiment_results) * 100,
            'negative_percentage': negative / len(sentiment_results) * 100,
        }

        return sentiment_summary

    except Exception as e:
        print(f"Error: {e}")
        return None


# Example Usage:
if __name__ == "__main__":
    ticker = "AAPL"
    sentiment_summary = analyze_sentiment(ticker)
    print(sentiment_summary)
