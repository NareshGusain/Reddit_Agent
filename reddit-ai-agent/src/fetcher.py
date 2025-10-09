import praw
from datetime import datetime, timedelta

class RedditFetcher:
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  user_agent=user_agent)

    def fetch_posts(self, subreddits: list, min_upvotes: int = 20, days: int = 7, limit: int = 100):
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