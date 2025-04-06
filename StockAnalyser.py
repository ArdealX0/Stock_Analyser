from StockClass import Stock
import google.generativeai as genai

def main():
    print("Initializing Stock Analyzer...")
    
    # Initialize the StockAnalyzer class with a list of stock symbols
    stock_symbols = input("Enter any of 5 stock symbols separated by commas: ").upper()   
    stock_symbols = stock_symbols.split(",")
    stock_symbols = [symbol.strip() for symbol in stock_symbols]
    
    investment_amount = float(input("Enter your investment amount (in CAD$): $"))

    risk_tolerance = input("Enter your risk tolerance (low, medium, high): ").lower()
    if risk_tolerance not in ["low", "medium", "high"]:
        print("Invalid risk tolerance. Please enter 'low', 'medium', or 'high'.")
        return

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


def create_portfolio(stocks, investment_amount, risk_tolerance):
    
    # Configure the API key
    genai.configure(api_key="AIzaSyACI6oQ57KxFUaptHV9-S5RNsDnG8VFR5s")
    
    # Create a model instance
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Generate content
    response = model.generate_content(
        f"""
        Here is the stocks information:
        Stock 1: {stocks[0].symbol}
        Price: ${stocks[0].get_current_price()}
        Financials: {stocks[0].get_financials()}
        Market Sentiment: {stocks[0].get_sentiment()}
        Stock 2: {stocks[1].symbol}
        Price: ${stocks[1].get_current_price()}
        Financials: {stocks[1].get_financials()}
        Market Sentiment: {stocks[1].get_sentiment()}
        Stock 3: {stocks[2].symbol}
        Price: ${stocks[2].get_current_price()}
        Financials: {stocks[2].get_financials()}
        Market Sentiment: {stocks[2].get_sentiment()}
        Stock 4: {stocks[3].symbol}
        Price: ${stocks[3].get_current_price()}
        Financials: {stocks[3].get_financials()}
        Market Sentiment: {stocks[3].get_sentiment()}
        Stock 5: {stocks[4].symbol}
        Price: ${stocks[4].get_current_price()}
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