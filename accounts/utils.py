from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings

def get_url_by_user_role(user):
    # if vendor then sending to vendor dashboard
    if user.role == 1:
        return 'vendor_dashboard'
    
    # if cutomer then sending to cutomer dashboard
    elif user.role == 2:
        return 'customer_dashboard'
    
    # if anything else then sending to login page
    else:
        return 'login'
    

def send_email(request, user, mail_subject, html_template_name):
    # importing from_email from settings.py
    from_email = settings.DEFAULT_FROM_EMAIL

    # getting the current site
    current_site = get_current_site(request)

    # setting the Email subject
    mail_subject = mail_subject

    # creating Email message with HTML template and necessary data
    message = render_to_string(
            html_template_name,  # rendering HTML template
            {
                'user' : user,  # passing the user object
                'current_site' : current_site,  # passing the current site
                'user_id_encoded' : urlsafe_base64_encode(force_bytes(user.pk)),    # passing the encoded user_id
                'token' : default_token_generator.make_token(user)  # generating token based on the user and sending it to the template
            } 
            # passing the dictionary to the template
        )

    # Email of the user
    to_email = user.email

    # Creating EmailMessage object
    mail = EmailMessage(subject=mail_subject, body=message, from_email=from_email, to=[to_email])

    # Sending the email message
    mail.send()