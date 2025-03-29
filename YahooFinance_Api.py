import yfinance as yf

def get_company_details(ticker):
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

def main():
    ticker = input("Enter stock ticker: ").upper()
    details = get_stock_details(ticker)
    
    print(f"\nFinancial details for {ticker}:")
    for key, value in details.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
