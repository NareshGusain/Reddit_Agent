from fetcher import RedditFetcher
from problem_identifier import ProblemIdentifier
from sender import EmailSender
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
    reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    reddit_user_agent = os.getenv('REDDIT_USER_AGENT')

    subreddits = ['NAME_OF_SUBREDDIT']  # Replace with actual subreddit names

    fetcher = RedditFetcher(reddit_client_id, reddit_client_secret, reddit_user_agent)
    posts = fetcher.fetch_posts(subreddits)

    if not posts:
        print("No posts fetched. Exiting.")
        return

    identifier = ProblemIdentifier()
    summary = identifier.identify_problems(posts)

    print("🧠 Summary of Reddit Pain Points:\n")
    print(summary)

    posts_pdf_path = identifier.save_combined_text_pdf(posts, output_path=os.path.abspath("reddit_raw_posts.pdf"))
    summary_pdf_path = identifier.save_summary_pdf(summary, output_path=os.path.abspath("reddit_summary_report.pdf"))

    # Debug checks for attachments
    for p in (posts_pdf_path, summary_pdf_path):
        exists = os.path.exists(p)
        size = os.path.getsize(p) if exists else 0
        print(f"Attachment check -> {p} | exists: {exists} | size: {size} bytes")

    pdf_paths = [p for p in (posts_pdf_path, summary_pdf_path) if os.path.exists(p)]
    print("Final attachments to send:", pdf_paths)

    sender = EmailSender(use_outlook=False)
    sender.send_email(
        subject="Weekly Reddit Pain Points Report",
        body="Hi Team,\n\nPlease find attached the latest Reddit insights report.\n\nBest,\nReddit AI Agent 🤖",
        to_emails=["email@gmail.com"],
        pdf_paths=pdf_paths
    )

if __name__ == "__main__":
    main()
