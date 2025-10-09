# Example main script to fetch, analyze, and print Reddit pain points
from fetcher import RedditFetcher
from problem_identifier import ProblemIdentifier
from dotenv import load_dotenv
from fpdf import FPDF
import os
import sys
# from email.sender import EmailSender  # Uncomment when implementing email

load_dotenv()

def save_summary_to_pdf(summary, filename="reddit_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Weekly Reddit Pain Points Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, "Summary of top 5 recurring pain points identified from Reddit communities:\n", align="L")
    pdf.ln(5)

    # Split summary into lines for bullet points if needed
    for idx, line in enumerate(summary.split('\n')):
        if line.strip():
            pdf.set_font("Arial", "B", 12)
            pdf.cell(10, 10, f"{idx+1}.", ln=0)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, line.strip())
            pdf.ln(2)

    pdf.output(filename)

def main():
    # TODO: Replace with your actual credentials and subreddits
    reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
    reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    reddit_user_agent = os.getenv('REDDIT_USER_AGENT')
    openai_api_key = os.getenv('GROQ_API_KEY')

    subreddits = ['SaaS', 'startups', 'StartUpIndia','indianstartups']

    fetcher = RedditFetcher(reddit_client_id, reddit_client_secret, reddit_user_agent)
    posts = fetcher.fetch_posts(subreddits)

    identifier = ProblemIdentifier()
    summary = identifier.identify_problems(posts)

    print("Weekly Reddit Pain Points Summary:\n")
    print(summary)
    # TODO: Format and send email with summary
    save_summary_to_pdf(summary)

if __name__ == "__main__":
    main()