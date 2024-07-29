from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from .emails import *
import uuid
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import timedelta

# Create your models here.
# BaseModel name is  given by me 
class BaseModel(models.Model):
    base_uuid=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    #uuid4 generated random uuid
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)

    #to create these as  a class we need to use 
    class meta:
            abstract=True



class CustomUser(AbstractBaseUser,PermissionsMixin):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    email=models.EmailField(_('email address'),unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    
    objects=CustomUserManager()
    
    def __str__(self):
        return self.email
        
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
        
class Profile(BaseModel):
    user=models.OneToOneField(CustomUser ,on_delete=models.CASCADE,related_name="profile")
    is_email_verified=models.BooleanField(default=False)
    email_token= models.UUIDField(max_length=100,null=True,blank=True)
    profile_image=models.ImageField(upload_to='profile')


@receiver(post_save, sender=CustomUser)
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
        
        
class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Token for {self.user.email}"
    