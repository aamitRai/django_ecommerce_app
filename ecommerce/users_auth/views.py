from django.utils import timezone
from datetime import timedelta
from django.forms import ValidationError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import CustomUser, Profile ,PasswordResetToken
from django.contrib import messages
from .emails import *
def handle_signin(request):
   if(request.method=="POST"):
      try :
         email=request.POST['email']
         password=request.POST['password']
         if not email or not password:
            return HttpResponse("Email and Password are required", status=400)
         try:
                user = CustomUser.objects.get(email=email)
         except CustomUser.DoesNotExist:
                return HttpResponse("Invalid User email", status=404)

         if (user.check_password(password)==False):
                return HttpResponse("Incorrect password", status=401)             
         if user.is_active==False:
               return HttpResponse("need to activate account , an activation link is end in the email")
         return HttpResponse("Success fully signin")

      except Exception as e:
            print(f"Error during sign in: {e}")
            return HttpResponse("Something went wrong", status=500)
   return render(request,"auth/signin.html")

def handle_signup(request):
    if request.method == "POST":
        try:
            print("method called handle_signup")
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not email or not password:
               messages.error(request,"Email and Password are required")               
               return render(request, "auth/signup.html")
             

            print("email", email, "password", password)

            if CustomUser.objects.filter(email=email).exists():
                return HttpResponse("Email Already Exists", status=401)

            if len(password) < 5:
               messages.warning(request,"Password is too short, at least 5 characters are required")               
               return render(request, "auth/signup.html")
            user = CustomUser.objects.create_user(email=email, password=password)
            messages.warning(request,"An email has been sent on your mail.")   
            return HttpResponse("Successfully signed up")

        except ValidationError as e:
            return HttpResponse(f"Validation error: {e}", status=400)
        except Exception as e:
            print(f"Error during sign up: {e}")
            return HttpResponse("Something went wrong", status=500)

    return render(request, "auth/signup.html")


def handle_account_activation(request,email_token):
            try:
               print("email_token",email_token)
               profile=Profile.objects.get(email_token=email_token)
               print(profile)
               user = CustomUser.objects.get(id=profile.user.id)
               user.is_active = 1 
               user.save()  
               messages.success(request,"Account activate successfully")
               return render(request, "auth/signin.html")

            except Exception as e:
               print("An error occurred:", str(e))  # Print the exception details
               print("got exception in handle account activation")
               return HttpResponse("invalid link")

def handle_forget_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if not email:
            messages.error(request, "Email address is required.")
            return HttpResponseRedirect(request.path_info)
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist.")
            return HttpResponseRedirect(request.path_info)
        try:
            passwordResetToken = PasswordResetToken.objects.create(
                user=user,
                expires_at=timezone.now() + timedelta(hours=1)  # 1 hour expiration
            )
            token = passwordResetToken.token
            send_forget_password_email(email, token)
            messages.success(request, "Change password link has been sent to your email.")
        except Exception as e:
            # Log the exception for debugging
            print(f"Error occurred: {e}")
            messages.error(request, "Something went wrong. Please try again.")
        return HttpResponseRedirect(request.path_info)
    
    return render(request, "auth/forget_password.html")
            
def handle_forget_password_creation(request, password_token=None):
    print("password_token",password_token)
    if password_token is None:
                messages.error(request, "Password token is required")
                return render(request, "auth/forget_password.html")
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        re_enter_password = request.POST.get('re_enter_password')

        if not new_password or not re_enter_password:
            return HttpResponse(" Password are required", status=400)

        if len(new_password) < 5:
            messages.error(request, "Password must be at least 5 characters")
            return HttpResponseRedirect(request.path_info)

        if new_password != re_enter_password:
            return HttpResponse("Passwords do not match", status=400)

        try:
            

            try:
                passwordResetToken = PasswordResetToken.objects.get(token= password_token)
            except PasswordResetToken.DoesNotExist:
                messages.error(request, "Invalid token")
                return render(request, "auth/forget_password.html")

            user_id = passwordResetToken.user_id
            try:
                user = CustomUser.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password updated successfully! Please remember your new password.")
                return render(request, "auth/signin.html")
            except CustomUser.DoesNotExist:
                messages.error(request, "User does not exist.")
                return render(request, "auth/forget_password.html")
        except Exception as e:
            print(f"Error occurred: {e}")
            return render(request, "auth/new_password_create_forget_password.html")
    my_data={
               "password_token":password_token
        }
    return render(request, "auth/new_password_create_forget_password.html",my_data)       
def handle_logout(request):
   pass


