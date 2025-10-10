from flask import Flask, render_template, request, abort, jsonify
import pandas as pd
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# ---------- Chargement et nettoyage des fichiers ----------
def load_tab_file(path):
    df = pd.read_csv(path, sep="\t", dtype=str, encoding="latin1", low_memory=False)
    df = df.fillna("")
    df[df.columns[0]] = df[df.columns[0]].astype(str).str.strip()
    return df

# Chargement fichiers
df_med = load_tab_file("Medicaments.txt")
df_presc = load_tab_file("Prescription_Medicaments.txt")
df_comp = load_tab_file("Compositions.txt")
df_smr = load_tab_file("avis_smr.txt")
df_asmr = load_tab_file("avis_asmr.txt")
df_groupes = load_tab_file("groupes_generiques.txt")
df_dispo = load_tab_file("dispo.txt")

# ---------- Dictionnaires ----------
dict_cis_nom = dict(zip(df_med.iloc[:, 0], df_med.iloc[:, 1]))

dict_cis_presc = {}
if not df_presc.empty:
    for code_cis, group in df_presc.groupby(df_presc.columns[0]):
        if df_presc.shape[1] > 2:
            dict_cis_presc[code_cis] = group.iloc[:, 2].astype(str).tolist()
        else:
            dict_cis_presc[code_cis] = group.apply(lambda r: " | ".join(r.astype(str)), axis=1).tolist()

dict_cis_comp = {}
if not df_comp.empty:
    for code_cis, group in df_comp.groupby(df_comp.columns[0]):
        comps = []
        for _, row in group.iterrows():
            forme = row.iloc[1] if df_comp.shape[1] > 1 else ""
            actif = row.iloc[3] if df_comp.shape[1] > 3 else ""
            dosage = row.iloc[4] if df_comp.shape[1] > 4 else ""
            unite = row.iloc[5] if df_comp.shape[1] > 5 else ""
            sous_forme = row.iloc[6] if df_comp.shape[1] > 6 else ""
            sous_dosage = row.iloc[7] if df_comp.shape[1] > 7 else ""

            lines = []
            if forme:
                lines.append(f"{forme} (Composition pour un {forme.lower()})")
            if actif:
                if dosage or unite:
                    lines.append(f"{actif} -> {dosage}{(' ' + unite) if unite else ''}".strip())
                else:
                    lines.append(f"{actif}")
            if sous_forme:
                sf_line = f"sous forme de : {sous_forme}"
                if sous_dosage:
                    sf_line += f" -> {sous_dosage}"
                lines.append(sf_line)
            comps.append("\n".join(lines))
        dict_cis_comp[code_cis] = comps

dict_cis_smr = {}
if not df_smr.empty:
    for _, row in df_smr.iterrows():
        code = row.iloc[0]
        niveau = row.iloc[4] if df_smr.shape[1] > 4 else ""
        texte = row.iloc[5] if df_smr.shape[1] > 5 else ""
        dict_cis_smr[code] = f"{niveau} - {texte}".strip(" -")

dict_cis_asmr = {}
if not df_asmr.empty:
    for _, row in df_asmr.iterrows():
        code = row.iloc[0]
        niveau = row.iloc[4] if df_asmr.shape[1] > 4 else ""
        texte = row.iloc[5] if df_asmr.shape[1] > 5 else ""
        dict_cis_asmr[code] = f"{niveau} - {texte}".strip(" -")

dict_groupes = {}
if not df_groupes.empty:
    for _, row in df_groupes.iterrows():
        key = row.iloc[2] if df_groupes.shape[1] > 2 else ""
        name = row.iloc[1] if df_groupes.shape[1] > 1 else ""
        if key:
            dict_groupes[str(key).strip()] = name

# Gestion de la dispo
dict_cis_dispo = {}
if not df_dispo.empty:
    for _, row in df_dispo.iterrows():
        code = row.iloc[0]
        statut = row.iloc[3] if len(row) > 3 else ""
        url = row.iloc[7] if len(row) > 7 else f"https://agence-prd.ansm.sante.fr/php/ecodex/extrait.php?specid={code}"
        if code:
            dict_cis_dispo[str(code).strip()] = (statut, url)

# ---------- Liste triée de médicaments ----------
medicaments = sorted([(code, nom) for code, nom in dict_cis_nom.items()], key=lambda x: x[1].lower())

# ---------- Onglets Résumé ----------
def get_resume_url(code):
    return f"https://base-donnees-publique.medicaments.gouv.fr/medicament/{code}/extrait#tab-rcp"

# ---------- Texte Résumé ----------
def fetch_resume_text(code):
    url = f"https://base-donnees-publique.medicaments.gouv.fr/medicament/{code}/extrait#tab-rcp"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        return f"Erreur lors de la récupération du resume : {e}"

    soup = BeautifulSoup(resp.content, "html.parser")
    # Récupération du contenu texte principal
    body = soup.find("body")
    return body.get_text(separator="\n", strip=True) if body else "Resume introuvable"

# ---------- Onglets Notice ----------
def get_notice_url(code):
    return f"https://base-donnees-publique.medicaments.gouv.fr/medicament/{code}/extrait#tab-notice"

# ---------- Texte Notice---------
def fetch_notice_text(code):
    url = f"https://base-donnees-publique.medicaments.gouv.fr/medicament/{code}/extrait#tab-notice"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        return f"Erreur lors de la récupération de la notice : {e}"

    soup = BeautifulSoup(resp.content, "html.parser")
    # Récupération du contenu texte principal
    body = soup.find("body")
    return body.get_text(separator="\n", strip=True) if body else "Notice introuvable"


# ---------- Routes ----------
@app.route("/", methods=["GET"])
def index():
    query = request.args.get("search", "").lower()
    if query:
        filtered = [(code, nom) for code, nom in medicaments if query in nom.lower() or query in code]
    else:
        filtered = medicaments
    return render_template("index.html", medicaments=filtered, search=query, groupes=dict_groupes)

@app.route("/medicament/<code>", methods=["GET"])
def medicament_detail(code):
    if code not in dict_cis_nom:
        abort(404)
    nom = dict_cis_nom[code]
    prescriptions = dict_cis_presc.get(code, [])
    compositions = dict_cis_comp.get(code, [])
    avis_smr = dict_cis_smr.get(code)
    avis_asmr = dict_cis_asmr.get(code)
    groupe_generique = dict_groupes.get(code)
    disponibilite = dict_cis_dispo.get(code, ("Statut inconnu", f"https://agence-prd.ansm.sante.fr/php/ecodex/extrait.php?specid={code}"))
    notice_url = get_notice_url(code)
    notice_text = fetch_notice_text(code)
    resume_url = get_resume_url(code)
    resume_text = fetch_resume_text(code)

    return render_template(
        "medicament.html",
        code=code,
        nom=nom,
        prescriptions=prescriptions,
        compositions=compositions,
        avis_smr=avis_smr,
        avis_asmr=avis_asmr,
        groupe_generique=groupe_generique,
        disponibilite=disponibilite,
        notice_url=notice_url,
        notice_text=notice_text,
        resume_url=resume_url,
        resume_text=resume_text
    )

if __name__ == "__main__":
    app.run(debug=True)
