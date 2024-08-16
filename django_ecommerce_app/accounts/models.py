from django.contrib import admin
from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid
from base.email import send_account_activation_email

class Profile(BaseModel):
    user=models.OneToOneField(User ,on_delete=models.CASCADE,related_name="profile")
    is_email_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=100,null=True,blank=True)
    profile_image=models.ImageField(upload_to='profile')


@receiver(post_save, sender=User)
#created is boolean value  
def sendEmailToken(sender,instance,created, **kwargs):
    try:
        if created:
            email_token=str(uuid.uuid4())   
            email=instance.email
            
            #it return two value in tuple ,here we unpacked in two variables 
            profile,created =  Profile.objects.get_or_create(user=instance)
            if created:
                profile.email_token = email_token
                profile.save()
                send_account_activation_email(email,email_token)
    except Exception as e:
        print(e)      
        