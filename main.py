from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from utils.fetch_pokemon import fetch_all_pokemon_data, fetch_pokemon
from routes.pokemon.pokemon import router as pokemon_router

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(pokemon_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    # Run initial sync on startup
    print("Starting initial Pokémon sync...")
    await fetch_all_pokemon_data()  # Use `await` instead of `asyncio.run`

    # Schedule periodic sync (this is still fine, as it’s not async)
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_pokemon, "interval", hours=24)  # Sync every 24 hours
    scheduler.start()

    # Ensure scheduler shuts down on application stop
    import atexit
    atexit.register(lambda: scheduler.shutdown())

@app.get("/")
def read_root():
    return {"message": "Welcome to the Pokémon Team Builder!"}
