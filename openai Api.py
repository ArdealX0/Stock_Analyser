from google import genai

client = genai.Client(api_key="AIzaSyACI6oQ57KxFUaptHV9-S5RNsDnG8VFR5s")
stock = {
    "price": 150,
    "financials": {"revenue_growth": "15%", "pe_ratio": 20, "debt_ratio": "low"},
    "sentiment": {"news": "positive", "social_media": "bullish"}
}


response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=f"""
    Analyze this stock:
    Price: ${stock['price']}
    Financials: {stock['financials']}
    Market Sentiment: {stock['sentiment']}
    Should I buy? Respond ONLY with 'Buy' or 'Don't buy' and a good reason.
    """
)

print(response.text)