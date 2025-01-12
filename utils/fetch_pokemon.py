import asyncio
import aiohttp

from sqlalchemy.orm import Session
from databases.database import engine
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
        # Setting the limit to 1500. Realistically only need around 1300, but 
        # this won't affect performance. Plus more Pokemon will be added by nintendo I'm sure
        meta_resp = await fetch_one_pokemon(session, f"{API_URL}?limit=1500")
        results = meta_resp["results"]
        print(f"Fetched metadata for {len(results)} Pokémon. Downloading in parallel...")

        # Fetch Pokemon in parallel
        tasks = [fetch_one_pokemon(session, poke["url"]) for poke in results]
        all_data = await asyncio.gather(*tasks)

        return all_data

async def fetch_pokemon():
    """Main function to fetch Pokémon concurrently and store in DB."""
    all_data = await fetch_all_pokemon_data()

    print("Inserting data into database...")
    db_session = Session(bind=engine)

    # Bulk insert data
    pokemons_to_insert = []
    for data in all_data:
        pokemon = Pokemon(
            id=data["id"],
            name=data["name"],
            abilities=[a["ability"]["name"] for a in data["abilities"]],
            types=[t["type"]["name"] for t in data["types"]],
            stats={stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
        )
        pokemons_to_insert.append(pokemon)

    db_session.bulk_save_objects(pokemons_to_insert)
    db_session.commit()
    db_session.close()

    print("Database population complete!")
