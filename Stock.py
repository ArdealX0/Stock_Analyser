class Stock:
    def __init__(self, symbol, price,price_change, financials, sentiment_Value):
        self.symbol = symbol
        self.financials = financials
        self.price = price
        self.price_change = price_change
        self.sentiment_Value = sentiment_Value

    def set_current_price(self):
        (self.price, self.price_change) = fetch_real_time_price(self.symbol)
    
    def get_current_price(self):
        return self.price, self.price_change
    
    def get_symbol(self):
        return self.symbol
    
    def get_financials(self):
        return self.financials
    
    def set_financials(self, financials):
        self.financials = fetch_financials(self.symbol)

    def get_sentiment(self):
        return self.sentiment_Value
    
    def set_sentiment_value(self):
        self.sentiment_Value = analyse_sentiment(self.symbol)

