from StockClass import Stock
from google import genai

def main():
    print("Initializing Stock Analyzer...")
    
    # Initialize the StockAnalyzer class with a list of stock symbols
    stock_symbols = input("Enter any of 5 stock symbols separated by commas: ").upper()   
    stock_symbols = stock_symbols.split(",")
    stock_symbols = [symbol.strip() for symbol in stock_symbols]
    
    
    print("Enter your investment amount (in CAD$):")
    investment_amount = float(input())

    stocks = []

    for symbol in stock_symbols:
        symbol = Stock(symbol)
        symbol.set_current_price()
        symbol.set_financials()
        symbol.set_sentiment_value()
        stocks.append(symbol)

    print (stocks[0].symbol, stocks[0].get_current_price(), stocks[0].get_financials(), stocks[0].get_sentiment())
    print("Analyzing stocks... and creating a portfolio: ")
    create_portfolio(stocks, investment_amount)
    print("Portfolio created successfully!")
    print("Stock Analysis Complete.")

    print("Exiting Stock Analyzer...")


def create_portfolio(stocks, investment_amount):
    
    client = genai.Client(api_key="AIzaSyACI6oQ57KxFUaptHV9-S5RNsDnG8VFR5s")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"""
        Here is the stocks information:
        Stock 1: {stocks[0].symbol}
        Price: ${stocks[0].price}
        Financials: {stocks[0].financials}
        Market Sentiment: {stocks[0].sentiment_value}
        Stock 2: {stocks[1].symbol}
        Price: ${stocks[1].price}
        Financials: {stocks[1].financials}
        Market Sentiment: {stocks[1].sentiment_value}
        Stock 3: {stocks[2].symbol}
        Price: ${stocks[2].price}
        Financials: {stocks[2].financials}
        Market Sentiment: {stocks[2].sentiment_value}
        Stock 4: {stocks[3].symbol}
        Price: ${stocks[3].price}
        Financials: {stocks[3].financials}
        Market Sentiment: {stocks[3].sentiment_value}
        Stock 5: {stocks[4].symbol}
        Price: ${stocks[4].price}
        Financials: {stocks[4].financials}
        Market Sentiment: {stocks[4].sentiment_value}
        Investment value = {investment_amount}
        Create a portfolio with the above stocks and their respective investment amounts.
        The portfolio should be optimized for maximum returns based on the current market conditions and sentiment analysis.
        The portfolio should also consider the risk tolerance of the investor.
        The result should be in a table format with the following columns:
        1. Stock Symbol
        2. Investment Amount (CAD$)
        3. Expected Return (CAD$)
        """
    )
    print(response.text)
        

if __name__ == "__main__":
    main()
