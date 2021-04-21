from django.http import HttpResponse


def index(request):
    return HttpResponse("Este es el home (tanto normal como de usuario! la url debe ser la misma)")

def login(request):
    return HttpResponse("Aquí va el formulario de login.")

def register(request):
    return HttpResponse("Aquí va el formulario de registro.")

def profile(request):
    return HttpResponse("Estas son las configuraciones de perfil.")

def new_publication(request):
    return HttpResponse("Aquí se manda una nueva publicación.")

