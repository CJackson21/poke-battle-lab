from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.get("/{name}")
async def get_pokemon(name: str):
    """
    Fetch details about a Pokémon from PokeAPI and return the response.
    """
    try:
        # Fetch Pokémon data from PokeAPI
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")
        response.raise_for_status()
        pokemon_data = response.json()

        # Process or filter the data
        result = {
            "name": pokemon_data['name'],
            "abilities": [ability['ability']['name'] for ability in pokemon_data['abilities']],
            "types": [ptype['type']['name'] for ptype in pokemon_data['types']],
            "stats": {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}
        }

        return result
    except requests.exceptions.HTTPError:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred")
