from django.http import HttpResponse, JsonResponse
from django.template import Template, Context, loader
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.core import serializers
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from .models import MatchForm, PersonalGames, PersonalTags


def sign_up(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, '¡Cuenta creada exitosamente!')
            fm.save()
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password1']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                messages.success(request, '¡Autenticado exitosamente!')
                return HttpResponseRedirect('/home_profile/')
            else:
                # no deberia pasar nunca
                return render(request, 'signup.html', {'form': fm})
        else:
            uname = fm.data['username']
            if User.objects.filter(username=uname).exists():
                messages.success(request, 'Usuario ya existe.')
            else:
                messages.success(request, 'Ups! Algo salió mal. A debuggear!')
            return render(request, 'signup.html', {'form': fm})
    else:
        # no deberia pasar nunca
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
                messages.success(request, '¡Credenciales incorrectas!')
                return render(request, 'userlogin.html', {'form': fm})
        else:
            fm = AuthenticationForm()
        return render(request, 'userlogin.html', {'form': fm})
    else:
        return HttpResponseRedirect('/home_profile/')


def home_profile(request):
    solicitudes = MatchForm.objects.all()
    solicitudes_user = MatchForm.objects.filter(user=User.objects.get(pk=request.user.id))

    if request.user.is_authenticated:
        return render(request, 'home_profile.html',
                      {'name': request.user, 'solicitudes': solicitudes, "solicitudes_user": solicitudes_user})
    else:
        return HttpResponseRedirect('/')


def change_password(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/profile_settings?tab=ajustes')
    elif request.user.is_authenticated and request.method == 'POST':
        pass_form = PasswordChangeForm(data=request.POST, user=request.user)

        if pass_form.is_valid():  # password change form
            pass_form.save()
            update_session_auth_hash(request, pass_form.user)
            messages.success(request, 'Password changed successfully')
        else:
            messages.error(request, 'Unable to change your password. Invalid form probably because some validations.')
        return redirect('/profile_settings?tab=ajustes')

def update_favorite_games(request):
    if request.method == 'GET':
        if request.is_ajax() and request.user.is_authenticated:
            # Get user favorites from db
            fv_games = PersonalGames.objects.filter(user_id=User.objects.get(pk=request.user.id))

            # Prepare json response
            json_data = {}
            if fv_games.count() == 1:
                fv_games = fv_games.values_list('lol', 'minecraft', 'smash', 'valorant', 'overwatch')
                json_data = serializers.serialize('json', fv_games)

            return JsonResponse(json_data, status=200)
        else:
            return HttpResponseRedirect('/profile_settings?tab=juegos')
    elif request.method == 'POST' and request.user.is_authenticated:
        def convert_to_bool(value):
            if value in ["true", "TRUE", "True"]:
                return True
            else:
                return False

        # Get the data
        lol_game = convert_to_bool(request.POST['lol_game'])
        minecraft_game = convert_to_bool(request.POST['minecraft_game'])
        smash_game = convert_to_bool(request.POST['smash_game'])
        valorant_game = convert_to_bool(request.POST['valorant_game'])
        overwatch_game = convert_to_bool(request.POST['overwatch_game'])
        user = User.objects.get(pk=request.user.id)

        data = {"lol": lol_game, "minecraft": minecraft_game, "smash": smash_game,
                "valorant": valorant_game, "overwatch": overwatch_game}
        PersonalGames.objects.update_or_create(user=user, defaults=data)

        if request.is_ajax():
            return JsonResponse({'message': "AJAX POST received. DB updated successfully.",
                                 'caution': "Guys, when we're ready with this, we have to remember removing this msg",
                                 'data_received': [lol_game, minecraft_game, smash_game,
                                                   valorant_game, overwatch_game]},
                                status=200)

        return JsonResponse({'message': 'POST received. Favorite games updated',
                             'data_received': [lol_game, minecraft_game, smash_game,
                                               valorant_game, overwatch_game]})


def update_tags(request):
    if request.method == 'GET':
        if request.is_ajax() and request.user.is_authenticated:
            # Get user favorites from db
            fv_tags = PersonalTags.objects.filter(user_id=User.objects.get(pk=request.user.id))

            # Prepare json response
            json_data = {}
            if fv_tags.count() == 1:
                fv_tags = fv_tags.values_list('tags')
                json_data = serializers.serialize('json', fv_tags)

            return JsonResponse(json_data, status=200)
        else:
            return HttpResponseRedirect('/profile_settings?tab=tags')
    elif request.method == 'POST' and request.user.is_authenticated:
        # Get the data
        tags_data = request.POST['tags_data']
        user = User.objects.get(pk=request.user.id)

        data = {"tags": tags_data}
        PersonalTags.objects.update_or_create(user=user, defaults=data)

        if request.is_ajax():
            return JsonResponse({'message': "AJAX POST received. DB updated successfully.",
                                 'caution': "Guys, when we're ready with this, we have to remember removing this msg",
                                 'data_received': [tags_data]},
                                status=200)

        return JsonResponse({'message': 'POST received. Tags updated',
                             'data_received': [tags_data]})

def profile_settings(request):
    # possible query parameter: ?tab, cuyos valores pueden ser {'ajustes', 'juegos', 'tags'}
    # pero es posible no recibir tab, lo que llevará a cargar la pestaña principal de esta página
    if request.user.is_authenticated:

        if request.method == 'GET':
            context = {}

            fv_games = PersonalGames.objects.filter(user_id=User.objects.get(pk=request.user.id))
            tags = PersonalTags.objects.filter(user_id=User.objects.get(pk=request.user.id))
            if fv_games.count() > 0:
                context['favorite_games'] = fv_games.values()[0]
            else:
                context['favorite_games'] = {'lol': False, 'minecraft': False, 'smash': False, 'valorant': False,
                                             'overwatch': False}
            if tags.count() > 0:
                value = tags.values()[0]
                if value['tags'] == "":
                    context['favorite_tags'] = {'tags' : "Ejemplo"}
                else:
                    context['favorite_tags'] = tags.values()[0]
            else:
                context['favorite_tags'] = {'tags': "Ejemplo"}
            return render(request, 'profile_settings.html', context)
    else:
        return HttpResponseRedirect('/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/userlogin/')


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home_profile')
        # return render(request, 'home_profile.html', {'name': request.user})
    else:
        return render(request, "home.html")


def go_faq(request):
    if request.user.is_authenticated:
        return render(request, "faq.html", {'icons': 1})
    else:
        return render(request, "faq.html", {'icons': 0})


def new_publication(request):
    if request.method == 'GET':  # Si estamos cargando la página
        return render(request, "upload.html")  # Mostrar el template

    elif request.method == 'POST':  # Si estamos recibiendo el form de registro

        if request.user.is_authenticated:
        #    pass

        #if True:  # Reemplazar este if con el anterior para permitir solo ingreso de user que inicio sesion

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
