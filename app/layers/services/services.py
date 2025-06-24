# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():# EN TEORIA ESTA HECHO Y FUNCIONA 
    lista_pokemon = transport.getAllImages()#trae la lista desde transport.py
    cards = [translator.fromRequestIntoCard(pokemon) for pokemon in lista_pokemon] #Convierte cada Pokémon en una tarjeta usando el traductor y guarda todas en la lista cards
    return cards

# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []
    nombreminusculas = name.lower()
    cartas = getAllImages()
    for card in cartas:
        if nombreminusculas in card.name.lower():
            filtered_cards.append(card)
    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []  # aca se guarda la lista de las cartas que sean del tipo que pedimos 
    tipo = type_filter.lower()  # Convertimos el tipo recibido a minúsculas para comparar sin importar mayúsculas/minúsculas

    # Recorremos todas las cartas que devuelve getAllImages()
    for card in getAllImages():
        # Normalizamos todos los tipos de la carta a minúsculas
        tiposDePokemon = [t.lower() for t in card.types]

        # Verificamos si el tipo buscado está dentro de los tipos de la carta
        if tipo in tiposDePokemon:
            filtered_cards.append(card)  # Si coincide se agrega la carta a la lista filtrada

    return filtered_cards  # Devolvemos la lista con todas las cartas que coinciden


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

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