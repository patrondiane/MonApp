from fastapi import FastAPI, Depends, HTTPException, Header
from sqlmodel import Session, select
from database import engine, init_db
from models import Commune, Adresse, Equipement

app = FastAPI(title="BDATA API")
init_db()

TOKEN = "123abc"  # Token simple

def get_session():
    with Session(engine) as session:
        yield session

def check_token(token: str = Header(default=None)):
    if token != TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans l'API de gestion des communes !"}

@app.get("/communes", tags=["store"], dependencies=[Depends(check_token)])
def get_communes(session: Session = Depends(get_session)):
    return session.exec(select(Commune)).all()

@app.get("/adresses", tags=["store"], dependencies=[Depends(check_token)])
def get_adresses(session: Session = Depends(get_session)):
    return session.exec(select(Adresse)).all()

@app.get("/equipements", tags=["store"], dependencies=[Depends(check_token)])
def get_equipements(session: Session = Depends(get_session)):
    return session.exec(select(Equipement)).all()

@app.get("/libre/communes", tags=["public"])
def get_communes_libres(session: Session = Depends(get_session)):
    return session.exec(select(Commune)).all()
