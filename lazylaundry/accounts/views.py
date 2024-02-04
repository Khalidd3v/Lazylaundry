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

@login_required(login_url='/accounts/login-user/')
def user_profile(request):
    user = LazyUser.objects.filter(username=request.user.username).first()

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        profile_pic = request.FILES.get('profile_image')  # Use get() to avoid KeyError
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        email_address = request.POST.get('email_address')

        if not first_name:
            messages.error(request, "First name can't be blank!")
        else:
            # Check for existing email excluding the current user's email
            if LazyUser.objects.exclude(id=user.id).filter(email=email_address).exists():
                messages.error(request, "Email already exists, please choose a different email.")
            if LazyUser.objects.exclude(id=user.id).filter(username=username).exists():
                messages.error(request, "Username already exists, please choose a different username.")
            if LazyUser.objects.exclude(id=user.id).filter(phone_number=phone_number).exists():
                messages.error(request, "Phone number already exists, please choose a different number.")

            if not messages.get_messages(request):  # If no error messages, update the user profile
                user.first_name = first_name
                user.last_name = last_name
                user.email = email_address
                user.address = address
                user.phone_number = phone_number
                user.username = username

                if profile_pic:
                    # If a profile picture is provided, save it to the 'profile_pic' directory
                    user.profile_pic.save(profile_pic.name, profile_pic)

                user.save()

                messages.success(request, "Your profile has been updated successfully.")
                return redirect('user_profile')

    context = {'user': user}
    return render(request, 'accounts/user-profile.html', context)