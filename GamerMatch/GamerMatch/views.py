from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import SignUpForm
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
    solicitudes 	 = MatchForm.objects.all().order_by('-time')
    solicitudes_user = MatchForm.objects.filter(user=User.objects.get(pk=request.user.id)).order_by('-time')

    # Solicitudes de juegos favoritos
    solicitudes_fav  = []
    fav_games = PersonalGames.objects.filter(user=User.objects.get(pk=request.user.id)) # Get jeugos favoritos del usuario

    # Asegurarse de que existan fav_games
    if len(fav_games) > 0:

        fav_games = fav_games[0]

        # Lista de juegos
        juegos_bool = [fav_games.lol, fav_games.minecraft, fav_games.smash, fav_games.valorant, fav_games.overwatch,
                       fav_games.otros]
        juegos_largo = ["League of Legends", "Minecraft", "Super Smash Bros.", "Valorant", "Overwatch", "Otros"]

        # Recuperar solicitudes favoritas
        for i, game in enumerate(juegos_bool):
            if game:
                for solicitud in solicitudes:
                    if solicitud.juego == juegos_largo[i] and solicitud.user != request.user.username:
                        solicitudes_fav.append(solicitud)

    if request.user.is_authenticated:
        return render(request, 'home_profile.html',
                      {'name': request.user, 'solicitudes': solicitudes, "solicitudes_user": solicitudes_user, "solicitudes_fav": solicitudes_fav})
    else:
        return HttpResponseRedirect('/')


def search(request):
    tags = request.GET.get('search_tag').replace(', ', ',').split(',')
    i = 0
    solicitudes = []
    if i < len(tags):
        condition = Q(tags__contains=tags[0])
        i += 1
        while i < len(tags):
            condition |= Q(tags__contains=tags[i])
            i += 1

        solicitudes = MatchForm.objects.filter(condition)

    if request.user.is_authenticated:
        return render(request, 'search.html',
                      {'name': request.user, 'solicitudes': solicitudes})
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
            messages.success(request, 'Su contraseña fue cambiada exitósamente.')
        else:
            messages.error(request, 'Ocurrió un error al cambiar la contraseña. '
                                    'Revise que haya ingresado correctamente la antigua')
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
        otros_game = convert_to_bool(request.POST['otros_game'])
        user = User.objects.get(pk=request.user.id)

        data = {"lol": lol_game, "minecraft": minecraft_game, "smash": smash_game,
                "valorant": valorant_game, "overwatch": overwatch_game, "otros": otros_game}
        # Update the database
        PersonalGames.objects.update_or_create(user=user, defaults=data)

        if request.is_ajax():
            return JsonResponse({'message': "AJAX POST received. DB updated successfully.",
                                 'data_received': [lol_game, minecraft_game, smash_game,
                                                   valorant_game, overwatch_game, otros_game]},
                                status=200)

        return JsonResponse({'message': 'POST received. Favorite games updated',
                             'data_received': [lol_game, minecraft_game, smash_game,
                                               valorant_game, overwatch_game, otros_game]})


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
                                             'overwatch': False, 'otros': False}
            if tags.count() > 0:
                value = tags.values()[0]
                if value['tags'] == "":
                    context['favorite_tags'] = {'tags': "Ejemplo"}
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
