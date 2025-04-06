# app/reddit_ingest.py

import os
from datetime import datetime
import praw
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

def get_reddit_posts(subreddit="CryptoCurrency", limit=10):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

    posts = []
    for post in reddit.subreddit(subreddit).hot(limit=limit):
        posts.append({
            "source": "reddit",
            "coin": "UNKNOWN",
            "text": post.title,
            "timestamp": datetime.utcfromtimestamp(post.created_utc)
        })

    return posts
