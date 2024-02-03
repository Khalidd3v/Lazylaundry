from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required



def signup_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email_address = request.POST.get('email_address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if LazyUser.objects.filter(email__iexact=email_address).exists():
            messages.error(request, "Email is already in use. Please try a different email address.")
            return render(request, 'accounts/signup.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match. Please re-type your password.")
            return render(request, 'accounts/signup.html')

        user = LazyUser.objects.create_user(email=email_address, password=password, first_name=first_name)

        messages.success(request, "Your account has been created successfully. You are now logged in.")
        return redirect('login_user')
    
    return render(request, 'accounts/signup.html')

def login_user(request):
    if request.method == "POST":
        email_address = request.POST.get('email_address')
        password = request.POST.get('password')

        if email_address and password:
            user = authenticate(request, email=email_address, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Email or password is incorrect. Please try again.")
        else:
            messages.error(request, "Email or password can't be blank.")

    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('login_user')


def user_profile(request):
    return render(request, 'accounts/user-profile.html')