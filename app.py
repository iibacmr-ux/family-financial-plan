# Plan Financier Stratégique Familial - Application Streamlit
# Alix & William - Vers l'Indépendance Financière 2030

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json

# Configuration de la page
st.set_page_config(
    page_title="Plan Financier Stratégique Familial - Alix & William",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour l'interface
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .warning-card {
        background: linear-gradient(90deg, #ff9800 0%, #f57c00 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        color: white;
    }
    .danger-card {
        background: linear-gradient(90deg, #f44336 0%, #d32f2f 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        color: white;
    }
    .mindset-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        color: white;
        border-left: 5px solid #fff;
    }
    .mentor-advice {
        border-left: 4px solid #2196F3;
        padding: 15px;
        margin: 10px 0;
        background: #f8f9fa;
        border-radius: 0 10px 10px 0;
    }
    .phase-indicator {
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 18px;
        margin: 20px 0;
    }
    .stabilisation { background: #ffebee; color: #c62828; }
    .transition { background: #fff3e0; color: #f57c00; }
    .expansion { background: #e8f5e8; color: #2e7d32; }
    .baby-step {
        display: flex;
        align-items: center;
        padding: 10px;
        margin: 5px 0;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
    }
    .completed { background: #e8f5e8; border-left-color: #4CAF50; }
    .current { background: #fff3e0; border-left-color: #ff9800; }
    .pending { background: #f5f5f5; border-left-color: #9e9e9e; }
</style>
""", unsafe_allow_html=True)

# Initialisation des données de session
if 'projects' not in st.session_state:
    st.session_state.projects = [
        {
            'nom': 'Titre foncier Mejeuh',
            'montant': 2815000,
            'type': 'Actif générateur',
            'statut': 'En cours',
            'roi_attendu': 12,
            'cash_flow_mensuel': 0,
            'categorie': 'Immobilier',
            'priorite': 'Haute',
            'echeance': '2025-06-30',
            'vocabulaire_kiyosaki': 'Acquisition d\'actif immobilier générant revenus passifs'
        },
        {
            'nom': 'Voyage enfants Suisse',
            'montant': 8189592,
            'type': 'Passif',
            'statut': 'Planifié',
            'roi_attendu': 0,
            'cash_flow_mensuel': -680000,
            'categorie': 'Famille',
            'priorite': 'Moyenne',
            'echeance': '2025-08-15',
            'vocabulaire_kiyosaki': 'Passif familial - Investissement capital social familial'
        },
        {
            'nom': 'Scolarité enfants',
            'montant': 6500000,
            'type': 'Investissement formation',
            'statut': 'En cours',
            'roi_attendu': 25,
            'cash_flow_mensuel': -542000,
            'categorie': 'Éducation',
            'priorite': 'Critique',
            'echeance': '2025-12-31',
            'vocabulaire_kiyosaki': 'Investissement capital humain - Actif intellectuel long terme'
        },
        {
            'nom': 'Projet IIBA',
            'montant': 2786480,
            'type': 'Actif générateur',
            'statut': 'Développement',
            'roi_attendu': 18,
            'cash_flow_mensuel': 232000,
            'categorie': 'Business',
            'priorite': 'Haute',
            'echeance': '2025-12-31',
            'vocabulaire_kiyosaki': 'Système générateur revenus passifs - Quadrant B vers I'
        }
    ]

if 'kpis' not in st.session_state:
    st.session_state.kpis = {
        'cash_flow_mensuel': -2200000,
        'ratio_actifs_passifs': 11.3,
        'regle_50_30_20': {'besoins': 75, 'envies': 45, 'epargne': 5},
        'fonds_urgence_mois': 0,
        'revenus_passifs_pct': 18,
        'phase_actuelle': 'Stabilisation',
        'baby_step_actuel': 1,
        'revenus_mensuels': 1082000,
        'depenses_mensuelles': 3282000,
        'nombre_actifs': 2,
        'objectif_independance': 30,
        'quadrant_william': 'E',
        'quadrant_alix': 'S',
        'progression_william': 25,
        'progression_alix': 40
    }

if 'vision_2030' not in st.session_state:
    st.session_state.vision_2030 = {
        'objectif_principal': 'Toute la famille en Suisse avec indépendance financière',
        'milestones': {
            '2025': 'Stabilisation finances + finalisation actifs Cameroun',
            '2026': 'Transition - développement revenus passifs',
            '2027': 'Expansion - multiplication actifs générateurs',
            '2028': 'Préparation déménagement famille',
            '2029': 'Installation progressive en Suisse',
            '2030': 'Indépendance financière complète'
        },
        'projets_enfants': {
            'uriel': {'age_2030': 19, 'projet': 'Université Suisse - Budget 200k CHF/an'},
            'naelle': {'age_2030': 12, 'projet': 'Collège international - Budget 50k CHF/an'},
            'nell_henri': {'age_2030': 10, 'projet': 'École primaire Suisse - Budget 30k CHF/an'}
        }
    }

# Fonctions utilitaires
def calculer_kpis():
    """Calcule les KPIs en temps réel basés sur les projets"""
    projects = st.session_state.projects
    
    total_actifs = sum(p['montant'] for p in projects if p['type'] == 'Actif générateur')
    total_passifs = sum(p['montant'] for p in projects if p['type'] == 'Passif')
    total_formation = sum(p['montant'] for p in projects if p['type'] == 'Investissement formation')
    cash_flow_total = sum(p['cash_flow_mensuel'] for p in projects)
    
    # Mise à jour des KPIs
    st.session_state.kpis['cash_flow_mensuel'] = cash_flow_total
    if (total_actifs + total_passifs) > 0:
        st.session_state.kpis['ratio_actifs_passifs'] = (total_actifs / (total_actifs + total_passifs)) * 100
    st.session_state.kpis['nombre_actifs'] = len([p for p in projects if p['type'] == 'Actif générateur'])
    
    # Calcul revenus passifs
    revenus_passifs = sum(p['cash_flow_mensuel'] for p in projects if p['cash_flow_mensuel'] > 0)
    if st.session_state.kpis['revenus_mensuels'] > 0:
        st.session_state.kpis['revenus_passifs_pct'] = (revenus_passifs / st.session_state.kpis['revenus_mensuels']) * 100
    
    # Détermination de la phase
    if cash_flow_total < 0 and st.session_state.kpis['ratio_actifs_passifs'] < 20:
        st.session_state.kpis['phase_actuelle'] = 'Stabilisation'
    elif cash_flow_total >= 0 and st.session_state.kpis['ratio_actifs_passifs'] < 40:
        st.session_state.kpis['phase_actuelle'] = 'Transition'
    else:
        st.session_state.kpis['phase_actuelle'] = 'Expansion'

def get_mentor_advice(project_type, montant, nom_projet):
    """Retourne les conseils des 3 mentors selon le type de projet"""
    advice = {
        'kiyosaki': '',
        'buffett': '',
        'ramsey': ''
    }
    
    if project_type == 'Actif générateur':
        advice['kiyosaki'] = f"✅ **Robert Kiyosaki**: Excellent choix! '{nom_projet}' est un véritable actif qui met de l'argent dans votre poche. Concentrez-vous sur l'augmentation de votre colonne d'actifs. Vocabulaire correct: 'Acquisition d'actif générateur' au lieu de 'investissement'."
        advice['buffett'] = f"🤔 **Warren Buffett**: Comprenez-vous parfaitement ce business? Pouvez-vous expliquer comment '{nom_projet}' génèrera de la valeur dans 10 ans? Avez-vous un avantage concurrentiel durable?"
        advice['ramsey'] = f"💰 **Dave Ramsey**: Payez-vous comptant ou créez-vous de la dette pour '{nom_projet}'? Respectez vos baby steps: emergency fund d'abord, puis investissements."
    
    elif project_type == 'Passif':
        advice['kiyosaki'] = f"⚠️ **Robert Kiyosaki**: '{nom_projet}' est un passif qui sort {montant:,.0f} FCFA de votre poche. Pouvez-vous le transformer en actif ou le réduire? Évitez d'acheter des passifs déguisés en actifs."
        advice['buffett'] = f"🎯 **Warren Buffett**: Le coût d'opportunité de '{nom_projet}' ({montant:,.0f} FCFA) vaut-il le bénéfice familial? Ces {montant:,.0f} FCFA investis à 8% annuel vaudraient {montant*1.47:,.0f} FCFA dans 5 ans."
        advice['ramsey'] = f"🚨 **Dave Ramsey**: '{nom_projet}' est-il un BESOIN ou une ENVIE? À {montant:,.0f} FCFA, vérifiez que ça respecte votre budget 50/30/20. Pas de dépenses 'envies' avant emergency fund complet."
    
    else:  # Investissement formation
        advice['kiyosaki'] = f"📚 **Robert Kiyosaki**: '{nom_projet}' est le meilleur investissement! Vous développez votre capital humain. L'éducation est un actif que personne ne peut vous retirer. ROI estimé: 25%/an."
        advice['buffett'] = f"🎓 **Warren Buffett**: '{nom_projet}' a un ROI excellent sur 20+ ans. L'éducation crée un avantage concurrentiel permanent. Investissement dans la 'zone de compétence' future des enfants."
        advice['ramsey'] = f"👨‍👩‍👧‍👦 **Dave Ramsey**: L'éducation des enfants est prioritaire absolue, mais dans les limites du budget. {montant:,.0f} FCFA/an doit rester dans les 50% 'besoins' de votre budget."
    
    return advice

def get_baby_step_status():
    """Détermine le Baby Step actuel selon Dave Ramsey"""
    kpis = st.session_state.kpis
    
    if kpis['fonds_urgence_mois'] < 1:
        return 1, "Créer fonds d'urgence de 1 mois (1M FCFA)"
    elif kpis['cash_flow_mensuel'] < 0:
        return 2, "Éliminer toutes les dettes (sauf immobilier)"
    elif kpis['fonds_urgence_mois'] < 6:
        return 3, "Fonds d'urgence complet 3-6 mois"
    elif kpis['revenus_passifs_pct'] < 15:
        return 4, "Investir 15% revenus pour retraite"
    elif 'scolarite' not in [p['nom'].lower() for p in st.session_state.projects]:
        return 5, "Épargne éducation enfants"
    elif kpis['phase_actuelle'] != 'Expansion':
        return 6, "Rembourser hypothèque anticipé"
    else:
        return 7, "Construire richesse et donner"

def get_phase_recommendations():
    """Recommandations spécifiques selon la phase actuelle"""
    phase = st.session_state.kpis['phase_actuelle']
    
    if phase == 'Stabilisation':
        return {
            'actions': [
                "Créer fonds d'urgence 3 mois (3.3M FCFA)",
                "Appliquer règle 50/30/20 strictement",
                "Finaliser titre foncier → premier cash flow positif",
                "Réduire voyage Suisse de 50% (économie 4M FCFA)"
            ],
            'objectifs': [
                "Cash flow mensuel > -1M FCFA",
                "Ratio actifs/passifs > 20%",
                "Fonds urgence > 2 mois"
            ],
            'duree': "6-12 mois"
        }
    elif phase == 'Transition':
        return {
            'actions': [
                "Développer IIBA pour 500k FCFA/mois passifs",
                "William: lancer side-business (200k/mois)",
                "Optimiser fiscalité Suisse-Cameroun",
                "Acquérir 2ème actif immobilier"
            ],
            'objectifs': [
                "Cash flow mensuel > 0 FCFA",
                "Ratio actifs/passifs > 40%",
                "Revenus passifs > 20%"
            ],
            'duree': "12-18 mois"
        }
    else:  # Expansion
        return {
            'actions': [
                "Multiplier actifs générateurs",
                "Diversifier: actions, crypto, business",
                "Préparer migration famille vers Suisse",
                "Formation avancée investissements"
            ],
            'objectifs': [
                "Revenus passifs > 50%",
                "Indépendance financière partielle",
                "Préparation vision 2030"
            ],
            'duree': "18+ mois"
        }

# Interface principale
def main():
    # Calcul KPIs
    calculer_kpis()
    
    # Sidebar navigation
    st.sidebar.title("🏠 Navigation Familiale")
    
    # Mindset reminders dans la sidebar
    st.sidebar.markdown("""
    <div class="mindset-box">
        <h3>💡 Changement Mindset</h3>
        <p><strong>William:</strong><br>
        ❌ "Je dois travailler plus pour financer"<br>
        ✅ "Comment développer des revenus qui travaillent sans moi?"</p>
        
        <p><strong>Alix:</strong><br>
        ❌ "Comment gérer tous ces projets dans le budget?"<br>
        ✅ "Quels actifs vais-je acquérir ce trimestre?"</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu navigation
    page = st.sidebar.selectbox("Choisir une page", [
        "📊 Dashboard Principal",
        "💼 Gestion Projets", 
        "🎯 Conseils 3 Mentors",
        "📈 KPIs & Analytics",
        "🚀 Progression Familiale",
        "👨‍👩‍👧‍👦 Éducation Enfants",
        "🔮 Vision 2030"
    ])
    
    # Affichage des pages
    if page == "📊 Dashboard Principal":
        show_dashboard()
    elif page == "💼 Gestion Projets":
        show_project_management()
    elif page == "🎯 Conseils 3 Mentors":
        show_mentor_advice()
    elif page == "📈 KPIs & Analytics":
        show_analytics()
    elif page == "🚀 Progression Familiale":
        show_progression()
    elif page == "👨‍👩‍👧‍👦 Éducation Enfants":
        show_children_education()
    elif page == "🔮 Vision 2030":
        show_vision_2030()

def show_dashboard():
    st.title("📊 Dashboard Financier Familial")
    st.markdown("**Vision:** Indépendance financière et migration en Suisse d'ici 2030")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    kpis = st.session_state.kpis
    
    with col1:
        cash_flow = kpis['cash_flow_mensuel']
        color = "normal" if cash_flow >= 0 else "inverse"
        st.metric(
            "Cash Flow Mensuel", 
            f"{cash_flow:,.0f} FCFA", 
            delta=f"Objectif: +500k FCFA",
            delta_color=color
        )
    
    with col2:
        ratio = kpis['ratio_actifs_passifs']
        st.metric(
            "Ratio Actifs/Passifs", 
            f"{ratio:.1f}%", 
            delta="Objectif: >40%",
            delta_color="normal" if ratio > 20 else "inverse"
        )
    
    with col3:
        passifs_pct = kpis['revenus_passifs_pct']
        st.metric(
            "Revenus Passifs", 
            f"{passifs_pct:.1f}%", 
            delta="Objectif: 30%",
            delta_color="normal" if passifs_pct > 15 else "inverse"
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
    phase_class = phase.lower()
    
    st.markdown(f"""
    <div class="phase-indicator {phase_class}">
        🎯 PHASE ACTUELLE: {phase.upper()}
    </div>
    """, unsafe_allow_html=True)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique Cash Flow
        months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
        cash_flows = [-2200000, -1800000, -1400000, -1000000, -600000, -200000, 200000, 600000, 1000000, 1400000, 1800000, 2200000]
        
        fig = px.line(
            x=months, y=cash_flows,
            title="Projection Cash Flow 2025",
            labels={'x': 'Mois', 'y': 'Cash Flow (FCFA)'}
        )
        fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Seuil Équilibre")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Répartition Actifs/Passifs
        projects = st.session_state.projects
        actifs = sum(p['montant'] for p in projects if p['type'] == 'Actif générateur')
        passifs = sum(p['montant'] for p in projects if p['type'] == 'Passif')
        formation = sum(p['montant'] for p in projects if p['type'] == 'Investissement formation')
        
        fig = px.pie(
            values=[actifs, passifs, formation],
            names=['Actifs Générateurs', 'Passifs', 'Formation'],
            title="Répartition Investissements",
            color_discrete_sequence=['#4CAF50', '#f44336', '#2196F3']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Règle 50/30/20
    st.subheader("📋 Règle 50/30/20 - Dave Ramsey")
    
    col1, col2, col3 = st.columns(3)
    
    besoins = kpis['regle_50_30_20']['besoins']
    envies = kpis['regle_50_30_20']['envies'] 
    epargne = kpis['regle_50_30_20']['epargne']
    
    with col1:
        st.metric("Besoins (50%)", f"{besoins}%", delta=f"{50-besoins:+.0f}%" if besoins != 50 else None)
        st.progress(min(besoins/50, 1.0))
    
    with col2:
        st.metric("Envies (30%)", f"{envies}%", delta=f"{30-envies:+.0f}%" if envies != 30 else None)
        st.progress(min(envies/30, 1.0))
    
    with col3:
        st.metric("Épargne (20%)", f"{epargne}%", delta=f"{20-epargne:+.0f}%" if epargne != 20 else None)
        st.progress(min(epargne/20, 1.0))

def show_project_management():
    st.title("💼 Gestion Intelligente des Projets")
    
    # Formulaire d'ajout de projet
    with st.expander("➕ Ajouter un Nouveau Projet"):
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
                    "Pas démarré", "En cours", "Terminé", "En pause", "Annulé"
                ])
                priorite = st.selectbox("Priorité", ["Critique", "Haute", "Moyenne", "Basse"])
                roi_attendu = st.number_input("ROI attendu (%)", min_value=0.0, max_value=100.0, step=0.5)
                cash_flow = st.number_input("Cash Flow mensuel (FCFA)", step=1000)
                echeance = st.date_input("Échéance")
            
            if st.form_submit_button("Ajouter le Projet"):
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
                    'vocabulaire_kiyosaki': vocabulaire_kiyosaki[type_projet]
                }
                
                st.session_state.projects.append(nouveau_projet)
                st.success(f"Projet '{nom}' ajouté avec succès!")
                st.experimental_rerun()
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtre_type = st.multiselect("Filtrer par type", 
            ["Actif générateur", "Passif", "Investissement formation"],
            default=["Actif générateur", "Passif", "Investissement formation"]
        )
    
    with col2:
        filtre_statut = st.multiselect("Filtrer par statut",
            ["Pas démarré", "En cours", "Terminé", "En pause"],
            default=["Pas démarré", "En cours"]
        )
    
    with col3:
        filtre_priorite = st.multiselect("Filtrer par priorité",
            ["Critique", "Haute", "Moyenne", "Basse"],
            default=["Critique", "Haute", "Moyenne", "Basse"]
        )
    
    # Affichage des projets filtrés
    projects_filtered = [
        p for p in st.session_state.projects 
        if p['type'] in filtre_type 
        and p['statut'] in filtre_statut 
        and p['priorite'] in filtre_priorite
    ]
    
    st.subheader(f"📋 Projets Familiaux ({len(projects_filtered)} projets)")
    
    for i, project in enumerate(projects_filtered):
        # Couleur selon le type
        if project['type'] == 'Actif générateur':
            couleur = "metric-card"
        elif project['type'] == 'Passif':
            couleur = "danger-card"
        else:
            couleur = "warning-card"
        
        with st.container():
            st.markdown(f"""
            <div class="{couleur}">
                <h4>🎯 {project['nom']}</h4>
                <p><strong>Montant:</strong> {project['montant']:,.0f} FCFA | 
                <strong>Cash Flow:</strong> {project['cash_flow_mensuel']:,.0f} FCFA/mois | 
                <strong>ROI:</strong> {project['roi_attendu']}%</p>
                <p><strong>Vocabulaire Kiyosaki:</strong> {project['vocabulaire_kiyosaki']}</p>
                <p><strong>Statut:</strong> {project['statut']} | 
                <strong>Priorité:</strong> {project['priorite']} | 
                <strong>Échéance:</strong> {project['echeance']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Conseils des mentors pour ce projet
            if st.button(f"📝 Conseils Mentors", key=f"advice_{i}"):
                advice = get_mentor_advice(project['type'], project['montant'], project['nom'])
                
                st.markdown(f"""
                <div class="mentor-advice">
                    {advice['kiyosaki']}
                </div>
                <div class="mentor-advice">
                    {advice['buffett']}
                </div>
                <div class="mentor-advice">
                    {advice['ramsey']}
                </div>
                """, unsafe_allow_html=True)

def show_mentor_advice():
    st.title("🎯 Conseil des 3 Mentors Financiers")
    
    # Sélection d'un projet pour conseil spécifique
    project_names = [p['nom'] for p in st.session_state.projects]
    selected_project = st.selectbox("Choisir un projet pour conseil détaillé", project_names)
    
    if selected_project:
        project = next(p for p in st.session_state.projects if p['nom'] == selected_project)
        
        st.subheader(f"Conseil pour: {project['nom']}")
        
        advice = get_mentor_advice(project['type'], project['montant'], project['nom'])
        
        # Robert Kiyosaki
        st.markdown("""
        ### 🏢 Robert Kiyosaki - "Père Riche, Père Pauvre"
        **Focus: Quadrants du Cash Flow (E-S-B-I)**
        """)
        st.info(advice['kiyosaki'])
        
        # Warren Buffett  
        st.markdown("""
        ### 💎 Warren Buffett - "L'Oracle d'Omaha"
        **Focus: Valeur Long Terme & Compréhension**
        """)
        st.info(advice['buffett'])
        
        # Dave Ramsey
        st.markdown("""
        ### 💪 Dave Ramsey - "Total Money Makeover"
        **Focus: Discipline & Baby Steps**
        """)
        st.info(advice['ramsey'])
        
        # Synthèse consensus
        st.markdown("""
        ### 🤝 Synthèse Consensus des 3 Mentors
        """)
        
        if project['type'] == 'Actif générateur':
            st.success("""
            ✅ **ACCORD UNANIME**: Ce projet est excellent pour votre indépendance financière.
            - **Kiyosaki**: Développe vos revenus passifs
            - **Buffett**: Investissement long terme compréhensible  
            - **Ramsey**: Si financé sans dette excessive
            
            **Action recommandée**: Poursuivre le projet en respectant votre budget.
            """)
        
        elif project['type'] == 'Passif':
            st.warning("""
            ⚠️ **ATTENTION REQUISE**: Les 3 mentors recommandent la prudence.
            - **Kiyosaki**: Questionner si c'est vraiment nécessaire
            - **Buffett**: Analyser le coût d'opportunité
            - **Ramsey**: Vérifier que c'est dans votre budget 50/30/20
            
            **Action recommandée**: Réduire ou reporter si possible.
            """)
        
        else:  # Formation
            st.info("""
            📚 **INVESTISSEMENT APPROUVÉ**: Tous soutiennent l'éducation.
            - **Kiyosaki**: Meilleur ROI pour le capital humain
            - **Buffett**: Avantage concurrentiel permanent
            - **Ramsey**: Priorité familiale dans budget équilibré
            
            **Action recommandée**: Maintenir l'investissement éducatif.
            """)

def show_analytics():
    st.title("📈 Analytics & KPIs Avancés")
    
    # Graphiques avancés
    col1, col2 = st.columns(2)
    
    with col1:
        # Évolution projetée vers indépendance financière
        years = [2025, 2026, 2027, 2028, 2029, 2030]
        independence_progress = [5, 15, 30, 50, 75, 100]
        
        fig = px.line(
            x=years, y=independence_progress,
            title="Projection Indépendance Financière",
            labels={'x': 'Année', 'y': 'Indépendance (%)'}
        )
        fig.add_hline(y=50, line_dash="dash", annotation_text="Seuil Liberté Partielle")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Quadrants familiaux
        family_members = ['William', 'Alix']
        current_quadrant = ['E', 'S'] 
        target_quadrant = ['B', 'I']
        progression = [25, 40]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=['E', 'S', 'B', 'I'], 
            y=[1, 1, 2, 2],
            mode='markers+text',
            marker=dict(size=100, color=['red', 'orange', 'lightblue', 'green']),
            text=['Employee<br>William', 'Self-Employed<br>Alix', 'Business Owner<br>Objectif Will', 'Investor<br>Objectif Alix'],
            textposition="middle center",
            name="Quadrants"
        ))
        fig.update_layout(title="Quadrants Familiaux - Position Actuelle vs Objectif")
        st.plotly_chart(fig, use_container_width=True)
    
    # Table détaillée des KPIs
    st.subheader("📊 Tableau de Bord KPIs Détaillé")
    
    kpi_data = {
        'KPI': [
            'Cash Flow Mensuel',
            'Ratio Actifs/Passifs', 
            'Revenus Passifs %',
            'Fonds d\'Urgence (mois)',
            'Nombre Actifs Générateurs',
            'Phase Progression',
            'Baby Step Dave Ramsey'
        ],
        'Valeur Actuelle': [
            f"{st.session_state.kpis['cash_flow_mensuel']:,.0f} FCFA",
            f"{st.session_state.kpis['ratio_actifs_passifs']:.1f}%",
            f"{st.session_state.kpis['revenus_passifs_pct']:.1f}%",
            f"{st.session_state.kpis['fonds_urgence_mois']} mois",
            f"{st.session_state.kpis['nombre_actifs']} actifs",
            st.session_state.kpis['phase_actuelle'],
            f"{st.session_state.kpis['baby_step_actuel']}/7"
        ],
        'Objectif 2026': [
            '+500k FCFA',
            '40%',
            '30%', 
            '6 mois',
            '5 actifs',
            'Transition',
            '4-5/7'
        ],
        'Statut': [
            '🔴' if st.session_state.kpis['cash_flow_mensuel'] < 0 else '🟢',
            '🔴' if st.session_state.kpis['ratio_actifs_passifs'] < 20 else ('🟡' if st.session_state.kpis['ratio_actifs_passifs'] < 40 else '🟢'),
            '🔴' if st.session_state.kpis['revenus_passifs_pct'] < 15 else ('🟡' if st.session_state.kpis['revenus_passifs_pct'] < 30 else '🟢'),
            '🔴' if st.session_state.kpis['fonds_urgence_mois'] < 3 else '🟢',
            '🔴' if st.session_state.kpis['nombre_actifs'] < 3 else '🟢',
            '🔴' if st.session_state.kpis['phase_actuelle'] == 'Stabilisation' else ('🟡' if st.session_state.kpis['phase_actuelle'] == 'Transition' else '🟢'),
            '🔴' if st.session_state.kpis['baby_step_actuel'] < 3 else ('🟡' if st.session_state.kpis['baby_step_actuel'] < 5 else '🟢')
        ]
    }
    
    df_kpis = pd.DataFrame(kpi_data)
    st.dataframe(df_kpis, use_container_width=True)

def show_progression():
    st.title("🚀 Progression Familiale vers l'Indépendance")
    
    # Baby Steps Dave Ramsey
    st.subheader("👶 Baby Steps Dave Ramsey - Progression")
    
    baby_steps = [
        "Fonds d'urgence starter 1 000$ (665k FCFA)",
        "Éliminer toutes dettes (sauf immobilier)",  
        "Fonds d'urgence complet 3-6 mois",
        "Investir 15% revenus pour retraite",
        "Épargne université enfants",
        "Rembourser hypothèque anticipé",
        "Construire richesse et donner"
    ]
    
    current_step = st.session_state.kpis['baby_step_actuel']
    
    for i, step in enumerate(baby_steps, 1):
        if i < current_step:
            status = "completed"
            icon = "✅"
        elif i == current_step:
            status = "current"  
            icon = "🔄"
        else:
            status = "pending"
            icon = "⏳"
            
        st.markdown(f"""
        <div class="baby-step {status}">
            <h4>{icon} Étape {i}: {step}</h4>
        </div>
        """, unsafe_allow_html=True)
    
    # Progression phases
    st.subheader("📈 Phases vers l'Indépendance Financière")
    
    phases_info = get_phase_recommendations()
    current_phase = st.session_state.kpis['phase_actuelle']
    
    col1, col2, col3 = st.columns(3)
    
    phases = [
        ('Stabilisation', 'stabilisation', col1),
        ('Transition', 'transition', col2), 
        ('Expansion', 'expansion', col3)
    ]
    
    for phase_name, phase_class, col in phases:
        with col:
            is_current = (current_phase == phase_name)
            border = "border: 3px solid #2196F3;" if is_current else ""
            
            st.markdown(f"""
            <div class="phase-indicator {phase_class}" style="{border}">
                {'🎯 PHASE ACTUELLE' if is_current else phase_name.upper()}
            </div>
            """, unsafe_allow_html=True)
            
            if is_current:
                st.markdown("**Actions prioritaires:**")
                for action in phases_info['actions']:
                    st.write(f"• {action}")
                
                st.markdown("**Objectifs:**")
                for objectif in phases_info['objectifs']:
                    st.write(f"• {objectif}")
                
                st.info(f"**Durée estimée:** {phases_info['duree']}")

def show_children_education():
    st.title("👨‍👩‍👧‍👦 Éducation Financière des Enfants")
    
    enfants = [
        {
            'nom': 'Uriel',
            'age': 14,
            'niveau': 'Adolescent - Concepts avancés',
            'concepts': [
                'Différence Actifs vs Passifs avec exemples concrets',
                'Simulation jeu Cashflow de Kiyosaki adapté',
                'Compréhension quadrants familiaux et choix orientation',
                'Première approche investissements (épargne, actions)',
                'Budget personnel et gestion argent de poche'
            ],
            'objectifs_2025': [
                'Créer son premier "actif" (vente créations artistiques)',
                'Comprendre le business model de ses parents',
                'Participer aux décisions financières familiales simples'
            ]
        },
        {
            'nom': 'Naelle', 
            'age': 7,
            'niveau': 'Enfant - Concepts fondamentaux',
            'concepts': [
                'Distinction épargne vs dépense avec exemples visuels',
                'Notion "argent qui travaille" (ex: tirelire qui grossit)',
                'Identifier les "actifs" dans son environnement',
                'Valeur de l\'effort pour gagner de l\'argent',
                'Premiers choix: acheter maintenant ou attendre'
            ],
            'objectifs_2025': [
                'Avoir sa tirelire et comprendre pourquoi épargner',
                'Faire ses premiers "investissements" (livres, matériel scolaire)',
                'Aider aux décisions d\'achat familiales simples'
            ]
        },
        {
            'nom': 'Nell-Henri',
            'age': 5,  
            'niveau': 'Petit enfant - Concepts très simples',
            'concepts': [
                'Valeur de l\'argent avec jeux éducatifs simples',
                'Concept "garder vs dépenser" avec exemples visuels',
                'Première approche "sous qui rapportent des sous"',
                'Distinguer besoins vs envies avec objets familiers',
                'Notion d\'échange et de valeur'
            ],
            'objectifs_2025': [
                'Comprendre qu\'il faut travailler pour avoir de l\'argent',
                'Savoir compter et reconnaître la monnaie',
                'Premiers choix simples d\'épargne'
            ]
        }
    ]
    
    for enfant in enfants:
        st.subheader(f"🧒 {enfant['nom']} ({enfant['age']} ans)")
        st.write(f"**Niveau:** {enfant['niveau']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎓 Concepts à enseigner:**")
            for concept in enfant['concepts']:
                st.write(f"• {concept}")
        
        with col2:
            st.markdown("**🎯 Objectifs 2025:**")
            for objectif in enfant['objectifs_2025']:
                st.write(f"• {objectif}")
        
        # Activités recommandées
        st.markdown("**🎮 Activités recommandées:**")
        
        if enfant['nom'] == 'Uriel':
            st.info("""
            - Jeu de société Cashflow for Kids de Kiyosaki
            - Simulation investissement avec argent virtuel
            - Création d'un petit business (art, tutorat)
            - Participation aux discussions financières familiales
            - Lecture: "Père Riche Père Pauvre pour les jeunes"
            """)
        
        elif enfant['nom'] == 'Naelle':
            st.info("""
            - Jeux de comptage et reconnaissance monnaie
            - Tirelire transparente pour voir l'argent grandir  
            - Sorties shopping éducatives (comparer prix)
            - Histoires et livres sur l'argent pour enfants
            - Récompenses pour épargne et bons choix
            """)
        
        else:  # Nell-Henri
            st.info("""
            - Jeux de rôle "magasin" et "banque"
            - Comptines et chansons sur l'argent
            - Images et dessins pour expliquer épargne
            - Récompenses visuelles pour attendre/épargner
            - Participation aux courses (porter, choisir)
            """)
        
        st.markdown("---")
    
    # Planning éducation familiale
    st.subheader("📅 Planning Éducation Financière Familiale 2025")
    
    planning = {
        'Janvier': 'Lancement tirelires individuelles + objectifs épargne',
        'Février': 'Première leçon Actifs vs Passifs avec objets maison', 
        'Mars': 'Jeu famille: "Construire notre empire financier"',
        'Avril': 'Visite banque + explication comptes épargne',
        'Mai': 'Uriel: Premier business plan (exposition art)',
        'Juin': 'Bilan mi-année + récompenses progression',
        'Juillet': 'Vacances: jeux financiers éducatifs',
        'Août': 'Préparation rentrée: budget fournitures scolaires',
        'Septembre': 'Révision concepts + nouveaux objectifs',
        'Octobre': 'Participation enfants aux décisions famille',
        'Novembre': 'Préparation budget cadeaux Noël',
        'Décembre': 'Bilan annuel + célébration réussites'
    }
    
    for mois, activite in planning.items():
        st.write(f"**{mois}:** {activite}")

def show_vision_2030():
    st.title("🔮 Vision Familiale 2030")
    st.subheader("🇨🇭 Objectif: Toute la famille en Suisse avec indépendance financière")
    
    # Timeline 2025-2030
    st.markdown("### 📅 Roadmap Stratégique 2025-2030")
    
    milestones = st.session_state.vision_2030['milestones']
    
    for year, milestone in milestones.items():
        progress = ((int(year) - 2025) / 5) * 100
        
        if year == '2025':
            color = "🔴"
            status = "EN COURS"
        elif year in ['2026', '2027']:
            color = "🟡"
            status = "PLANIFIÉ"
        else:
            color = "🟢"
            status = "OBJECTIF"
            
        st.markdown(f"""
        <div style="padding: 15px; margin: 10px 0; border-left: 4px solid #2196F3; background: #f8f9fa; border-radius: 0 10px 10px 0;">
            <h4>{color} {year} - {status}</h4>
            <p>{milestone}</p>
            <div style="background: #e0e0e0; border-radius: 10px; height: 20px;">
                <div style="background: linear-gradient(90deg, #4CAF50, #45a049); width: {progress}%; height: 100%; border-radius: 10px; transition: width 0.3s;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Projets enfants spécifiques 2030
    st.markdown("### 👨‍👩‍👧‍👦 Projets Enfants - Situation 2030")
    
    projets_enfants = st.session_state.vision_2030['projets_enfants']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🎓 Uriel (19 ans)")
        st.write(f"**Âge en 2030:** {projets_enfants['uriel']['age_2030']} ans")
        st.write(f"**Situation:** {projets_enfants['uriel']['projet']}")
        st.info("""
        **Préparation requise:**
        - Dossier université suisse (2027-2028)
        - Maîtrise français/allemand
        - Portfolio artistique international
        - Budget: 200k CHF/an (133M FCFA/an)
        """)
    
    with col2:
        st.markdown("#### 📚 Naelle (12 ans)")  
        st.write(f"**Âge en 2030:** {projets_enfants['naelle']['age_2030']} ans")
        st.write(f"**Situation:** {projets_enfants['naelle']['projet']}")
        st.info("""
        **Préparation requise:**
        - Intégration système scolaire suisse (2028)
        - Apprentissage allemand précoce
        - Adaptation sociale et culturelle
        - Budget: 50k CHF/an (33M FCFA/an)
        """)
    
    with col3:
        st.markdown("#### 🏫 Nell-Henri (10 ans)")
        st.write(f"**Âge en 2030:** {projets_enfants['nell_henri']['age_2030']} ans")
        st.write(f"**Situation:** {projets_enfants['nell_henri']['projet']}")  
        st.info("""
        **Préparation requise:**
        - Intégration école primaire suisse (2029)
        - Bilinguisme français-allemand
        - Adaptation plus facile (plus jeune)
        - Budget: 30k CHF/an (20M FCFA/an)
        """)
    
    # Calculs financiers 2030
    st.markdown("### 💰 Exigences Financières 2030")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Coûts Annuels Suisse (2030)")
        
        cout_enfants_2030 = 200000 + 50000 + 30000  # CHF
        cout_famille_2030 = 150000  # CHF logement + vie
        cout_total_chf = cout_enfants_2030 + cout_famille_2030
        cout_total_fcfa = cout_total_chf * 665  # Taux approximatif
        
        st.metric("Éducation enfants", f"{cout_enfants_2030:,} CHF/an")
        st.metric("Vie familiale", f"{cout_famille_2030:,} CHF/an") 
        st.metric("TOTAL REQUIS", f"{cout_total_chf:,} CHF/an")
        st.metric("Équivalent FCFA", f"{cout_total_fcfa:,.0f} FCFA/an")
    
    with col2:
        st.markdown("#### 🎯 Revenus Passifs Requis")
        
        revenus_passifs_requis = cout_total_fcfa * 1.3  # Marge sécurité 30%
        revenus_passifs_mensuels = revenus_passifs_requis / 12
        
        st.metric("Revenus passifs requis", f"{revenus_passifs_requis:,.0f} FCFA/an")
        st.metric("Soit par mois", f"{revenus_passifs_mensuels:,.0f} FCFA/mois")
        
        # Comparaison avec situation actuelle
        revenus_actuels = st.session_state.kpis['revenus_mensuels'] * st.session_state.kpis['revenus_passifs_pct'] / 100
        gap = revenus_passifs_mensuels - revenus_actuels
        
        st.metric("Gap à combler", f"{gap:,.0f} FCFA/mois", delta=f"Actuels: {revenus_actuels:,.0f}")
    
    # Plan d'action 2025-2030
    st.markdown("### 🚀 Plan d'Action Stratégique")
    
    plan_action = {
        '2025-2026': [
            'Finaliser tous actifs immobiliers Cameroun',
            'Développer IIBA → 1M FCFA/mois revenus passifs',  
            'William: créer side-business → 500k FCFA/mois',
            'Constituer fonds migration 50M FCFA'
        ],
        '2026-2027': [
            'Multiplier actifs: 2ème immeuble + diversification',
            'Optimiser fiscalité internationale',
            'Préparation administrative migration',
            'Objectif: 3M FCFA/mois revenus passifs'
        ],
        '2027-2028': [
            'Vente sélective actifs Cameroun',
            'Acquisition actifs Suisse/Europe',
            'Dossiers université Uriel',
            'Objectif: 5M FCFA/mois revenus passifs'
        ],
        '2028-2029': [
            'Migration progressive famille',
            'Installation infrastructure Suisse', 
            'Uriel → Université suisse',
            'Objectif: 8M FCFA/mois revenus passifs'
        ],
        '2029-2030': [
            'Indépendance financière complète',
            'Famille stabilisée en Suisse',
            'Objectif: 12M+ FCFA/mois revenus passifs',
            'Début transmission patrimoine enfants'
        ]
    }
    
    for periode, actions in plan_action.items():
        st.markdown(f"#### 📅 {periode}")
        for action in actions:
            st.write(f"• {action}")
    
    # Indicateurs de succès
    st.markdown("### 📈 Indicateurs de Succès Vision 2030")
    
    success_metrics = {
        'Financier': [
            '12M+ FCFA/mois revenus passifs',
            'Patrimoine net 2+ milliards FCFA', 
            'Indépendance financière complète',
            'Fonds éducation enfants sécurisé'
        ],
        'Familial': [
            'Famille unie et stabilisée en Suisse',
            'Enfants intégrés système éducatif',
            'Maîtrise langues locales',
            'Réseau social et professionnel établi'
        ],
        'Éducatif': [
            'Uriel: diplôme universitaire suisse',
            'Naelle: excellence scolaire adaptée',
            'Nell-Henri: intégration réussie',
            'Tous: éducation financière solide'
        ],
        'Personnel': [
            'William: transition E→B réussie',
            'Alix: expertise investissements',
            'Santé familiale optimale', 
            'Épanouissement personnel de tous'
        ]
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        for category, metrics in list(success_metrics.items())[:2]:
            st.markdown(f"#### {category}")
            for metric in metrics:
                st.write(f"✅ {metric}")
    
    with col2:
        for category, metrics in list(success_metrics.items())[2:]:
            st.markdown(f"#### {category}")
            for metric in metrics:
                st.write(f"✅ {metric}")

# Lancement de l'application
if __name__ == "__main__":
    main()
