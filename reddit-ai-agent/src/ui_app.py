import streamlit as st
from fetcher import RedditFetcher
from problem_identifier import ProblemIdentifier
from sender import EmailSender
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Reddit AI Agent", page_icon="🤖", layout="centered")

st.title("🤖 Reddit AI Agent – Pain Point Analyzer")
st.markdown("Monitor niche Reddit communities and get AI-powered reports via email!")

with st.form("reddit_form"):
    subreddits_input = st.text_input("Enter subreddit names (comma separated):", "Capgemini_india, TCS, IndiaJobs")
    email_input = st.text_input("Enter your email to receive the report:")
    submitted = st.form_submit_button("Generate & Send Report")

if submitted:
    if not email_input or not subreddits_input:
        st.error("Please enter both subreddit names and your email.")
    else:
        subreddits = [s.strip() for s in subreddits_input.split(",")]
        st.info(f"Fetching posts from: {', '.join(subreddits)} ...")

        reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        reddit_user_agent = os.getenv('REDDIT_USER_AGENT')

        fetcher = RedditFetcher(reddit_client_id, reddit_client_secret, reddit_user_agent)
        posts = fetcher.fetch_posts(subreddits)

        if not posts:
            st.warning("No posts found. Try different subreddits or reduce filters.")
        else:
            st.success(f"Fetched {len(posts)} posts ✅")

            st.info("Analyzing posts with AI model (LLM)... this may take a few moments ⏳")
            identifier = ProblemIdentifier()
            summary = identifier.identify_problems(posts)

            st.subheader("🧠 Top Pain Points Identified:")
            st.text_area("Summary", summary, height=250)

            # Generate both PDFs
            posts_pdf_path = identifier.save_combined_text_pdf(posts, output_path="reddit_raw_posts.pdf")
            summary_pdf_path = identifier.save_summary_pdf(summary, output_path="reddit_summary_report.pdf")

            # Add both download buttons
            with open(posts_pdf_path, "rb") as f1, open(summary_pdf_path, "rb") as f2:
                st.download_button("📄 Download Raw Posts PDF", data=f1, file_name="reddit_raw_posts.pdf")
                st.download_button("🧠 Download Summary Report PDF", data=f2, file_name="reddit_summary_report.pdf")

            st.info("Sending both reports via email...")
            sender = EmailSender(use_outlook=False)
            sender.send_email(
                subject="Weekly Reddit Pain Points Report",
                body="Hi,\n\nPlease find attached your Reddit AI Agent reports — both the raw Reddit posts and the summarized insights.\n\nBest,\nReddit AI Agent 🤖",
                to_emails=[email_input],
                pdf_paths=[posts_pdf_path, summary_pdf_path]
            )
            st.success(f"✅ Email sent successfully to {email_input} 📧")
