import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import json
import io
import xlsxwriter

# Configuration de la page
st.set_page_config(
    page_title="Plan Financier Familial 3",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================================
# CSS CUSTOM
def load_css():
    st.markdown("""
    <style>
        /* Add your CSS styles here */
        .metric-card {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .project-card {
            background: #f8f9fa;
            border-left: 4px solid;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .project-card.actif {
            border-color: #28a745;
            background-color: #d4edda;
        }
        .project-card.passif {
            border-color: #dc3545;
            background-color: #f8d7da;
        }
        .project-card.formation {
            border-color: #ffc107;
            background-color: #fff3cd;
        }
    </style>
    """, unsafe_allow_html=True)
# ======================================================================
# INITIALIZATION & DATA

def initialize_session_state():
    if 'projets' not in st.session_state:
        st.session_state.projets = [
            {
                'id': 'PRJ001',
                'nom': 'Titre foncier Mejeuh',
                'type': 'Actif générateur',
                'montant_total': 2815000,
                'budget_alloue_mensuel': 200000,
                'montant_utilise': 50000,
                'cash_flow_mensuel': 0,
                'statut': 'En cours',
                'echeance': date(2025, 6, 30),
                'roi_attendu': 12,
                'priorite': 'Haute',
                'description': 'Acquisition terrain pour location future',
                'source_financement': 'REV001',
                'responsable': 'Alix',
                'date_creation': datetime(2025, 1, 15),
                'date_modification': datetime(2025, 2, 10),
                'suivi_mensuel': [
                    {'mois': '2025-01', 'prevu': 200000, 'reel': 50000}
                ]
            },
            {
                'id': 'PRJ002',
                'nom': 'Voyage enfants Suisse',
                'type': 'Passif',
                'montant_total': 8189592,
                'budget_alloue_mensuel': 680000,
                'montant_utilise': 0,
                'cash_flow_mensuel': -680000,
                'statut': 'Planifié',
                'echeance': date(2025, 8, 15),
                'roi_attendu': 0,
                'priorite': 'Moyenne',
                'description': 'Voyage familial cohésion',
                'source_financement': 'REV001',
                'responsable': 'William',
                'date_creation': datetime(2025, 1, 20),
                'date_modification': datetime(2025, 1, 20),
                'suivi_mensuel': []
            }
            # You can add more default projects here.
        ]

    if 'revenus' not in st.session_state:
        st.session_state.revenus = [
            {
                'id': 'REV001',
                'nom': 'Salaire William',
                'type': 'Salaire',
                'montant': 800000,
                'mois': 1,
                'annee': 2025,
                'responsable': 'William',
                'date_creation': datetime(2024, 12, 1),
                'date_modification': datetime(2025, 1, 1),
            },
            {
                'id': 'REV002',
                'nom': 'Revenus IIBA',
                'type': 'Business',
                'montant': 232000,
                'mois': 1,
                'annee': 2025,
                'responsable': 'William',
                'date_creation': datetime(2025, 1, 15),
                'date_modification': datetime(2025, 2, 1),
            }
            # More revenues can be added.
        ]

    if 'admin_config' not in st.session_state:
        st.session_state.admin_config = {
            'kpis': {
                'objective_cash_flow': 500000,
                'objective_ratio_actifs': 40,
                'objective_revenus_passifs': 30,
                'objective_fonds_urgence_mois': 6,
            },
            'listes': {
                'types_projets': ['Actif générateur', 'Passif', 'Formation'],
                'statuts_projets': ['Planifié', 'En cours', 'Terminé'],
                'priorites': ['Critique', 'Haute', 'Normale'],
                'types_revenus': ['Salaire', 'Business', 'Investissement', 'Autre'],
                'responsables': ['Alix', 'William', 'Famille'],
            },
            'mentors': {
                'Kiyosaki': {...},
                'Buffett': {...},
                'Ramsey': {...},
            }
        }
# Utilitaires et fonctions de base

def safe_get(dct, key, default='N/A'):
    """Récupère une clé dans un dict sans erreur."""
    return dct.get(key, default)

def format_currency(amount):
    """Formate un montant en FCFA."""
    return f"{amount:,.0f} FCFA".replace(',', ' ')

def get_sources_financement():
    """Retourne la liste des sources financement sous forme ID - nom."""
    sources = []
    for r in st.session_state.revenus:
        sources.append(f"{r['id']} - {r['nom']}")
    return sources if sources else ['Épargne', 'Crédit']

def filter_data_by_period(data_list, year_field='annee', month_field='mois'):
    """Filtre une liste de dict selon les filtres globaux année et mois."""
    filtered = []
    for item in data_list:
        item_year = item.get(year_field, None)
        item_month = item.get(month_field, None)
        year_ok = (st.session_state.filter_year == "Tout" or item_year == st.session_state.filter_year)
        month_ok = (st.session_state.filter_month == "Tout" or item_month == st.session_state.filter_month)
        if year_ok and month_ok:
            filtered.append(item)
    return filtered
# Calcul des KPIs

def calculer_kpis():
    projets = filter_data_by_period(st.session_state.projets, year_field='date_creation_year', month_field='date_creation_month')
    revenus = filter_data_by_period(st.session_state.revenus, 'annee', 'mois')

    total_revenus = sum(r['montant'] for r in revenus)
    total_cashflow = sum(p['cash_flow_mensuel'] for p in projets)
    
    total_actifs = sum(p['montant_total'] for p in projets if p['type'] == 'Actif générateur')
    total_passifs = sum(p['montant_total'] for p in projets if p['type'] == 'Passif')
    total_formation = sum(p['montant_total'] for p in projets if p['type'] == 'Formation')
    total_investissements = total_actifs + total_passifs + total_formation
    
    ratio_actifs = (total_actifs / total_investissements * 100) if total_investissements > 0 else 0

    revenus_passifs = sum(p['cash_flow_mensuel'] for p in projets if p['type'] == 'Actif générateur' and p['cash_flow_mensuel'] > 0)
    pct_revenus_passifs = (revenus_passifs / total_revenus * 100) if total_revenus > 0 else 0

    nombre_actifs = len([p for p in projets if p['type'] == 'Actif générateur'])

    # Détermination phase financière
    if total_cashflow < 0 or pct_revenus_passifs < 10:
        phase = "Stabilisation"
        baby_step = 1
    elif total_cashflow >= 0 and 10 <= pct_revenus_passifs < 30:
        phase = "Transition"
        baby_step = 3
    else:
        phase = "Expansion"
        baby_step = 5

    # Fonds d'urgence estimation (exemple)
    depenses = sum(-p['cash_flow_mensuel'] for p in projets if p['cash_flow_mensuel'] < 0)
    fonds_urgence_mois = total_actifs / depenses if depenses else 0

    # Positionnement Quadrant Kiyosaki (simplifié)
    salaire = sum(r['montant'] for r in revenus if r['type'] == 'Salaire')
    business = sum(r['montant'] for r in revenus if r['type'] == 'Business')
    investissement = sum(r['montant'] for r in revenus if r['type'] == 'Investissement')

    total_income = salaire + business + investissement
    if total_income == 0:
        quadrant = "E"
        commentaire = "Dépendant du salaire (Rat Race)"
    else:
        pct_salaire = salaire / total_income * 100
        pct_business = business / total_income * 100
        pct_investissement = investissement / total_income * 100
        if pct_salaire > 70:
            quadrant = "E"
            commentaire = "Principalement salarié (Rat Race)"
        elif pct_business > 50:
            quadrant = "S"
            commentaire = "Propriétaire de business"
        elif pct_investissement > 40:
            quadrant = "I"
            commentaire = "Investisseur indépendant"
        else:
            quadrant = "B"
            commentaire = "Diversification activité et investissements"

    return {
        'total_revenus': total_revenus,
        'total_cashflow': total_cashflow,
        'total_actifs': total_actifs,
        'total_passifs': total_passifs,
        'total_formation': total_formation,
        'ratio_actifs': ratio_actifs,
        'pct_revenus_passifs': pct_revenus_passifs,
        'nombre_actifs': nombre_actifs,
        'phase': phase,
        'baby_step': baby_step,
        'fonds_urgence_mois': fonds_urgence_mois,
        'quadrant': quadrant,
        'commentaire_quadrant': commentaire,
    }
# Fonction pour afficher les projets sous forme de tableau passifs vs actifs avec quadrant

def afficher_passifs_actifs_quadrant():
    projets = st.session_state.projets
    total_actifs = sum(p['montant_total'] for p in projets if p['type'] == 'Actif générateur')
    total_passifs = sum(p['montant_total'] for p in projets if p['type'] == 'Passif')
    total_formation = sum(p['montant_total'] for p in projets if p['type'] == 'Formation')
    total = total_actifs + total_passifs + total_formation

    pct_actifs = (total_actifs / total * 100) if total > 0 else 0
    pct_passifs = (total_passifs / total * 100) if total > 0 else 0
    pct_formation = (total_formation / total * 100) if total > 0 else 0

    st.markdown("### Répartition Actifs / Passifs / Formation")
    df = pd.DataFrame({
        'Type': ['Actifs Générateurs', 'Passifs', 'Formation'],
        'Montant Total': [total_actifs, total_passifs, total_formation],
        'Pourcentage': [pct_actifs, pct_passifs, pct_formation]
    })

    st.dataframe(df.style.format({"Montant Total": "{:,.0f} FCFA", "Pourcentage": "{:.1f}%"}), use_container_width=True)

    # Position dans quadrant E-S-B-I (simplifié)
    kpis = calculer_kpis()
    st.markdown(f"### Position personnelle dans le quadrant Kiyosaki : **{kpis['quadrant']}**")
    st.info(kpis['commentaire_quadrant'])
# Texte dynamique explicatif dans progression familiale

def afficher_texte_progression():
    kpis = calculer_kpis()
    phase = kpis['phase']
    baby_step = kpis['baby_step']
    fonds_urgence = kpis['fonds_urgence_mois']

    st.markdown("### Analyse Synthétique de la Progression Familiale")

    texte = f"Vous êtes actuellement en phase : **{phase}**.\n\n"
    if phase == "Stabilisation":
        texte += "Votre cash flow est négatif ou vos revenus passifs sont faibles. Il est crucial d'améliorer vos revenus passifs.\n"
    elif phase == "Transition":
        texte += "Votre cash flow est positif et vous développez vos revenus passifs. Continuez sur cette voie.\n"
    else:
        texte += "Félicitations, vous êtes en phase d’expansion avec des revenus passifs importants.\n"

    # Tendance couleur selon baby_step
    couleur = "🟢"
    if baby_step < 3:
        couleur = "🔴"
    elif baby_step < 5:
        couleur = "🟡"

    texte += f"\n**Progression Baby Step:** {baby_step}/7 {couleur}\n"
    texte += f"Votre fonds d'urgence couvre environ {fonds_urgence:.1f} mois de dépenses.\n"

    objectif_urgence = st.session_state.admin_config['kpis']['objective_fonds_urgence_mois']
    if fonds_urgence < objectif_urgence:
        texte += f"Il est conseillé d’atteindre un fonds d’urgence de {objectif_urgence} mois pour sécuriser votre situation.\n"
    else:
        texte += "Votre fonds d’urgence est suffisant pour couvrir vos besoins.\n"

    st.markdown(texte)
# Formulaire de gestion des projets (ajout, modification, suppression)
def form_projet(projet=None):
    is_new = projet is None
    if is_new:
        projet = {
            'id': '',
            'nom': '',
            'type': '',
            'montant_total': 0,
            'budget_alloue_mensuel': 0,
            'montant_utilise': 0,
            'cash_flow_mensuel': 0,
            'statut': '',
            'echeance': date.today(),
            'roi_attendu': 0,
            'priorite': '',
            'description': '',
            'source_financement': '',
            'responsable': '',
            'date_creation': datetime.now(),
            'date_modification': datetime.now(),
            'suivi_mensuel': []
        }
    
    st.text_input("ID du Projet (non modifiable)" if not is_new else "ID du Projet (généré automatiquement)", value=projet['id'], disabled=not is_new, key="id_projet")
    projet['nom'] = st.text_input("Nom du Projet", value=projet['nom'], key="nom_projet")
    projet['type'] = st.selectbox("Type de Projet", st.session_state.admin_config['listes']['types_projets'], index=st.session_state.admin_config['listes']['types_projets'].index(projet['type']) if projet['type'] in st.session_state.admin_config['listes']['types_projets'] else 0, key="type_projet")
    projet['montant_total'] = st.number_input("Budget Total (FCFA)", value=projet['montant_total'], min_value=0, step=10000, key="montant_total")
    projet['budget_alloue_mensuel'] = st.number_input("Budget Alloué Mensuel (FCFA)", value=projet['budget_alloue_mensuel'], min_value=0, step=10000, key="budget_mensuel")
    projet['montant_utilise'] = st.number_input("Montant Utilisé Réel (FCFA)", value=projet['montant_utilise'], min_value=0, step=10000, key="montant_utilise")
    projet['cash_flow_mensuel'] = st.number_input("Cash Flow Mensuel (FCFA)", value=projet['cash_flow_mensuel'], key="cashflow")
    projet['statut'] = st.selectbox("Statut", st.session_state.admin_config['listes']['statuts_projets'], index=st.session_state.admin_config['listes']['statuts_projets'].index(projet['statut']) if projet['statut'] in st.session_state.admin_config['listes']['statuts_projets'] else 0, key="statut")
    projet['echeance'] = st.date_input("Échéance", value=projet['echeance'], key="echeance")
    projet['roi_attendu'] = st.number_input("ROI Attendu (%)", value=projet['roi_attendu'], min_value=0, max_value=100, step=0.1, key="roi")
    projet['priorite'] = st.selectbox("Priorité", st.session_state.admin_config['listes']['priorites'], index=st.session_state.admin_config['listes']['priorites'].index(projet['priorite']) if projet['priorite'] in st.session_state.admin_config['listes']['priorites'] else 0, key="priorite")
    source_financement_choices = get_sources_financement()
    selected_source = projet['source_financement'] if projet['source_financement'] in source_financement_choices else None
    projet['source_financement'] = st.selectbox("Source de Financement (ID - Nom)", options=source_financement_choices, index=source_financement_choices.index(selected_source) if selected_source else 0, key="source_financement")
    projet['responsable'] = st.selectbox("Responsable", st.session_state.admin_config['listes']['responsables'], index=st.session_state.admin_config['listes']['responsables'].index(projet['responsable']) if projet['responsable'] in st.session_state.admin_config['listes']['responsables'] else 0, key="responsable")
    projet['description'] = st.text_area("Description", value=projet['description'], key="desc")

    if st.button("Sauvegarder Projet"):
        # Validation
        errors = []
        if not projet['nom']:
            errors.append("Le nom du projet est obligatoire.")
        if projet['montant_total'] <= 0:
            errors.append("Le budget total doit être supérieur à 0.")
        if not projet['source_financement']:
            errors.append("La source de financement doit être choisie.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            # Création ou modification
            if is_new:
                projet['id'] = f"PRJ{len(st.session_state.projets)+1:03d}"
                projet['date_creation'] = datetime.now()
                st.session_state.projets.append(projet)
                st.success(f"Projet '{projet['nom']}' ajouté avec succès.")
            else:
                index = next((i for i, p in enumerate(st.session_state.projets) if p['id'] == projet['id']), None)
                if index is not None:
                    projet['date_modification'] = datetime.now()
                    st.session_state.projets[index] = projet
                    st.success(f"Projet '{projet['nom']}' modifié avec succès.")
            st.experimental_rerun()
# Formulaire gestion revenus (avec mois/année obligatoire, sans régulier)

def form_revenu(revenu=None):
    is_new = revenu is None
    if is_new:
        revenu = {
            'id': '',
            'nom': '',
            'type': '',
            'montant': 0,
            'mois': 1,
            'annee': date.today().year,
            'responsable': '',
            'date_creation': datetime.now(),
            'date_modification': datetime.now(),
        }

    st.text_input("ID du Revenu (non modifiable)" if not is_new else "ID du Revenu (généré automatiquement)", value=revenu['id'], disabled=not is_new, key="id_revenu")
    revenu['nom'] = st.text_input("Nom du Revenu", value=revenu['nom'], key="nom_revenu")
    revenu['type'] = st.selectbox("Type de Revenu", st.session_state.admin_config['listes']['types_revenus'], index=st.session_state.admin_config['listes']['types_revenus'].index(revenu['type']) if revenu['type'] in st.session_state.admin_config['listes']['types_revenus'] else 0, key="type_revenu")
    revenu['montant'] = st.number_input("Montant (FCFA)", value=revenu['montant'], min_value=0, step=10000, key="montant_revenu")
    revenu['annee'] = st.number_input("Année", value=revenu['annee'], min_value=2020, max_value=2100, step=1, key="annee_revenu")
    revenu['mois'] = st.selectbox("Mois", list(range(1,13)), index=revenu['mois']-1 if 1 <= revenu['mois'] <=12 else 0, key="mois_revenu")
    revenu['responsable'] = st.selectbox("Responsable", st.session_state.admin_config['listes']['responsables'], index=st.session_state.admin_config['listes']['responsables'].index(revenu['responsable']) if revenu['responsable'] in st.session_state.admin_config['listes']['responsables'] else 0, key="responsable_revenu")

    if st.button("Sauvegarder Revenu"):
        errors = []
        if not revenu['nom']:
            errors.append("Le nom du revenu est obligatoire.")
        if revenu['montant'] <= 0:
            errors.append("Le montant doit être supérieur à 0.")
        if revenu['annee'] < 2020 or revenu['annee'] > 2100:
            errors.append("Année invalide.")
        if not revenu['mois'] or revenu['mois'] <1 or revenu['mois']>12:
            errors.append("Mois invalide.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            if is_new:
                revenu['id'] = f"REV{len(st.session_state.revenus)+1:03d}"
                revenu['date_creation'] = datetime.now()
                st.session_state.revenus.append(revenu)
                st.success(f"Revenu '{revenu['nom']}' ajouté avec succès.")
            else:
                index = next((i for i, r in enumerate(st.session_state.revenus) if r['id'] == revenu['id']), None)
                if index is not None:
                    revenu['date_modification'] = datetime.now()
                    st.session_state.revenus[index] = revenu
                    st.success(f"Revenu '{revenu['nom']}' modifié avec succès.")
            st.experimental_rerun()
# Page principale d'affichage des KPIs, Dashboard, et navigation

def afficher_dashboard():
    st.title("📊 Dashboard Principal")
    kpis = calculer_kpis()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Cash Flow Mensuel", format_currency(kpis['total_cashflow']), delta="Objectif: " + format_currency(st.session_state.admin_config['kpis']['objective_cash_flow']))
    col2.metric("⚖️ Ratio Actifs / Total", f"{kpis['ratio_actifs']:.1f}%", delta=f"Objectif: >{st.session_state.admin_config['kpis']['objective_ratio_actifs']}%")
    col3.metric("📈 Revenus Passifs %", f"{kpis['pct_revenus_passifs']:.1f}%", delta=f"Objectif: {st.session_state.admin_config['kpis']['objective_revenus_passifs']}%")
    col4.metric("🎯 Phase Financière", kpis['phase'], delta=f"Baby Step {kpis['baby_step']}/7")

    st.markdown("---")
    afficher_passifs_actifs_quadrant()

    st.markdown("---")
    afficher_texte_progression()
# Fonction principale

def main():
    load_css()
    initialize_session_state()

    # Filtres Globaux
    with st.sidebar:
        st.header("Filtres")
        filtre_annee = st.selectbox("Année", options=["Tout"] + [2024, 2025, 2026, 2027, 2028], index=0)
        filtre_mois = st.selectbox("Mois", options=["Tout"] + list(range(1,13)), index=0)
        st.session_state.filter_year = filtre_annee if filtre_annee != "Tout" else "Tout"
        st.session_state.filter_month = filtre_mois if filtre_mois != "Tout" else "Tout"

        st.markdown("---")
        page = st.radio("Navigation", ["Dashboard", "Gestion Projets", "Gestion Revenus"])
        
    if page == "Dashboard":
        afficher_dashboard()
    elif page == "Gestion Projets":
        st.header("Gestion des Projets")
        projet_selectionne = st.selectbox("Sélectionner un projet", options=["Nouveau"] + [p['nom'] for p in st.session_state.projets])
        if projet_selectionne == "Nouveau":
            form_projet()
        else:
            projet = next((p for p in st.session_state.projets if p['nom'] == projet_selectionne), None)
            if projet:
                form_projet(projet)
    elif page == "Gestion Revenus":
        st.header("Gestion des Revenus")
        revenu_selectionne = st.selectbox("Sélectionner un revenu", options=["Nouveau"] + [r['nom'] for r in st.session_state.revenus])
        if revenu_selectionne == "Nouveau":
            form_revenu()
        else:
            revenu = next((r for r in st.session_state.revenus if r['nom'] == revenu_selectionne), None)
            if revenu:
                form_revenu(revenu)

if __name__ == "__main__":
    main()
