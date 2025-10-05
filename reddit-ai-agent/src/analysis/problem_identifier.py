import os
from groq import Groq

class ProblemIdentifier:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)

    def identify_problems(self, posts):
        combined_text = "\n\n".join([
            f"Title: {post['title']}\nBody: {post['body']}" for post in posts
        ])
        prompt = (
            "You are an expert product researcher. Given the following Reddit posts, "
            "identify the top 5 recurring pain points or problems users are facing. "
            "Summarize each pain point in 1-2 sentences, suitable for a business audience.\n\n"
            f"Posts:\n{combined_text}\n\nTop 5 Pain Points:"
        )
        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None
        )
        summary = ""
        for chunk in completion:
            summary += chunk.choices[0].delta.content or ""
        return summary