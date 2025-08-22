# Plan Financier Stratégique Familial - Version Streamlit
# Conversion de l'application HTML/CSS/JS vers Python Streamlit
# Famille Alix & William - Vers l'Indépendance Financière 2030

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import base64

# Configuration de la page
st.set_page_config(
    page_title="Plan Financier Familial - Alix & William",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé reprenant le design system original
def load_css():
    st.markdown("""
    <style>
    /* Import du design system original */
    :root {
        --color-primary: rgba(33, 128, 141, 1);
        --color-primary-hover: rgba(29, 116, 128, 1);
        --color-surface: rgba(255, 255, 253, 1);
        --color-background: rgba(252, 252, 249, 1);
        --color-text: rgba(19, 52, 59, 1);
        --color-text-secondary: rgba(98, 108, 113, 1);
        --color-success: rgba(33, 128, 141, 1);
        --color-error: rgba(192, 21, 47, 1);
        --color-warning: rgba(168, 75, 47, 1);
        --color-border: rgba(94, 82, 64, 0.2);
        --font-family-base: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
        --radius-lg: 12px;
        --space-16: 16px;
        --space-24: 24px;
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.04);
    }

    /* Streamlit customizations */
    .main > div {
        padding-top: 2rem;
    }
    
    .stApp {
        background-color: var(--color-background);
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--color-surface);
        border-right: 1px solid var(--color-border);
    }

    /* Mindset box styling */
    .mindset-box {
        background: linear-gradient(135deg, rgba(33, 128, 141, 0.1) 0%, rgba(50, 184, 198, 0.1) 100%);
        border: 1px solid var(--color-primary);
        border-radius: var(--radius-lg);
        padding: var(--space-16);
        margin: var(--space-16) 0;
        color: var(--color-text);
    }

    .mindset-box h3 {
        color: var(--color-primary);
        font-size: 14px;
        margin-bottom: var(--space-16);
        font-weight: 600;
    }

    .mindset-reminder {
        margin-bottom: 12px;
        font-size: 11px;
    }

    .mindset-reminder strong {
        color: var(--color-primary);
        font-weight: 500;
    }

    .mindset-reminder p {
        color: var(--color-text-secondary);
        margin: 4px 0 0 0;
        font-style: italic;
        line-height: 1.4;
    }

    /* KPI Cards */
    .kpi-card {
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: var(--space-16);
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
        margin: 10px 0;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .kpi-value {
        font-size: 24px;
        font-weight: 700;
        color: var(--color-text);
        margin-bottom: 8px;
    }

    .kpi-negative .kpi-value {
        color: var(--color-error);
    }

    .kpi-positive .kpi-value {
        color: var(--color-success);
    }

    .kpi-warning .kpi-value {
        color: var(--color-warning);
    }

    /* Phase indicators */
    .phase-stabilisation {
        background-color: rgba(192, 21, 47, 0.1);
        color: var(--color-error);
        border: 1px solid rgba(192, 21, 47, 0.25);
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 500;
        font-size: 12px;
        text-align: center;
    }

    .phase-transition {
        background-color: rgba(168, 75, 47, 0.1);
        color: var(--color-warning);
        border: 1px solid rgba(168, 75, 47, 0.25);
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 500;
        font-size: 12px;
        text-align: center;
    }

    .phase-expansion {
        background-color: rgba(33, 128, 141, 0.1);
        color: var(--color-success);
        border: 1px solid rgba(33, 128, 141, 0.25);
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 500;
        font-size: 12px;
        text-align: center;
    }

    /* Project cards */
    .project-card {
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: var(--space-16);
        margin: 10px 0;
        box-shadow: var(--shadow-sm);
    }

    .project-type-actif {
        background-color: rgba(33, 128, 141, 0.1);
        color: var(--color-success);
        border: 1px solid rgba(33, 128, 141, 0.25);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        display: inline-block;
    }

    .project-type-passif {
        background-color: rgba(192, 21, 47, 0.1);
        color: var(--color-error);
        border: 1px solid rgba(192, 21, 47, 0.25);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        display: inline-block;
    }

    .project-type-formation {
        background-color: rgba(98, 108, 113, 0.1);
        color: var(--color-text-secondary);
        border: 1px solid rgba(98, 108, 113, 0.25);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        display: inline-block;
    }

    /* Mentor advice */
    .mentor-card {
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: var(--space-24);
        margin: var(--space-16) 0;
        box-shadow: var(--shadow-sm);
    }

    .mentor-advice {
        border-left: 4px solid var(--color-primary);
        padding: 12px 16px;
        margin: 10px 0;
        background: rgba(33, 128, 141, 0.05);
        border-radius: 0 8px 8px 0;
        font-size: 14px;
        line-height: 1.5;
    }

    /* Status badges */
    .status-termine {
        background-color: rgba(33, 128, 141, 0.1);
        color: var(--color-success);
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 500;
    }

    .status-en-cours {
        background-color: rgba(168, 75, 47, 0.1);
        color: var(--color-warning);
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 500;
    }

    .status-pas-demarre {
        background-color: rgba(98, 108, 113, 0.1);
        color: var(--color-text-secondary);
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 500;
    }

    /* Alert boxes */
    .alert-error {
        background-color: rgba(192, 21, 47, 0.1);
        color: var(--color-error);
        border: 1px solid rgba(192, 21, 47, 0.2);
        padding: 12px 16px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 14px;
    }

    .alert-warning {
        background-color: rgba(168, 75, 47, 0.1);
        color: var(--color-warning);
        border: 1px solid rgba(168, 75, 47, 0.2);
        padding: 12px 16px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 14px;
    }

    .alert-success {
        background-color: rgba(33, 128, 141, 0.1);
        color: var(--color-success);
        border: 1px solid rgba(33, 128, 141, 0.2);
        padding: 12px 16px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 14px;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom buttons */
    .stButton > button {
        background-color: var(--color-primary);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background-color: var(--color-primary-hover);
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialisation des données
@st.cache_data
def load_initial_data():
    return {
        "projets": [
            {
                "nom": "Titre foncier Mejeuh",
                "montant": 2815000,
                "type": "Actif générateur",
                "statut": "En cours",
                "roi_attendu": 12,
                "cash_flow_mensuel": 0,
                "categorie": "Immobilier",
                "priorite": "Haute",
                "echeance": "2025-06-30",
                "description": "Acquisition terrain pour location future",
                "vocabulaire_kiyosaki": "Acquisition d'actif immobilier générant revenus passifs"
            },
            {
                "nom": "Voyage enfants Suisse",
                "montant": 8189592,
                "type": "Passif",
                "statut": "Planifié",
                "roi_attendu": 0,
                "cash_flow_mensuel": -680000,
                "categorie": "Famille",
                "priorite": "Moyenne",
                "echeance": "2025-08-15",
                "description": "Voyage familial cohésion",
                "vocabulaire_kiyosaki": "Passif familial - Investissement capital social"
            },
            {
                "nom": "Scolarité enfants",
                "montant": 6500000,
                "type": "Investissement formation",
                "statut": "En cours",
                "roi_attendu": 25,
                "cash_flow_mensuel": -542000,
                "categorie": "Éducation",
                "priorite": "Critique",
                "echeance": "2025-12-31",
                "description": "Éducation Uriel, Naelle, Nell-Henri",
                "vocabulaire_kiyosaki": "Investissement capital humain long terme"
            },
            {
                "nom": "Projet IIBA",
                "montant": 2786480,
                "type": "Actif générateur",
                "statut": "Développement",
                "roi_attendu": 18,
                "cash_flow_mensuel": 232000,
                "categorie": "Business",
                "priorite": "Haute",
                "echeance": "2025-12-31",
                "description": "Business génération revenus passifs",
                "vocabulaire_kiyosaki": "Système générateur revenus passifs - Quadrant I"
            }
        ],
        "kpis": {
            "cash_flow_mensuel": -2200000,
            "ratio_actifs_passifs": 11.3,
            "regle_50_30_20": {"besoins": 75, "envies": 45, "epargne": 5},
            "fonds_urgence_mois": 0,
            "revenus_passifs_pct": 18,
            "phase_actuelle": "Stabilisation",
            "baby_step_actuel": 1,
            "revenus_mensuels": 1082000,
            "depenses_mensuelles": 3282000,
            "nombre_actifs": 2,
            "objectif_independance": 30
        }
    }

# Initialiser session state
if 'data' not in st.session_state:
    st.session_state.data = load_initial_data()

# Fonctions utilitaires
def calculer_kpis():
    """Calcule les KPIs en temps réel"""
    projets = st.session_state.data['projets']
    
    total_actifs = sum(p['montant'] for p in projets if p['type'] == 'Actif générateur')
    total_passifs = sum(p['montant'] for p in projets if p['type'] == 'Passif')
    total_formation = sum(p['montant'] for p in projets if p['type'] == 'Investissement formation')
    cash_flow_total = sum(p['cash_flow_mensuel'] for p in projets)
    
    # Mise à jour KPIs
    kpis = st.session_state.data['kpis']
    kpis['cash_flow_mensuel'] = cash_flow_total
    kpis['nombre_actifs'] = len([p for p in projets if p['type'] == 'Actif générateur'])
    
    if (total_actifs + total_passifs) > 0:
        kpis['ratio_actifs_passifs'] = (total_actifs / (total_actifs + total_passifs)) * 100
    
    # Détermination phase
    if cash_flow_total < 0 and kpis['ratio_actifs_passifs'] < 20:
        kpis['phase_actuelle'] = 'Stabilisation'
    elif cash_flow_total >= 0 and kpis['ratio_actifs_passifs'] < 40:
        kpis['phase_actuelle'] = 'Transition'
    else:
        kpis['phase_actuelle'] = 'Expansion'

def get_mentor_advice(project_type, montant, nom_projet):
    """Retourne les conseils des 3 mentors"""
    advice = {
        'kiyosaki': '',
        'buffett': '',
        'ramsey': ''
    }
    
    if project_type == 'Actif générateur':
        advice['kiyosaki'] = f"✅ **Robert Kiyosaki**: Excellent! '{nom_projet}' est un véritable actif qui met de l'argent dans votre poche. Concentrez-vous sur l'augmentation de votre colonne d'actifs."
        advice['buffett'] = f"🤔 **Warren Buffett**: Comprenez-vous parfaitement ce business? Pouvez-vous expliquer comment '{nom_projet}' génèrera de la valeur dans 10 ans?"
        advice['ramsey'] = f"💰 **Dave Ramsey**: Payez-vous comptant ou créez-vous de la dette pour '{nom_projet}'? Respectez vos baby steps avant d'investir massivement."
    
    elif project_type == 'Passif':
        advice['kiyosaki'] = f"⚠️ **Robert Kiyosaki**: '{nom_projet}' est un passif qui sort {montant:,.0f} FCFA de votre poche. Pouvez-vous le transformer en actif ou le réduire?"
        advice['buffett'] = f"🎯 **Warren Buffett**: Le coût d'opportunité de '{nom_projet}' ({montant:,.0f} FCFA) vaut-il le bénéfice familial à long terme?"
        advice['ramsey'] = f"🚨 **Dave Ramsey**: '{nom_projet}' est-il un BESOIN ou une ENVIE? Respecte-t-il votre budget 50/30/20?"
    
    else:  # Formation
        advice['kiyosaki'] = f"📚 **Robert Kiyosaki**: '{nom_projet}' développe votre capital humain. L'éducation est un actif que personne ne peut vous retirer."
        advice['buffett'] = f"🎓 **Warren Buffett**: L'éducation crée un avantage concurrentiel permanent. ROI excellent sur 20+ ans."
        advice['ramsey'] = f"👨‍👩‍👧‍👦 **Dave Ramsey**: L'éducation des enfants est prioritaire, mais dans les limites du budget équilibré."
    
    return advice

def format_currency(amount):
    """Formate les montants en FCFA"""
    return f"{amount:,.0f} FCFA"

def get_baby_step_status():
    """Détermine le Baby Step actuel selon Dave Ramsey"""
    kpis = st.session_state.data['kpis']
    
    if kpis['fonds_urgence_mois'] < 1:
        return 1, "Créer fonds d'urgence de 1 mois (1M FCFA)"
    elif kpis['cash_flow_mensuel'] < 0:
        return 2, "Éliminer toutes les dettes (sauf immobilier)"
    elif kpis['fonds_urgence_mois'] < 6:
        return 3, "Fonds d'urgence complet 3-6 mois"
    elif kpis['revenus_passifs_pct'] < 15:
        return 4, "Investir 15% revenus pour retraite"
    elif kpis['revenus_passifs_pct'] < 25:
        return 5, "Épargne éducation enfants"
    elif kpis['phase_actuelle'] != 'Expansion':
        return 6, "Rembourser hypothèque anticipé"
    else:
        return 7, "Construire richesse et donner"

# Chargement du CSS
load_css()

# Sidebar avec mindset reminders
def render_sidebar():
    st.sidebar.title("🏠 Navigation Familiale")
    
    # Mindset reminders
    st.sidebar.markdown("""
    <div class="mindset-box">
        <h3>💡 Changement Mindset</h3>
        <div class="mindset-reminder">
            <strong>William:</strong>
            <p>❌ "Je dois travailler plus pour financer"<br>
            ✅ "Comment développer des revenus qui travaillent sans moi?"</p>
        </div>
        
        <div class="mindset-reminder">
            <strong>Alix:</strong>
            <p>❌ "Comment gérer tous ces projets dans le budget?"<br>
            ✅ "Quels actifs vais-je acquérir ce trimestre?"</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu
    pages = {
        "📊 Dashboard Principal": "dashboard",
        "💼 Gestion Projets": "projects", 
        "🎯 Conseils 3 Mentors": "mentors",
        "📈 KPIs & Analytics": "analytics",
        "🚀 Progression Familiale": "progression",
        "👨‍👩‍👧‍👦 Éducation Enfants": "education",
        "🔮 Vision 2030": "vision"
    }
    
    return st.sidebar.selectbox("Choisir une page", list(pages.keys()))

# Pages de l'application
def show_dashboard():
    st.title("📊 Dashboard Financier Familial")
    st.markdown("**Vision:** Indépendance financière et migration en Suisse d'ici 2030")
    
    # Calculer les KPIs
    calculer_kpis()
    kpis = st.session_state.data['kpis']
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cash_flow = kpis['cash_flow_mensuel']
        delta_color = "normal" if cash_flow >= 0 else "inverse"
        st.metric(
            "Cash Flow Mensuel", 
            format_currency(cash_flow), 
            delta="Objectif: +500k FCFA",
            delta_color=delta_color
        )
    
    with col2:
        ratio = kpis['ratio_actifs_passifs']
        st.metric(
            "Ratio Actifs/Passifs", 
            f"{ratio:.1f}%", 
            delta="Objectif: >40%"
        )
    
    with col3:
        passifs_pct = kpis['revenus_passifs_pct']
        st.metric(
            "Revenus Passifs", 
            f"{passifs_pct:.1f}%", 
            delta="Objectif: 30%"
        )
    
    with col4:
        baby_step, description = get_baby_step_status()
        st.metric(
            "Baby Step Dave Ramsey", 
            f"Étape {baby_step}/7", 
            delta=description
        )
    
    # Phase actuelle
    phase = kpis['phase_actuelle']
    phase_class = f"phase-{phase.lower()}"
    
    st.markdown(f"""
    <div class="{phase_class}">
        🎯 PHASE ACTUELLE: {phase.upper()}
    </div>
    """, unsafe_allow_html=True)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        # Cash flow projection
        months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
        cash_flows = [-2200000, -1800000, -1400000, -1000000, -600000, -200000, 
                     200000, 600000, 1000000, 1400000, 1800000, 2200000]
        
        fig = px.line(
            x=months, y=cash_flows,
            title="🎯 Projection Cash Flow 2025",
            labels={'x': 'Mois', 'y': 'Cash Flow (FCFA)'}
        )
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Répartition actifs/passifs
        projets = st.session_state.data['projets']
        actifs = sum(p['montant'] for p in projets if p['type'] == 'Actif générateur')
        passifs = sum(p['montant'] for p in projets if p['type'] == 'Passif')
        formation = sum(p['montant'] for p in projets if p['type'] == 'Investissement formation')
        
        fig = px.pie(
            values=[actifs, passifs, formation],
            names=['Actifs Générateurs', 'Passifs', 'Formation'],
            title="🏦 Répartition Investissements",
            color_discrete_sequence=['#1FB8CD', '#B4413C', '#626C71']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Règle 50/30/20
    st.subheader("📋 Règle 50/30/20 - Dave Ramsey")
    
    col1, col2, col3 = st.columns(3)
    
    besoins = kpis['regle_50_30_20']['besoins']
    envies = kpis['regle_50_30_20']['envies']
    epargne = kpis['regle_50_30_20']['epargne']
    
    with col1:
        st.metric("Besoins (50%)", f"{besoins}%")
        st.progress(min(besoins/50, 1.0))
    
    with col2:
        st.metric("Envies (30%)", f"{envies}%")
        st.progress(min(envies/30, 1.0))
    
    with col3:
        st.metric("Épargne (20%)", f"{epargne}%")
        st.progress(min(epargne/20, 1.0))

def show_project_management():
    st.title("💼 Gestion Intelligente des Projets")
    
    # Formulaire d'ajout de projet
    with st.expander("➕ Ajouter un Nouveau Projet", expanded=False):
        with st.form("nouveau_projet"):
            col1, col2 = st.columns(2)
            
            with col1:
                nom = st.text_input("Nom du projet")
                montant = st.number_input("Montant (FCFA)", min_value=0, step=10000)
                type_projet = st.selectbox("Type selon Kiyosaki", [
                    "Actif générateur", "Passif", "Investissement formation"
                ])
                categorie = st.selectbox("Catégorie", [
                    "Immobilier", "Business", "Éducation", "Famille", "Santé", "Transport", "Autre"
                ])
            
            with col2:
                statut = st.selectbox("Statut", [
                    "Pas démarré", "En cours", "Terminé", "En pause"
                ])
                priorite = st.selectbox("Priorité", ["Critique", "Haute", "Moyenne", "Basse"])
                roi_attendu = st.number_input("ROI attendu (%)", min_value=0.0, max_value=100.0, step=0.5)
                cash_flow = st.number_input("Cash Flow mensuel (FCFA)", step=1000)
                echeance = st.date_input("Échéance")
            
            description = st.text_area("Description")
            
            if st.form_submit_button("Ajouter le Projet", use_container_width=True):
                vocabulaire_kiyosaki = {
                    "Actif générateur": "Système générateur revenus passifs",
                    "Passif": "Sortie de trésorerie - Évaluer transformation en actif", 
                    "Investissement formation": "Investissement capital humain long terme"
                }
                
                nouveau_projet = {
                    'nom': nom,
                    'montant': montant,
                    'type': type_projet,
                    'statut': statut,
                    'roi_attendu': roi_attendu,
                    'cash_flow_mensuel': cash_flow,
                    'categorie': categorie,
                    'priorite': priorite,
                    'echeance': echeance.strftime('%Y-%m-%d'),
                    'description': description,
                    'vocabulaire_kiyosaki': vocabulaire_kiyosaki[type_projet]
                }
                
                st.session_state.data['projets'].append(nouveau_projet)
                st.success(f"✅ Projet '{nom}' ajouté avec succès!")
                st.experimental_rerun()
    
    # Filtres
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filtre_type = st.multiselect("Filtrer par type", 
            ["Actif générateur", "Passif", "Investissement formation"],
            default=["Actif générateur", "Passif", "Investissement formation"]
        )
    
    with col2:
        filtre_statut = st.multiselect("Filtrer par statut",
            ["Pas démarré", "En cours", "Terminé", "En pause"],
            default=["Pas démarré", "En cours", "Terminé"]
        )
    
    with col3:
        filtre_priorite = st.multiselect("Filtrer par priorité",
            ["Critique", "Haute", "Moyenne", "Basse"],
            default=["Critique", "Haute", "Moyenne", "Basse"]
        )
    
    with col4:
        filtre_categorie = st.multiselect("Filtrer par catégorie",
            ["Immobilier", "Business", "Éducation", "Famille", "Santé", "Transport", "Autre"],
            default=["Immobilier", "Business", "Éducation", "Famille", "Santé", "Transport", "Autre"]
        )
    
    # Affichage des projets
    projets_filtres = [
        p for p in st.session_state.data['projets'] 
        if p['type'] in filtre_type 
        and p['statut'] in filtre_statut 
        and p['priorite'] in filtre_priorite
        and p['categorie'] in filtre_categorie
    ]
    
    st.subheader(f"📋 Projets Familiaux ({len(projets_filtres)} projets)")
    
    for i, projet in enumerate(projets_filtres):
        # Carte de projet
        type_class = projet['type'].replace(' ', '-').lower()
        statut_class = projet['statut'].replace(' ', '-').lower()
        
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"### 🎯 {projet['nom']}")
                st.markdown(f"**Description:** {projet['description']}")
                st.markdown(f"**Vocabulaire Kiyosaki:** {projet['vocabulaire_kiyosaki']}")
                
                # Métriques du projet
                subcol1, subcol2, subcol3, subcol4 = st.columns(4)
                with subcol1:
                    st.metric("Montant", format_currency(projet['montant']))
                with subcol2:
                    st.metric("Cash Flow/mois", format_currency(projet['cash_flow_mensuel']))
                with subcol3:
                    st.metric("ROI attendu", f"{projet['roi_attendu']}%")
                with subcol4:
                    st.metric("Échéance", projet['echeance'])
            
            with col2:
                # Type et statut
                type_color = "success" if projet['type'] == 'Actif générateur' else ("error" if projet['type'] == 'Passif' else "info")
                st.markdown(f"<span class='project-type-{type_class}'>{projet['type']}</span>", unsafe_allow_html=True)
                st.markdown(f"<span class='status-{statut_class}'>{projet['statut']}</span>", unsafe_allow_html=True)
                st.write(f"**Priorité:** {projet['priorite']}")
                st.write(f"**Catégorie:** {projet['categorie']}")
            
            with col3:
                # Actions CRUD
                if st.button(f"📝 Modifier", key=f"edit_{i}"):
                    st.session_state[f'editing_{i}'] = True
                
                if st.button(f"🗑️ Supprimer", key=f"delete_{i}"):
                    st.session_state.data['projets'].remove(projet)
                    st.success("Projet supprimé!")
                    st.experimental_rerun()
                
                if st.button(f"💡 Conseils", key=f"advice_{i}"):
                    st.session_state[f'show_advice_{i}'] = not st.session_state.get(f'show_advice_{i}', False)
            
            # Formulaire de modification
            if st.session_state.get(f'editing_{i}', False):
                with st.form(f"edit_form_{i}"):
                    st.subheader("Modifier le projet")
                    
                    edit_col1, edit_col2 = st.columns(2)
                    with edit_col1:
                        new_nom = st.text_input("Nom", value=projet['nom'])
                        new_montant = st.number_input("Montant", value=projet['montant'])
                        new_type = st.selectbox("Type", ["Actif générateur", "Passif", "Investissement formation"], 
                                              index=["Actif générateur", "Passif", "Investissement formation"].index(projet['type']))
                    
                    with edit_col2:
                        new_statut = st.selectbox("Statut", ["Pas démarré", "En cours", "Terminé", "En pause"],
                                                index=["Pas démarré", "En cours", "Terminé", "En pause"].index(projet['statut']))
                        new_roi = st.number_input("ROI attendu (%)", value=projet['roi_attendu'])
                        new_cash_flow = st.number_input("Cash Flow mensuel", value=projet['cash_flow_mensuel'])
                    
                    new_description = st.text_area("Description", value=projet['description'])
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.form_submit_button("💾 Sauvegarder"):
                            # Mettre à jour le projet
                            index = st.session_state.data['projets'].index(projet)
                            st.session_state.data['projets'][index].update({
                                'nom': new_nom,
                                'montant': new_montant,
                                'type': new_type,
                                'statut': new_statut,
                                'roi_attendu': new_roi,
                                'cash_flow_mensuel': new_cash_flow,
                                'description': new_description
                            })
                            st.session_state[f'editing_{i}'] = False
                            st.success("Projet modifié!")
                            st.experimental_rerun()
                    
                    with col_cancel:
                        if st.form_submit_button("❌ Annuler"):
                            st.session_state[f'editing_{i}'] = False
                            st.experimental_rerun()
            
            # Conseils des mentors
            if st.session_state.get(f'show_advice_{i}', False):
                advice = get_mentor_advice(projet['type'], projet['montant'], projet['nom'])
                
                st.markdown('<div class="mentor-advice">', unsafe_allow_html=True)
                st.markdown(advice['kiyosaki'])
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="mentor-advice">', unsafe_allow_html=True)  
                st.markdown(advice['buffett'])
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="mentor-advice">', unsafe_allow_html=True)
                st.markdown(advice['ramsey'])
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")

# Interface principale
def main():
    # Chargement CSS
    load_css()
    
    # Sidebar
    selected_page = render_sidebar()
    
    # Routing des pages
    if selected_page == "📊 Dashboard Principal":
        show_dashboard()
    elif selected_page == "💼 Gestion Projets":
        show_project_management()
    # Ajouter les autres pages ici...
    else:
        st.title("🚧 Page en construction")
        st.info("Cette fonctionnalité sera disponible dans la prochaine version.")

if __name__ == "__main__":
    main()
