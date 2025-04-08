from StockClass import Stock
import google.generativeai as genai
from StockDataFetcher import validate_ticker

def main():
    print("Initializing Stock Analyzer...")
    
    # Initialize the StockAnalyzer class with a list of stock symbols
    stock_symbols = input("\nEnter any of 5 stock symbols separated by commas: ").upper()   
    stock_symbols = stock_symbols.split(",")
    stock_symbols = [symbol.strip() for symbol in stock_symbols]
    while len(stock_symbols) != 5 and stock_symbols:
        stock_symbols = input("Please enter exactly 5 stock symbols.")
        stock_symbols = stock_symbols.split(",")
        stock_symbols = [symbol.strip() for symbol in stock_symbols]
    
    investment_amount = float(input("\nEnter your investment amount (in CAD$): $"))
    while investment_amount <= 0 and type(investment_amount) != float:
        investment_amount = input("Please enter a valid investment amount (in CAD$): $")

    risk_tolerance = input("\nEnter your risk tolerance (low, medium, high): ").lower()
    while risk_tolerance not in ["low", "medium", "high"]:
        risk_tolerance = input("Enter your risk tolerance (low, medium, high): ").lower()

    stocks = []

    for symbol in stock_symbols:
        symbol = Stock(symbol)
        symbol.set_current_price()
        symbol.set_financials()
        symbol.set_sentiment_value()
        stocks.append(symbol)

    print("\nAnalyzing stocks... and creating a portfolio: ")
    create_portfolio(stocks, investment_amount, risk_tolerance)
    print("\nPortfolio created successfully!")
    print("\nStock Analysis Complete.")

    print("\nExiting Stock Analyzer...")


def validate_stocks_data(stocks):
    """Validate that all stocks have valid data."""
    for stock in stocks:
        # Check if the stock has a valid symbol
        if validate_ticker(stock.symbol) is False:
            return False, f"Invalid symbol for stock: {stock.symbol}"
        
        # Check if the stock has a valid current price (price and change)
        price, change = stock.get_current_price()
        if price is None or change is None or not isinstance(price, (int, float)) or not isinstance(change, (int, float)):
            return False, f"Invalid price data for stock: {stock.symbol}"
        
        # Check if the stock has valid financial data
        financials = stock.get_financials()
        if not financials or not isinstance(financials, dict):
            return False, f"Invalid financial data for stock: {stock.symbol}"
        
        # Check if the stock has valid sentiment data
        sentiment = stock.get_sentiment()
        if not sentiment or not isinstance(sentiment, dict):
            return False, f"Invalid sentiment data for stock: {stock.symbol}"
        
        else:
            return True, f"Stock {stock.symbol} is valid."
    


def create_portfolio(stocks, investment_amount, risk_tolerance):

    #Validate stocks data
    (valid, message) = validate_stocks_data(stocks)
    if not valid:
        print(f"Error: {message}")
        return
    
    # Configure the API key
    genai.configure(api_key="AIzaSyACI6oQ57KxFUaptHV9-S5RNsDnG8VFR5s")
    
    # Create a model instance
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Generate content
    response = model.generate_content(
        f"""
        Here is the stocks information:
        Stock 1: {stocks[0].symbol}
        Price and change from previous close: ${stocks[0].get_current_price()}
        Financials: {stocks[0].get_financials()}
        Market Sentiment: {stocks[0].get_sentiment()}
        Stock 2: {stocks[1].symbol}
        Price and change from previous close: ${stocks[1].get_current_price()}
        Financials: {stocks[1].get_financials()}
        Market Sentiment: {stocks[1].get_sentiment()}
        Stock 3: {stocks[2].symbol}
        Price and change from previous close: ${stocks[2].get_current_price()}
        Financials: {stocks[2].get_financials()}
        Market Sentiment: {stocks[2].get_sentiment()}
        Stock 4: {stocks[3].symbol}
        Price and change from previous close: ${stocks[3].get_current_price()}
        Financials: {stocks[3].get_financials()}
        Market Sentiment: {stocks[3].get_sentiment()}
        Stock 5: {stocks[4].symbol}
        Price and change from previous close: ${stocks[4].get_current_price()}
        Financials: {stocks[4].get_financials()}
        Market Sentiment: {stocks[4].get_sentiment()}
        Investment value = {investment_amount}
        Risk tolerance = {risk_tolerance}
        Create a portfolio with the above stocks and their respective investment amounts given in canadian dollars.
        The portfolio should be optimized for maximum returns based on the current market conditions and sentiment analysis.
        The result should only be in a table format with the following columns:
        1. Stock Symbol
        2. Investment Amount (CAD$)
        After the table, provide a summary of the portfolio and reasoning using the provided data.
        and organise the table to make it look professional on a terminal.
        """
    )
    print(response.text)
        
if __name__ == "__main__":
    main()