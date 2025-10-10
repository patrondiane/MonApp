import json
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

FICHIER_TACHES = "taches.json"
CATEGORIES = ["travail", "perso","sport"]

# Charger les taches
def charger_taches():
    if not os.path.exists(FICHIER_TACHES):
        return []
    with open(FICHIER_TACHES,"r", encoding="utf-8") as f:
        return json.load(f)
    
# Sauvegarder les tâches
def sauvegarder_taches(taches):
    with open(FICHIER_TACHES, "w", encoding="utf-8") as f:
        json.dump(taches, f, indent=4)

# Afficher les tâches avec couleurs
def afficher_taches(taches):
    if not taches:
        print(Fore.YELLOW + "Aucune tâche pour le moment.")
        return
    
    print(Fore.CYAN + "\n📋 Liste des tâches :")
    for i, t in enumerate(taches, 1):
        statut = "✅" if t["fait"] else "⏳"
        cat = t["categorie"].capitalize()
        date = t["date_limite"]
        couleur = Fore.GREEN if t["fait"] else Fore.RED