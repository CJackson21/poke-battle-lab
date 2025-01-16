from django.urls import path
from .views import get_pokemon

urlpatterns = [
    path("pokemon/", get_pokemon, name="get_pokemon"),
]
