class EmailSender:
    def __init__(self, smtp_server: str, port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password

    def format_report(self, pain_points: list) -> str:
        report = "Weekly Summary of User Problems:\n\n"
        for point in pain_points:
            report += f"- {point}\n"
        return report

    def send_email(self, report: str, recipient: str) -> None:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = recipient
        msg['Subject'] = "Weekly User Problems Report"

        msg.attach(MIMEText(report, 'plain'))

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)