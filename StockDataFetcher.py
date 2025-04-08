import yfinance as yf
import requests
from requests.exceptions import RequestException

def fetch_financials(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Check if we got valid data
        if not info or 'symbol' not in info:
            return {"error": f"Invalid ticker symbol: {ticker}"}
        
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
            "Total Revenue (Annual)": info.get("total_revenue"),
            "Total Debt": info.get("total_debt"),
            "Sector": info.get("sector"),
            "Industry": info.get("industry"),
            "Analyst Recommendation": info.get("recommendationKey"),
        }
        
        return details
    except Exception as e:
        return {"error": f"Error fetching financial data for {ticker}: {str(e)}"}

def fetch_real_time_price(ticker):
    API_KEY = 'VBMIVRFXPBIF0X6P'
    
    try:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}'
        r = requests.get(url, timeout=10)
        r.raise_for_status()  # Raise an exception for HTTP errors
        data = r.json()
        
        if "Global Quote" in data and data["Global Quote"]:
            if "05. price" in data["Global Quote"] and "09. change" in data["Global Quote"]:
                try:
                    price = float(data["Global Quote"]["05. price"])
                    change = float(data["Global Quote"]["09. change"])
                    return price, change
                except (ValueError, TypeError):
                    return {"error": f"Invalid price data for {ticker}"}, 0.0
        elif "Note" in data:
            # Handle API limit reached
            return {"error": f"API limit reached: {data['Note']}"}, 0.0
        else:
            return {"error": f"Invalid ticker or no data for {ticker}"}, 0.0
    except RequestException as e:
        return {"error": f"Request error for {ticker}: {str(e)}"}, 0.0
    except Exception as e:
        return {"error": f"Unexpected error for {ticker}: {str(e)}"}, 0.0

def validate_ticker(ticker):
    """
    Validate if a ticker symbol exists before attempting to fetch data
    """
    try:
        stock = yf.Ticker(ticker)
        # Try to get basic info as a validation check
        info = stock.info
        
        # Check if we got valid data - different libraries might have different ways to validate
        if not info or len(info) <= 1 or 'symbol' not in info:
            return False
        return True
    except:
        return False