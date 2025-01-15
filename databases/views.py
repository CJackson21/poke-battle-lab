from django.http import JsonResponse
from .models import Pokemon

def get_pokemon(request):
    """
    Fetch all Pokémon from the database and return as JSON.
    """
    pokemons = Pokemon.objects.all().values()
    return JsonResponse(list(pokemons), safe=False)
