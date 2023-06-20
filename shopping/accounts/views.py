from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from core.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('/')
        messages.info(request,"Login failed, please try again.")
    return render(request, 'accounts/login.html')

def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        phone = request.POST.get('phoneField')
        print(username, email)

        if password == confirmPassword:
                if User.objects.filter(username = username ).exists():
                    print("username already exists")
                    return redirect('user_register')

                if User.objects.filter(email = email ).exists():
                    messages.info(request,"Email already exists")
                    return redirect('user_register')

                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    data = Customer(user=user, phoneField = phone)
                    data.save()

                    ourUser = authenticate(username = username, password = password)
                    if ourUser is not None:
                        return redirect('/')
                    
        else:
            messages.info(request,"Passwords do not match.")
            return redirect('user_register')

    return render(request, 'accounts/register.html')


def user_logout(request):
    logout(request)
    return redirect('/')