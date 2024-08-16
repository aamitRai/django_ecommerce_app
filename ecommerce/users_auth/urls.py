from django.urls import path
from .views import *
urlpatterns = [
    path('signup',handle_signup,name="handle_signup"),   
    path('account_activation/<email_token>',handle_account_activation,name="handle_account_activation"),
    path('signin',handle_signin,name="handle_signin"),
    path('forget_password',handle_forget_password,name="handle_forget_password"),   
    path('create_password/<password_token>',handle_forget_password_creation,name='handle_forget_password_creation'),
    path('logout',handle_logout,name="handle_logout"),
]