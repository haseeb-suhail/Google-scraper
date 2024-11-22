import smtplib
from email.mime.text import MIMEText

# Email configuration
smtp_server = "guvenlisatkirala.com"
smtp_port = 465
username = "destek@guvenlisatkirala.com"
password = "3yEKgCqITuhx"

# Email content
from_email = "destek@guvenlisatkirala.com"
to_email = "recipient@example.com"
subject = "Test Email"
body = "This is a test email."

# Create the email message
msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = from_email
msg["To"] = to_email

# Connect to the SMTP server
try:
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(username, password)
        server.sendmail(from_email, to_email, msg.as_string())
    print("Email sent successfully.")
except Exception as e:
    print(f"Failed to send email: {e}")
