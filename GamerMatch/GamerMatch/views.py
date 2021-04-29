from django.http import HttpResponse
from django.template import Template, Context, loader
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash


def sign_up(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account Created Successfully!!!')
            fm.save()
    else:
        fm = SignUpForm()
    return render(request, 'signup.html', {'form': fm})


def sign_in(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully!!!')
                    return HttpResponseRedirect('/home_profile/')
        else:
            fm = AuthenticationForm()
        return render(request, 'userlogin.html', {'form': fm})
    else:
        return HttpResponseRedirect('/home_profile/')


def home_profile(request):
    if request.user.is_authenticated:
        return render(request, 'home_profile.html', {'name': request.user})
    else:
        return HttpResponseRedirect('/')


def profile_settings(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=request.user)

            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password changed successfully')
            else:
                messages.error(request, 'Unable to change your password. Invalid form.')
            return redirect('/profile_settings')
        else:
            password_change_form = PasswordChangeForm(user=request.user)

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

def go_faq(request):
    return render(request, "faq.html")