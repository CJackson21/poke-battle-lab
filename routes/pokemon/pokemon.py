from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from databases.database import get_db
from databases.models import Pokemon

router = APIRouter()

@router.get("/pokemon")
def get_pokemon(db: Session = Depends(get_db)):
    """
    Fetch all Pokémon from the database.
    """
    return db.query(Pokemon).all()
