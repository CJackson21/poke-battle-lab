import asyncio
import aiohttp
from django.core.management.base import BaseCommand
from databases.models import Pokemon

API_URL = "https://pokeapi.co/api/v2/pokemon"

async def fetch_one_pokemon(session: aiohttp.ClientSession, url: str):
    """Fetch a single Pokémon's detailed data asynchronously."""
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()

async def fetch_all_pokemon_data():
    """Fetch metadata for all Pokémon, then fetch each detail concurrently."""
    async with aiohttp.ClientSession() as session:
        meta_resp = await fetch_one_pokemon(session, f"{API_URL}?limit=1500")
        results = meta_resp["results"]
        print(f"Fetched metadata for {len(results)} Pokémon. Downloading in parallel...")

        # Fetch Pokemon in parallel
        tasks = [fetch_one_pokemon(session, poke["url"]) for poke in results]
        all_data = await asyncio.gather(*tasks)

        return all_data

class Command(BaseCommand):
    help = "Fetch and populate Pokémon data from PokeAPI."

    def handle(self, *args, **kwargs):
        """Fetch Pokémon data and populate the database."""
        all_data = asyncio.run(fetch_all_pokemon_data())

        print("Inserting data into database...")
        pokemons_to_insert = []
        for data in all_data:
            pokemon = Pokemon(
                id=data["id"],
                name=data["name"],
                abilities=[a["ability"]["name"] for a in data["abilities"]],
                types=[t["type"]["name"] for t in data["types"]],
                stats={stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]},
            )
            pokemons_to_insert.append(pokemon)

        Pokemon.objects.bulk_create(pokemons_to_insert, ignore_conflicts=True)
        print("Database population complete!")
