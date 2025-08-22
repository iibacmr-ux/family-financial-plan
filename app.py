import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import json

# Configuration de la page
st.set_page_config(
    page_title="Plan Financier Familial",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS CUSTOM - DESIGN SYSTEM REPRODUIT
# ============================================================================

def load_css():
    st.markdown("""
    <style>
    /* Import des fontes */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Variables CSS du design system original */
    :root {
        --color-primary: rgba(33, 128, 141, 1);
        --color-primary-hover: rgba(29, 116, 128, 1);
        --color-success: rgba(33, 128, 141, 1);
        --color-error: rgba(192, 21, 47, 1);
        --color-warning: rgba(168, 75, 47, 1);
        --color-info: rgba(98, 108, 113, 1);
        --color-background: rgba(252, 252, 249, 1);
        --color-surface: rgba(255, 255, 253, 1);
        --color-text: rgba(19, 52, 59, 1);
        --color-text-secondary: rgba(98, 108, 113, 1);
        --color-border: rgba(94, 82, 64, 0.2);
    }
    
    /* Reset Streamlit */
    .main .block-container {
        padding: 2rem 1rem;
        max-width: none;
        background-color: var(--color-background);
    }
    
    /* Kanban Cards */
    .kanban-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .kanban-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .kanban-card.en-retard {
        border-left: 4px solid #ff4444;
        background: #fff5f5;
    }
    
    .kanban-card.a-risque {
        border-left: 4px solid #ff8800;
        background: #fff8f0;
    }
    
    .kanban-card.en-avance {
        border-left: 4px solid #00aa00;
        background: #f0fff0;
    }
    
    .kanban-card.bloque {
        border-left: 4px solid #666666;
        background: #f5f5f5;
    }
    
    .kanban-column {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        margin: 0 8px;
        min-height: 400px;
    }
    
    .project-progress {
        background: #e9ecef;
        border-radius: 10px;
        height: 8px;
        margin: 8px 0;
        overflow: hidden;
    }
    
    .project-progress-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DONNÉES ET LOGIQUE METIER
# ============================================================================

def initialize_session_state():
    """Initialise les données de session"""
    if 'projets' not in st.session_state:
        st.session_state.projets = [
            {
                'id': 1,
                'nom': 'Titre foncier Mejeuh',
                'type': 'Actif générateur',
                'montant_total': 2815000,
                'budget_alloue_mensuel': 200000,
                'montant_utilise_reel': 50000,
                'cash_flow_mensuel': 0,
                'statut': 'En cours',
                'echeance': date(2025, 6, 30),
                'roi_attendu': 12,
                'priorite': 'Haute',
                'description': 'Acquisition terrain pour location future',
                'source_financement': 'Salaire William',
                'suivi_mensuel': [
                    {'mois': '2025-01', 'prevu': 200000, 'reel': 50000}
                ]
            },
            {
                'id': 2,
                'nom': 'Voyage enfants Suisse',
                'type': 'Passif',
                'montant_total': 8189592,
                'budget_alloue_mensuel': 680000,
                'montant_utilise_reel': 0,
                'cash_flow_mensuel': -680000,
                'statut': 'Planifié',
                'echeance': date(2025, 8, 15),
                'roi_attendu': 0,
                'priorite': 'Moyenne',
                'description': 'Voyage familial cohésion',
                'source_financement': 'Salaire William',
                'suivi_mensuel': []
            },
            {
                'id': 3,
                'nom': 'Scolarité enfants',
                'type': 'Investissement formation',
                'montant_total': 6500000,
                'budget_alloue_mensuel': 542000,
                'montant_utilise_reel': 1084000,
                'cash_flow_mensuel': -542000,
                'statut': 'En cours',
                'echeance': date(2025, 12, 31),
                'roi_attendu': 25,
                'priorite': 'Critique',
                'description': 'Éducation Uriel, Naelle, Nell-Henri',
                'source_financement': 'Revenus IIBA',
                'suivi_mensuel': [
                    {'mois': '2025-01', 'prevu': 542000, 'reel': 542000},
                    {'mois': '2025-02', 'prevu': 542000, 'reel': 542000}
                ]
            },
            {
                'id': 4,
                'nom': 'Projet IIBA',
                'type': 'Actif générateur',
                'montant_total': 2786480,
                'budget_alloue_mensuel': 100000,
                'montant_utilise_reel': 150000,
                'cash_flow_mensuel': 232000,
                'statut': 'Développement',
                'echeance': date(2025, 3, 30),  # Date passée pour test
                'roi_attendu': 18,
                'priorite': 'Critique',
                'description': 'Business génération revenus passifs',
                'source_financement': 'Épargne',
                'suivi_mensuel': [
                    {'mois': '2025-01', 'prevu': 100000, 'reel': 75000},
                    {'mois': '2025-02', 'prevu': 100000, 'reel': 75000}
                ]
            }
        ]
    
    if 'revenus_variables' not in st.session_state:
        st.session_state.revenus_variables = [
            {
                'id': 1,
                'nom': 'Salaire William',
                'montant_mensuel': 800000,
                'type': 'Salaire',
                'regulier': True
            },
            {
                'id': 2,
                'nom': 'Revenus IIBA',
                'montant_mensuel': 232000,
                'type': 'Business',
                'regulier': False
            },
            {
                'id': 3,
                'nom': 'Épargne',
                'montant_mensuel': 50000,
                'type': 'Épargne',
                'regulier': True
            }
        ]

def calculer_kpis():
    """Calcule les KPIs en temps réel"""
    projets = st.session_state.projets
    revenus = st.session_state.revenus_variables
    
    # Revenus totaux
    revenus_mensuels = sum(r['montant_mensuel'] for r in revenus)
    
    # Cash flow mensuel total
    cash_flow_mensuel = sum(p['cash_flow_mensuel'] for p in projets)
    
    # Totaux par type
    total_actifs = sum(p['montant_total'] for p in projets if p['type'] == 'Actif générateur')
    total_passifs = sum(p['montant_total'] for p in projets if p['type'] == 'Passif')
    total_formation = sum(p['montant_total'] for p in projets if p['type'] == 'Investissement formation')
    total_global = total_actifs + total_passifs + total_formation
    
    # Ratios
    ratio_actifs_passifs = (total_actifs / total_global * 100) if total_global > 0 else 0
    
    # Revenus passifs
    revenus_passifs = sum(p['cash_flow_mensuel'] for p in projets if p['type'] == 'Actif générateur' and p['cash_flow_mensuel'] > 0)
    revenus_passifs_pct = (revenus_passifs / revenus_mensuels * 100) if revenus_mensuels > 0 else 0
    
    # Nombre d'actifs générateurs
    nombre_actifs = len([p for p in projets if p['type'] == 'Actif générateur'])
    
    # Phase financière
    if cash_flow_mensuel < 0 or revenus_passifs_pct < 10:
        phase_actuelle = 'Stabilisation'
    elif cash_flow_mensuel >= 0 and 10 <= revenus_passifs_pct < 30:
        phase_actuelle = 'Transition'  
    else:
        phase_actuelle = 'Expansion'
    
    # Fonds d'urgence (simulation)
    depenses_mensuelles = abs(sum(p['cash_flow_mensuel'] for p in projets if p['cash_flow_mensuel'] < 0))
    fonds_urgence_mois = 0  # À calculer selon épargne réelle
    
    # Baby step Dave Ramsey
    baby_step = 1
    if fonds_urgence_mois >= 1:
        baby_step = 2
    if fonds_urgence_mois >= 6:
        baby_step = 3
    
    return {
        'revenus_mensuels': revenus_mensuels,
        'cash_flow_mensuel': cash_flow_mensuel,
        'ratio_actifs_passifs': ratio_actifs_passifs,
        'revenus_passifs_pct': revenus_passifs_pct,
        'nombre_actifs': nombre_actifs,
        'phase_actuelle': phase_actuelle,
        'fonds_urgence_mois': fonds_urgence_mois,
        'baby_step_actuel': baby_step,
        'depenses_mensuelles': depenses_mensuelles
    }

def format_currency(amount):
    """Formate un montant en FCFA"""
    return f"{amount:,.0f} FCFA".replace(",", " ")

def categorize_project(projet):
    """Catégorise un projet selon son état"""
    aujourd_hui = date.today()
    echeance = projet['echeance']
    
    # Calcul progression
    progression = (projet['montant_utilise_reel'] / projet['montant_total']) * 100 if projet['montant_total'] > 0 else 0
    
    # Jours jusqu'à échéance
    jours_restants = (echeance - aujourd_hui).days
    
    # Logique de catégorisation
    if echeance < aujourd_hui:
        return 'en-retard', 'En Retard', '#ff4444'
    elif jours_restants <= 30 and progression < 70:
        return 'a-risque', 'À Risque', '#ff8800'
    elif progression > 90:
        return 'en-avance', 'En Avance', '#00aa00'
    elif projet['montant_utilise_reel'] >= projet['montant_total']:
        return 'bloque', 'Budget Épuisé', '#666666'
    else:
        return 'en-cours', 'En Cours', '#007bff'

def get_sources_financement():
    """Retourne la liste des sources de financement disponibles"""
    revenus = st.session_state.revenus_variables
    return [r['nom'] for r in revenus] + ['Épargne', 'Crédit']

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

def render_sidebar():
    """Affiche la sidebar avec navigation radio"""
    with st.sidebar:
        st.markdown("### 💰 Plan Financier Familial")
        st.markdown("*Alix & William - Vers l'Indépendance 2030*")
        
        # Navigation avec radio buttons
        pages = [
            "📊 Dashboard Principal",
            "📋 Vue Kanban Projets",
            "💼 Gestion Projets", 
            "💰 Revenus Variables",
            "🎯 Conseils 3 Mentors",
            "📈 Analytics & KPIs",
            "🚀 Progression Familiale", 
            "👨‍👩‍👧‍👦 Éducation Enfants",
            "🔮 Vision 2030"
        ]
        
        selected_page = st.radio(
            "Navigation",
            pages,
            key="nav_radio",
            label_visibility="collapsed"
        )
        
        # Phase actuelle
        kpis = calculer_kpis()
        phase = kpis['phase_actuelle']
        
        st.markdown("---")
        st.markdown(f"**🎯 Phase:** {phase}")
        st.markdown(f"**💰 Revenus:** {format_currency(kpis['revenus_mensuels'])}")
        st.markdown(f"**📊 Cash Flow:** {format_currency(kpis['cash_flow_mensuel'])}")
        
    return selected_page

# ============================================================================
# PAGES DE L'APPLICATION
# ============================================================================

def show_dashboard():
    """Page Dashboard Principal"""
    st.title("📊 Dashboard Principal")
    
    # KPIs
    kpis = calculer_kpis()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_color = "normal" if kpis['cash_flow_mensuel'] >= 0 else "inverse"
        st.metric(
            "💸 Cash Flow Mensuel", 
            format_currency(kpis['cash_flow_mensuel']), 
            delta="Objectif: +500k",
            delta_color=delta_color
        )
    
    with col2:
        st.metric(
            "⚖️ Ratio Actifs/Passifs", 
            f"{kpis['ratio_actifs_passifs']:.1f}%", 
            delta="Objectif: >40%"
        )
    
    with col3:
        st.metric(
            "💰 Revenus Passifs", 
            f"{kpis['revenus_passifs_pct']:.1f}%", 
            delta="Objectif: 30%"
        )
    
    with col4:
        st.metric(
            "🎯 Phase", 
            kpis['phase_actuelle'],
            delta=f"Baby Step {kpis['baby_step_actuel']}/7"
        )
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Évolution Cash Flow")
        
        import numpy as np
        mois = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')
        cash_flow_evolution = np.random.normal(kpis['cash_flow_mensuel'], 500000, len(mois))
        
        fig = px.line(
            x=mois, 
            y=cash_flow_evolution,
            title="Cash Flow Mensuel (FCFA)"
        )
        fig.add_hline(y=0, line_dash="dash", annotation_text="Équilibre")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Répartition Investissements")
        
        projets = st.session_state.projets
        total_actifs = sum(p['montant_total'] for p in projets if p['type'] == 'Actif générateur')
        total_passifs = sum(p['montant_total'] for p in projets if p['type'] == 'Passif')
        total_formation = sum(p['montant_total'] for p in projets if p['type'] == 'Investissement formation')
        
        if total_actifs + total_passifs + total_formation > 0:
            fig = px.pie(
                values=[total_actifs, total_passifs, total_formation],
                names=['Actifs Générateurs', 'Passifs', 'Formation'],
                color_discrete_map={
                    'Actifs Générateurs': '#1FB8CD',
                    'Passifs': '#B4413C', 
                    'Formation': '#FFC185'
                }
            )
            st.plotly_chart(fig, use_container_width=True)

def show_kanban_view():
    """Vue Kanban des projets avec catégorisation avancée"""
    st.title("📋 Vue Kanban - Gestion Visuelle des Projets")
    
    # Catégorisation des projets
    categories = {
        'en-retard': {'projets': [], 'titre': '🔴 En Retard', 'couleur': '#ff4444'},
        'a-risque': {'projets': [], 'titre': '🟡 À Risque', 'couleur': '#ff8800'},
        'en-cours': {'projets': [], 'titre': '🔵 En Cours', 'couleur': '#007bff'},
        'en-avance': {'projets': [], 'titre': '🟢 En Avance', 'couleur': '#00aa00'},
        'bloque': {'projets': [], 'titre': '⚫ Bloqué', 'couleur': '#666666'}
    }
    
    # Répartition des projets
    for projet in st.session_state.projets:
        categorie, _, _ = categorize_project(projet)
        if categorie in categories:
            categories[categorie]['projets'].append(projet)
        else:
            categories['en-cours']['projets'].append(projet)
    
    # Affichage en colonnes
    colonnes = st.columns(len(categories))
    
    for i, (cat_key, cat_data) in enumerate(categories.items()):
        with colonnes[i]:
            st.markdown(f"### {cat_data['titre']} ({len(cat_data['projets'])})")
            
            if cat_data['projets']:
                for projet in cat_data['projets']:
                    show_kanban_card(projet, cat_data['couleur'])
            else:
                st.info("Aucun projet dans cette catégorie")
    
    # Statistiques
    st.markdown("---")
    st.subheader("📊 Statistiques Projet")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_projets = len(st.session_state.projets)
    
    with col1:
        st.metric("Total Projets", total_projets)
    
    with col2:
        en_retard = len(categories['en-retard']['projets'])
        st.metric("En Retard", en_retard, delta=f"{(en_retard/total_projets*100):.0f}%" if total_projets > 0 else "0%")
    
    with col3:
        a_risque = len(categories['a-risque']['projets'])
        st.metric("À Risque", a_risque, delta=f"{(a_risque/total_projets*100):.0f}%" if total_projets > 0 else "0%")
    
    with col4:
        en_avance = len(categories['en-avance']['projets'])
        st.metric("En Avance", en_avance, delta=f"{(en_avance/total_projets*100):.0f}%" if total_projets > 0 else "0%")

def show_kanban_card(projet, couleur):
    """Affiche une carte Kanban pour un projet"""
    progression = (projet['montant_utilise_reel'] / projet['montant_total']) * 100 if projet['montant_total'] > 0 else 0
    
    # Calcul jours restants
    jours_restants = (projet['echeance'] - date.today()).days
    
    with st.container():
        # En-tête carte
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{projet['nom']}**")
        
        with col2:
            # Type badge
            type_colors = {
                'Actif générateur': '🟢',
                'Passif': '🔴',
                'Investissement formation': '🔵'
            }
            st.markdown(f"{type_colors.get(projet['type'], '⚪')} {projet['type'][:8]}...")
        
        # Infos projet
        st.markdown(f"💰 **Budget:** {format_currency(projet['montant_total'])}")
        st.markdown(f"💸 **Utilisé:** {format_currency(projet['montant_utilise_reel'])}")
        st.markdown(f"📅 **Échéance:** {projet['echeance'].strftime('%d/%m/%Y')}")
        st.markdown(f"⏰ **Jours restants:** {jours_restants}")
        
        # Barre de progression
        st.progress(progression / 100)
        st.markdown(f"📊 **Progression:** {progression:.1f}%")
        
        # Source financement
        st.markdown(f"🏦 **Financement:** {projet['source_financement']}")
        
        # Actions
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✏️ Modifier", key=f"kanban_edit_{projet['id']}"):
                st.session_state.edit_project_id = projet['id']
                st.session_state.current_page = "💼 Gestion Projets"
                st.rerun()
        
        with col2:
            if st.button("📊 Détails", key=f"kanban_details_{projet['id']}"):
                show_project_details_modal(projet)
        
        st.markdown("---")

def show_project_details_modal(projet):
    """Affiche les détails d'un projet dans un modal"""
    with st.expander(f"📊 Détails: {projet['nom']}", expanded=True):
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💰 Informations Financières")
            st.write(f"**Budget Total:** {format_currency(projet['montant_total'])}")
            st.write(f"**Budget Mensuel:** {format_currency(projet['budget_alloue_mensuel'])}")
            st.write(f"**Utilisé Réel:** {format_currency(projet['montant_utilise_reel'])}")
            st.write(f"**Cash Flow/Mois:** {format_currency(projet['cash_flow_mensuel'])}")
            st.write(f"**ROI Attendu:** {projet['roi_attendu']}%")
        
        with col2:
            st.markdown("### 📋 Informations Projet")
            st.write(f"**Statut:** {projet['statut']}")
            st.write(f"**Priorité:** {projet['priorite']}")
            st.write(f"**Échéance:** {projet['echeance'].strftime('%d/%m/%Y')}")
            st.write(f"**Source Financement:** {projet['source_financement']}")
        
        st.markdown("### 📝 Description")
        st.write(projet['description'])
        
        # Suivi mensuel
        if projet['suivi_mensuel']:
            st.markdown("### 📊 Suivi Mensuel")
            df_suivi = pd.DataFrame(projet['suivi_mensuel'])
            df_suivi['ecart'] = df_suivi['reel'] - df_suivi['prevu']
            st.dataframe(df_suivi, use_container_width=True)

def show_project_management():
    """Page Gestion Projets CRUD complète (CORRIGÉE)"""
    st.title("💼 Gestion des Projets")
    
    # Actions principales
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Nouveau Projet", type="primary"):
            st.session_state.show_add_form = True
    
    # Gestion des modals
    if st.session_state.get('show_add_form', False):
        show_add_project_form()
    
    if st.session_state.get('edit_project_id'):
        show_edit_project_form()
    
    # Filtres
    st.subheader("🔍 Filtres")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filter_type = st.selectbox(
            "Type", 
            ["Tous", "Actif générateur", "Passif", "Investissement formation"]
        )
    
    with col2:
        filter_status = st.selectbox(
            "Statut",
            ["Tous", "Planifié", "En cours", "Développement", "Réalisé", "Suspendu"]
        )
    
    with col3:
        filter_priority = st.selectbox(
            "Priorité",
            ["Toutes", "Critique", "Haute", "Moyenne", "Faible"]
        )
    
    with col4:
        sort_by = st.selectbox(
            "Trier par",
            ["Nom", "Montant", "Échéance", "ROI", "Type"]
        )
    
    # Application des filtres
    projets_filtered = filter_projects(filter_type, filter_status, filter_priority, sort_by)
    
    # Affichage des projets avec COMPOSANTS STREAMLIT NATIFS
    st.subheader(f"📋 Projets ({len(projets_filtered)})")
    
    if projets_filtered:
        for projet in projets_filtered:
            show_project_card_native(projet)
    else:
        st.info("Aucun projet ne correspond aux filtres sélectionnés.")

def show_project_card_native(projet):
    """Affiche une carte projet avec composants Streamlit natifs (CORRIGÉ)"""
    
    # Calculs
    delta_budget = projet['montant_total'] - projet['montant_utilise_reel']
    progress = (projet['montant_utilise_reel'] / projet['montant_total']) * 100 if projet['montant_total'] > 0 else 0
    
    # Container principal
    with st.container():
        # En-tête avec nom et type
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.subheader(f"🎯 {projet['nom']}")
        
        with col2:
            # Badge type
            type_colors = {
                'Actif générateur': '🟢',
                'Passif': '🔴',
                'Investissement formation': '🔵'
            }
            st.markdown(f"{type_colors.get(projet['type'], '⚪')} **{projet['type']}**")
        
        with col3:
            # Badge statut
            status_colors = {
                'Planifié': '🔵',
                'En cours': '🟡', 
                'Développement': '🟠',
                'Réalisé': '🟢',
                'Suspendu': '🔴'
            }
            st.markdown(f"{status_colors.get(projet['statut'], '⚪')} {projet['statut']}")
        
        # Métriques financières
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Budget Total", format_currency(projet['montant_total']))
        
        with col2:
            st.metric("💸 Utilisé", format_currency(projet['montant_utilise_reel']))
        
        with col3:
            st.metric("📊 Delta", format_currency(delta_budget))
        
        with col4:
            cash_flow_color = "normal" if projet['cash_flow_mensuel'] >= 0 else "inverse"
            st.metric(
                "💵 Cash Flow/Mois", 
                format_currency(projet['cash_flow_mensuel']),
                delta_color=cash_flow_color
            )
        
        # Barre de progression
        st.write(f"**Progression: {progress:.1f}%**")
        st.progress(progress / 100)
        
        # Description
        st.write(f"**Description:** {projet['description']}")
        
        # Infos supplémentaires
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"📅 **Échéance:** {projet['echeance'].strftime('%d/%m/%Y')}")
        
        with col2:
            st.write(f"📊 **ROI:** {projet['roi_attendu']}%")
        
        with col3:
            st.write(f"🏦 **Financement:** {projet['source_financement']}")
        
        # Actions
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("✏️ Modifier", key=f"edit_{projet['id']}"):
                st.session_state.edit_project_id = projet['id']
                st.rerun()
        
        with col2:
            if st.button("🗑️ Supprimer", key=f"delete_{projet['id']}"):
                if st.session_state.get(f"confirm_delete_{projet['id']}", False):
                    # Suppression confirmée
                    st.session_state.projets = [p for p in st.session_state.projets if p['id'] != projet['id']]
                    st.success(f"Projet '{projet['nom']}' supprimé.")
                    if f"confirm_delete_{projet['id']}" in st.session_state:
                        del st.session_state[f"confirm_delete_{projet['id']}"]
                    st.rerun()
                else:
                    # Demande de confirmation
                    st.session_state[f"confirm_delete_{projet['id']}"] = True
                    st.warning("Cliquez à nouveau pour confirmer la suppression.")
        
        with col3:
            if st.button("📊 Suivi", key=f"suivi_{projet['id']}"):
                st.session_state.show_suivi_id = projet['id']
        
        with col4:
            if st.button("🎯 Conseils", key=f"advice_{projet['id']}"):
                st.session_state.show_advice_id = projet['id']
    
    # Affichage conditionnel du suivi
    if st.session_state.get('show_suivi_id') == projet['id']:
        show_project_tracking(projet)
    
    # Affichage conditionnel des conseils
    if st.session_state.get('show_advice_id') == projet['id']:
        show_project_advice(projet)
        
    st.markdown("---")

def show_project_tracking(projet):
    """Affiche le suivi mensuel d'un projet"""
    with st.expander(f"📊 Suivi Mensuel: {projet['nom']}", expanded=True):
        
        if projet['suivi_mensuel']:
            df_suivi = pd.DataFrame(projet['suivi_mensuel'])
            df_suivi['écart'] = df_suivi['reel'] - df_suivi['prevu']
            df_suivi['% écart'] = (df_suivi['écart'] / df_suivi['prevu'] * 100).round(1)
            
            st.dataframe(df_suivi, use_container_width=True)
            
            # Graphique évolution
            fig = px.bar(
                df_suivi,
                x='mois',
                y=['prevu', 'reel'],
                title="Prévisionnel vs Réel",
                barmode='group'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucun suivi mensuel enregistré.")
        
        # Ajouter une entrée de suivi
        st.subheader("➕ Ajouter un Suivi")
        
        with st.form(f"suivi_form_{projet['id']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                mois = st.date_input("Mois").strftime('%Y-%m')
            
            with col2:
                montant_prevu = st.number_input("Montant Prévu (FCFA)", min_value=0, step=10000)
            
            with col3:
                montant_reel = st.number_input("Montant Réel (FCFA)", min_value=0, step=10000)
            
            if st.form_submit_button("💾 Ajouter Suivi"):
                # Trouver le projet et ajouter le suivi
                for i, p in enumerate(st.session_state.projets):
                    if p['id'] == projet['id']:
                        if 'suivi_mensuel' not in st.session_state.projets[i]:
                            st.session_state.projets[i]['suivi_mensuel'] = []
                        
                        st.session_state.projets[i]['suivi_mensuel'].append({
                            'mois': mois,
                            'prevu': montant_prevu,
                            'reel': montant_reel
                        })
                        
                        # Mettre à jour le montant utilisé réel
                        total_reel = sum(s['reel'] for s in st.session_state.projets[i]['suivi_mensuel'])
                        st.session_state.projets[i]['montant_utilise_reel'] = total_reel
                        
                        st.success("Suivi ajouté!")
                        st.rerun()

def show_project_advice(projet):
    """Affiche les conseils des 3 mentors pour un projet"""
    with st.expander(f"🎯 Conseils des 3 Mentors: {projet['nom']}", expanded=True):
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🏢 Robert Kiyosaki")
            st.markdown("*Père Riche, Père Pauvre*")
            
            if projet['type'] == 'Actif générateur':
                st.success("✅ Excellent ! Cet actif génère des revenus passifs et vous rapproche du quadrant I (Investisseur).")
            elif projet['type'] == 'Passif':
                st.warning("⚠️ Ce passif retire de l'argent de votre poche. Est-il vraiment nécessaire ?")
            else:
                st.info("📚 L'éducation est un actif qui génère des revenus futurs plus élevés.")
        
        with col2:
            st.markdown("#### 💎 Warren Buffett")
            st.markdown("*L'Oracle d'Omaha*")
            
            if projet['type'] == 'Actif générateur':
                st.success("🔍 Assurez-vous de comprendre parfaitement ce business et son potentiel long terme.")
            elif projet['type'] == 'Passif':
                st.warning("🤔 Quel est le coût d'opportunité ? Cet argent pourrait-il être mieux investi ?")
            else:
                st.info("🎯 Le meilleur investissement est en vous-même et votre famille.")
        
        with col3:
            st.markdown("#### 💪 Dave Ramsey")
            st.markdown("*Total Money Makeover*")
            
            if projet['type'] == 'Actif générateur':
                st.success("💰 Si ce projet ne vous endette pas excessivement, c'est excellent pour votre indépendance.")
            elif projet['type'] == 'Passif':
                st.warning("🚨 Vérifiez que cet investissement respecte votre budget 50/30/20.")
            else:
                st.info("✅ L'éducation est toujours rentable à long terme.")

def show_add_project_form():
    """Formulaire d'ajout de projet"""
    with st.expander("➕ Nouveau Projet", expanded=True):
        with st.form("add_project_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nom = st.text_input("Nom du projet*", placeholder="ex: Groupe électrogène meublés")
                type_projet = st.selectbox(
                    "Type selon Kiyosaki*",
                    ["Actif générateur", "Passif", "Investissement formation"],
                    help="Actif = génère revenus, Passif = coûte de l'argent, Formation = capital humain"
                )
                montant_total = st.number_input("Budget total nécessaire (FCFA)*", min_value=0, step=10000)
                roi_attendu = st.number_input("ROI attendu (%)", min_value=0.0, max_value=100.0, step=0.1)
                priorite = st.selectbox("Priorité", ["Critique", "Haute", "Moyenne", "Faible"])
            
            with col2:
                statut = st.selectbox(
                    "Statut", 
                    ["Planifié", "En cours", "Développement", "Réalisé", "Suspendu"]
                )
                echeance = st.date_input("Échéance prévue", min_value=date.today())
                budget_mensuel = st.number_input("Budget alloué/mois (FCFA)", min_value=0, step=10000)
                cash_flow_mensuel = st.number_input(
                    "Cash flow mensuel estimé (FCFA)", 
                    help="Positif pour revenus, négatif pour dépenses",
                    step=10000
                )
                source_financement = st.selectbox(
                    "Source de financement",
                    get_sources_financement()
                )
            
            description = st.text_area("Description détaillée", height=100)
            
            col1, col2 = st.columns(2)
            
            with col1:
                submitted = st.form_submit_button("✅ Créer Projet", type="primary")
            
            with col2:
                if st.form_submit_button("❌ Annuler"):
                    st.session_state.show_add_form = False
                    st.rerun()
            
            if submitted:
                if nom and type_projet and montant_total > 0:
                    # Créer nouveau projet
                    new_id = max([p['id'] for p in st.session_state.projets]) + 1 if st.session_state.projets else 1
                    
                    nouveau_projet = {
                        'id': new_id,
                        'nom': nom,
                        'type': type_projet,
                        'montant_total': montant_total,
                        'budget_alloue_mensuel': budget_mensuel,
                        'montant_utilise_reel': 0,
                        'cash_flow_mensuel': cash_flow_mensuel,
                        'statut': statut,
                        'echeance': echeance,
                        'roi_attendu': roi_attendu,
                        'priorite': priorite,
                        'description': description,
                        'source_financement': source_financement,
                        'suivi_mensuel': []
                    }
                    
                    st.session_state.projets.append(nouveau_projet)
                    st.session_state.show_add_form = False
                    st.success(f"✅ Projet '{nom}' créé avec succès !")
                    st.rerun()
                else:
                    st.error("⚠️ Veuillez remplir tous les champs obligatoires.")

def show_edit_project_form():
    """Formulaire de modification de projet"""
    project_id = st.session_state.edit_project_id
    projet = next((p for p in st.session_state.projets if p['id'] == project_id), None)
    
    if not projet:
        st.error("Projet introuvable")
        st.session_state.edit_project_id = None
        return
    
    with st.expander(f"✏️ Modifier: {projet['nom']}", expanded=True):
        with st.form("edit_project_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nom = st.text_input("Nom du projet*", value=projet['nom'])
                type_projet = st.selectbox(
                    "Type selon Kiyosaki*",
                    ["Actif générateur", "Passif", "Investissement formation"],
                    index=["Actif générateur", "Passif", "Investissement formation"].index(projet['type'])
                )
                montant_total = st.number_input("Budget total nécessaire (FCFA)*", value=projet['montant_total'], step=10000)
                roi_attendu = st.number_input("ROI attendu (%)", value=projet['roi_attendu'], step=0.1)
                priorite = st.selectbox(
                    "Priorité", 
                    ["Critique", "Haute", "Moyenne", "Faible"],
                    index=["Critique", "Haute", "Moyenne", "Faible"].index(projet['priorite'])
                )
            
            with col2:
                statut = st.selectbox(
                    "Statut",
                    ["Planifié", "En cours", "Développement", "Réalisé", "Suspendu"],
                    index=["Planifié", "En cours", "Développement", "Réalisé", "Suspendu"].index(projet['statut'])
                )
                echeance = st.date_input("Échéance prévue", value=projet['echeance'])
                budget_mensuel = st.number_input("Budget alloué/mois (FCFA)", value=projet['budget_alloue_mensuel'], step=10000)
                cash_flow_mensuel = st.number_input("Cash flow mensuel estimé (FCFA)", value=projet['cash_flow_mensuel'], step=10000)
                source_financement = st.selectbox(
                    "Source de financement",
                    get_sources_financement(),
                    index=get_sources_financement().index(projet['source_financement']) if projet['source_financement'] in get_sources_financement() else 0
                )
            
            description = st.text_area("Description détaillée", value=projet['description'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("💾 Sauvegarder", type="primary"):
                    # Mettre à jour le projet
                    index = next(i for i, p in enumerate(st.session_state.projets) if p['id'] == project_id)
                    
                    st.session_state.projets[index].update({
                        'nom': nom,
                        'type': type_projet,
                        'montant_total': montant_total,
                        'budget_alloue_mensuel': budget_mensuel,
                        'cash_flow_mensuel': cash_flow_mensuel,
                        'statut': statut,
                        'echeance': echeance,
                        'roi_attendu': roi_attendu,
                        'priorite': priorite,
                        'description': description,
                        'source_financement': source_financement
                    })
                    
                    st.session_state.edit_project_id = None
                    st.success("Projet modifié!")
                    st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Annuler"):
                    st.session_state.edit_project_id = None
                    st.rerun()

def filter_projects(filter_type, filter_status, filter_priority, sort_by):
    """Filtre et trie les projets"""
    projets = st.session_state.projets.copy()
    
    # Filtrage
    if filter_type != "Tous":
        projets = [p for p in projets if p['type'] == filter_type]
    
    if filter_status != "Tous":
        projets = [p for p in projets if p['statut'] == filter_status]
    
    if filter_priority != "Toutes":
        projets = [p for p in projets if p['priorite'] == filter_priority]
    
    # Tri
    if sort_by == "Nom":
        projets.sort(key=lambda x: x['nom'])
    elif sort_by == "Montant":
        projets.sort(key=lambda x: x['montant_total'], reverse=True)
    elif sort_by == "Échéance":
        projets.sort(key=lambda x: x['echeance'])
    elif sort_by == "ROI":
        projets.sort(key=lambda x: x['roi_attendu'], reverse=True)
    elif sort_by == "Type":
        projets.sort(key=lambda x: x['type'])
    
    return projets

def show_revenue_management():
    """Page Gestion des Revenus Variables (AMÉLIORÉE)"""
    st.title("💰 Gestion des Revenus Variables")
    
    st.markdown("""
    Cette section permet de gérer les revenus qui fluctuent chaque mois 
    (salaires supplémentaires, revenus business IIBA, loyers, etc.)
    """)
    
    # Actions principales
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Ajouter Revenu", type="primary"):
            st.session_state.show_add_revenue_form = True
    
    # Formulaire d'ajout
    if st.session_state.get('show_add_revenue_form', False):
        show_add_revenue_form()
    
    # Formulaire de modification
    if st.session_state.get('edit_revenue_id'):
        show_edit_revenue_form()
    
    # Affichage revenus actuels
    st.subheader("💼 Revenus Mensuels Actuels")
    
    if st.session_state.revenus_variables:
        for revenu in st.session_state.revenus_variables:
            show_revenue_card(revenu)
        
        # Total
        total_revenus = sum(r['montant_mensuel'] for r in st.session_state.revenus_variables)
        st.markdown(f"### **Total Revenus: {format_currency(total_revenus)}**")
        
    else:
        st.info("Aucun revenu variable configuré.")
    
    # Graphique évolution
    st.subheader("📈 Évolution des Revenus")
    
    if st.session_state.revenus_variables:
        # Simulation données historiques
        import numpy as np
        mois = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')
        
        revenus_evolution = []
        for revenu in st.session_state.revenus_variables:
            if revenu['regulier']:
                revenus_evolution.append([revenu['montant_mensuel']] * len(mois))
            else:
                # Simulation variation pour revenus variables
                base = revenu['montant_mensuel'] 
                variation = np.random.normal(base, base*0.2, len(mois))
                variation = np.maximum(variation, 0)  # Pas de revenus négatifs
                revenus_evolution.append(variation)
        
        if revenus_evolution:
            df_revenus = pd.DataFrame({
                revenu['nom']: evolution 
                for revenu, evolution in zip(st.session_state.revenus_variables, revenus_evolution)
            }, index=mois)
            
            fig = px.line(df_revenus, title="Évolution des Revenus par Source")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

def show_revenue_card(revenu):
    """Affiche une carte de revenu avec possibilité de modification"""
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
        
        with col1:
            st.write(f"**{revenu['nom']}**")
        
        with col2:
            st.write(revenu['type'])
        
        with col3:
            st.write(format_currency(revenu['montant_mensuel']))
        
        with col4:
            st.write("🔄 Régulier" if revenu['regulier'] else "📊 Variable")
        
        with col5:
            col_edit, col_delete = st.columns(2)
            
            with col_edit:
                if st.button("✏️", key=f"edit_rev_{revenu['id']}"):
                    st.session_state.edit_revenue_id = revenu['id']
                    st.rerun()
            
            with col_delete:
                if st.button("🗑️", key=f"del_rev_{revenu['id']}"):
                    if st.session_state.get(f"confirm_delete_rev_{revenu['id']}", False):
                        # Suppression confirmée
                        st.session_state.revenus_variables = [r for r in st.session_state.revenus_variables if r['id'] != revenu['id']]
                        st.success(f"Revenu '{revenu['nom']}' supprimé.")
                        if f"confirm_delete_rev_{revenu['id']}" in st.session_state:
                            del st.session_state[f"confirm_delete_rev_{revenu['id']}"]
                        st.rerun()
                    else:
                        # Demande de confirmation
                        st.session_state[f"confirm_delete_rev_{revenu['id']}"] = True
                        st.warning("Cliquez à nouveau pour confirmer.")
    
    st.markdown("---")

def show_add_revenue_form():
    """Formulaire d'ajout de revenu"""
    with st.expander("➕ Ajouter un Revenu Variable", expanded=True):
        with st.form("add_revenue_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nom_revenu = st.text_input("Nom du revenu*", placeholder="ex: Bonus William")
                type_revenu = st.selectbox("Type", ["Salaire", "Business", "Loyer", "Investissement", "Autre"])
            
            with col2:
                montant_mensuel = st.number_input("Montant ce mois (FCFA)*", min_value=0, step=10000)
                regulier = st.checkbox("Revenu régulier ?", help="Cocher si le montant est prévisible chaque mois")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("✅ Ajouter Revenu", type="primary"):
                    if nom_revenu and montant_mensuel > 0:
                        new_id = max([r['id'] for r in st.session_state.revenus_variables]) + 1 if st.session_state.revenus_variables else 1
                        
                        nouveau_revenu = {
                            'id': new_id,
                            'nom': nom_revenu,
                            'montant_mensuel': montant_mensuel,
                            'type': type_revenu,
                            'regulier': regulier
                        }
                        st.session_state.revenus_variables.append(nouveau_revenu)
                        st.session_state.show_add_revenue_form = False
                        st.success(f"Revenu '{nom_revenu}' ajouté !")
                        st.rerun()
                    else:
                        st.error("Veuillez remplir tous les champs obligatoires.")
            
            with col2:
                if st.form_submit_button("❌ Annuler"):
                    st.session_state.show_add_revenue_form = False
                    st.rerun()

def show_edit_revenue_form():
    """Formulaire de modification de revenu"""
    revenue_id = st.session_state.edit_revenue_id
    revenu = next((r for r in st.session_state.revenus_variables if r['id'] == revenue_id), None)
    
    if not revenu:
        st.error("Revenu introuvable")
        st.session_state.edit_revenue_id = None
        return
    
    with st.expander(f"✏️ Modifier: {revenu['nom']}", expanded=True):
        with st.form("edit_revenue_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nom_revenu = st.text_input("Nom du revenu*", value=revenu['nom'])
                type_revenu = st.selectbox(
                    "Type", 
                    ["Salaire", "Business", "Loyer", "Investissement", "Autre"],
                    index=["Salaire", "Business", "Loyer", "Investissement", "Autre"].index(revenu['type'])
                )
            
            with col2:
                montant_mensuel = st.number_input("Montant ce mois (FCFA)*", value=revenu['montant_mensuel'], step=10000)
                regulier = st.checkbox("Revenu régulier ?", value=revenu['regulier'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("💾 Sauvegarder", type="primary"):
                    # Mettre à jour le revenu
                    index = next(i for i, r in enumerate(st.session_state.revenus_variables) if r['id'] == revenue_id)
                    
                    st.session_state.revenus_variables[index].update({
                        'nom': nom_revenu,
                        'montant_mensuel': montant_mensuel,
                        'type': type_revenu,
                        'regulier': regulier
                    })
                    
                    st.session_state.edit_revenue_id = None
                    st.success("Revenu modifié!")
                    st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Annuler"):
                    st.session_state.edit_revenue_id = None
                    st.rerun()

# ============================================================================
# PAGES COMPLÈTES (simplifiées pour l'exemple)
# ============================================================================

def show_mentor_advice():
    """Page Conseils des 3 Mentors"""
    st.title("🎯 Conseil des 3 Mentors Financiers")
    
    # Sélection d'un projet
    projets = st.session_state.projets
    project_names = [p['nom'] for p in projets]
    
    if project_names:
        selected_project_name = st.selectbox("Choisir un projet pour conseil détaillé", project_names)
        
        if selected_project_name:
            project = next(p for p in projets if p['nom'] == selected_project_name)
            show_project_advice(project)
    else:
        st.info("Aucun projet disponible. Ajoutez des projets dans la section 'Gestion Projets'.")

def show_analytics():
    """Page Analytics simplifiée"""
    st.title("📈 Analytics & KPIs Avancés")
    st.info("Page Analytics complète - En développement")

def show_progression():
    """Page Progression simplifiée"""
    st.title("🚀 Progression Familiale")
    st.info("Page Progression complète - En développement")

def show_children_education():
    """Page Éducation simplifiée"""
    st.title("👨‍👩‍👧‍👦 Éducation Enfants")
    st.info("Page Éducation complète - En développement")

def show_vision_2030():
    """Page Vision simplifiée"""
    st.title("🔮 Vision 2030")
    st.info("Page Vision complète - En développement")

# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    # Chargement CSS
    load_css()
    
    # Initialisation session state
    initialize_session_state()
    
    # Sidebar navigation
    selected_page = render_sidebar()
    
    # Routing des pages
    if selected_page == "📊 Dashboard Principal":
        show_dashboard()
    elif selected_page == "📋 Vue Kanban Projets":
        show_kanban_view()
    elif selected_page == "💼 Gestion Projets":
        show_project_management()
    elif selected_page == "💰 Revenus Variables":
        show_revenue_management()
    elif selected_page == "🎯 Conseils 3 Mentors":
        show_mentor_advice()
    elif selected_page == "📈 Analytics & KPIs":
        show_analytics()
    elif selected_page == "🚀 Progression Familiale":
        show_progression()
    elif selected_page == "👨‍👩‍👧‍👦 Éducation Enfants":
        show_children_education()
    elif selected_page == "🔮 Vision 2030":
        show_vision_2030()

if __name__ == "__main__":
    main()
