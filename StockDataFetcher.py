import yfinance as yf
import requests 

def fetch_financials(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    try:
        total_revenue = stock.financials.loc['Total Revenue'][0]
    except:
        total_revenue = None

    try:
        total_debt = stock.balance_sheet.loc['Total Debt'][0]
    except:
        total_debt = None

    details = {
        "Current Price": info.get("currentPrice"),
        "Market Cap": info.get("marketCap"),
        "PE Ratio": info.get("trailingPE"),
        "Forward PE": info.get("forwardPE"),
        "EPS": info.get("trailingEps"),
        "Dividend Yield": info.get("dividendYield"),
        "Beta": info.get("beta"),
        "Price to Book": info.get("priceToBook"),
        "52 Week High": info.get("fiftyTwoWeekHigh"),
        "52 Week Low": info.get("fiftyTwoWeekLow"),
        "Revenue Growth (YoY)": info.get("revenueGrowth"),
        "Earnings Growth (YoY)": info.get("earningsGrowth"),
        "Total Revenue (Annual)": total_revenue,
        "Total Debt": total_debt,
        "Sector": info.get("sector"),
        "Industry": info.get("industry"),
        "Analyst Recommendation": info.get("recommendationKey"),
    }

    return details

API_KEY = '8LKQHDEJY9AJ1ASK8LKQHDEJY9AJ1ASK'

def fetch_real_time_price(ticker):

    stock = ticker
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()

    if "Global Quote" in data:
        price = float(data["Global Quote"]["05. price"])
        change = float(data["Global Quote"]["09. change"])

    return (price, change)