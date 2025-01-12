import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

interface Pokemon {
  id: number;
  name: string;
  abilities: string[];
  types: string[];
  stats: Record<string, number>;
}

function App() {
  const [pokemonList, setPokemonList] = useState<Pokemon[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch Pokémon data from the backend
  const fetchPokemon = async () => {
    try {
      const response = await axios.get<Pokemon[]>(
        "http://127.0.0.1:8000/api/pokemon"
      );
      setPokemonList(response.data);
      setError(null);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.detail || err.message);
      } else {
        setError("An unexpected error occurred.");
      }
    } finally {
      setLoading(false);
    }
  };

  // Use useEffect to fetch Pokémon on component mount
  useEffect(() => {
    fetchPokemon();
  }, []);

  return (
    <>
      <div>
        <a href='https://vite.dev' target='_blank'>
          <img src='/vite.svg' className='logo' alt='Vite logo' />
        </a>
        <a href='https://react.dev' target='_blank'>
          <img
            src='./assets/react.svg'
            className='logo react'
            alt='React logo'
          />
        </a>
      </div>
      <h1>Pokémon Data Viewer</h1>
      <div className='card'>
        {loading ? (
          <p>Loading Pokémon...</p>
        ) : error ? (
          <p>Error: {error}</p>
        ) : (
          <ul>
            {pokemonList.map((poke) => (
              <li key={poke.id}>
                <h2>{poke.name}</h2>
                <p>
                  <strong>Abilities:</strong> {poke.abilities.join(", ")}
                </p>
                <p>
                  <strong>Types:</strong> {poke.types.join(", ")}
                </p>
                <p>
                  <strong>Stats:</strong>
                </p>
                <ul>
                  {Object.entries(poke.stats).map(([stat, value]) => (
                    <li key={stat}>
                      {stat}: {value}
                    </li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        )}
      </div>
    </>
  );
}

export default App;
