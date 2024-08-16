from django.urls import path
from .views import *

urlpatterns = [
    path('signin/', signin_page,name="signin"),
    path('signup/', signup_page,name="signup"),
    path('dashboard/', dashboard_page,name="dashboard"),
    path('resetpassword/',reset_password,name='resetpassword'),
    path('activate/<email_token>',account_activate,name='activateaccount')
] 