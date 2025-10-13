import sys, os
from spinner import start_spinner, stop_spinner

def send(to, subject, body):
    import smtplib
    from email.message import EmailMessage
    _from = os.getenv("EMAIL_FROM")
    _password = os.getenv("EMAIL_PASSWORD")
    _server = os.getenv("EMAIL_SMTP_SERVER")
    _port = os.getenv("EMAIL_SMTP_PORT")

    msg = EmailMessage()
    msg["From"] = "NHL Stats"
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body, subtype='html')

    try:
        stop, spinner = start_spinner(f"✉️ Sending email to {to}... ")
        with smtplib.SMTP(_server, _port) as server:
            server.starttls()
            server.login(_from, _password)
            server.send_message(msg)
        stop_spinner(stop, spinner)
        print(f"✅ Email sent successfully to {to}.")
    except Exception as stop:
        sys.exit(f"Failed to send email: {stop}")
...



if __name__ == "__main__":
    raise Exception("emailer.py can not be run directly.")
...
