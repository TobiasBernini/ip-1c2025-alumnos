# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    lista_pokemon = transport.getAllImages() # pide todos los Pokemon desde transport.py
    cards = [translator.fromRequestIntoCard(pokemon) for pokemon in lista_pokemon]# recorre la lista y convierte cada uno en una Card usando el traductor
    return cards # devuelve la lista completa de Cards


# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []  # aca guardamos las cartas que coincidan con la busqueda
    nombreminusculas = name.lower()  # pasamos el nombre ingresado a minusculas
    cartas = getAllImages()  # obtenemos todas las cartas
    for card in cartas:
        # si el nombre buscado esta dentro del nombre del Pokemon 
        if nombreminusculas in card.name.lower():
            filtered_cards.append(card)  # lo agregamos a la lista filtrada
    return filtered_cards


# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []  # lista para guardar los Pokemon que coincidan con el tipo
    # recorre todas las cartas que devuelve getAllImages
    for card in getAllImages():
        # si el tipo buscado esta en los tipos del Pokemon lo agregamos a la lista
        if type_filter in card.types:
            filtered_cards.append(card)
    return filtered_cards



# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = translator.fromTemplateIntoCard(request)
    fav.user = get_user(request)

    if repositories.favourite_exists(fav):
        return False 
    else:
        repositories.save_favourite(fav)
        return True


# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []

    user = get_user(request)

    favourite_list = repositories.get_all_favourites(user) 
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