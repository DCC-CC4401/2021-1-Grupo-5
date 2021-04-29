from django.http import HttpResponse
from django.template import Template, Context, loader
import datetime
from django.shortcuts import render


def index(request):
    return render(request, "home.html")
    
def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def profile(request):
    return render(request, "profile.html")

def new_publication(request):
    return render(request, "upload.html")

