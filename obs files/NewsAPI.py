import requests

def get_stock_news(symbols, api_key):
    base_url = "https://newsapi.org/v2/everything"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    articles = []
    
    for symbol in symbols:
        params = {
            "q": symbol,
            "sortBy": "publishedAt",
            "language": "en"
        }
        response = requests.get(base_url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            articles.extend(data.get("articles", []))
        else:
            print(f"Error fetching news for {symbol}: {response.status_code}")
    
    return articles

def main():
    api_key = "cca8274c-27e2-496c-a0af-0842f5eb5500"
    symbols = input("Enter stock symbols (comma-separated): ").split(',')
    symbols = [s.strip().upper() for s in symbols]
    
    news_articles = get_stock_news(symbols, api_key)
    
    if news_articles:
        for i, article in enumerate(news_articles[:10], 1):  # Show top 10 articles
            print(f"{i}. {article['title']}")
            print(f"   Source: {article['source']['name']}")
            print(f"   URL: {article['url']}")
            print("---")
    else:
        print("No news articles found.")

if __name__ == "__main__":
    main()
