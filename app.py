
# -*- coding: utf-8 -*-
"""
Plan Financier Stratégique Familial - Streamlit
Auteurs : Alix & William — Modèle d'application
Description : Suivi des projets, revenus/dépenses, KPI (50/30/20, fonds d'urgence, actifs/passifs, cashflow),
recommandations croisés (Kiyosaki, Ramsey, Orman), vision 2030.
"""
import io
import json
import math
from datetime import datetime, date
from typing import Tuple

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Plan Financier Stratégique Familial",
                   page_icon="💡",
                   layout="wide")

@st.cache_data
def load_default_projects() -> pd.DataFrame:
    df = pd.read_csv("projects_sample.csv")
    df["Budget_prevu"] = pd.to_numeric(df["Budget_prevu"], errors="coerce").fillna(0.0)
    df["Budget_cotise"] = pd.to_numeric(df["Budget_cotise"], errors="coerce").fillna(0.0)
    df["ROI_estime_pct"] = pd.to_numeric(df["ROI_estime_pct"], errors="coerce").fillna(0.0)
    df["Date_echeance"] = pd.to_datetime(df["Date_echeance"], errors="coerce")
    return df

@st.cache_data
def load_default_transactions() -> pd.DataFrame:
    df = pd.read_csv("transactions_sample.csv", parse_dates=["Date"])
    df["Montant"] = pd.to_numeric(df["Montant"], errors="coerce").fillna(0.0)
    return df

def pct(x: float, y: float) -> float:
    if y == 0:
        return 0.0
    return float(x) / float(y)

def fmt_fcfa(x: float) -> str:
    try:
        return f"{x:,.0f} FCFA".replace(",", " ")
    except Exception:
        return f"{x} FCFA"

DEFAULT_503020 = {
    "Besoins": ["Scolarité", "Santé", "Loyer", "Transports essentiels", "Nourriture"],
    "Envies": ["Voyage", "Cadeaux", "Sorties", "Culture", "Électronique"],
    "Épargne/Dette": ["Épargne projet", "Fonds d'urgence", "Remboursement dette"]
}

DEFAULT_QUADRANT_SOURCES = {
    "E": ["Salaire William", "Job", "Salariat"],
    "S": ["Freelance", "Consulting"],
    "B": ["IIBA", "Atekys", "Entreprise familiale"],
    "I": ["Dividendes", "Intérêts", "Immobilier", "Rente"]
}

st.sidebar.header("⚙️ Paramètres & Données")

uploaded_projects = st.sidebar.file_uploader("Importer Projets (CSV)", type=["csv"])
uploaded_tx = st.sidebar.file_uploader("Importer Transactions (CSV)", type=["csv"])

if uploaded_projects:
    projects_df = pd.read_csv(uploaded_projects, parse_dates=["Date_echeance"])
else:
    projects_df = load_default_projects()

if uploaded_tx:
    tx_df = pd.read_csv(uploaded_tx, parse_dates=["Date"])
else:
    tx_df = load_default_transactions()

st.sidebar.subheader("Paramètres Financiers")
currency = st.sidebar.selectbox("Devise", ["FCFA", "CHF", "EUR"], index=0)
rate_fcfa_per_currency = 1.0

emergency_target = st.sidebar.number_input("Objectif Fonds d'urgence (FCFA)", min_value=0, value=1_000_000, step=100_000)
months_ef = st.sidebar.slider("Fonds d'urgence cible (mois de dépenses)", min_value=1, max_value=12, value=3)

independence_target_ratio = st.sidebar.slider("Cible indépendance : revenus passifs / dépenses", 0.0, 2.0, 1.0, 0.1)

st.sidebar.subheader("Règle 50/30/20")
needs_labels = st.sidebar.text_area("Besoins (séparés par virgules)", value=", ".join(DEFAULT_503020["Besoins"]))
wants_labels = st.sidebar.text_area("Envies (séparés par virgules)", value=", ".join(DEFAULT_503020["Envies"]))
save_labels  = st.sidebar.text_area("Épargne/Dette (séparés par virgules)", value=", ".join(DEFAULT_503020["Épargne/Dette"]))

st.sidebar.subheader("Quadrants (sources revenus)")
import json as _json
quadrant_map_json = st.sidebar.text_area("Mapping Quadrants JSON", value=_json.dumps(DEFAULT_QUADRANT_SOURCES, ensure_ascii=False, indent=2))

try:
    QUAD_MAP = _json.loads(quadrant_map_json)
except Exception:
    QUAD_MAP = DEFAULT_QUADRANT_SOURCES

# Nettoyage & enrichissement
projects_df["Budget_prevu"] = pd.to_numeric(projects_df["Budget_prevu"], errors="coerce").fillna(0.0)
projects_df["Budget_cotise"] = pd.to_numeric(projects_df["Budget_cotise"], errors="coerce").fillna(0.0)
projects_df["ROI_estime_pct"] = pd.to_numeric(projects_df.get("ROI_estime_pct", 0.0), errors="coerce").fillna(0.0)
projects_df["Date_echeance"] = pd.to_datetime(projects_df["Date_echeance"], errors="coerce")

tx_df["Montant"] = pd.to_numeric(tx_df["Montant"], errors="coerce").fillna(0.0)
tx_df["Date"] = pd.to_datetime(tx_df["Date"], errors="coerce")

def label_503020(row) -> str:
    cat = str(row.get("Categorie", ""))
    needs = [c.strip().lower() for c in needs_labels.split(",") if c.strip()]
    wants = [c.strip().lower() for c in wants_labels.split(",") if c.strip()]
    saving = [c.strip().lower() for c in save_labels.split(",") if c.strip()]
    c = cat.lower()
    if c in [x.lower() for x in needs]:
        return "Besoins"
    if c in [x.lower() for x in wants]:
        return "Envies"
    if c in [x.lower() for x in saving]:
        return "Épargne/Dette"
    return "Autre"

if "Nature" not in tx_df.columns:
    tx_df["Nature"] = np.where(tx_df["Montant"]>=0, "Revenu", "Dépense")
if "Categorie" not in tx_df.columns:
    tx_df["Categorie"] = ""

tx_df["Label_503020"] = tx_df.apply(label_503020, axis=1)

def is_passive_income(src: str) -> bool:
    src = str(src).lower()
    passive_keywords = ["iiba", "dividende", "intérêt", "immobilier", "rente", "location", "invest"]
    return any(k in src for k in passive_keywords)

tx_df["Revenu_Passif"] = np.where((tx_df["Nature"]=="Revenu") & (tx_df["Source"].astype(str).apply(is_passive_income)), 1, 0)

# KPI
tx_df["Mois"] = tx_df["Date"].dt.to_period("M").astype(str)
rev = tx_df[tx_df["Nature"]=="Revenu"].groupby("Mois")["Montant"].sum().rename("Revenus")
dep = -tx_df[tx_df["Nature"]=="Dépense"].groupby("Mois")["Montant"].sum().rename("Dépenses")
kpi_df = pd.concat([rev, dep], axis=1).fillna(0.0)
kpi_df["Solde"] = kpi_df["Revenus"] - kpi_df["Dépenses"]

revenus_cum = kpi_df["Revenus"].sum()
depenses_cum = kpi_df["Dépenses"].sum()
solde_cum = revenus_cum - depenses_cum

ef_realise = tx_df[(tx_df["Nature"]=="Revenu") & (tx_df["Categorie"].str.lower().str.contains("urgence|épargne", na=False))]["Montant"].sum()
avg_monthly_exp = kpi_df["Dépenses"].mean() if len(kpi_df)>0 else 0.0
ef_required = max(emergency_target, months_ef * avg_monthly_exp)

def _pct(x,y):
    try:
        return float(x)/float(y) if y else 0.0
    except:
        return 0.0

ef_coverage = _pct(ef_realise, ef_required)

passive_income = tx_df[(tx_df["Nature"]=="Revenu") & (tx_df["Revenu_Passif"]==1)]["Montant"].sum()
passive_ratio = _pct(passive_income, revenus_cum) if revenus_cum>0 else 0.0

independence_attained = (passive_income >= depenses_cum) or (passive_ratio >= 1.0)

lab = tx_df[tx_df["Nature"]=="Dépense"].groupby("Label_503020")["Montant"].sum().abs()
tot_dep = lab.sum()
if tot_dep > 0:
    need_p = _pct(lab.get("Besoins",0), tot_dep)
    want_p = _pct(lab.get("Envies",0), tot_dep)
    save_p  = _pct(lab.get("Épargne/Dette",0), tot_dep)
    rule_ok = (need_p<=0.55) and (want_p<=0.35) and (save_p>=0.15)
else:
    need_p = want_p = save_p = 0.0
    rule_ok = True

if ef_coverage < 1.0 or solde_cum < 0:
    phase = "Stabilisation"
elif passive_ratio < 0.5:
    phase = "Transition"
else:
    phase = "Expansion"

if ef_realise < min(1_000_000, ef_required*0.2):
    baby_step = 1
elif ef_realise < ef_required:
    baby_step = 3
else:
    baby_step = 4

# Header KPIs
st.title("🏠 Plan Financier Stratégique Familial")
left, mid, right, extra = st.columns([1.2,1.2,1.2,1])
with left:
    st.metric("Revenus cumulés", f"{revenus_cum:,.0f} FCFA".replace(",", " "))
with mid:
    st.metric("Dépenses cumulées", f"{depenses_cum:,.0f} FCFA".replace(",", " "))
with right:
    st.metric("Solde net", f"{solde_cum:,.0f} FCFA".replace(",", " "))
with extra:
    st.metric("Phase", phase)
    st.metric("Baby Step (Ramsey)", f"{baby_step}")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Couverture Fonds d'urgence", f"{ef_coverage*100:.0f}%", help=f"Réalisé {ef_realise:,.0f} / Cible {ef_required:,.0f} FCFA".replace(",", " "))
with c2:
    st.metric("Ratio revenus passifs", f"{passive_ratio*100:.0f}%")
with c3:
    st.metric("Indépendance financière", "✅ Oui" if independence_attained else "❌ Non")
with c4:
    st.metric("Règle 50/30/20", "✅ OK" if rule_ok else "⚠️ À surveiller", help=f"Besoins {need_p*100:.0f}% | Envies {want_p*100:.0f}% | Épargne/Dette {save_p*100:.0f}%")

st.divider()

# Graphiques
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("📈 Cashflow mensuel")
    if not kpi_df.empty:
        cash = kpi_df.reset_index().rename(columns={"Mois":"Mois"})
        fig = px.line(cash, x="Mois", y=["Revenus","Dépenses","Solde"], markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune transaction pour tracer le cashflow.")

with col_b:
    st.subheader("🍩 Répartition 50/30/20")
    if tot_dep > 0:
        donut_df = pd.DataFrame({
            "Catégorie":["Besoins","Envies","Épargne/Dette","Autre"],
            "Montant":[lab.get("Besoins",0), lab.get("Envies",0), lab.get("Épargne/Dette",0), lab.get("Autre",0)]
        })
        fig2 = px.pie(donut_df, values="Montant", names="Catégorie", hole=0.6)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Aucune dépense catégorisée pour la règle 50/30/20.")

st.subheader("🧭 Quadrants Familiaux (Kiyosaki)")
revenus = tx_df[tx_df["Nature"]=="Revenu"].copy()
revenus["Quadrant"] = "Autre"
for quad, keys in QUAD_MAP.items():
    mask = False
    for k in keys:
        mask = mask | revenus["Source"].astype(str).str.contains(k, case=False, na=False)
    revenus.loc[mask, "Quadrant"] = quad

quad_pivot = revenus.groupby("Quadrant")["Montant"].sum().reset_index()
if not quad_pivot.empty:
    fig3 = px.bar(quad_pivot, x="Quadrant", y="Montant", text_auto=True)
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Pas de revenus pour afficher les quadrants.")

st.divider()

# Projets
st.header("📋 Projets : faisabilité & conseils croisés")
projects_df["Avancement"] = projects_df.apply(lambda r: (r["Budget_cotise"]/r["Budget_prevu"] if r["Budget_prevu"] else 0.0), axis=1)
projects_df["Actif_Passif"] = np.where(projects_df["Type"].str.lower().str.contains("actif", na=False), "Actif", "Passif")

def avis_kiyosaki(row) -> str:
    if row["Actif_Passif"] == "Actif":
        if row.get("ROI_estime_pct",0) > 0:
            return "✅ Actif : à financer en priorité si ROI > coût. Utiliser revenus passifs / business."
        else:
            return "ℹ️ Actif neutre : préciser le ROI attendu avant d'engager de gros montants."
    else:
        return "⚠️ Passif : financer via revenus d'actifs ; si Fonds d'urgence < 100%, reporter."

def avis_ramsey(row) -> str:
    if row["Actif_Passif"] == "Passif" and (baby_step < 3):
        return "⛔ Reporter (Baby Steps 1-3 : sécurité d'abord)."
    if str(row.get("Categorie","")).lower() in ["scolarité","santé"]:
        return "✅ Priorité vitale (OK même en Baby Steps 1-2)."
    if (ef_coverage < 1.0):
        return "🟠 Attendre couverture EF à 100%."
    return "✅ Autoriser avec budget mensuel fixe."

def avis_orman(row) -> str:
    cat = str(row.get("Categorie","")).lower()
    if cat in ["scolarité","santé","administratif"]:
        return "✅ Personnes d'abord : à financer avant biens matériels."
    if row["Actif_Passif"] == "Passif":
        return "🟠 Passif : ne pas entamer EF ; vérifier 50/30/20."
    return "✅ Si contribue à la sécurité/indépendance, feu vert."

projects_df["Avis_Kiyosaki"] = projects_df.apply(avis_kiyosaki, axis=1)
projects_df["Avis_Ramsey"]   = projects_df.apply(avis_ramsey, axis=1)
projects_df["Avis_Orman"]    = projects_df.apply(avis_orman, axis=1)

st.dataframe(projects_df[["Projet","Categorie","Type","Priorite","Budget_prevu","Budget_cotise","Avancement","Actif_Passif","Avis_Kiyosaki","Avis_Ramsey","Avis_Orman","Tags"]],
             use_container_width=True)

st.subheader("🎯 Faisabilité des projets (Budget côtisé / Budget prévu)")
if not projects_df.empty:
    fdf = projects_df[["Projet","Budget_prevu","Budget_cotise","Avancement"]].copy()
    fdf["%"] = (fdf["Avancement"]*100).round(1)
    fig4 = px.bar(fdf, x="Projet", y="Avancement", text="%")
    fig4.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("Aucun projet à afficher.")

st.subheader("📦 Import / Export")
colx, coly = st.columns(2)
with colx:
    st.download_button("Télécharger projets (CSV)", data=projects_df.to_csv(index=False).encode("utf-8"), file_name="projets_export.csv", mime="text/csv")
with coly:
    st.download_button("Télécharger transactions (CSV)", data=tx_df.to_csv(index=False).encode("utf-8"), file_name="transactions_export.csv", mime="text/csv")

st.caption("⚠️ Avertissement : outil pédagogique. Pas un conseil financier personnalisé.")
