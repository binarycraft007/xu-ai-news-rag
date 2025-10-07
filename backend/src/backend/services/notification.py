from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_notification(recipient, title, message_body):
    """Sends an email notification."""
    if not current_app.config.get('MAIL_SERVER'):
        print("Mail server not configured. Skipping email notification.")
        return

    msg = Message(title, sender=current_app.config['MAIL_USERNAME'], recipients=[recipient])
    msg.body = message_body
    
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")
