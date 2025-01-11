from sqlalchemy import Column, Integer, String, JSON, Text
from sqlalchemy.dialects.postgresql import ARRAY
from databases.database import Base

class Pokemon(Base):
    __tablename__ = "pokemon" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # Name of the Pokémon
    abilities = Column(ARRAY(Text))  # Array of abilities
    types = Column(ARRAY(Text))  # Array of types (e.g., electric, fire)
    stats = Column(JSON)  # JSON field for stats like HP, attack, defense, etc.
