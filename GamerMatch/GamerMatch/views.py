from django.http import HttpResponse
from django.template import Template, Context, loader
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout


def sign_up(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request,'Account Created Successfully!!!')
            fm.save()
    else:
        fm = SignUpForm()
    return render(request,'signup.html',{'form':fm})


def sign_in(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in successfully!!!')
                    return HttpResponseRedirect('/home_profile/')
        else:
            fm = AuthenticationForm()
        return render(request,'userlogin.html',{'form':fm})
    else:
        return HttpResponseRedirect('/home_profile/')


def home_profile(request):
    if request.user.is_authenticated:
        return render(request,'home_profile.html',{'name':request.user})
    else:
        return HttpResponseRedirect('/')


def profile_settings(request):
    if request.user.is_authenticated:
        return render(request, 'profile_settings.html')
    else:
        return HttpResponseRedirect('/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/userlogin/')


def index(request):
    return render(request, "home.html")
    

def new_publication(request):
    return render(request, "upload.html")

