from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from collections import Counter
import string


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

STOPWORDS = {"le", "la", "les", "un", "une", "de", "des", "et", "à", "a", "il", "elle", "est", "ce", "sur", "du", "en", "pour", "au"}

def analyser_texte(texte: str):
    lignes = texte.strip().split("\n")
    paragraphes = texte.strip().split("\n\n")
    texte_nettoye = texte.lower().translate(str.maketrans('','',string.punctuation))
    mots = texte_nettoye.split()
    mots_utiles = [m for m in mots if m not in STOPWORDS]
    frequence = Counter(mots_utiles).most_common(10)
    caracteres_sans_espaces = len(texte.replace(" ", "").replace("\n", ""))

    return {
        "lignes": len(lignes),
        "paragraphes": len(paragraphes),
        "mots": len(mots),
        "caractères_sans_espaces": caracteres_sans_espaces,
        "top_mots": frequence
    }

@app.get("/", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "resultats": None})

@app.post("/", response_class=HTMLResponse)
async def analyser(request: Request, fichier: UploadFile):
    contenu = await fichier.read()
    texte = contenu.decode("utf-8")
    stats = analyser_texte(texte)
    return templates.TemplateResponse("index.html", {"request": request,"resultats": stats})