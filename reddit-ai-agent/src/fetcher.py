import os
from datetime import datetime, timedelta
import praw
from dotenv import load_dotenv

class RedditFetcher:
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  user_agent=user_agent)

    def fetch_posts(self, subreddits: list, min_upvotes: int = 2, days: int = 7, limit: int = 100):
        all_posts = []
        since = datetime.utcnow() - timedelta(days=days)
        for subreddit in subreddits:
            subreddit_obj = self.reddit.subreddit(subreddit)
            for post in subreddit_obj.hot(limit=limit):
                created_utc = datetime.utcfromtimestamp(post.created_utc)
                if created_utc < since:
                    continue
                if post.score < min_upvotes:
                    continue
                post_data = {
                    'id': post.id,
                    'title': post.title,
                    'body': post.selftext,
                    'upvotes': post.score,
                    'num_comments': post.num_comments,
                    'created_utc': created_utc,
                    'url': post.url,
                    'subreddit': subreddit
                }
                all_posts.append(post_data)
        return all_posts

# Convenience wrapper so other modules can `from fetcher import fetch_posts`
def fetch_posts(subreddits: list, min_upvotes: int = 2, days: int = 7, limit: int = 100,
                client_id: str = None, client_secret: str = None, user_agent: str = None):
    load_dotenv()
    client_id = client_id or os.getenv('REDDIT_CLIENT_ID')
    client_secret = client_secret or os.getenv('REDDIT_CLIENT_SECRET')
    user_agent = user_agent or os.getenv('REDDIT_USER_AGENT')
    if not (client_id and client_secret and user_agent):
        raise ValueError("Reddit credentials missing: set REDDIT_CLIENT_ID/REDDIT_CLIENT_SECRET/REDDIT_USER_AGENT")
    rf = RedditFetcher(client_id, client_secret, user_agent)
    return rf.fetch_posts(subreddits, min_upvotes=min_upvotes, days=days, limit=limit)