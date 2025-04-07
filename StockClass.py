import StockDataFetcher as fetcher
import NewsFetcher as news

class Stock:

    price = 0 
    price_change = 0 
    financials = 0 
    sentiment_Value = 0
    symbol = ""

    def __init__(self, symbol):
        self.symbol = symbol

    def set_current_price(self):
        (self.price, self.price_change) = fetcher.fetch_real_time_price(self.symbol)
    
    def get_current_price(self):
        return (self.price, self.price_change)
    
    def get_symbol(self):
        return self.symbol
    
    def get_financials(self):
        return self.financials
    
    def set_financials(self):
        self.financials = fetcher.fetch_financials(self.symbol)

    def get_sentiment(self):
        return self.sentiment_Value
    
    def set_sentiment_value(self):
        self.sentiment_Value = news.analyze_sentiment(self.symbol)

