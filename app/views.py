# capa de vista/presentación
from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,get_user
from .layers.services.services import filterByCharacter,filterByType
from .layers.utilities import translator
from .layers.persistence import repositories

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages()  # todas las imágenes Pokémon
    favourite_list = services.getAllFavourites(request)  # favoritos del usuario (objetos Card)
    favorite_names = [fav.name for fav in favourite_list]  # lista solo con nombres

    context = {'images': images,'favourite_list': favourite_list,'favorite_names': favorite_names,}
    return render(request, 'home.html', context)

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')

    if name != '':
        images = filterByCharacter(name)
        favourite_list = services.getAllFavourites(request)
        favorite_names = [fav.name for fav in favourite_list]

        return render(request, 'home.html', {'images': images,'favourite_list': favourite_list,'favorite_names': favorite_names})
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '')

    if type != '':
        images = filterByType(type)
        favourite_list = services.getAllFavourites(request) 
        favorite_names = [fav.name for fav in favourite_list]

        return render(request, 'home.html', {'images': images,'favourite_list': favourite_list,'favorite_names': favorite_names})
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourites = services.getAllFavourites(request)
    return render(request, 'favourites.html', {'favourite_list': favourites})   

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        services.saveFavourite(request)  # Esto evita el duplicado
    return redirect('home')

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        favId = request.POST.get('id')
        if favId:
            success = services.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect('home')

#funcion nueva para los mails
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import UserRegisterForm

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Enviar correo
            subject = '¡Bienvenido a la Pokédex!'
            message = (
                f'Hola {user.first_name},\n\n'
                f'Tu cuenta fue registrada exitosamente.\n'
                f'Usuario: {user.username}\n'
                f'Contraseña: {password}\n\n'
                '¡Gracias por unirte!'
            )
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                messages.success(request, 'Usuario registrado exitosamente. Se envió un correo con tus credenciales.')
            except Exception as e:
                print(f"Error enviando correo: {e}")
                messages.warning(request, 'Usuario registrado, pero no se pudo enviar el correo.')

            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})

