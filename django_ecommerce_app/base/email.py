from django.conf import settings
from django.core.mail import send_mail


def send_account_activation_email(email,email_token):
    subject='Rai Ecommerce App , Your Account need to be verified'
    email_from =settings.EMAIL_HOST_USER
    if email_token:
     message=f'Hi  click on the link to activate your account http://127.0.0.1:8000/account/activate/{email_token}'
     #django predefined function 
     send_mail(subject,message,email_from,[email])
    # here need to pass list of email on which we need to send the emails  
    # needs to add variables in the settings.py file 
      
