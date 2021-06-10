from django.http import HttpResponse
from django.template import Template, Context, loader
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from .models import MatchForm, PersonalTags


def sign_up(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, '¡Cuenta creada exitosamente!')
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
                    messages.success(request, '¡Autenticado exitosamente!')
                    return HttpResponseRedirect('/home_profile/')
        else:
            fm = AuthenticationForm()
        return render(request, 'userlogin.html', {'form': fm})
    else:
        return HttpResponseRedirect('/home_profile/')


def home_profile(request):

    solicitudes = MatchForm.objects.all()

    if request.user.is_authenticated:
        return render(request, 'home_profile.html', {'name': request.user, 'solicitudes': solicitudes})
    else:
        return HttpResponseRedirect('/')


def profile_settings(request):
    # possible query parameter: ?tab, cuyos valores pueden ser {'ajustes', 'juegos', 'tags'}
    # pero es posible no recibir tab, lo que llevará a cargar la pestaña principal de esta página
    if request.user.is_authenticated:
        if request.method == 'POST':
            pass_form = PasswordChangeForm(data=request.POST, user=request.user)

            if pass_form.is_valid():  # password change form
                pass_form.save()
                update_session_auth_hash(request, pass_form.user)
                messages.success(request, 'Password changed successfully')
                return redirect('/profile_settings?tab=ajustes')
            elif 'tags' in request.POST:  # tags form
                tags = request.POST['tags']
                user = User.objects.get(pk=request.user.id)
                personal_tags = PersonalTags(tags=tags, user=user)
                personal_tags.save()
                return redirect('/profile_settings?tab=tags')

            else:
                messages.error(request, 'Unable to change your password. Invalid form.')
            return redirect('/profile_settings')
        else:
            tags = PersonalTags.tags.most_common()
            context = {
                'user_tags': tags
            }

            return render(request, 'profile_settings.html', context)
    else:
        return HttpResponseRedirect('/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/userlogin/')


def index(request):
    if request.user.is_authenticated:
        return render(request, 'home_profile.html', {'name': request.user})
    else:
        return render(request, "home.html")

def go_faq(request):
    return render(request, "faq.html")

def new_publication(request):

    if request.method == 'GET':  # Si estamos cargando la página
        return render(request, "upload.html")  # Mostrar el template

    elif request.method == 'POST':  # Si estamos recibiendo el form de registro

        if request.user.is_authenticated:
            pass

        if True: # Reemplazar este if con el anterior para permitir solo ingreso de user que inicio sesion

            # Tomar los elementos del formulario que vienen en request.POST
            juego = request.POST['nombre_juego']
            tags = request.POST['tags']
            descripcion = request.POST['descripcion']
            user = User.objects.get(pk=request.user.id)

            # Crear el nuevo usuario
            matchForm = MatchForm(juego=juego, tags=tags, descripcion=descripcion, user=user)
            matchForm.save()

            # Redireccionar la página /tareas
            return HttpResponseRedirect('/home_profile')




