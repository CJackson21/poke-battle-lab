from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.pokemon.getPokemon import router as pokemon_router

app = FastAPI()

# Enable CORS so frontend and backend can communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React development server
    allow_methods=["*"],
    allow_headers=["*"]
)

# Add routes
app.include_router(pokemon_router, prefix="/api/pokemon")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Pokémon Team Builder!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
