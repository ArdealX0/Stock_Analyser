FROM python:3.9-slim

WORKDIR /app

# Install required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -m nltk.downloader vader_lexicon

# Copy application files
COPY StockClass.py StockDataFetcher.py NewsFetcher.py StockAnalyser.py ./
COPY test_stock_analysis.py Test_runner.py ./

# Set entry point
ENTRYPOINT ["python", "StockAnalyser.py"]