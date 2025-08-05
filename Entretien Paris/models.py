from sqlmodel import SQLModel, Field
from typing import Optional

class Commune(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code_insee: str
    nom: str
    pays: str

class Adresse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    voie: str
    code_postal: str
    ville: str

class Equipement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    type: str
    commune: str