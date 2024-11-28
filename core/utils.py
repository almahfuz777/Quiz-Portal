"""
This file generate the email's token that will send to the user's email
"""
from django.conf import settings
from django.core.mail import send_mail

def send_email_token(email, token):
    """
    Sends an email containing a verification link to the specified email address.

    Args:
        email (str): The recipient's email address.
        token (str): The unique verification token to be included in the verification link.

    Returns:
        bool: Returns True if the email was sent successfully, False otherwise.
    
    The email contains a verification link in the form:
    http://127.0.0.1:8000/verify/{token}
    Where {token} is a unique token used to verify the user's email address.
    """
    try:
        subject = 'Your account needs to be verified'
        message = f'click on the link to verify http://127.0.0.1:8000/verify/{token}'

        # Get the sender's email from settings
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email,]

        # Send the email using Django's send_mail function
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        # Return False if there's an error during the email sending process
        return False
    return True
