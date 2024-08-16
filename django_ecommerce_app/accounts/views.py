from django.shortcuts import render ,redirect
from Template.accounts import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate ,login,logout
from django.http import HttpResponse
from .models import Profile 

def reset_password(request):
        if(request.method=="POST"):
          email=request.POST.get('mail')
          password=request.POST.get('password')
          users = User.objects.filter(email=email)
          if users.count() == 1:
             user = users.first()
             user.set_password(password)
             user.save()
             print("password saved")
             return HttpResponse("password saved")
          else:   
                return HttpResponse("password not saved")
        return render(request,'accounts/reset.html')
      
               
               
def  signin_page(request):
        if(request.method=="POST"):
            email=request.POST.get('mail')
            password=request.POST.get('password')
            print("email :",email,"password",password)
            user_obj = authenticate(username=email ,password=password)   
            print('user_obj',user_obj)         
            if user_obj:
                  if not user_obj.profile.is_email_verified:
                    messages.error(request,"Need to verfy email ")
                    print("Need to  verify email ")                    
                    return  HttpResponseRedirect(request.path_info)
                  print("successful login ")                    
                  return render(request,'accounts/home.html')
            else :
                messages.error(request,"Invalid Credentials , Try Again !!")
                print("Invalid Credentials ")
                return  HttpResponseRedirect(request.path_info)
        return  render(request,'accounts/signin.html')
        
def  signup_page(request):
    if(request.method=="POST"):
      email=request.POST.get('mail')
      user_obj=User.objects.filter(username = email)
      if user_obj.exists():
          messages.warning(request,"Email is al ready Taken")
          return  HttpResponseRedirect(request.path_info)
      print("user not exists")
      password=request.POST.get('password')
      first_name=request.POST.get('name')
      last_name=request.POST.get('surname')
    #   address=request.POST.get('address')
      user_obj=User.objects.create(password=password,first_name=first_name,last_name=last_name,email=email  ,username=email)
      user_obj.set_password(password)
      user_obj.save()
      messages.warning(request,"An email has been sent on your mail.")     
      return  HttpResponseRedirect(request.path_info)
    return  render(request,'accounts/signup.html')
  




def  dashboard_page(request):
    return render(request,'accounts/home.html')



def account_activate(request,email_token):
    if Profile.objects.filter(email_token=email_token).exists():
     user = Profile.objects.get(email_token=email_token)
     user.is_email_verified=True
     user.save() 
     print(user)
     return  render(request,'home/index.html')
    else :
      messages.error(request,"Invalid Email  Token , Try Again !!")
      print("false link ")
      return  HttpResponse("<h1>Invalid Email  Verification Link</h1>")
    