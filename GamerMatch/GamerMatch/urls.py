"""GamerMatch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from GamerMatch.views import index, sign_in, sign_up, home_profile, user_logout, new_publication, profile_settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('userlogin/', sign_in,name='userlogin'),
    path('signup/', sign_up,name='signup'),
    path('home_profile/', home_profile, name='profile'),
    path('profile_settings/', profile_settings, name='profile_settings'),
    path('upload/', new_publication, name='upload'),
    path('logout/',user_logout,name='logout'),
]
