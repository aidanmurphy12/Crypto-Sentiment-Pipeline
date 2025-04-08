# /app/sentiment.py

import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy import insert, select
from datetime import datetime
from db_utils import get_engine
from models import sentiment_data, top_coins


# === CLEANING FUNCTION ===
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)  # remove links
    text = re.sub(r"[^a-z0-9\s]", "", text)  # remove punctuation/symbols
    return text.strip()


# === LOAD COIN KEYWORDS FROM DB ===
def load_coin_map():
    engine = get_engine()
    with engine.connect() as conn:
        coins = conn.execute(select(top_coins)).fetchall()
    return {coin.symbol.lower(): coin.id for coin in coins}


# === COIN DETECTION ===
def detect_coin(text, coin_map):
    for symbol, coin_id in coin_map.items():
        if symbol in text:
            return coin_id
    return "UNKNOWN"


# === FULL ANALYSIS & INSERT ===
def analyze_and_store(posts):
    analyzer = SentimentIntensityAnalyzer()
    coin_map = load_coin_map()
    engine = get_engine()

    rows = []
    for post in posts:
        cleaned_text = clean_text(post["text"])
        coin = detect_coin(cleaned_text, coin_map)
        score = analyzer.polarity_scores(cleaned_text)["compound"]

        rows.append({
            "source": post["source"],
            "coin": coin,
            "text": post["text"],  # original text (cleaned version is used only internally)
            "sentiment_score": score,
            "timestamp": post.get("timestamp", datetime.utcnow())
        })

    if rows:
        with engine.begin() as conn:
            conn.execute(insert(sentiment_data), rows)
        print(f"Inserted {len(rows)} sentiment scores into sentiment_data.")
    else:
        print("No rows to insert.")