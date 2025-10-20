import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

load_dotenv()

class EmailSender:
    def __init__(self, use_outlook: bool = False):
        self.use_outlook = use_outlook

        if use_outlook:
            self.smtp_host = os.getenv("OUTLOOK_HOST")
            self.smtp_port = int(os.getenv("OUTLOOK_PORT") or 587)
            self.smtp_user = os.getenv("OUTLOOK_USER")
            self.smtp_pass = os.getenv("OUTLOOK_PASS")
        else:
            self.smtp_host = os.getenv("EMAIL_HOST")
            self.smtp_port = int(os.getenv("EMAIL_PORT") or 587)
            self.smtp_user = os.getenv("EMAIL_USER")
            self.smtp_pass = os.getenv("EMAIL_PASS")

        if not (self.smtp_host and self.smtp_user and self.smtp_pass):
            raise ValueError("SMTP configuration missing in environment variables")

    def send_email(self, subject: str, body: str, to_emails: list, pdf_paths: list = None):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.smtp_user
            msg["To"] = ", ".join(to_emails)
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            # Attach every PDF path provided (skip missing files with a warning)
            if pdf_paths:
                for pdf_path in pdf_paths:
                    if not pdf_path:
                        continue
                    abs_path = os.path.abspath(pdf_path)
                    if not os.path.exists(abs_path):
                        print(f"⚠️ Attachment not found, skipping: {abs_path}")
                        continue
                    with open(abs_path, "rb") as f:
                        part = MIMEApplication(f.read(), _subtype="pdf")
                        part.add_header("Content-Disposition", "attachment", filename=os.path.basename(abs_path))
                        msg.attach(part)

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)

            print(f"✅ Email sent successfully to {to_emails}")
            return True

        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False

