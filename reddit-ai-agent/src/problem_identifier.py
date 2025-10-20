import os
import re
from collections import Counter
from groq import Groq
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from fpdf import FPDF


class ProblemIdentifier:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)

    def _fallback_summary(self, combined_text: str) -> str:
        """Create a short fallback summary if LLM returns nothing."""
        words = re.findall(r"\w+", combined_text.lower())
        stop = {
            "the","and","to","a","i","is","in","for","of","it","you","that","on","this",
            "with","are","was","be","have","as","but","they","not","or","we","from"
        }
        filtered = [w for w in words if w not in stop]
        if not filtered:
            return "No extractable content to summarize."
        common = [w for w, _ in Counter(filtered).most_common(5)]
        return "Fallback summary — common topics: " + ", ".join(common) + "."

    def identify_problems(self, posts):
        combined_text = "\n\n".join([
            f"Title: {post.get('title','')}\nBody: {post.get('body','')}" for post in posts
        ])
        prompt = (
            "You are an expert product researcher. Given the following Reddit posts, "
            "identify the top 5 recurring pain points or problems users are facing. "
            "Summarize each pain point in 1-2 sentences, suitable for a business audience.\n\n"
            f"Posts:\n{combined_text}\n\nTop 5 Pain Points:"
        )
        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None
        )
        summary = ""
        for chunk in completion:
            summary += chunk.choices[0].delta.content or ""

        if not summary or not summary.strip():
            print("⚠️ LLM returned empty summary. Generating fallback summary.")
            summary = self._fallback_summary(combined_text)

        # small debug output
        print(f"Summary length: {len(summary)} characters")
        return summary

    def save_combined_text_pdf(self, posts, output_path=None):
        """
        Save combined posts text to a PDF and return absolute path.
        """
        combined_text = "\n\n".join([
            f"Title: {post.get('title','')}\nBody: {post.get('body','')}" for post in posts
        ])

        if output_path is None:
            output_path = os.path.join(os.getcwd(), "combined_text.pdf")
        output_path = os.path.abspath(output_path)

        width, height = letter
        margin = 40
        font_name = "Helvetica"
        font_size = 10
        max_width = width - 2 * margin

        c = canvas.Canvas(output_path, pagesize=letter)
        text_obj = c.beginText(margin, height - margin)
        text_obj.setFont(font_name, font_size)

        for paragraph in combined_text.split("\n"):
            lines = simpleSplit(paragraph, font_name, font_size, max_width)
            if not lines:
                lines = [""]
            for line in lines:
                if text_obj.getY() < margin:
                    c.drawText(text_obj)
                    c.showPage()
                    text_obj = c.beginText(margin, height - margin)
                    text_obj.setFont(font_name, font_size)
                text_obj.textLine(line)

        c.drawText(text_obj)
        c.save()
        return output_path

    def save_summary_pdf(self, summary_text, output_path=None):
        """
        Save LLM summary text to a PDF and return absolute path.
        """
        if output_path is None:
            output_path = os.path.join(os.getcwd(), "summary_report.pdf")
        output_path = os.path.abspath(output_path)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Reddit Pain Points Summary", ln=True, align="C")
        pdf.ln(8)
        pdf.set_font("Arial", size=12)

        if not summary_text or not summary_text.strip():
            pdf.multi_cell(0, 8, "No summary available.")
        else:
            pdf.multi_cell(0, 8, summary_text)

        pdf.output(output_path)
        return output_path
