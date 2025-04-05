# app/sentiment.py

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy import insert
from db_utils import get_engine
from models import sentiment_data
from datetime import datetime

# Mock input
sample_posts = [
    {"source": "reddit", "coin": "BTC", "text": "Bitcoin is exploding today 🚀"},
    {"source": "reddit", "coin": "ETH", "text": "Ethereum is such a scam..."},
    {"source": "twitter", "coin": "DOGE", "text": "Dogecoin to the moon!!! #HODL"},
]

def analyze_and_store(posts):
    analyzer = SentimentIntensityAnalyzer()
    engine = get_engine()

    rows = []
    for post in posts:
        score = analyzer.polarity_scores(post["text"])["compound"]
        rows.append({
            "source": post["source"],
            "coin": post["coin"],
            "text": post["text"],
            "sentiment_score": score,
            "timestamp": datetime.utcnow()
        })

    with engine.begin() as conn:
        conn.execute(insert(sentiment_data), rows)

    print(f"Inserted {len(rows)} sentiment scores into sentiment_data.")