# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .layers.services.services import filterByCharacter,filterByType

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):# A LA MITAD
    images = services.getAllImages()#llama a la funcion getallimages()desde services.py
    favourite_list = []

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')

    if name != '':
        images = filterByCharacter(name)  # llama a la función para filtrar las imágenes
        favourite_list = []  # o si tenés función para obtener favoritos, usala aquí

        return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})
    else:
        return redirect('home')


# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '')

    if type != '':
        images = filterByType(type)  # ← CORREGIDO
        favourite_list = []  # ← si querés, más adelante podés cargar favoritos reales

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    pass

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('home')
