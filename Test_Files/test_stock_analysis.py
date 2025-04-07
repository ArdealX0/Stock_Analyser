import pytest
from unittest.mock import patch
from io import StringIO

# Import modules to test
from StockClass import Stock
from StockDataFetcher import fetch_financials, fetch_real_time_price
from NewsFetcher import NewsFetcher, SentimentAnalyzer, analyze_sentiment
from StockAnalyser import main, validate_stocks_data

class MockStock:
        def __init__(self, symbol, price, change, financials, sentiment):
            self.symbol = symbol
            self._price = price
            self._change = change
            self._financials = financials
            self._sentiment = sentiment

        def get_current_price(self):
            return self._price, self._change

        def get_financials(self):
            return self._financials

        def get_sentiment(self):
            return self._sentiment

# Input validation helpers
def is_valid_stock_symbol(symbol):
    """Validate if a string is a valid stock symbol format."""
    if not isinstance(symbol, str):
        return False
    # Basic validation: 1-5 uppercase letters
    return symbol.isalpha() and symbol.isupper() and 1 <= len(symbol) <= 5

def is_valid_price(price):
    """Validate if a price is a positive number."""
    if not isinstance(price, (int, float)):
        return False
    return price > 0

def is_valid_sentiment_data(sentiment):
    """Validate if sentiment data has the expected structure."""
    if not isinstance(sentiment, dict):
        return False
    
    required_keys = ['positive', 'negative', 'neutral', 
                     'positive_percentage', 'negative_percentage', 'neutral_percentage']
    return all(key in sentiment for key in required_keys)

def is_valid_financials(financials):
    """Validate if financials data has the expected structure."""
    if not isinstance(financials, dict):
        return False
    
    # Check for at least some essential financial metrics
    essential_keys = ['Current Price', 'Market Cap', 'PE Ratio']
    return any(key in financials for key in essential_keys)


# Test cases for StockClass.py
class TestStockClass:
    def test_stock_initialization_bug(self):
        """Test that uncovers a bug in Stock class initialization."""
        # Bug: Symbol not being validated before assignment
        symbol = 123  # Invalid type for symbol (should be string)
        
        try:
            stock = Stock(symbol)
            # If we get here, there's no type checking in the constructor
            assert not is_valid_stock_symbol(stock.symbol), "Stock class should validate symbol type"
            print(f"BUG FOUND: Stock class accepts non-string symbols: {stock.symbol}")
        except Exception as e:
            # If an error is raised, that might be expected behavior
            print(f"Stock class rejected invalid symbol type with error: {e}")
            pytest.fail("Stock class threw an exception but should handle invalid input gracefully")
    
    def test_get_current_price_bug(self):
        """Test that uncovers a bug in the get_current_price method."""
        stock = Stock("AAPL")
        
        # Bug: get_current_price returns a tuple but it's used as a scalar in StockAnalyser.py
        price_data = stock.get_current_price()
        
        assert isinstance(price_data, tuple), "get_current_price should return a tuple"
        assert len(price_data) == 2, "get_current_price should return a tuple of (price, change)"
        
        # The bug is that in StockAnalyser.py, this tuple is used as if it were a single value
        print(f"BUG FOUND: get_current_price returns a tuple {price_data} but is used as a scalar in StockAnalyser.py")


# Test cases for StockDataFetcher.py
class TestStockDataFetcher:
    def test_fetch_real_time_price_api_bug(self):
        """Test that uncovers a bug in the fetch_real_time_price function's API handling."""
        # Bug: Hardcoded API key that might expire or hit rate limits
        ticker = "INVALIDTICKERSYMBOL"
        try:
            (price, change) = fetch_real_time_price(ticker)
            
            # If we got here without an exception, check if the result is valid
            if not is_valid_price(price):
                print(f"BUG FOUND: fetch_real_time_price returns invalid price data for {ticker}: {price}, {change}")
        except Exception as e:
            # If an exception occurs, that's the bug - it should handle errors gracefully
            print(f"BUG FOUND: fetch_real_time_price doesn't handle errors properly: {e}")
            assert False, f"fetch_real_time_price should handle errors, but raised: {e}"
    
    
    def test_fetch_financials_error_handling_bug(self):
        """Test that uncovers a bug in the fetch_financials function's error handling."""
        # Bug: Exception handling - it doesn't handle errors gracefully
        ticker = "NONEXISTENT"  # This should cause an API error
        
        try:
            result = fetch_financials(ticker)
            
            # If we get here without an exception, check if the result is valid
            if not is_valid_financials(result):
                print(f"BUG FOUND: fetch_financials returns invalid data for non-existent ticker: {result}")
            
        except Exception as e:
            # If an exception occurs, that's the bug - it should handle errors gracefully
            print(f"BUG FOUND: fetch_financials doesn't handle errors properly: {e}")
            assert False, f"fetch_financials should handle errors, but raised: {e}"


# Test cases for NewsFetcher.py
class TestNewsFetcher:
    def test_news_fetcher_api_key_bug(self):
        """Test that uncovers a bug in the NewsFetcher initialization."""
        # Bug: The NewsFetcher doesn't handle missing API keys gracefully
        
        try:
            # Try to create a NewsFetcher with no API key
            news_fetcher = NewsFetcher(api_key=None)
            assert False, "NewsFetcher should raise an error when no API key is provided"
        except ValueError as e:
            # This is expected behavior
            assert "NewsAPI key must be provided" in str(e)
            print("NewsFetcher correctly validates API key")
        except Exception as e:
            # If a different exception is raised, that's a bug
            print(f"BUG FOUND: NewsFetcher raises incorrect exception for missing API key: {e}")
            assert False, f"NewsFetcher should raise ValueError, but raised: {e.__class__.__name__}"
    
    
    def test_positive_sentiment(self):
        """Test that positive content receives positive sentiment score"""
        
        analyzer = SentimentAnalyzer()
        positive_article = {
            'title': 'Company XYZ reports record profits, stock soars',
            'content': 'The company announced excellent quarterly results exceeding all analyst expectations. Investors are thrilled with the performance.'
        }
        
        result = analyzer.analyze_sentiment([positive_article], 'XYZ')
        
        assert len(result) == 1
        assert result[0]['sentiment_label'] == 'positive'
        assert result[0]['sentiment_score'] > 0.05

    def test_negative_sentiment(self):
        """Test that negative content receives negative sentiment score"""
        analyzer = SentimentAnalyzer()
        negative_article = {
            'title': 'Company XYZ faces major lawsuit, stock plummets',
            'content': 'The company is being sued for misleading investors. The stock dropped 15% on the news.'
        }
        
        result = analyzer.analyze_sentiment([negative_article], 'XYZ')
        
        assert len(result) == 1
        assert result[0]['sentiment_label'] == 'negative'
        assert result[0]['sentiment_score'] < -0.05

    def test_neutral_sentiment(self):
        """Test that neutral content receives neutral sentiment score"""
        analyzer = SentimentAnalyzer()
        neutral_article = {
            'title': 'Company XYZ releases quarterly report',
            'content': 'The company released its quarterly financial statements today. Analysts are reviewing the numbers.'
        }
        
        result = analyzer.analyze_sentiment([neutral_article], 'XYZ')
        
        assert len(result) == 1
        assert result[0]['sentiment_label'] == 'neutral'
        assert -0.05 <= result[0]['sentiment_score'] <= 0.05

    def test_empty_article_list(self):
        """Test that empty article list returns empty result list"""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze_sentiment([], 'XYZ')
        
        assert result == []

    def test_extremely_positive_sentiment(self):
        """Test sentiment scoring for extremely positive content"""
        analyzer = SentimentAnalyzer()
        extremely_positive = {
            'title': 'AMAZING breakthrough sends stocks to the MOON! Best news EVER!',
            'content': 'Incredible profits! Revolutionary product! Phenomenal growth! Exceptional leadership! Wonderful future ahead!'
        }
        
        result = analyzer.analyze_sentiment([extremely_positive], 'XYZ')
        
        assert len(result) == 1
        assert result[0]['sentiment_label'] == 'positive'
        assert result[0]['sentiment_score'] > 0.5  # Expect very high positive score

    def test_extremely_negative_sentiment(self):
        """Test sentiment scoring for extremely negative content"""
        analyzer = SentimentAnalyzer()
        extremely_negative = {
            'title': 'TERRIBLE disaster DESTROYS company value! WORST news EVER!',
            'content': 'Catastrophic losses! Failing product! Horrible decline! Awful management! Disastrous future ahead!'
        }
        
        result = analyzer.analyze_sentiment([extremely_negative], 'XYZ')
        
        assert len(result) == 1
        assert result[0]['sentiment_label'] == 'negative'
        assert result[0]['sentiment_score'] < -0.5  # Expect very low negative score

    def test_sentiment_label_classification(self):
        """Test the _get_sentiment_label method directly"""
        analyzer = SentimentAnalyzer()
        
        assert analyzer._get_sentiment_label(0.1) == "positive"
        assert analyzer._get_sentiment_label(0.05) == "neutral"  # Edge case
        assert analyzer._get_sentiment_label(0.0) == "neutral"
        assert analyzer._get_sentiment_label(-0.05) == "neutral"  # Edge case
        assert analyzer._get_sentiment_label(-0.1) == "negative"
    
    def test_analyze_sentiment_error_handling_bug(self):
        """Test that uncovers a bug in the analyze_sentiment function's error handling."""
        # Bug: The function catches all exceptions but doesn't provide enough information
        
        # Test with an invalid API key to trigger an error
        invalid_api_key = "invalid_key_that_will_fail"
        ticker = "AAPL"
        
        # The function should return None on error, but with better error info
        result = analyze_sentiment(ticker, news_api_key=invalid_api_key)
        
        assert result is None, "analyze_sentiment should return None when an error occurs"
        print("BUG FOUND: analyze_sentiment catches all exceptions generically without proper logging or reporting")


# Test cases for StockAnalyser.py
class TestStockAnalyser:
    
    def test_validate_stocks_data_invalid(self):

        invalid_stocks = [
        MockStock('AAPL', None, 2.5, {'revenue': 1000000, 'profit': 500000}, {'positive': 0.75}),  # Invalid price
        MockStock('GOOG', 2800.0, None, {'revenue': 2000000, 'profit': 1000000}, {'neutral': 0.5}),  # Invalid change
        MockStock('AMZN', 3400.0, 50.0, None, {'positive': 0.8}),  # Invalid financials
        MockStock('MSFT', 299.0, 1.0, {'revenue': 4000000, 'profit': 2000000}, None),  # Invalid sentiment
        ]
        for stock in invalid_stocks:
            valid, message = validate_stocks_data([stock])
            assert valid == False, f"Expected invalid stock data for {stock.symbol}: {message}"

    def test_main_input_validation_bug(self):
        """Test that uncovers a bug in the main function's input validation."""
        # Bug: No validation for the number of stocks entered
        
        # Simulate user input with fewer than 5 stocks
        test_input = "AAPL,MSFT\n1000\n"
        expected_output = "Error: Please enter exactly 5 stock symbols"
        
        # Redirect stdin and stdout to capture the output
        with patch('sys.stdin', StringIO(test_input)), patch('sys.stdout', StringIO()) as fake_output:
            try:
                # This should ideally validate that 5 symbols are required
                main()
                output = fake_output.getvalue()
                
                # If we got here without an error, that's the bug
                print(f"BUG FOUND: main() doesn't validate the number of stock symbols (should be 5)")
                assert False, "main() should validate that exactly 5 stock symbols are entered"
                
            except Exception as e:
                # If an exception is raised, that might be expected but should be handled better
                print(f"BUG FOUND: main() throws an exception when fewer than 5 stocks are entered: {e}")
                assert False, f"main() should handle invalid input gracefully, but raised: {e}"