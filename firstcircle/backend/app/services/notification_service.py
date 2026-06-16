import logging

logger = logging.getLogger("firstcircle.notifications")

def send_push_notification(profile_id: int, title: str, body: str):
    """
    Stubs standard push notification output to console/log.
    """
    message = f"[PUSH NOTIFICATION to User Profile {profile_id}] '{title}': {body}"
    print(message)
    logger.info(message)

def send_email_stub(email: str, subject: str, html_content: str):
    """
    Stubs email transmission.
    """
    message = f"[EMAIL to {email}] Subject: '{subject}'\nContent: {html_content[:100]}..."
    print(message)
    logger.info(message)
