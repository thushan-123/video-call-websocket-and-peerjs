import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Loggers.log import app_log, err_log
import os
from dotenv import load_dotenv

load_dotenv()

COMPANY_EMAIL = os.getenv("COMPANY_EMAIL")
COMPANY_EMAIL_PASSWORD = os.getenv("COMPANY_EMAIL_PASSWORD")  # want a ap password


class Mail:
    receiver: str
    subject: str
    html_content: str

    def __init__(self, receiver, subject, html_content):
        self.receiver = receiver
        self.subject = subject
        self.html_content = html_content

    def send(self):
        from_email = COMPANY_EMAIL
        password = COMPANY_EMAIL_PASSWORD

        # Setup MIME
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = self.receiver
        message['Subject'] = self.subject

        # Attach to body with HTML message
        message.attach(MIMEText(self.html_content, "html"))

        # Create SMTP session -> sending email
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()  # Enable transport layer security
            server.login(from_email, password)  # Login Gmail account
            text = message.as_string()
            server.sendmail(from_email, self.receiver, text)
            app_log.info(f"|Mails - mail| -> email send to {self.receiver}")
            #return True
        except Exception as e:
            print(e)
            err_log.error(f"| Mails - mail | - Email Send Failed - {e}")
            #return False
