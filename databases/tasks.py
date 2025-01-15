import asyncio
from databases.management.commands.fetch_pokemon import fetch_all_pokemon_data, fetch_pokemon

def sync_pokemon():
    """Periodic task to sync Pokémon data."""
    asyncio.run(fetch_pokemon())
