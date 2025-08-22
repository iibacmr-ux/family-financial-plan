import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import json
import io
from typing import Dict, List, Any
import uuid

# Configuration de la page
st.set_page_config(
    page_title="Plan Financier Stratégique Familial",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour conserver le design original
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79, #2e7d8f);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
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
        border-left: 4px solid #20b2aa;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .actif-card {
        border-left-color: #28a745;
        background: #f8fff9;
    }
    
    .passif-card {
        border-left-color: #dc3545;
        background: #fff8f8;
    }
    
    .investissement-card {
        border-left-color: #ffc107;
        background: #fffef8;
    }
    
    .kanban-column {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem;
        min-height: 400px;
    }
    
    .kanban-card {
        background: white;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid;
    }
    
    .kanban-retard { border-left-color: #dc3545; }
    .kanban-risque { border-left-color: #ffc107; }
    .kanban-cours { border-left-color: #17a2b8; }
    .kanban-avance { border-left-color: #28a745; }
    .kanban-bloque { border-left-color: #6c757d; }
    
    .mindset-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .mentor-kiyosaki {
        border-left: 4px solid #ff6b6b;
        background: #fff5f5;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .mentor-buffett {
        border-left: 4px solid #4ecdc4;
        background: #f0fdfc;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .mentor-ramsey {
        border-left: 4px solid #45b7d1;
        background: #f0f9ff;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .phase-stabilisation { color: #dc3545; font-weight: bold; }
    .phase-transition { color: #ffc107; font-weight: bold; }
    .phase-expansion { color: #28a745; font-weight: bold; }
    
    .progress-bar {
        background: #e9ecef;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    .info-tooltip {
        background: #e3f2fd;
        border: 1px solid #2196f3;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #28a745;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Fonction utilitaire sécurisée
def safe_get(data: Dict, key: str, default=None):
    """Fonction sécurisée pour obtenir une valeur d'un dictionnaire"""
    return data.get(key, default) if data else default

# Initialisation du state
def init_session_state():
    """Initialise le state de la session avec des données par défaut"""
    if 'projets' not in st.session_state:
        st.session_state.projets = [
            {
                'id': str(uuid.uuid4()),
                'nom': 'Projet IIBA',
                'type': 'Actif générateur',
                'montant_total': 2790000,
                'budget_alloue_mensuel': 0,
                'montant_utilise_reel': 2790000,
                'cash_flow_mensuel': 232500,
                'roi_attendu': 10.0,
                'statut': 'En cours',
                'priorite': 'Haute',
                'echeance': date(2025, 12, 31),
                'categorie': 'Business',
                'description': 'Développement du projet IIBA',
                'source_financement': 'Revenus William',
                'responsable': 'William',
                'date_creation': datetime.now(),
                'date_modification': datetime.now(),
                'suivi_mensuel': []
            },
            {
                'id': str(uuid.uuid4()),
                'nom': 'Voyage Suisse famille',
                'type': 'Passif',
                'montant_total': 8200000,
                'budget_alloue_mensuel': 1366667,
                'montant_utilise_reel': 0,
                'cash_flow_mensuel': -1366667,
                'roi_attendu': 0.0,
                'statut': 'À venir',
                'priorite': 'Haute',
                'echeance': date(2025, 6, 23),
                'categorie': 'Familial',
                'description': 'Voyage en famille en Suisse',
                'source_financement': 'Revenus William',
                'responsable': 'Alix',
                'date_creation': datetime.now(),
                'date_modification': datetime.now(),
                'suivi_mensuel': []
            },
            {
                'id': str(uuid.uuid4()),
                'nom': 'Scolarité enfants',
                'type': 'Investissement',
                'montant_total': 6500000,
                'budget_alloue_mensuel': 541667,
                'montant_utilise_reel': 1700000,
                'cash_flow_mensuel': -541667,
                'roi_attendu': 15.0,
                'statut': 'En cours',
                'priorite': 'Critique',
                'echeance': date(2025, 12, 31),
                'categorie': 'Éducation',
                'description': 'Scolarité des trois enfants',
                'source_financement': 'Revenus William',
                'responsable': 'Famille',
                'date_creation': datetime.now(),
                'date_modification': datetime.now(),
                'suivi_mensuel': []
            }
        ]
    
    if 'revenus' not in st.session_state:
        st.session_state.revenus = [
            {
                'id': str(uuid.uuid4()),
                'nom': 'Salaire William',
                'type': 'Salaire',
                'montant': 1400000,
                'mois': 'Mars',
                'annee': 2025,
                'recurrent': True,
                'description': 'Salaire mensuel de William',
                'responsable': 'William',
                'date_creation': datetime.now(),
                'date_modification': datetime.now()
            },
            {
                'id': str(uuid.uuid4()),
                'nom': 'Revenus IIBA',
                'type': 'Business',
                'montant': 782000,
                'mois': 'Septembre',
                'annee': 2025,
                'recurrent': False,
                'description': 'Revenus du projet IIBA',
                'responsable': 'William',
                'date_creation': datetime.now(),
                'date_modification': datetime.now()
            }
        ]
    
    if 'config_admin' not in st.session_state:
        st.session_state.config_admin = {
            'seuils': {
                'fonds_urgence_mois': 6,
                'ratio_actifs_min': 50,
                'cash_flow_positif': 0,
                'revenus_passifs_min': 30,
                'objectif_independance': 100
            },
            'listes': {
                'types_projets': ['Actif générateur', 'Passif', 'Investissement'],
                'statuts': ['À venir', 'En cours', 'Terminé', 'Suspendu', 'Annulé'],
                'priorites': ['Critique', 'Haute', 'Moyenne', 'Basse'],
                'categories': ['Business', 'Familial', 'Éducation', 'Immobilier', 'Personnel'],
                'responsables': ['Alix', 'William', 'Famille'],
                'types_revenus': ['Salaire', 'Business', 'Loyer', 'Investissement', 'Bonus']
            },
            'conseils_mentors': {
                'kiyosaki': {
                    'Actif générateur': 'Excellent choix ! Cet actif va mettre de l\'argent dans votre poche. Concentrez-vous sur la scalabilité.',
                    'Passif': 'Attention ! Ceci sort de l\'argent de votre poche. Limitez ces dépenses et privilégiez les actifs.',
                    'Investissement': 'Bon pour le capital humain, mais assurez-vous que cela génère des revenus futurs.'
                },
                'buffett': {
                    'Actif générateur': 'Comprenez-vous parfaitement ce business ? Investissez seulement dans ce que vous maîtrisez.',
                    'Passif': 'Ces dépenses sont-elles vraiment nécessaires ? Privilégiez la valeur long terme.',
                    'Investissement': 'L\'éducation est le meilleur investissement. Excellent choix pour l\'avenir.'
                },
                'ramsey': {
                    'Actif générateur': 'Payez comptant si possible. Évitez l\'endettement même pour les actifs.',
                    'Passif': 'Est-ce un BESOIN ou une ENVIE ? Respectez votre budget 50/30/20.',
                    'Investissement': 'Priorité à l\'éducation ! Mais respectez votre budget d\'urgence.'
                }
            }
        }

    if 'edit_project_id' not in st.session_state:
        st.session_state.edit_project_id = None
    if 'edit_revenue_id' not in st.session_state:
        st.session_state.edit_revenue_id = None

# Fonctions de calcul des KPIs
def calculer_kpis(projets, revenus, mois_filtre=None, annee_filtre=None):
    """Calcule tous les KPIs en fonction des filtres"""
    
    # Filtrer les données selon la période
    projets_filtres = projets
    revenus_filtres = revenus
    
    if mois_filtre and mois_filtre != "Tout":
        revenus_filtres = [r for r in revenus if r.get('mois') == mois_filtre]
    
    if annee_filtre and annee_filtre != "Tout":
        revenus_filtres = [r for r in revenus_filtres if r.get('annee') == annee_filtre]
    
    # Calculs des KPIs
    total_revenus = sum(r.get('montant', 0) for r in revenus_filtres)
    total_actifs = sum(p.get('montant_total', 0) for p in projets_filtres if p.get('type') == 'Actif générateur')
    total_passifs = sum(p.get('montant_total', 0) for p in projets_filtres if p.get('type') == 'Passif')
    total_investissements = sum(p.get('montant_total', 0) for p in projets_filtres if p.get('type') == 'Investissement')
    
    cash_flow_mensuel = sum(p.get('cash_flow_mensuel', 0) for p in projets_filtres)
    revenus_passifs = sum(p.get('cash_flow_mensuel', 0) for p in projets_filtres if p.get('cash_flow_mensuel', 0) > 0)
    
    ratio_actifs_passifs = (total_actifs / max(total_passifs, 1)) * 100
    ratio_revenus_passifs = (revenus_passifs / max(total_revenus, 1)) * 100 if total_revenus > 0 else 0
    
    # Phases
    if cash_flow_mensuel < 0 and ratio_actifs_passifs < 20:
        phase = "Stabilisation"
    elif cash_flow_mensuel >= 0 and ratio_actifs_passifs >= 20 and ratio_actifs_passifs < 40:
        phase = "Transition" 
    else:
        phase = "Expansion"
    
    # Baby Steps Dave Ramsey
    fonds_urgence = sum(p.get('montant_total', 0) for p in projets_filtres if 'urgence' in p.get('nom', '').lower())
    baby_step = 1
    if fonds_urgence >= 500000:  # 1000$ = ~500k FCFA
        baby_step = 2
    if fonds_urgence >= 3 * abs(cash_flow_mensuel):  # 3-6 mois de dépenses
        baby_step = 3
    
    return {
        'total_revenus': total_revenus,
        'total_actifs': total_actifs,
        'total_passifs': total_passifs,
        'total_investissements': total_investissements,
        'cash_flow_mensuel': cash_flow_mensuel,
        'revenus_passifs': revenus_passifs,
        'ratio_actifs_passifs': ratio_actifs_passifs,
        'ratio_revenus_passifs': ratio_revenus_passifs,
        'phase': phase,
        'baby_step': baby_step,
        'fonds_urgence': fonds_urgence,
        'nombre_actifs': len([p for p in projets_filtres if p.get('type') == 'Actif générateur'])
    }

def determiner_quadrant_kiyosaki(projets, revenus):
    """Détermine le quadrant selon Kiyosaki"""
    revenus_salaire = sum(r.get('montant', 0) for r in revenus if r.get('type') == 'Salaire')
    revenus_business = sum(r.get('montant', 0) for r in revenus if r.get('type') == 'Business')
    revenus_investissement = sum(r.get('montant', 0) for r in revenus if r.get('type') in ['Loyer', 'Investissement'])
    total_revenus = revenus_salaire + revenus_business + revenus_investissement
    
    if total_revenus == 0:
        return "E", "🐭 Rat Race - Aucun revenu"
    
    pct_salaire = (revenus_salaire / total_revenus) * 100
    pct_business = (revenus_business / total_revenus) * 100
    pct_investissement = (revenus_investissement / total_revenus) * 100
    
    if pct_salaire > 70:
        quadrant = "E"
        status = "🐭 Rat Race - Dépendant du salaire"
    elif pct_business > 50:
        quadrant = "S/B"
        status = "⚡ En transition - Développement business"
    elif pct_investissement > 40:
        quadrant = "I"
        status = "🎯 Liberté financière - Revenus passifs"
    else:
        quadrant = "Mixte"
        status = "🔄 En évolution - Portfolio diversifié"
    
    return quadrant, status

# Pages de l'application
def show_dashboard():
    """Dashboard principal avec KPIs"""
    st.markdown('<div class="main-header"><h1>📊 Dashboard Familial</h1></div>', unsafe_allow_html=True)
    
    # Calcul des KPIs avec filtre
    mois_filtre = st.session_state.get('mois_filtre')
    annee_filtre = st.session_state.get('annee_filtre')
    kpis = calculer_kpis(st.session_state.projets, st.session_state.revenus, mois_filtre, annee_filtre)
    
    # Affichage période active
    periode = "Toutes les données"
    if mois_filtre and mois_filtre != "Tout" and annee_filtre and annee_filtre != "Tout":
        periode = f"{mois_filtre} {annee_filtre}"
    elif mois_filtre and mois_filtre != "Tout":
        periode = f"Tous les {mois_filtre}"
    elif annee_filtre and annee_filtre != "Tout":
        periode = f"Année {annee_filtre}"
    
    st.info(f"📅 **Période active :** {periode}")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Cash Flow Mensuel", 
                 f"{kpis['cash_flow_mensuel']:,.0f} FCFA",
                 delta="Positif" if kpis['cash_flow_mensuel'] > 0 else "Négatif")
    
    with col2:
        st.metric("📈 Ratio Actifs/Passifs", 
                 f"{kpis['ratio_actifs_passifs']:.1f}%",
                 delta="Bon" if kpis['ratio_actifs_passifs'] > 50 else "À améliorer")
    
    with col3:
        st.metric("🎯 Revenus Passifs", 
                 f"{kpis['ratio_revenus_passifs']:.1f}%",
                 delta="Objectif: 30%")
    
    with col4:
        phase_color = {"Stabilisation": "🔴", "Transition": "🟡", "Expansion": "🟢"}
        st.metric("🚀 Phase Actuelle", 
                 f"{phase_color.get(kpis['phase'], '🔵')} {kpis['phase']}",
                 delta="Baby Step " + str(kpis['baby_step']))
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Répartition Financière")
        fig_pie = px.pie(
            values=[kpis['total_actifs'], kpis['total_passifs'], kpis['total_investissements']],
            names=['Actifs générateurs', 'Passifs', 'Investissements'],
            colors=['#28a745', '#dc3545', '#ffc107']
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("📈 Évolution Cash Flow")
        mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
        cash_flow_data = [kpis['cash_flow_mensuel'] + np.random.randint(-100000, 100000) for _ in mois]
        
        fig_line = px.line(x=mois, y=cash_flow_data, title="Projection Cash Flow 2025")
        fig_line.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_line, use_container_width=True)

def show_kanban_view():
    """Vue Kanban avec colonnes par statut"""
    st.markdown('<div class="main-header"><h1>📋 Vue Kanban Projets</h1></div>', unsafe_allow_html=True)
    
    # Filtrage des projets
    mois_filtre = st.session_state.get('mois_filtre')
    annee_filtre = st.session_state.get('annee_filtre')
    projets_filtres = st.session_state.projets
    
    # Catégorisation des projets
    categories = {
        'En Retard': {'projets': [], 'couleur': '#dc3545', 'icone': '🔴'},
        'À Risque': {'projets': [], 'couleur': '#ffc107', 'icone': '🟡'},
        'En Cours': {'projets': [], 'couleur': '#17a2b8', 'icone': '🔵'},
        'En Avance': {'projets': [], 'couleur': '#28a745', 'icone': '🟢'},
        'Bloqué': {'projets': [], 'couleur': '#6c757d', 'icone': '⚫'}
    }
    
    today = date.today()
    
    for projet in projets_filtres:
        echeance = projet.get('echeance', today)
        if isinstance(echeance, str):
            try:
                echeance = datetime.strptime(echeance, '%Y-%m-%d').date()
            except:
                echeance = today
        
        # Logique de catégorisation
        if echeance < today:
            categories['En Retard']['projets'].append(projet)
        elif projet.get('statut') == 'Suspendu' or projet.get('montant_utilise_reel', 0) >= projet.get('montant_total', 1):
            categories['Bloqué']['projets'].append(projet)
        elif projet.get('statut') == 'Terminé':
            categories['En Avance']['projets'].append(projet)
        elif (echeance - today).days < 30:
            categories['À Risque']['projets'].append(projet)
        else:
            categories['En Cours']['projets'].append(projet)
    
    # Affichage des statistiques
    col1, col2, col3, col4, col5 = st.columns(5)
    colonnes = [col1, col2, col3, col4, col5]
    
    for i, (nom_cat, cat_data) in enumerate(categories.items()):
        with colonnes[i]:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <h3>{cat_data['icone']} {nom_cat}</h3>
                <h2 style="color: {cat_data['couleur']};">{len(cat_data['projets'])}</h2>
            </div>
            """, unsafe_allow_html=True)
    
    # Colonnes Kanban
    st.markdown("---")
    cols = st.columns(5)
    
    for i, (nom_cat, cat_data) in enumerate(categories.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="kanban-column">
                <h4 style="color: {cat_data['couleur']};">{cat_data['icone']} {nom_cat} ({len(cat_data['projets'])})</h4>
            """, unsafe_allow_html=True)
            
            for projet in cat_data['projets']:
                show_kanban_card(projet, cat_data['couleur'])
            
            st.markdown("</div>", unsafe_allow_html=True)

def show_kanban_card(projet, couleur):
    """Affiche une carte projet dans le Kanban"""
    type_icons = {
        'Actif générateur': '📈',
        'Passif': '📉', 
        'Investissement': '🎓'
    }
    
    with st.container():
        st.markdown(f"""
        <div class="kanban-card" style="border-left-color: {couleur};">
            <h5>{type_icons.get(projet.get('type', ''), '📋')} {projet.get('nom', 'Projet')}</h5>
            <p><strong>Budget:</strong> {projet.get('montant_total', 0):,.0f} FCFA</p>
            <p><strong>Utilisé:</strong> {projet.get('montant_utilise_reel', 0):,.0f} FCFA</p>
            <p><strong>Échéance:</strong> {projet.get('echeance', 'Non définie')}</p>
            <p><strong>Financement:</strong> {safe_get(projet, 'source_financement', 'Non défini')}</p>
            <p><strong>Responsable:</strong> {safe_get(projet, 'responsable', 'Non défini')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Modifier", key=f"edit_kanban_{projet.get('id', 'temp')}"):
                st.session_state.edit_project_id = projet.get('id')
                st.rerun()
        with col2:
            if st.button("👁️ Détails", key=f"view_kanban_{projet.get('id', 'temp')}"):
                show_project_details_modal(projet)

def show_project_details_modal(projet):
    """Affiche les détails complets d'un projet"""
    with st.expander(f"📋 Détails: {projet.get('nom', 'Projet')}", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Type:** {projet.get('type', 'Non défini')}")
            st.write(f"**Statut:** {projet.get('statut', 'Non défini')}")
            st.write(f"**Priorité:** {projet.get('priorite', 'Non définie')}")
            st.write(f"**Catégorie:** {projet.get('categorie', 'Non définie')}")
            st.write(f"**Responsable:** {safe_get(projet, 'responsable', 'Non défini')}")
        
        with col2:
            st.write(f"**Budget total:** {projet.get('montant_total', 0):,.0f} FCFA")
            st.write(f"**Utilisé réel:** {projet.get('montant_utilise_reel', 0):,.0f} FCFA")
            st.write(f"**Cash flow mensuel:** {projet.get('cash_flow_mensuel', 0):,.0f} FCFA")
            st.write(f"**ROI attendu:** {projet.get('roi_attendu', 0):.1f}%")
            st.write(f"**Échéance:** {projet.get('echeance', 'Non définie')}")
        
        if projet.get('description'):
            st.write(f"**Description:** {projet.get('description')}")
        
        # Dates de gestion
        if safe_get(projet, 'date_creation'):
            st.write(f"**Créé le:** {projet['date_creation'].strftime('%d/%m/%Y à %H:%M')}")
        if safe_get(projet, 'date_modification'):
            st.write(f"**Modifié le:** {projet['date_modification'].strftime('%d/%m/%Y à %H:%M')}")

def show_project_management():
    """Gestion des projets avec CRUD complet"""
    st.markdown('<div class="main-header"><h1>💼 Gestion des Projets</h1></div>', unsafe_allow_html=True)
    
    # Si en mode édition
    if st.session_state.edit_project_id:
        show_edit_project_form()
        return
    
    # Bouton ajouter et filtres
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("➕ Ajouter un nouveau projet", type="primary"):
            st.session_state.show_add_form = True
    
    with col2:
        type_filter = st.selectbox("Filtrer par type", ["Tous"] + st.session_state.config_admin['listes']['types_projets'])
    
    with col3:
        statut_filter = st.selectbox("Filtrer par statut", ["Tous"] + st.session_state.config_admin['listes']['statuts'])
    
    # Formulaire d'ajout
    if st.session_state.get('show_add_form', False):
        show_add_project_form()
    
    st.markdown("---")
    
    # Liste des projets
    projets_filtres = st.session_state.projets
    if type_filter != "Tous":
        projets_filtres = [p for p in projets_filtres if p.get('type') == type_filter]
    if statut_filter != "Tous":
        projets_filtres = [p for p in projets_filtres if p.get('statut') == statut_filter]
    
    if not projets_filtres:
        st.info("Aucun projet trouvé avec les filtres sélectionnés.")
        return
    
    for projet in projets_filtres:
        show_project_card_native(projet)

def show_add_project_form():
    """Formulaire d'ajout de projet avec validation améliorée"""
    st.subheader("➕ Nouveau Projet")
    
    with st.form("add_project_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("*Nom du projet", help="Nom descriptif du projet")
            type_projet = st.selectbox("*Type", st.session_state.config_admin['listes']['types_projets'])
            montant_total = st.number_input("*Budget total (FCFA)", min_value=0, value=0, step=1000)
            cash_flow = st.number_input("Cash flow mensuel (FCFA)", value=0, step=1000, 
                                      help="Positif = génère des revenus, Négatif = coûte de l'argent")
            roi_attendu = st.number_input("ROI attendu (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        
        with col2:
            statut = st.selectbox("*Statut", st.session_state.config_admin['listes']['statuts'])
            priorite = st.selectbox("*Priorité", st.session_state.config_admin['listes']['priorites'])
            categorie = st.selectbox("*Catégorie", st.session_state.config_admin['listes']['categories'])
            echeance = st.date_input("*Échéance", value=date.today() + timedelta(days=30))
            source_financement = st.selectbox("Source de financement", 
                                            ["Non défini"] + [r['nom'] for r in st.session_state.revenus])
            responsable = st.selectbox("*Responsable", st.session_state.config_admin['listes']['responsables'])
        
        description = st.text_area("Description", help="Description détaillée du projet")
        
        submitted = st.form_submit_button("✅ Créer le projet", type="primary")
        
        if submitted:
            # Validation améliorée
            champs_obligatoires = {
                'nom': nom,
                'type_projet': type_projet,
                'montant_total': montant_total,
                'statut': statut,
                'priorite': priorite,
                'categorie': categorie,
                'responsable': responsable
            }
            
            champs_manquants = [k for k, v in champs_obligatoires.items() if not v or v == 0]
            
            if champs_manquants:
                champs_manquants_str = ", ".join([
                    "Nom" if k == "nom" else
                    "Type" if k == "type_projet" else
                    "Budget total" if k == "montant_total" else
                    "Statut" if k == "statut" else
                    "Priorité" if k == "priorite" else
                    "Catégorie" if k == "categorie" else
                    "Responsable" if k == "responsable" else k
                    for k in champs_manquants
                ])
                st.error(f"⚠️ Champs manquants: {champs_manquants_str}")
                return
            
            # Création du projet
            nouveau_projet = {
                'id': str(uuid.uuid4()),
                'nom': nom,
                'type': type_projet,
                'montant_total': int(montant_total),
                'budget_alloue_mensuel': int(montant_total / 12) if montant_total > 0 else 0,
                'montant_utilise_reel': 0,
                'cash_flow_mensuel': int(cash_flow),
                'roi_attendu': float(roi_attendu),
                'statut': statut,
                'priorite': priorite,
                'echeance': echeance,
                'categorie': categorie,
                'description': description,
                'source_financement': source_financement,
                'responsable': responsable,
                'date_creation': datetime.now(),
                'date_modification': datetime.now(),
                'suivi_mensuel': []
            }
            
            st.session_state.projets.append(nouveau_projet)
            st.session_state.show_add_form = False
            st.success(f"✅ Projet '{nom}' créé avec succès!")
            st.rerun()
        
        if st.form_submit_button("❌ Annuler"):
            st.session_state.show_add_form = False
            st.rerun()

def show_project_card_native(projet):
    """Affiche une carte projet avec composants Streamlit natifs"""
    type_styles = {
        'Actif générateur': ('actif-card', '📈', '#28a745'),
        'Passif': ('passif-card', '📉', '#dc3545'),
        'Investissement': ('investissement-card', '🎓', '#ffc107')
    }
    
    card_class, icon, color = type_styles.get(projet.get('type', ''), ('project-card', '📋', '#20b2aa'))
    
    with st.container():
        st.markdown(f"""
        <div class="project-card {card_class}">
            <h4>{icon} {projet.get('nom', 'Projet sans nom')}</h4>
            <div style="color: {color}; font-weight: bold;">Type: {projet.get('type', 'Non défini')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Informations détaillées
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"**💰 Budget:** {projet.get('montant_total', 0):,.0f} FCFA")
            st.write(f"**📊 Utilisé:** {projet.get('montant_utilise_reel', 0):,.0f} FCFA")
            st.write(f"**💵 Cash flow:** {projet.get('cash_flow_mensuel', 0):,.0f} FCFA/mois")
        
        with col2:
            st.write(f"**📈 ROI:** {projet.get('roi_attendu', 0):.1f}%")
            st.write(f"**📅 Échéance:** {projet.get('echeance', 'Non définie')}")
            st.write(f"**🎯 Statut:** {projet.get('statut', 'Non défini')}")
        
        with col3:
            st.write(f"**🔥 Priorité:** {projet.get('priorite', 'Non définie')}")
            st.write(f"**🏦 Financement:** {safe_get(projet, 'source_financement', 'Non défini')}")
            st.write(f"**👤 Responsable:** {safe_get(projet, 'responsable', 'Non défini')}")
        
        if projet.get('description'):
            st.write(f"**📝 Description:** {projet.get('description')}")
        
        # Dates de création et modification
        if safe_get(projet, 'date_creation'):
            st.caption(f"📅 Créé le {projet['date_creation'].strftime('%d/%m/%Y à %H:%M')}")
        if safe_get(projet, 'date_modification') and projet['date_modification'] != projet.get('date_creation'):
            st.caption(f"📝 Modifié le {projet['date_modification'].strftime('%d/%m/%Y à %H:%M')}")
        
        # Conseils des mentors
        show_mentors_advice(projet)
        
        # Boutons d'action
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✏️ Modifier", key=f"edit_project_{projet.get('id')}"):
                st.session_state.edit_project_id = projet.get('id')
                st.rerun()
        with col2:
            if st.button("🗑️ Supprimer", key=f"delete_project_{projet.get('id')}"):
                if st.session_state.get(f"confirm_delete_{projet.get('id')}", False):
                    st.session_state.projets = [p for p in st.session_state.projets if p.get('id') != projet.get('id')]
                    if f"confirm_delete_{projet.get('id')}" in st.session_state:
                        del st.session_state[f"confirm_delete_{projet.get('id')}"]
                    st.success(f"Projet '{projet.get('nom')}' supprimé!")
                    st.rerun()
                else:
                    st.session_state[f"confirm_delete_{projet.get('id')}"] = True
                    st.warning("⚠️ Cliquez à nouveau pour confirmer la suppression")
        with col3:
            if st.button("📊 Suivi mensuel", key=f"track_project_{projet.get('id')}"):
                show_monthly_tracking(projet)
        
        st.markdown("---")

def show_edit_project_form():
    """Formulaire d'édition de projet"""
    projet = next((p for p in st.session_state.projets if p.get('id') == st.session_state.edit_project_id), None)
    
    if not projet:
        st.error("Projet introuvable")
        st.session_state.edit_project_id = None
        return
    
    st.subheader(f"✏️ Modifier: {projet.get('nom', 'Projet')}")
    
    with st.form("edit_project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("*Nom du projet", value=projet.get('nom', ''))
            type_projet = st.selectbox("*Type", st.session_state.config_admin['listes']['types_projets'],
                                     index=st.session_state.config_admin['listes']['types_projets'].index(projet.get('type', 'Actif générateur')))
            montant_total = st.number_input("*Budget total (FCFA)", min_value=0, value=int(projet.get('montant_total', 0)), step=1000)
            cash_flow = st.number_input("Cash flow mensuel (FCFA)", value=int(projet.get('cash_flow_mensuel', 0)), step=1000)
            roi_attendu = st.number_input("ROI attendu (%)", min_value=0.0, max_value=100.0, 
                                        value=float(projet.get('roi_attendu', 0.0)), step=0.1)
        
        with col2:
            statut = st.selectbox("*Statut", st.session_state.config_admin['listes']['statuts'],
                                index=st.session_state.config_admin['listes']['statuts'].index(projet.get('statut', 'À venir')))
            priorite = st.selectbox("*Priorité", st.session_state.config_admin['listes']['priorites'],
                                  index=st.session_state.config_admin['listes']['priorites'].index(projet.get('priorite', 'Moyenne')))
            categorie = st.selectbox("*Catégorie", st.session_state.config_admin['listes']['categories'],
                                   index=st.session_state.config_admin['listes']['categories'].index(projet.get('categorie', 'Business')))
            
            echeance_actuelle = projet.get('echeance', date.today())
            if isinstance(echeance_actuelle, str):
                try:
                    echeance_actuelle = datetime.strptime(echeance_actuelle, '%Y-%m-%d').date()
                except:
                    echeance_actuelle = date.today()
            
            echeance = st.date_input("*Échéance", value=echeance_actuelle)
            
            sources_disponibles = ["Non défini"] + [r['nom'] for r in st.session_state.revenus]
            source_actuelle = safe_get(projet, 'source_financement', 'Non défini')
            source_index = sources_disponibles.index(source_actuelle) if source_actuelle in sources_disponibles else 0
            source_financement = st.selectbox("Source de financement", sources_disponibles, index=source_index)
            
            responsables = st.session_state.config_admin['listes']['responsables']
            responsable_actuel = safe_get(projet, 'responsable', 'Famille')
            responsable_index = responsables.index(responsable_actuel) if responsable_actuel in responsables else 0
            responsable = st.selectbox("*Responsable", responsables, index=responsable_index)
        
        description = st.text_area("Description", value=projet.get('description', ''))
        montant_utilise = st.number_input("Montant utilisé réel (FCFA)", min_value=0, 
                                        value=int(projet.get('montant_utilise_reel', 0)), step=1000)
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("✅ Sauvegarder", type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Annuler")
        
        if submitted:
            # Validation
            champs_obligatoires = {
                'nom': nom,
                'montant_total': montant_total
            }
            
            champs_manquants = [k for k, v in champs_obligatoires.items() if not v or (k == 'montant_total' and v <= 0)]
            
            if champs_manquants:
                champs_manquants_str = ", ".join([
                    "Nom" if k == "nom" else "Budget total" if k == "montant_total" else k
                    for k in champs_manquants
                ])
                st.error(f"⚠️ Champs manquants ou invalides: {champs_manquants_str}")
                return
            
            # Mise à jour
            for p in st.session_state.projets:
                if p.get('id') == st.session_state.edit_project_id:
                    p.update({
                        'nom': nom,
                        'type': type_projet,
                        'montant_total': int(montant_total),
                        'montant_utilise_reel': int(montant_utilise),
                        'cash_flow_mensuel': int(cash_flow),
                        'roi_attendu': float(roi_attendu),
                        'statut': statut,
                        'priorite': priorite,
                        'echeance': echeance,
                        'categorie': categorie,
                        'description': description,
                        'source_financement': source_financement,
                        'responsable': responsable,
                        'date_modification': datetime.now()
                    })
                    break
            
            st.session_state.edit_project_id = None
            st.success("✅ Projet mis à jour avec succès!")
            st.rerun()
        
        if cancel:
            st.session_state.edit_project_id = None
            st.rerun()

def show_revenue_management():
    """Gestion des revenus variables"""
    st.markdown('<div class="main-header"><h1>💰 Gestion des Revenus Variables</h1></div>', unsafe_allow_html=True)
    
    # Si en mode édition
    if st.session_state.edit_revenue_id:
        show_edit_revenue_form()
        return
    
    # Boutons et filtres
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("➕ Ajouter un nouveau revenu", type="primary"):
            st.session_state.show_add_revenue_form = True
    
    with col2:
        type_filter = st.selectbox("Type", ["Tous"] + st.session_state.config_admin['listes']['types_revenus'])
    
    with col3:
        mois_filter = st.selectbox("Mois", ["Tous"] + ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                                                      "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"])
    
    # Formulaire d'ajout
    if st.session_state.get('show_add_revenue_form', False):
        show_add_revenue_form()
    
    st.markdown("---")
    
    # Affichage des revenus avec filtres
    revenus_filtres = st.session_state.revenus
    if type_filter != "Tous":
        revenus_filtres = [r for r in revenus_filtres if r.get('type') == type_filter]
    if mois_filter != "Tous":
        revenus_filtres = [r for r in revenus_filtres if r.get('mois') == mois_filter]
    
    if not revenus_filtres:
        st.info("Aucun revenu trouvé avec les filtres sélectionnés.")
        return
    
    # Calcul du total
    total_revenus = sum(r.get('montant', 0) for r in revenus_filtres)
    st.metric("💰 Total des revenus affichés", f"{total_revenus:,.0f} FCFA")
    
    st.markdown("---")
    
    for revenu in revenus_filtres:
        show_revenue_card(revenu)

def show_add_revenue_form():
    """Formulaire d'ajout de revenu"""
    st.subheader("➕ Nouveau Revenu")
    
    with st.form("add_revenue_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("*Nom du revenu", help="Ex: Bonus William février")
            type_revenu = st.selectbox("*Type", st.session_state.config_admin['listes']['types_revenus'])
            montant = st.number_input("*Montant (FCFA)", min_value=0, value=0, step=1000)
        
        with col2:
            mois = st.selectbox("*Mois", ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                                        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"])
            annee = st.number_input("*Année", min_value=2020, max_value=2030, value=2025, step=1)
            responsable = st.selectbox("*Responsable", st.session_state.config_admin['listes']['responsables'])
        
        recurrent = st.checkbox("Revenu récurrent", help="Ce revenu se répète-t-il chaque mois ?")
        description = st.text_area("Description", help="Description optionnelle du revenu")
        
        submitted = st.form_submit_button("✅ Ajouter le revenu", type="primary")
        cancel = st.form_submit_button("❌ Annuler")
        
        if submitted:
            # Validation améliorée
            champs_obligatoires = {
                'nom': nom,
                'type_revenu': type_revenu,
                'montant': montant,
                'responsable': responsable
            }
            
            champs_manquants = [k for k, v in champs_obligatoires.items() if not v or (k == 'montant' and v <= 0)]
            
            if champs_manquants:
                champs_manquants_str = ", ".join([
                    "Nom" if k == "nom" else
                    "Type" if k == "type_revenu" else
                    "Montant" if k == "montant" else
                    "Responsable" if k == "responsable" else k
                    for k in champs_manquants
                ])
                st.error(f"⚠️ Champs manquants: {champs_manquants_str}")
                return
            
            nouveau_revenu = {
                'id': str(uuid.uuid4()),
                'nom': nom,
                'type': type_revenu,
                'montant': int(montant),
                'mois': mois,
                'annee': int(annee),
                'recurrent': recurrent,
                'description': description,
                'responsable': responsable,
                'date_creation': datetime.now(),
                'date_modification': datetime.now()
            }
            
            st.session_state.revenus.append(nouveau_revenu)
            st.session_state.show_add_revenue_form = False
            st.success(f"✅ Revenu '{nom}' ajouté avec succès!")
            st.rerun()
        
        if cancel:
            st.session_state.show_add_revenue_form = False
            st.rerun()

def show_revenue_card(revenu):
    """Affiche une carte revenu"""
    type_icons = {
        'Salaire': '💼',
        'Business': '📈',
        'Loyer': '🏠',
        'Investissement': '📊',
        'Bonus': '🎁'
    }
    
    icon = type_icons.get(revenu.get('type', ''), '💰')
    
    with st.container():
        st.markdown(f"""
        <div class="project-card" style="border-left-color: #28a745;">
            <h4>{icon} {revenu.get('nom', 'Revenu')}</h4>
            <div style="color: #28a745; font-weight: bold;">Type: {revenu.get('type', 'Non défini')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"**💰 Montant:** {revenu.get('montant', 0):,.0f} FCFA")
            st.write(f"**📅 Période:** {revenu.get('mois', 'Non défini')} {revenu.get('annee', 'Non définie')}")
        
        with col2:
            st.write(f"**🔄 Récurrent:** {'Oui' if revenu.get('recurrent', False) else 'Non'}")
            st.write(f"**👤 Responsable:** {safe_get(revenu, 'responsable', 'Non défini')}")
        
        with col3:
            if safe_get(revenu, 'date_creation'):
                st.write(f"**📅 Créé:** {revenu['date_creation'].strftime('%d/%m/%Y')}")
            if safe_get(revenu, 'date_modification') and revenu['date_modification'] != revenu.get('date_creation'):
                st.write(f"**📝 Modifié:** {revenu['date_modification'].strftime('%d/%m/%Y')}")
        
        if revenu.get('description'):
            st.write(f"**📝 Description:** {revenu.get('description')}")
        
        # Boutons d'action
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️", key=f"edit_rev_{revenu.get('id', 'temp')}", help="Modifier"):
                st.session_state.edit_revenue_id = revenu.get('id')
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"delete_rev_{revenu.get('id', 'temp')}", help="Supprimer"):
                if st.session_state.get(f"confirm_delete_rev_{revenu.get('id')}", False):
                    st.session_state.revenus = [r for r in st.session_state.revenus if r.get('id') != revenu.get('id')]
                    if f"confirm_delete_rev_{revenu.get('id')}" in st.session_state:
                        del st.session_state[f"confirm_delete_rev_{revenu.get('id')}"]
                    st.success(f"Revenu '{revenu.get('nom')}' supprimé!")
                    st.rerun()
                else:
                    st.session_state[f"confirm_delete_rev_{revenu.get('id')}"] = True
                    st.warning("⚠️ Cliquez à nouveau pour confirmer")
        
        st.markdown("---")

def show_edit_revenue_form():
    """Formulaire d'édition de revenu"""
    revenu = next((r for r in st.session_state.revenus if r.get('id') == st.session_state.edit_revenue_id), None)
    
    if not revenu:
        st.error("Revenu introuvable")
        st.session_state.edit_revenue_id = None
        return
    
    st.subheader(f"✏️ Modifier: {revenu.get('nom', 'Revenu')}")
    
    with st.form("edit_revenue_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("*Nom du revenu", value=revenu.get('nom', ''))
            type_revenu = st.selectbox("*Type", st.session_state.config_admin['listes']['types_revenus'],
                                     index=st.session_state.config_admin['listes']['types_revenus'].index(revenu.get('type', 'Salaire')))
            montant = st.number_input("*Montant (FCFA)", min_value=0, value=int(revenu.get('montant', 0)), step=1000)
        
        with col2:
            mois_list = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
            mois_actuel = revenu.get('mois', 'Janvier')
            mois_index = mois_list.index(mois_actuel) if mois_actuel in mois_list else 0
            mois = st.selectbox("*Mois", mois_list, index=mois_index)
            
            annee = st.number_input("*Année", min_value=2020, max_value=2030, value=int(revenu.get('annee', 2025)), step=1)
            
            responsables = st.session_state.config_admin['listes']['responsables']
            responsable_actuel = safe_get(revenu, 'responsable', 'William')
            responsable_index = responsables.index(responsable_actuel) if responsable_actuel in responsables else 0
            responsable = st.selectbox("*Responsable", responsables, index=responsable_index)
        
        recurrent = st.checkbox("Revenu récurrent", value=revenu.get('recurrent', False))
        description = st.text_area("Description", value=revenu.get('description', ''))
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("✅ Sauvegarder", type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Annuler")
        
        if submitted:
            # Validation
            if not nom or not montant or montant <= 0:
                st.error("⚠️ Le nom et le montant sont obligatoires")
                return
            
            # Mise à jour
            for r in st.session_state.revenus:
                if r.get('id') == st.session_state.edit_revenue_id:
                    r.update({
                        'nom': nom,
                        'type': type_revenu,
                        'montant': int(montant),
                        'mois': mois,
                        'annee': int(annee),
                        'recurrent': recurrent,
                        'description': description,
                        'responsable': responsable,
                        'date_modification': datetime.now()
                    })
                    break
            
            st.session_state.edit_revenue_id = None
            st.success("✅ Revenu mis à jour avec succès!")
            st.rerun()
        
        if cancel:
            st.session_state.edit_revenue_id = None
            st.rerun()

def show_mentors_page():
    """Page conseils des 3 mentors avec sélection de projet"""
    st.markdown('<div class="main-header"><h1>🎯 Conseils des 3 Mentors Financiers</h1></div>', unsafe_allow_html=True)
    
    # Sélection de projet avec filtre par période
    mois_filtre = st.session_state.get('mois_filtre')
    annee_filtre = st.session_state.get('annee_filtre')
    
    projets_filtres = st.session_state.projets
    # Le filtre par période n'est pas directement applicable aux projets, mais on peut l'utiliser pour contextualiser
    
    if not projets_filtres:
        st.warning("Aucun projet disponible pour analyse.")
        return
    
    projet_noms = [f"{p.get('nom', 'Projet')} ({p.get('type', 'Type')})" for p in projets_filtres]
    
    selected_index = st.selectbox("Sélectionnez un projet à analyser", 
                                 range(len(projet_noms)),
                                 format_func=lambda x: projet_noms[x])
    
    projet_selectionne = projets_filtres[selected_index]
    
    st.markdown("---")
    
    # Affichage des conseils des 3 mentors
    show_mentors_advice(projet_selectionne, detailed=True)

def show_mentors_advice(projet, detailed=False):
    """Affiche les conseils des 3 mentors pour un projet"""
    type_projet = projet.get('type', 'Actif générateur')
    
    if detailed:
        st.subheader(f"🎯 Analyse du projet: {projet.get('nom', 'Projet')}")
        
        # Résumé du projet
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 Budget", f"{projet.get('montant_total', 0):,.0f} FCFA")
        with col2:
            st.metric("📈 Cash Flow", f"{projet.get('cash_flow_mensuel', 0):,.0f} FCFA/mois")
        with col3:
            st.metric("🎯 ROI", f"{projet.get('roi_attendu', 0):.1f}%")
    
    # Conseils Robert Kiyosaki
    conseil_kiyosaki = st.session_state.config_admin['conseils_mentors']['kiyosaki'].get(
        type_projet, "Analysez si ce projet vous fait passer du quadrant E vers B ou I."
    )
    
    st.markdown(f"""
    <div class="mentor-kiyosaki">
        <h4>💎 Robert Kiyosaki - "Père Riche, Père Pauvre"</h4>
        <p><strong>Focus Quadrants E-S-B-I:</strong></p>
        <p>{conseil_kiyosaki}</p>
        <p><em>💡 Vocabulaire: Remplacez "dépense" par "passif" et "revenu" par "flux de trésorerie"</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Conseils Warren Buffett
    conseil_buffett = st.session_state.config_admin['conseils_mentors']['buffett'].get(
        type_projet, "Investissez seulement dans ce que vous comprenez parfaitement."
    )
    
    st.markdown(f"""
    <div class="mentor-buffett">
        <h4>🎯 Warren Buffett - "L'Oracle d'Omaha"</h4>
        <p><strong>Focus Valeur Long Terme:</strong></p>
        <p>{conseil_buffett}</p>
        <p><em>💡 Question clé: "Seriez-vous prêt à garder cet investissement 10 ans ?"</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Conseils Dave Ramsey
    conseil_ramsey = st.session_state.config_admin['conseils_mentors']['ramsey'].get(
        type_projet, "Respectez votre budget et évitez les dettes. Priorité au fonds d'urgence."
    )
    
    st.markdown(f"""
    <div class="mentor-ramsey">
        <h4>💪 Dave Ramsey - "Baby Steps"</h4>
        <p><strong>Focus Discipline Budgétaire:</strong></p>
        <p>{conseil_ramsey}</p>
        <p><em>💡 Règle d'or: 50% besoins, 30% envies, 20% épargne/investissement</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    if detailed:
        # Synthèse consensus
        st.markdown("""
        <div class="success-box">
            <h4>🤝 Synthèse des 3 Mentors</h4>
            <p><strong>Consensus:</strong> Analysez ce projet selon trois critères:</p>
            <ul>
                <li><strong>Kiyosaki:</strong> Est-ce un actif qui génère des revenus passifs ?</li>
                <li><strong>Buffett:</strong> Comprenez-vous parfaitement ce business ?</li>
                <li><strong>Ramsey:</strong> Respectez-vous votre discipline budgétaire ?</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_analytics():
    """Page Analytics & KPIs Avancés avec filtre période"""
    st.markdown('<div class="main-header"><h1>📊 Analytics & KPIs Avancés</h1></div>', unsafe_allow_html=True)
    
    # Récupération des filtres
    mois_filtre = st.session_state.get('mois_filtre')
    annee_filtre = st.session_state.get('annee_filtre')
    
    # Calcul des KPIs avec filtre
    kpis = calculer_kpis(st.session_state.projets, st.session_state.revenus, mois_filtre, annee_filtre)
    
    # Affichage période active
    periode = "Toutes les données"
    if mois_filtre and mois_filtre != "Tout" and annee_filtre and annee_filtre != "Tout":
        periode = f"{mois_filtre} {annee_filtre}"
    elif mois_filtre and mois_filtre != "Tout":
        periode = f"Tous les {mois_filtre}"
    elif annee_filtre and annee_filtre != "Tout":
        periode = f"Année {annee_filtre}"
    
    st.info(f"📅 **Analyse pour :** {periode}")
    
    # Tableau Passifs vs Actifs selon Kiyosaki
    st.subheader("💎 Analyse Kiyosaki - Actifs vs Passifs")
    
    quadrant, status_rat = determiner_quadrant_kiyosaki(st.session_state.projets, st.session_state.revenus)
    
    # Tableau comparatif
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 ACTIFS (mettent de l'argent dans votre poche)")
        actifs_data = []
        for projet in st.session_state.projets:
            if projet.get('cash_flow_mensuel', 0) > 0:
                actifs_data.append({
                    'Nom': projet.get('nom', ''),
                    'Cash Flow/mois': f"{projet.get('cash_flow_mensuel', 0):,.0f} FCFA",
                    'ROI': f"{projet.get('roi_attendu', 0):.1f}%"
                })
        
        if actifs_data:
            df_actifs = pd.DataFrame(actifs_data)
            st.dataframe(df_actifs, use_container_width=True)
            total_actifs_cashflow = sum(p.get('cash_flow_mensuel', 0) for p in st.session_state.projets if p.get('cash_flow_mensuel', 0) > 0)
            st.success(f"💰 Total revenus passifs: {total_actifs_cashflow:,.0f} FCFA/mois")
        else:
            st.warning("❌ Aucun actif générateur identifié")
    
    with col2:
        st.markdown("#### 📉 PASSIFS (sortent de l'argent de votre poche)")
        passifs_data = []
        for projet in st.session_state.projets:
            if projet.get('cash_flow_mensuel', 0) < 0:
                passifs_data.append({
                    'Nom': projet.get('nom', ''),
                    'Cash Flow/mois': f"{projet.get('cash_flow_mensuel', 0):,.0f} FCFA",
                    'Budget Total': f"{projet.get('montant_total', 0):,.0f} FCFA"
                })
        
        if passifs_data:
            df_passifs = pd.DataFrame(passifs_data)
            st.dataframe(df_passifs, use_container_width=True)
            total_passifs_cashflow = abs(sum(p.get('cash_flow_mensuel', 0) for p in st.session_state.projets if p.get('cash_flow_mensuel', 0) < 0))
            st.error(f"💸 Total sorties: {total_passifs_cashflow:,.0f} FCFA/mois")
        else:
            st.info("✅ Aucun passif identifié")
    
    # Quadrants E-S-B-I de Kiyosaki
    st.markdown("---")
    st.subheader("🎯 Quadrants Kiyosaki E-S-B-I")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Calcul des pourcentages par quadrant
        revenus_par_type = {}
        for revenu in st.session_state.revenus:
            type_rev = revenu.get('type', 'Autre')
            revenus_par_type[type_rev] = revenus_par_type.get(type_rev, 0) + revenu.get('montant', 0)
        
        quadrants_data = {
            'E - Employee (Salaire)': revenus_par_type.get('Salaire', 0),
            'S - Self Employed (Business actif)': revenus_par_type.get('Business', 0),
            'B - Business Owner (Système)': revenus_par_type.get('Loyer', 0),
            'I - Investor (Passif)': revenus_par_type.get('Investissement', 0)
        }
        
        if any(quadrants_data.values()):
            fig_quadrants = px.pie(
                values=list(quadrants_data.values()),
                names=list(quadrants_data.keys()),
                title="Répartition des revenus par Quadrant Kiyosaki"
            )
            st.plotly_chart(fig_quadrants, use_container_width=True)
        else:
            st.info("Aucune donnée de revenus disponible pour l'analyse des quadrants")
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <h3>Position Actuelle</h3>
            <h2 style="color: {'#dc3545' if 'Rat' in status_rat else '#28a745' if 'Liberté' in status_rat else '#ffc107'};">
                Quadrant {quadrant}
            </h2>
            <p>{status_rat}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Recommandations selon quadrant
        if quadrant == "E":
            st.warning("🎯 **Objectif:** Développer des revenus B et I pour sortir de la Rat Race")
        elif quadrant == "S/B":
            st.info("🔄 **En transition:** Continuez à développer des systèmes et investissements")
        elif quadrant == "I":
            st.success("🎉 **Bravo!** Vous êtes sur la voie de l'indépendance financière")
        else:
            st.info("📊 **Portfolio mixte:** Équilibrez davantage vers B et I")
    
    # KPIs détaillés avec filtres
    st.markdown("---")
    st.subheader(f"📊 KPIs Détaillés - {periode}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Investissements", f"{kpis['total_investissements']:,.0f} FCFA")
        st.metric("📈 Actifs Générateurs", f"{kpis['nombre_actifs']} projets")
    
    with col2:
        st.metric("💸 Total Passifs", f"{kpis['total_passifs']:,.0f} FCFA") 
        st.metric("🏦 Fonds d'Urgence", f"{kpis['fonds_urgence']:,.0f} FCFA")
    
    with col3:
        st.metric("📊 Ratio Actifs/Passifs", f"{kpis['ratio_actifs_passifs']:.1f}%")
        st.metric("🎯 Revenus Passifs", f"{kpis['ratio_revenus_passifs']:.1f}%")
    
    with col4:
        st.metric("💵 Cash Flow Net", f"{kpis['cash_flow_mensuel']:,.0f} FCFA/mois")
        st.metric("👶 Baby Step", f"Étape {kpis['baby_step']}")
    
    # Graphiques avancés
    col1, col2 = st.columns(2)
    
    with col1:
        # Évolution projetée 
        mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
        cash_flow_evolution = []
        base_cf = kpis['cash_flow_mensuel']
        
        for i, m in enumerate(mois):
            # Simulation d'évolution avec croissance progressive
            variation = base_cf * (1 + i * 0.05)  # 5% croissance par mois
            cash_flow_evolution.append(variation)
        
        fig_evolution = px.line(x=mois, y=cash_flow_evolution, 
                               title=f"Projection Cash Flow 2025 - {periode}")
        fig_evolution.add_hline(y=0, line_dash="dash", line_color="red", 
                               annotation_text="Seuil rentabilité")
        st.plotly_chart(fig_evolution, use_container_width=True)
    
    with col2:
        # Répartition par catégorie
        categories = {}
        for projet in st.session_state.projets:
            cat = projet.get('categorie', 'Autre')
            categories[cat] = categories.get(cat, 0) + projet.get('montant_total', 0)
        
        if categories:
            fig_categories = px.bar(x=list(categories.keys()), y=list(categories.values()),
                                   title=f"Investissements par Catégorie - {periode}")
            st.plotly_chart(fig_categories, use_container_width=True)

def show_progression():
    """Page progression familiale vers indépendance"""
    st.markdown('<div class="main-header"><h1>🚀 Progression Familiale</h1></div>', unsafe_allow_html=True)
    
    # Calcul des KPIs avec filtre
    mois_filtre = st.session_state.get('mois_filtre')
    annee_filtre = st.session_state.get('annee_filtre')
    kpis = calculer_kpis(st.session_state.projets, st.session_state.revenus, mois_filtre, annee_filtre)
    
    # Baby Steps Dave Ramsey
    st.subheader("👶 Baby Steps Dave Ramsey")
    
    # Information sur les Baby Steps
    st.markdown("""
    <div class="info-tooltip">
        <h4>ℹ️ Les 7 Baby Steps de Dave Ramsey</h4>
        <p>Méthodologie éprouvée pour atteindre l'indépendance financière étape par étape.</p>
    </div>
    """, unsafe_allow_html=True)
    
    baby_steps = [
        {"num": 1, "titre": "Fonds d'urgence de démarrage", "montant": 500000, "description": "500k FCFA pour les petites urgences"},
        {"num": 2, "titre": "Éliminer toutes les dettes", "montant": 0, "description": "Sauf la résidence principale"},
        {"num": 3, "titre": "Fonds d'urgence complet", "montant": abs(kpis['cash_flow_mensuel']) * 6, "description": "3-6 mois de dépenses"},
        {"num": 4, "titre": "Investir 15% revenus", "montant": kpis['total_revenus'] * 0.15, "description": "Pour la retraite"},
        {"num": 5, "titre": "Épargne université enfants", "montant": 2000000, "description": "Fonds éducation Uriel, Naelle, Nell-Henri"},
        {"num": 6, "titre": "Rembourser résidence", "montant": 0, "description": "Propriété sans dette"},
        {"num": 7, "titre": "Construire richesse", "montant": 10000000, "description": "Investir et donner"}
    ]
    
    current_step = kpis['baby_step']
    
    for step in baby_steps:
        statut = "✅ Terminé" if step['num'] < current_step else "🔄 En cours" if step['num'] == current_step else "⏳ À venir"
        couleur = "#28a745" if step['num'] < current_step else "#ffc107" if step['num'] == current_step else "#6c757d"
        
        st.markdown(f"""
        <div style="border-left: 4px solid {couleur}; padding: 1rem; margin: 0.5rem 0; background: {'#d4edda' if step['num'] < current_step else '#fff3cd' if step['num'] == current_step else '#f8f9fa'};">
            <h4>Baby Step {step['num']}: {step['titre']} {statut}</h4>
            <p>{step['description']}</p>
            {f"<strong>Objectif: {step['montant']:,.0f} FCFA</strong>" if step['montant'] > 0 else ""}
        </div>
        """, unsafe_allow_html=True)
    
    # Information fonds d'urgence
    st.markdown("""
    <div class="warning-box">
        <h4>💡 Comment mesurer le fonds d'urgence ?</h4>
        <p><strong>Deux options pour créer votre fonds d'urgence :</strong></p>
        <ul>
            <li><strong>Option 1:</strong> Créer un projet spécifique "Fonds d'urgence" avec le montant cible</li>
            <li><strong>Option 2:</strong> Utiliser un compte épargne séparé (recommandé)</li>
        </ul>
        <p><strong>Calcul automatique:</strong> Le système détecte automatiquement les projets contenant "urgence" dans le nom.</p>
        <p><strong>Objectif actuel:</strong> {abs(kpis['cash_flow_mensuel']) * 6:,.0f} FCFA (6 mois de dépenses courantes)</p>
    </div>
    """.format(**kpis), unsafe_allow_html=True)
    
    # Progression vers indépendance
    st.markdown("---")
    st.subheader("🎯 Progression Familiale vers l'Indépendance")
    
    # Calcul du pourcentage d'indépendance
    revenus_passifs_requis = abs(kpis['cash_flow_mensuel']) * 1.2  # 120% pour marge de sécurité
    pct_independance = min((kpis['revenus_passifs'] / max(revenus_passifs_requis, 1)) * 100, 100) if revenus_passifs_requis > 0 else 0
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {pct_independance}%; background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1);"></div>
        </div>
        <p style="text-align: center; margin-top: 0.5rem;"><strong>{pct_independance:.1f}% vers l'indépendance financière</strong></p>
        """, unsafe_allow_html=True)
    
    with col2:
        phase_couleurs = {"Stabilisation": "#dc3545", "Transition": "#ffc107", "Expansion": "#28a745"}
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <h3>Phase Actuelle</h3>
            <h2 style="color: {phase_couleurs.get(kpis['phase'], '#20b2aa')};">{kpis['phase']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Étapes pour passer à la phase suivante
    st.markdown("""
    <div class="info-tooltip">
        <h4>📋 Comment passer à la phase suivante ?</h4>
        <p><strong>Stabilisation → Transition :</strong></p>
        <ul>
            <li>Cash flow mensuel positif ou proche de zéro</li>
            <li>Au moins 20% d'actifs générateurs</li>
            <li>Fonds d'urgence constitué</li>
        </ul>
        <p><strong>Transition → Expansion :</strong></p>
        <ul>
            <li>Cash flow mensuel durablement positif</li>
            <li>Plus de 40% d'actifs générateurs</li>
            <li>Revenus passifs couvrant 50%+ des dépenses</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Règle 50/30/20
    st.markdown("---")
    st.subheader("📊 Règle 50/30/20 de Dave Ramsey")
    
    total_revenus = kpis['total_revenus']
    if total_revenus > 0:
        besoins_max = total_revenus * 0.5
        envies_max = total_revenus * 0.3
        epargne_min = total_revenus * 0.2
        
        # Calcul réel
        besoins_reel = sum(p.get('montant_total', 0) for p in st.session_state.projets 
                          if p.get('categorie') in ['Éducation', 'Personnel'] or 'essentiel' in p.get('description', '').lower())
        envies_reel = sum(p.get('montant_total', 0) for p in st.session_state.projets 
                         if p.get('categorie') == 'Familial' or p.get('type') == 'Passif')
        epargne_reel = sum(p.get('montant_total', 0) for p in st.session_state.projets 
                          if p.get('type') == 'Actif générateur')
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            respect_besoins = besoins_reel <= besoins_max
            couleur = "#28a745" if respect_besoins else "#dc3545"
            st.markdown(f"""
            <div style="border: 2px solid {couleur}; padding: 1rem; border-radius: 8px;">
                <h4>🏠 BESOINS (50%)</h4>
                <p><strong>Budget:</strong> {besoins_max:,.0f} FCFA</p>
                <p><strong>Réel:</strong> {besoins_reel:,.0f} FCFA</p>
                <p style="color: {couleur};"><strong>{'✅ Respecté' if respect_besoins else '❌ Dépassé'}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            respect_envies = envies_reel <= envies_max
            couleur = "#28a745" if respect_envies else "#dc3545"
            st.markdown(f"""
            <div style="border: 2px solid {couleur}; padding: 1rem; border-radius: 8px;">
                <h4>🎯 ENVIES (30%)</h4>
                <p><strong>Budget:</strong> {envies_max:,.0f} FCFA</p>
                <p><strong>Réel:</strong> {envies_reel:,.0f} FCFA</p>
                <p style="color: {couleur};"><strong>{'✅ Respecté' if respect_envies else '❌ Dépassé'}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            respect_epargne = epargne_reel >= epargne_min
            couleur = "#28a745" if respect_epargne else "#dc3545"
            st.markdown(f"""
            <div style="border: 2px solid {couleur}; padding: 1rem; border-radius: 8px;">
                <h4>💰 ÉPARGNE (20%)</h4>
                <p><strong>Minimum:</strong> {epargne_min:,.0f} FCFA</p>
                <p><strong>Réel:</strong> {epargne_reel:,.0f} FCFA</p>
                <p style="color: {couleur};"><strong>{'✅ Respecté' if respect_epargne else '❌ Insuffisant'}</strong></p>
            </div>
            """, unsafe_allow_html=True)
    
    # Évolution par période
    st.markdown("---")
    st.subheader("📈 Évolution par Période")
    
    # Texte explicatif
    st.markdown("""
    <div class="info-tooltip">
        <h4>📖 Comment lire ces graphiques ?</h4>
        <p><strong>Graphique 1 - Évolution Cash Flow:</strong> Montre l'évolution de votre cash flow mensuel. 
        Objectif: ligne au-dessus de zéro (cash flow positif).</p>
        <p><strong>Graphique 2 - Progression Actifs/Passifs:</strong> Montre l'équilibre entre vos actifs (qui rapportent) 
        et passifs (qui coûtent). Objectif: plus d'actifs que de passifs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Génération résumé dynamique basé sur les données
    periode_actuelle = "toutes les données"
    if mois_filtre and mois_filtre != "Tout":
        periode_actuelle = f"le mois de {mois_filtre.lower()}"
    if annee_filtre and annee_filtre != "Tout":
        periode_actuelle = f"l'année {annee_filtre}"
    
    # Analyse dynamique simple (sans IA)
    tendance_cash_flow = "positive" if kpis['cash_flow_mensuel'] > 0 else "négative"
    niveau_actifs = "élevé" if kpis['ratio_actifs_passifs'] > 50 else "moyen" if kpis['ratio_actifs_passifs'] > 20 else "faible"
    
    st.markdown(f"""
    <div class="success-box" style="background: #e3f2fd; border-color: #2196f3;">
        <h4>🤖 Analyse Dynamique - {periode_actuelle.title()}</h4>
        <p><strong>Tendance Cash Flow:</strong> {tendance_cash_flow.upper()} 
        ({kpis['cash_flow_mensuel']:,.0f} FCFA/mois)</p>
        <p><strong>Niveau d'actifs:</strong> {niveau_actifs.upper()} 
        ({kpis['ratio_actifs_passifs']:.1f}% ratio actifs/passifs)</p>
        <p><strong>Recommandation:</strong> 
        {"Continuez sur cette voie, votre situation s'améliore!" if tendance_cash_flow == "positive" else "Concentrez-vous sur la création d'actifs générateurs de revenus."}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Graphiques évolution
    col1, col2 = st.columns(2)
    
    with col1:
        mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
        # Simulation évolution cash flow
        cf_evolution = []
        base_cf = kpis['cash_flow_mensuel']
        for i in range(12):
            variation = base_cf + (i * 50000) + np.random.randint(-100000, 150000)
            cf_evolution.append(variation)
        
        fig_cf = px.line(x=mois, y=cf_evolution, title="Évolution Cash Flow Mensuel")
        fig_cf.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_cf, use_container_width=True)
    
    with col2:
        # Évolution ratio actifs/passifs
        ratios = []
        base_ratio = kpis['ratio_actifs_passifs']
        for i in range(12):
            nouveau_ratio = base_ratio + (i * 2) + np.random.uniform(-5, 10)
            ratios.append(max(0, nouveau_ratio))
        
        fig_ratio = px.bar(x=mois, y=ratios, title="Évolution Ratio Actifs/Passifs (%)")
        fig_ratio.add_hline(y=50, line_dash="dash", line_color="green", annotation_text="Objectif 50%")
        st.plotly_chart(fig_ratio, use_container_width=True)

def show_education():
    """Page éducation financière des enfants"""
    st.markdown('<div class="main-header"><h1>👨‍👩‍👧‍👦 Éducation Financière des Enfants</h1></div>', unsafe_allow_html=True)
    
    # Calcul des âges selon l'année filtrée
    annee_filtre = st.session_state.get('annee_filtre', 2025)
    if annee_filtre == "Tout":
        annee_reference = 2025
    else:
        annee_reference = int(annee_filtre) if isinstance(annee_filtre, str) and annee_filtre.isdigit() else annee_filtre
    
    # Âges de base en 2025
    ages_2025 = {"Uriel": 14, "Naelle": 7, "Nell-Henri": 5}
    difference_annee = annee_reference - 2025
    
    ages_actuels = {enfant: age + difference_annee for enfant, age in ages_2025.items()}
    
    st.info(f"📅 **Âges pour l'année {annee_reference}:** Uriel ({ages_actuels['Uriel']} ans), Naelle ({ages_actuels['Naelle']} ans), Nell-Henri ({ages_actuels['Nell-Henri']} ans)")
    
    # Programme par enfant
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="project-card" style="border-left-color: #ff6b6b;">
            <h3>🎨 Uriel ({ages_actuels['Uriel']} ans)</h3>
            <h4>Programme Avancé</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if ages_actuels['Uriel'] >= 14:
            st.write("**📚 Concepts à enseigner:**")
            st.write("• Différence Actifs vs Passifs")
            st.write("• Quadrants E-S-B-I de Kiyosaki")
            st.write("• ROI et Cash Flow")
            st.write("• Business plan simple")
            
            st.write("**🎯 Activités pratiques:**")
            st.write("• Jeu Cashflow de Kiyosaki")
            st.write("• Création business artistique")
            st.write("• Participation décisions familiales")
            st.write("• Gestion compte bancaire")
        else:
            st.write(f"**Programme adapté pour {ages_actuels['Uriel']} ans:**")
            st.write("• Valeur de l'argent")
            st.write("• Épargne vs dépense")
            st.write("• Premiers choix financiers")
    
    with col2:
        st.markdown(f"""
        <div class="project-card" style="border-left-color: #4ecdc4;">
            <h3>🌟 Naelle ({ages_actuels['Naelle']} ans)</h3>
            <h4>Programme Intermédiaire</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if ages_actuels['Naelle'] >= 7:
            st.write("**📚 Concepts à enseigner:**")
            st.write("• Épargne vs dépense")
            st.write("• Notion 'argent qui travaille'")
            st.write("• Besoins vs envies")
            st.write("• Patience financière")
            
            st.write("**🎯 Activités pratiques:**")
            st.write("• Tirelire transparente")
            st.write("• Premiers choix d'achat")
            st.write("• Jeux éducatifs financiers")
            st.write("• Identification des 'actifs'")
        else:
            st.write(f"**Programme adapté pour {ages_actuels['Naelle']} ans:**")
            st.write("• Reconnaissance des pièces/billets")
            st.write("• Concept simple d'échange")
            st.write("• Patience et attente")
    
    with col3:
        st.markdown(f"""
        <div class="project-card" style="border-left-color: #45b7d1;">
            <h3>⭐ Nell-Henri ({ages_actuels['Nell-Henri']} ans)</h3>
            <h4>Programme Découverte</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if ages_actuels['Nell-Henri'] >= 5:
            st.write("**📚 Concepts à enseigner:**")
            st.write("• Valeur de l'argent")
            st.write("• Garder vs dépenser")
            st.write("• Concept simple d'échange")
            st.write("• 'Sous qui rapportent des sous'")
            
            st.write("**🎯 Activités pratiques:**")
            st.write("• Jeux avec pièces/billets")
            st.write("• Premier 'investissement' (livre)")
            st.write("• Comptage simple")
            st.write("• Observation des achats")
        else:
            st.write(f"**Programme adapté pour {ages_actuels['Nell-Henri']} ans:**")
            st.write("• Reconnaissance des couleurs/formes")
            st.write("• Jeux sensoriels avec objets")
            st.write("• Concept très simple d'échange")
    
    # Planning éducatif annuel
    st.markdown("---")
    st.subheader(f"📅 Planning Éducatif {annee_reference}")
    
    mois_activites = [
        {"mois": "Janvier", "activite": "Lancement tirelires & objectifs annuels", "enfants": "Tous"},
        {"mois": "Février", "activite": "Jeu 'Besoins vs Envies' en famille", "enfants": "Naelle + Nell-Henri"},
        {"mois": "Mars", "activite": "Première sortie 'éducation financière'", "enfants": "Tous"},
        {"mois": "Avril", "activite": "Visite banque éducative", "enfants": "Uriel + Naelle"},
        {"mois": "Mai", "activite": "Business plan artistique Uriel", "enfants": "Uriel"},
        {"mois": "Juin", "activite": "Jeu Cashflow familial", "enfants": "Tous"},
        {"mois": "Juillet", "activite": "Évaluation mi-année des objectifs", "enfants": "Tous"},
        {"mois": "Août", "activite": "Préparation budget rentrée", "enfants": "Uriel + Naelle"},
        {"mois": "Septembre", "activite": "Nouvelle tirelire projet spécial", "enfants": "Tous"},
        {"mois": "Octobre", "activite": "Exposition art Uriel & gestion finances", "enfants": "Uriel"},
        {"mois": "Novembre", "activite": "Préparation budget Noël", "enfants": "Tous"},
        {"mois": "Décembre", "activite": "Bilan annuel & objectifs année suivante", "enfants": "Tous"}
    ]
    
    for activite in mois_activites:
        with st.expander(f"{activite['mois']} - {activite['activite']}"):
            st.write(f"**👥 Enfants concernés:** {activite['enfants']}")
            
            if activite['mois'] == "Janvier":
                st.write("**📋 Détails:** Chaque enfant définit un objectif d'épargne adapté à son âge. Uriel peut viser l'achat d'un matériel artistique, Naelle un jouet éducatif, Nell-Henri des autocollants.")
            elif activite['mois'] == "Mai" and ages_actuels['Uriel'] >= 14:
                st.write("**📋 Détails:** Uriel développe un business plan pour ses créations artistiques : coûts matériaux, prix de vente, marge, réinvestissement.")
            elif activite['mois'] == "Juin":
                st.write("**📋 Détails:** Version simplifiée du jeu Cashflow adaptée aux différents âges. Focus sur les concepts actifs/passifs.")
            elif activite['mois'] == "Octobre" and ages_actuels['Uriel'] >= 14:
                st.write("**📋 Détails:** Uriel gère intégralement les aspects financiers de son exposition : budget, revenus, bénéfices, réinvestissement.")
            else:
                st.write("**📋 Détails:** Activité adaptée aux âges et capacités de chaque enfant, avec support parental selon besoin.")
            
            # Statut de l'activité
            mois_actuel = datetime.now().month
            mois_index = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                         "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"].index(activite['mois']) + 1
            
            if annee_reference == 2025:
                if mois_index < mois_actuel:
                    st.success("✅ **Statut:** Complété")
                elif mois_index == mois_actuel:
                    st.warning("🔄 **Statut:** En cours")
                else:
                    st.info("⏳ **Statut:** À venir")
            else:
                st.info(f"📅 **Statut:** Planifié pour {annee_reference}")
    
    # Ressources et outils
    st.markdown("---")
    st.subheader("📚 Ressources & Outils Recommandés")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📖 Livres adaptés par âge:**")
        st.write("• **Uriel:** 'Père Riche, Père Pauvre pour Ados'")
        st.write("• **Naelle:** 'Mon premier livre sur l'argent'")
        st.write("• **Nell-Henri:** Livres imagés sur les échanges")
        
        st.markdown("**🎮 Jeux éducatifs:**")
        st.write("• Jeu Cashflow de Kiyosaki (version famille)")
        st.write("• Jeux de plateau sur l'argent")
        st.write("• Applications éducatives financières")
    
    with col2:
        st.markdown("**🛠️ Outils pratiques:**")
        st.write("• Tirelires transparentes pour visualisation")
        st.write("• Tableau de suivi des objectifs")
        st.write("• Carnets de compte simplifiés")
        
        st.markdown("**🎯 Objectifs 2025:**")
        if ages_actuels['Uriel'] >= 14:
            st.write("• Uriel: Premier revenu business artistique")
        st.write("• Naelle: Première épargne objectif (100k FCFA)")
        st.write("• Nell-Henri: Compréhension pièces/billets")

def show_vision_2030():
    """Page vision long terme 2030"""
    st.markdown('<div class="main-header"><h1>🔮 Vision Familiale 2030</h1></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
        <h3>🎯 Objectif Principal: Toute la famille en Suisse d'ici 2030</h3>
        <p>Planification stratégique pour une migration familiale réussie avec indépendance financière.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Âges des enfants en 2030
    ages_2030 = {"Uriel": 19, "Naelle": 12, "Nell-Henri": 10}
    
    st.subheader("👨‍👩‍👧‍👦 Situation Familiale en 2030")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>🎓 Uriel (19 ans)</h4>
            <p><strong>Situation:</strong> Université en Suisse</p>
            <p><strong>Coût estimé:</strong> 25,000 CHF/an</p>
            <p><strong>Statut:</strong> Étudiant indépendant</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>🏫 Naelle (12 ans)</h4>
            <p><strong>Situation:</strong> Collège Suisse</p>
            <p><strong>Coût estimé:</strong> 15,000 CHF/an</p>
            <p><strong>Statut:</strong> Adolescence</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>🎒 Nell-Henri (10 ans)</h4>
            <p><strong>Situation:</strong> École primaire Suisse</p>
            <p><strong>Coût estimé:</strong> 12,000 CHF/an</p>
            <p><strong>Statut:</strong> Enfance</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Calculs financiers 2030
    st.markdown("---")
    st.subheader("💰 Projection Financière 2030")
    
    # Coûts annuels en Suisse
    cout_vie_suisse = {
        'Logement famille': 180000,  # 18k CHF
        'Université Uriel': 166700,   # 25k CHF  
        'Scolarité Naelle': 100000,  # 15k CHF
        'Scolarité Nell-Henri': 80000, # 12k CHF
        'Vie courante famille': 200000, # 20k CHF
        'Assurances & taxes': 66700,   # 10k CHF
        'Transport': 33300,           # 5k CHF
        'Loisirs & vacances': 50000,  # 7.5k CHF
        'Divers & urgences': 33300    # 5k CHF
    }
    
    total_cout_annuel_2030 = sum(cout_vie_suisse.values())  # ~910k CHF = ~606M FCFA
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**💸 Coûts Annuels 2030 (FCFA)**")
        for categorie, montant in cout_vie_suisse.items():
            montant_fcfa = montant * 667  # Taux approximatif CHF/FCFA
            st.write(f"• **{categorie}:** {montant_fcfa:,.0f} FCFA ({montant:,.0f} CHF)")
        
        st.markdown(f"**🔴 TOTAL ANNUEL: {total_cout_annuel_2030 * 667:,.0f} FCFA ({total_cout_annuel_2030:,.0f} CHF)**")
    
    with col2:
        # Objectifs de revenus passifs nécessaires
        revenus_passifs_requis_mensuel = (total_cout_annuel_2030 * 667) / 12  # ~50M FCFA/mois
        
        st.markdown("**🎯 Objectifs Revenus Passifs 2030**")
        st.write(f"• **Mensuel requis:** {revenus_passifs_requis_mensuel:,.0f} FCFA")
        st.write(f"• **Annuel requis:** {total_cout_annuel_2030 * 667:,.0f} FCFA")
        
        # Revenus passifs actuels
        kpis = calculer_kpis(st.session_state.projets, st.session_state.revenus)
        revenus_passifs_actuels = kpis['revenus_passifs']
        
        st.write(f"• **Actuel (2025):** {revenus_passifs_actuels:,.0f} FCFA/mois")
        
        gap_mensuel = revenus_passifs_requis_mensuel - revenus_passifs_actuels
        st.write(f"• **🚀 Gap à combler:** {gap_mensuel:,.0f} FCFA/mois")
        
        # Progression nécessaire
        progression_annuelle = (gap_mensuel / revenus_passifs_actuels * 100) if revenus_passifs_actuels > 0 else 0
        st.write(f"• **Croissance annuelle requise:** {progression_annuelle:.1f}%")
    
    # Roadmap stratégique
    st.markdown("---")
    st.subheader("🗺️ Roadmap Stratégique 2025-2030")
    
    roadmap_phases = [
        {
            "periode": "2025-2026",
            "phase": "Consolidation",
            "objectifs": [
                "Finaliser projets immobiliers Cameroun",
                "Développer IIBA vers 1M FCFA/mois",
                "Créer fonds d'urgence 6 mois",
                "Optimiser revenus William en Suisse"
            ],
            "target_revenus": "2M FCFA/mois passifs"
        },
        {
            "periode": "2026-2027", 
            "phase": "Accélération",
            "objectifs": [
                "Multiplier actifs locatifs",
                "Lancer business secondaire William",
                "Développer expertise Alix en investissement",
                "Débuter préparation administrative Suisse"
            ],
            "target_revenus": "8M FCFA/mois passifs"
        },
        {
            "periode": "2027-2028",
            "phase": "Diversification", 
            "objectifs": [
                "Portfolio investissements internationaux",
                "Business scalable famille",
                "Préparation déménagement progressif",
                "Formation spécialisée enfants"
            ],
            "target_revenus": "20M FCFA/mois passifs"
        },
        {
            "periode": "2028-2030",
            "phase": "Migration",
            "objectifs": [
                "Installation progressive famille Suisse",
                "Maintien revenus passifs à distance", 
                "Intégration système suisse",
                "Indépendance financière totale"
            ],
            "target_revenus": "50M+ FCFA/mois passifs"
        }
    ]
    
    for phase in roadmap_phases:
        couleur = "#28a745" if "2025" in phase["periode"] else "#ffc107" if "2026" in phase["periode"] else "#17a2b8" if "2027" in phase["periode"] else "#dc3545"
        
        with st.expander(f"{phase['periode']} - Phase {phase['phase']} | 🎯 {phase['target_revenus']}"):
            st.markdown(f"""
            <div style="border-left: 4px solid {couleur}; padding: 1rem; background: #f8f9fa;">
                <h4 style="color: {couleur};">Objectifs {phase['phase']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for obj in phase["objectifs"]:
                st.write(f"• {obj}")
            
            # Actions suggérées selon la phase
            if "2025" in phase["periode"]:
                st.markdown("**⚡ Actions immédiates:**")
                st.write("• Finaliser titre foncier pour générer premiers loyers")
                st.write("• Développer IIBA avec plan marketing structuré")
                st.write("• Négocier augmentation ou promotion William")
                
            elif "2026" in phase["periode"]:
                st.markdown("**🚀 Actions de croissance:**")
                st.write("• Acquisition 2ème propriété locative")
                st.write("• Formation Alix en investment immobilier avancé")
                st.write("• Side-business William (consulting/freelance)")
                
            elif "2027" in phase["periode"]:
                st.markdown("**🌍 Actions d'expansion:**")
                st.write("• Diversification géographique des investissements")
                st.write("• Business familial exportable en Suisse")
                st.write("• Début procédures administratives migration")
                
            else:  # 2028-2030
                st.markdown("**✈️ Actions de migration:**")
                st.write("• Installation logistique progressive en Suisse")
                st.write("• Maintien revenus passifs depuis Suisse")
                st.write("• Intégration complète système suisse")
    
    # Projets suggérés activés/désactivés
    st.markdown("---")
    st.subheader("💡 Projets Suggérés pour Vision 2030")
    
    projets_suggests = [
        {
            "nom": "Acquisition immeuble locatif #2",
            "budget": "15M FCFA",
            "roi": "12%",
            "priorite": "Haute",
            "echeance": "2026",
            "actif": True
        },
        {
            "nom": "Formation expertise fiscale Suisse-Cameroun",
            "budget": "500k FCFA", 
            "roi": "25%",
            "priorite": "Moyenne",
            "echeance": "2025",
            "actif": False
        },
        {
            "nom": "Business e-commerce international",
            "budget": "2M FCFA",
            "roi": "30%",
            "priorite": "Haute", 
            "echeance": "2027",
            "actif": True
        },
        {
            "nom": "Portefeuille actions suisses",
            "budget": "5M FCFA",
            "roi": "8%",
            "priorite": "Moyenne",
            "echeance": "2026",
            "actif": False
        },
        {
            "nom": "Préparation administrative migration",
            "budget": "1M FCFA",
            "roi": "0%",
            "priorite": "Critique",
            "echeance": "2028",
            "actif": True
        }
    ]
    
    for projet in projets_suggests:
        statut_couleur = "#28a745" if projet["actif"] else "#6c757d"
        statut_texte = "✅ Activé" if projet["actif"] else "⏸️ En attente"
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div style="border-left: 4px solid {statut_couleur}; padding: 0.5rem; margin: 0.2rem 0;">
                <strong>{projet['nom']}</strong> | {projet['budget']} | ROI: {projet['roi']} | {projet['echeance']}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.write(f"**{statut_texte}**")
        
        with col3:
            if st.button(f"{'Désactiver' if projet['actif'] else 'Activer'}", 
                        key=f"toggle_{projet['nom'][:10]}"):
                # Ici on pourrait toggle le statut
                st.success(f"Statut modifié pour: {projet['nom']}")
    
    # Indicateurs de réussite
    st.markdown("---")
    st.subheader("📊 Indicateurs de Réussite Vision 2030")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎯 KPIs Financiers 2030:**")
        st.write("• 50M+ FCFA revenus passifs/mois")
        st.write("• 100% coûts Suisse couverts par passifs")
        st.write("• 10+ actifs générateurs diversifiés")
        st.write("• Fonds urgence = 12 mois coûts Suisse")
        st.write("• 0% dépendance salaires")
    
    with col2:
        st.markdown("**👨‍👩‍👧‍👦 KPIs Familiaux 2030:**")
        st.write("• 3 enfants scolarisés système suisse")
        st.write("• Uriel autonome financièrement")
        st.write("• Intégration sociale et culturelle réussie")
        st.write("• Maîtrise française/allemande/anglais")
        st.write("• Réseau professionnel établi en Suisse")
    
    # Message de motivation
    st.markdown("""
    <div class="mindset-box">
        <h3>🌟 Vision Familiale 2030 - "De Yaoundé à Zurich"</h3>
        <p><strong>Alix & William :</strong> Vous avez 5 ans pour transformer votre rêve en réalité. 
        Avec discipline, stratégie et les principes des grands mentors financiers, votre famille 
        peut atteindre l'indépendance financière et s'installer durablement en Suisse.</p>
        <p><em>"Le meilleur moment pour planter un arbre était il y a 20 ans. 
        Le deuxième meilleur moment est maintenant." - Proverbe chinois</em></p>
    </div>
    """, unsafe_allow_html=True)

def show_admin():
    """Page administration complète"""
    st.markdown('<div class="main-header"><h1>⚙️ Administration</h1></div>', unsafe_allow_html=True)
    
    # Onglets admin
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 KPIs & Objectifs", "📋 Listes & Vocabulaire", 
                                           "🧠 Conseils Mentors", "📊 Export/Import", "🗑️ Gestion Base"])
    
    with tab1:
        st.subheader("🎯 Configuration des KPIs et Objectifs")
        
        with st.form("config_kpis"):
            st.write("**Seuils et Objectifs Familiaux**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fonds_urgence_mois = st.number_input("Fonds d'urgence (mois de dépenses)", 
                                                   min_value=1, max_value=12, 
                                                   value=st.session_state.config_admin['seuils']['fonds_urgence_mois'])
                
                ratio_actifs_min = st.number_input("Ratio actifs minimum (%)", 
                                                 min_value=0, max_value=100,
                                                 value=st.session_state.config_admin['seuils']['ratio_actifs_min'])
                
                revenus_passifs_min = st.number_input("Objectif revenus passifs (%)", 
                                                    min_value=0, max_value=100,
                                                    value=st.session_state.config_admin
