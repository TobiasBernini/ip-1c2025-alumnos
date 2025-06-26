# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    lista_pokemon = transport.getAllImages() # Pide todos los Pokémon desde transport.py
    cards = [translator.fromRequestIntoCard(pokemon) for pokemon in lista_pokemon]# Recorre la lista y convierte cada uno en una Card usando el traductor
    return cards # Devuelve la lista completa de Cards


# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []  # Acá guardamos las cartas que coincidan con la búsqueda
    nombreminusculas = name.lower()  # Pasamos el nombre ingresado a minúsculas
    cartas = getAllImages()  # Obtenemos todas las cartas
    for card in cartas:
        # Si el nombre buscado está dentro del nombre del Pokémon (sin importar mayúsculas)
        if nombreminusculas in card.name.lower():
            filtered_cards.append(card)  # Lo agregamos a la lista filtrada
    return filtered_cards


# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []  # Lista para guardar los Pokémon que coincidan con el tipo
    # Recorremos todas las cartas que devuelve getAllImages()
    for card in getAllImages():
        # Si el tipo buscado está en los tipos del Pokémon, lo agregamos a la lista
        if type_filter in card.types:
            filtered_cards.append(card)
    return filtered_cards



# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = translator.fromTemplateIntoCard(request)
    fav.user = get_user(request)

    if repositories.favourite_exists(fav):
        return False  # Ya existe, no guardamos
    else:
        repositories.save_favourite(fav)
        return True


# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []

    user = get_user(request)

    favourite_list = repositories.get_all_favourites(user)  # ← función que devuelve queryset o lista de diccionarios
    mapped_favourites = [translator.fromRepositoryIntoCard(fav) for fav in favourite_list]

    return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)