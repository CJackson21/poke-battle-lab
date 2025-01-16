from django.http import JsonResponse
from .models import Pokemon

def root_view(request):
    return JsonResponse({"message": "Welcome to the Pokémon Team Builder!"})

def get_pokemon(request):
    pokemons = Pokemon.objects.all().values()
    return JsonResponse(list(pokemons), safe=False)
