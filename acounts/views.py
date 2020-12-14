from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    else:
        if request.method=="POST":
            form=RegistrationForm(request.POST or None)

            if form.is_valid():
                user=form.save()

                raw_password=form.cleaned_data.get('password1')

                user=authenticate(username=user.username,password=raw_password)

                login(request,user)

                return redirect("main:home")
        else:
            form=RegistrationForm()
        return render(request,"acounts/register.html",{"form":form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    else:
        if request.method=="POST":
            username = request.POST['username']
            password = request.POST['password']
            #check crendtials
            user = authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect("main:home")
                else:
                    return render(request,'acounts/login.html',{"error":"Your account has been disabled"})
            else:
                return render(request,'acounts/login.html',{"error":"invalid username password try again"})
        return render(request,'acounts/login.html')

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("acounts:login")
    else:
        return redirect("acounts:login")
