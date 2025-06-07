import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailService:
    def __init__(self):
        self.sender_email = "@gmail.com"  # Replace with your email
        self.email_password = ""  # Replace with Gmail App Password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_reset_email(self, receiver_email, reset_token):
        # Create message
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = "Password Reset Request"

        # Create email body
        body = f"""
        Hello,

        You have requested to reset your password.
        Click the link below to reset your password:

        http://127.0.0.1:8000/forgot-password/{reset_token}  # Changed port to 8000

        If you did not request this, please ignore this email.

        This link will expire in 1 hours.
        """

        message.attach(MIMEText(body, "plain"))

        try:
            # Create SMTP session
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()

            # Login to email
            server.login(self.sender_email, self.email_password)

            # Send email
            text = message.as_string()
            server.sendmail(self.sender_email, receiver_email, text)
            server.quit()
            return True

        except Exception as e:
            print(f"Error sending email: {e}")
            return False


if __name__ == "__main__":
    boj = EmailService()
    print(boj.send_reset_email("himanshuamlavad2002@gmail.com", "token.yyyy"))
