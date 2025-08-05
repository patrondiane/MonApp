from sqlmodel import SQLModel, Session, create_engine, select
from models import Commune, Adresse, Equipement

sqlite_file = "bdapi.db"
engine = create_engine(f"sqlite:///{sqlite_file}", echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        if not session.exec(select(Commune)).first():
            session.add_all([
                Commune(code_insee="75056", nom="Paris", pays="France"),
                Commune(code_insee="13055", nom="Marseille", pays="France")
            ])
            session.add_all([
                Adresse(voie="1 rue de Paris", code_postal="75001", ville="Paris"),
                Adresse(voie="5 avenue Méditerranée", code_postal="13001", ville="Marseille")
            ])
            session.add_all([
                Equipement(nom="Gymnase Dunois", type="Sport", commune="Paris"),
                Equipement(nom="Bibliothèque St Charles", type="Culture", commune="Marseille")
            ])
            session.commit()
