import requests 

API_KEY = '8LKQHDEJY9AJ1ASK8LKQHDEJY9AJ1ASK'

def get_stock_price(ticker):

    symbol = ticker
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()

    if "Global Quote" in data:
        price = float(data["Global Quote"]["05. price"])
        change = float(data["Global Quote"]["09. change"])
        print(f"The real-time price of {symbol} is: ${price:.2f} with a change of ${change:.2f}")
    else:
        print("Error retrieving data:", data)

    return price

def main():
    ticker = input("Enter a stock ticker symbol: ").upper()
    real_time_price = get_stock_price(ticker)

if __name__ == "__main__":
    main()