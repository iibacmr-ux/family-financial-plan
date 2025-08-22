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
        st.session_state.projets = []
    
    if 'revenus' not in st.session_state:
        st.session_state.revenus = []
    
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
                    'Actif générateur': 'Excellent choix ! Cet actif va mettre de l argent dans votre poche. Concentrez-vous sur la scalabilité.',
                    'Passif': 'Attention ! Ceci sort de l argent de votre poche. Limitez ces dépenses et privilégiez les actifs.',
                    'Investissement': 'Bon pour le capital humain, mais assurez-vous que cela génère des revenus futurs.'
                },
                'buffett': {
                    'Actif générateur': 'Comprenez-vous parfaitement ce business ? Investissez seulement dans ce que vous maîtrisez.',
                    'Passif': 'Ces dépenses sont-elles vraiment nécessaires ? Privilégiez la valeur long terme.',
                    'Investissement': 'L éducation est le meilleur investissement. Excellent choix pour l avenir.'
                },
                'ramsey': {
                    'Actif générateur': 'Payez comptant si possible. Évitez l endettement même pour les actifs.',
                    'Passif': 'Est-ce un BESOIN ou une ENVIE ? Respectez votre budget 50/30/20.',
                    'Investissement': 'Priorité à l éducation ! Mais respectez votre budget d urgence.'
                }
            }
        }

    if 'edit_project_id' not in st.session_state:
        st.session_state.edit_project_id = None
    if 'edit_revenue_id' not in st.session_state:
        st.session_state.edit_revenue_id = None
    if 'mois_filtre' not in st.session_state:
        st.session_state.mois_filtre = "Tout"
    if 'annee_filtre' not in st.session_state:
        st.session_state.annee_filtre = "Tout"

# Fonctions de calcul
def calculer_kpis(projets, revenus, mois_filtre=None, annee_filtre=None):
    """Calcule tous les KPIs en fonction des filtres"""
    projets_filtres = projets
    revenus_filtres = revenus
    
    if mois_filtre and mois_filtre != "Tout":
        revenus_filtres = [r for r in revenus if r.get('mois') == mois_filtre]
    
    if annee_filtre and annee_filtre != "Tout":
        revenus_filtres = [r for r in revenus_filtres if str(r.get('annee')) == str(annee_filtre)]
    
    total_revenus = sum(r.get('montant', 0) for r in revenus_filtres)
    total_actifs = sum(p.get('montant_total', 0) for p in projets_filtres if p.get('type') == 'Actif générateur')
    total_passifs = sum(p.get('montant_total', 0) for p in projets_filtres if p.get('type') == 'Passif')
    total_investissements = sum(p.get('montant_total', 0) for p in projets_filtres if p.get('type') == 'Investissement')
    
    cash_flow_mensuel = sum(p.get('cash_flow_mensuel', 0) for p in projets_filtres)
    revenus_passifs = sum(p.get('cash_flow_mensuel', 0) for p in projets_filtres if p.get('cash_flow_mensuel', 0) > 0)
    
    ratio_actifs_passifs = (total_actifs / max(total_passifs, 1)) * 100
    ratio_revenus_passifs = (revenus_passifs / max(total_revenus, 1)) * 100 if total_revenus > 0 else 0
    
    if cash_flow_mensuel < 0 and ratio_actifs_passifs < 20:
        phase = "Stabilisation"
    elif cash_flow_mensuel >= 0 and ratio_actifs_passifs >= 20 and ratio_actifs_passifs < 40:
        phase = "Transition" 
    else:
        phase = "Expansion"
    
    fonds_urgence = sum(p.get('montant_total', 0) for p in projets_filtres if 'urgence' in p.get('nom', '').lower())
    baby_step = 1
    if fonds_urgence >= 500000:
        baby_step = 2
    if fonds_urgence >= 3 * abs(cash_flow_mensuel):
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

# Pages principales
def show_dashboard():
    """Dashboard principal avec KPIs"""
    st.markdown('<div class="main-header"><h1>📊 Dashboard Familial</h1></div>', unsafe_allow_html=True)
    
    mois_filtre = st.session_state.get('mois_filtre')
    annee_filtre = st.session_state.get('annee_filtre')
    kpis = calculer_kpis(st.session_state.projets, st.session_state.revenus, mois_filtre, annee_filtre)
    
    periode = "Toutes les données"
    if mois_filtre and mois_filtre != "Tout" and annee_filtre and annee_filtre != "Tout":
        periode = f"{mois_filtre} {annee_filtre}"
    elif mois_filtre and mois_filtre != "Tout":
        periode = f"Tous les {mois_filtre}"
    elif annee_filtre and annee_filtre != "Tout":
        periode = f"Année {annee_filtre}"
    
    st.info(f"📅 **Période active :** {periode}")
    
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

def show_project_management():
    """Gestion des projets avec CRUD complet"""
    st.markdown('<div class="main-header"><h1>💼 Gestion des Projets</h1></div>', unsafe_allow_html=True)
    
    if st.session_state.edit_project_id:
        show_edit_project_form()
        return
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("➕ Ajouter un nouveau projet", type="primary"):
            st.session_state.show_add_form = True
    
    with col2:
        type_filter = st.selectbox("Filtrer par type", ["Tous"] + st.session_state.config_admin['listes']['types_projets'])
    
    with col3:
        statut_filter = st.selectbox("Filtrer par statut", ["Tous"] + st.session_state.config_admin['listes']['statuts'])
    
    if st.session_state.get('show_add_form', False):
        show_add_project_form()
    
    st.markdown("---")
    
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
            cash_flow = st.number_input("Cash flow mensuel (FCFA)", value=0, step=1000)
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
        cancel = st.form_submit_button("❌ Annuler")
        
        if submitted:
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
                st.error(f"⚠️ Champs manquants: {champs_manquants_str}")
                return
            
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
        
        if cancel:
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
        
        if safe_get(projet, 'date_creation'):
            st.caption(f"📅 Créé le {projet['date_creation'].strftime('%d/%m/%Y à %H:%M')}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Modifier", key=f"edit_project_{projet.get('id')}"):
                st.session_state.edit_project_id = projet.get('id')
                st.rerun()
        with col2:
            if st.button("🗑️ Supprimer", key=f"delete_project_{projet.get('id')}"):
                st.session_state.projets = [p for p in st.session_state.projets if p.get('id') != projet.get('id')]
                st.success("Projet supprimé!")
                st.rerun()
        
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
                                     index=st.session_state.config_admin['listes']['types_projets'].index(projet.get('type', 'Actif générateur')) if projet.get('type') in st.session_state.config_admin['listes']['types_projets'] else 0)
            montant_total = st.number_input("*Budget total (FCFA)", min_value=0, value=int(projet.get('montant_total', 0)), step=1000)
        
        with col2:
            cash_flow = st.number_input("Cash flow mensuel (FCFA)", value=int(projet.get('cash_flow_mensuel', 0)), step=1000)
            roi_attendu = st.number_input("ROI attendu (%)", min_value=0.0, max_value=100.0, 
                                        value=float(projet.get('roi_attendu', 0.0)), step=0.1)
            responsable = st.selectbox("*Responsable", st.session_state.config_admin['listes']['responsables'],
                                     index=st.session_state.config_admin['listes']['responsables'].index(safe_get(projet, 'responsable', 'Famille')) if safe_get(projet, 'responsable') in st.session_state.config_admin['listes']['responsables'] else 0)
        
        description = st.text_area("Description", value=projet.get('description', ''))
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("✅ Sauvegarder", type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Annuler")
        
        if submitted:
            if not nom or not montant_total or montant_total <= 0:
                st.error("⚠️ Champs manquants: Nom, Budget total")
                return
            
            for p in st.session_state.projets:
                if p.get('id') == st.session_state.edit_project_id:
                    p.update({
                        'nom': nom,
                        'type': type_projet,
                        'montant_total': int(montant_total),
                        'cash_flow_mensuel': int(cash_flow),
                        'roi_attendu': float(roi_attendu),
                        'description': description,
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
    
    if st.session_state.edit_revenue_id:
        show_edit_revenue_form()
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("➕ Ajouter un nouveau revenu", type="primary"):
            st.session_state.show_add_revenue_form = True
    
    if st.session_state.get('show_add_revenue_form', False):
        show_add_revenue_form()
    
    st.markdown("---")
    
    if not st.session_state.revenus:
        st.info("Aucun revenu enregistré.")
        return
    
    total_revenus = sum(r.get('montant', 0) for r in st.session_state.revenus)
    st.metric("💰 Total des revenus", f"{total_revenus:,.0f} FCFA")
    
    st.markdown("---")
    
    for revenu in st.session_state.revenus:
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
        
        description = st.text_area("Description", help="Description optionnelle du revenu")
        
        submitted = st.form_submit_button("✅ Ajouter le revenu", type="primary")
        cancel = st.form_submit_button("❌ Annuler")
        
        if submitted:
            if not nom or not montant or montant <= 0:
                st.error("⚠️ Champs manquants: Nom, Montant")
                return
            
            nouveau_revenu = {
                'id': str(uuid.uuid4()),
                'nom': nom,
                'type': type_revenu,
                'montant': int(montant),
                'mois': mois,
                'annee': int(annee),
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
            st.write(f"**👤 Responsable:** {safe_get(revenu, 'responsable', 'Non défini')}")
            if safe_get(revenu, 'date_creation'):
                st.write(f"**📅 Créé:** {revenu['date_creation'].strftime('%d/%m/%Y')}")
        
        with col3:
            if revenu.get('description'):
                st.write(f"**📝 Description:** {revenu.get('description')}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️", key=f"edit_rev_{revenu.get('id')}", help="Modifier"):
                st.session_state.edit_revenue_id = revenu.get('id')
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"delete_rev_{revenu.get('id')}", help="Supprimer"):
                st.session_state.revenus = [r for r in st.session_state.revenus if r.get('id') != revenu.get('id')]
                st.success("Revenu supprimé!")
                st.rerun()
        
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
            montant = st.number_input("*Montant (FCFA)", min_value=0, value=int(revenu.get('montant', 0)), step=1000)
        
        with col2:
            responsable = st.selectbox("*Responsable", st.session_state.config_admin['listes']['responsables'],
                                     index=st.session_state.config_admin['listes']['responsables'].index(safe_get(revenu, 'responsable', 'William')) if safe_get(revenu, 'responsable') in st.session_state.config_admin['listes']['responsables'] else 0)
        
        description = st.text_area("Description", value=revenu.get('description', ''))
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("✅ Sauvegarder", type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Annuler")
        
        if submitted:
            if not nom or not montant or montant <= 0:
                st.error("⚠️ Le nom et le montant sont obligatoires")
                return
            
            for r in st.session_state.revenus:
                if r.get('id') == st.session_state.edit_revenue_id:
                    r.update({
                        'nom': nom,
                        'montant': int(montant),
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

def show_kanban_view():
    """Vue Kanban avec colonnes par statut"""
    st.markdown('<div class="main-header"><h1>📋 Vue Kanban Projets</h1></div>', unsafe_allow_html=True)
    
    if not st.session_state.projets:
        st.info("Aucun projet disponible. Ajoutez des projets depuis la page Gestion des Projets.")
        return
    
    categories = {
        'En Retard': {'projets': [], 'couleur': '#dc3545', 'icone': '🔴'},
        'À Risque': {'projets': [], 'couleur': '#ffc107', 'icone': '🟡'},
        'En Cours': {'projets': [], 'couleur': '#17a2b8', 'icone': '🔵'},
        'En Avance': {'projets': [], 'couleur': '#28a745', 'icone': '🟢'},
        'Bloqué': {'projets': [], 'couleur': '#6c757d', 'icone': '⚫'}
    }
    
    today = date.today()
    
    for projet in st.session_state.projets:
        echeance = projet.get('echeance', today)
        if isinstance(echeance, str):
            try:
                echeance = datetime.strptime(echeance, '%Y-%m-%d').date()
            except:
                echeance = today
        
        if echeance < today:
            categories['En Retard']['projets'].append(projet)
        elif projet.get('statut') == 'Suspendu':
            categories['Bloqué']['projets'].append(projet)
        elif projet.get('statut') == 'Terminé':
            categories['En Avance']['projets'].append(projet)
        elif (echeance - today).days < 30:
            categories['À Risque']['projets'].append(projet)
        else:
            categories['En Cours']['projets'].append(projet)
    
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
    
    st.markdown("---")
    cols = st.columns(5)
    
    for i, (nom_cat, cat_data) in enumerate(categories.items()):
        with cols[i]:
            st.markdown(f"#### {cat_data['icone']} {nom_cat}")
            
            for projet in cat_data['projets']:
                show_kanban_card(projet, cat_data['couleur'])

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
            <p><strong>Responsable:</strong> {safe_get(projet, 'responsable', 'Non défini')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️", key=f"edit_kanban_{projet.get('id')}", help="Modifier"):
                st.session_state.edit_project_id = projet.get('id')
                st.rerun()
        with col2:
            if st.button("👁️", key=f"view_kanban_{projet.get('id')}", help="Détails"):
                with st.expander(f"Détails: {projet.get('nom')}", expanded=True):
                    st.write(f"**Type:** {projet.get('type')}")
                    st.write(f"**Statut:** {projet.get('statut')}")
                    st.write(f"**Cash flow:** {projet.get('cash_flow_mensuel', 0):,.0f} FCFA/mois")
                    if projet.get('description'):
                        st.write(f"**Description:** {projet.get('description')}")

def show_analytics():
    """Page Analytics & KPIs Avancés avec Kiyosaki"""
    st.markdown('<div class="main-header"><h1>📊 Analytics & KPIs Avancés</h1></div>', unsafe_allow_html=True)
    
    mois_filtre = st.session_state.get('mois_filtre')
    annee_filtre = st.session_state.get('annee_filtre')
    kpis = calculer_kpis(st.session_state.projets, st.session_state.revenus, mois_filtre, annee_filtre)
    
    periode = "Toutes les données"
    if mois_filtre and mois_filtre != "Tout" and annee_filtre and annee_filtre != "Tout":
        periode = f"{mois_filtre} {annee_filtre}"
    elif mois_filtre and mois_filtre != "Tout":
        periode = f"Tous les {mois_filtre}"
    elif annee_filtre and annee_filtre != "Tout":
        periode = f"Année {annee_filtre}"
    
    st.info(f"📅 **Analyse pour :** {periode}")
    
    st.subheader("💎 Analyse Kiyosaki - Actifs vs Passifs")
    
    quadrant, status_rat = determiner_quadrant_kiyosaki(st.session_state.projets, st.session_state.revenus)
    
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
    
    st.markdown("---")
    st.subheader("🎯 Quadrants Kiyosaki E-S-B-I")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
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

def show_progression():
    """Page progression familiale"""
    st.markdown('<div class="main-header"><h1>🚀 Progression Familiale</h1></div>', unsafe_allow_html=True)
    
    mois_filtre = st.session_state.get('mois_filtre')
    annee_filtre = st.session_state.get('annee_filtre')
    kpis = calculer_kpis(st.session_state.projets, st.session_state.revenus, mois_filtre, annee_filtre)
    
    st.subheader("👶 Baby Steps Dave Ramsey")
    
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
    
    st.markdown("""
    <div class="warning-box">
        <h4>💡 Comment mesurer le fonds d'urgence ?</h4>
        <p><strong>Deux options pour créer votre fonds d'urgence :</strong></p>
        <ul>
            <li><strong>Option 1:</strong> Créer un projet spécifique "Fonds d'urgence" avec le montant cible</li>
            <li><strong>Option 2:</strong> Utiliser un compte épargne séparé (recommandé)</li>
        </ul>
        <p><strong>Calcul automatique:</strong> Le système détecte automatiquement les projets contenant "urgence" dans le nom.</p>
        <p><strong>Objectif actuel:</strong> {0:,.0f} FCFA (6 mois de dépenses courantes)</p>
    </div>
    """.format(abs(kpis['cash_flow_mensuel']) * 6), unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📈 Évolution par Période")
    
    st.markdown("""
    <div class="info-tooltip">
        <h4>📖 Comment lire ces graphiques ?</h4>
        <p><strong>Graphique 1 - Évolution Cash Flow:</strong> Montre l'évolution de votre cash flow mensuel. 
        Objectif: ligne au-dessus de zéro (cash flow positif).</p>
        <p><strong>Graphique 2 - Progression Actifs/Passifs:</strong> Montre l'équilibre entre vos actifs (qui rapportent) 
        et passifs (qui coûtent). Objectif: plus d'actifs que de passifs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    periode_actuelle = "toutes les données"
    if mois_filtre and mois_filtre != "Tout":
        periode_actuelle = f"le mois de {mois_filtre.lower()}"
    if annee_filtre and annee_filtre != "Tout":
        periode_actuelle = f"l'année {annee_filtre}"
    
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

def show_education():
    """Page éducation financière des enfants"""
    st.markdown('<div class="main-header"><h1>👨‍👩‍👧‍👦 Éducation Financière des Enfants</h1></div>', unsafe_allow_html=True)
    
    annee_filtre = st.session_state.get('annee_filtre', 2025)
    if annee_filtre == "Tout":
        annee_reference = 2025
    else:
        try:
            annee_reference = int(annee_filtre)
        except:
            annee_reference = 2025
    
    ages_2025 = {"Uriel": 14, "Naelle": 7, "Nell-Henri": 5}
    difference_annee = annee_reference - 2025
    ages_actuels = {enfant: age + difference_annee for enfant, age in ages_2025.items()}
    
    st.info(f"📅 **Âges pour l'année {annee_reference}:** Uriel ({ages_actuels['Uriel']} ans), Naelle ({ages_actuels['Naelle']} ans), Nell-Henri ({ages_actuels['Nell-Henri']} ans)")
    
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
        else:
            st.write(f"**Programme adapté pour {ages_actuels['Nell-Henri']} ans:**")
            st.write("• Reconnaissance des couleurs/formes")
            st.write("• Jeux sensoriels avec objets")
            st.write("• Concept très simple d'échange")

def show_vision_2030():
    """Page vision long terme 2030"""
    st.markdown('<div class="main-header"><h1>🔮 Vision Familiale 2030</h1></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
        <h3>🎯 Objectif Principal: Toute la famille en Suisse d'ici 2030</h3>
        <p>Planification stratégique pour une migration familiale réussie avec indépendance financière.</p>
    </div>
    """, unsafe_allow_html=True)
    
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

def show_mentors_page():
    """Page conseils des 3 mentors"""
    st.markdown('<div class="main-header"><h1>🎯 Conseils des 3 Mentors Financiers</h1></div>', unsafe_allow_html=True)
    
    if not st.session_state.projets:
        st.warning("Aucun projet disponible pour analyse.")
        return
    
    projet_noms = [f"{p.get('nom', 'Projet')} ({p.get('type', 'Type')})" for p in st.session_state.projets]
    
    selected_index = st.selectbox("Sélectionnez un projet à analyser", 
                                 range(len(projet_noms)),
                                 format_func=lambda x: projet_noms[x])
    
    projet_selectionne = st.session_state.projets[selected_index]
    
    st.markdown("---")
    
    type_projet = projet_selectionne.get('type', 'Actif générateur')
    
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

def show_admin():
    """Page administration"""
    st.markdown('<div class="main-header"><h1>⚙️ Administration</h1></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📊 Export des Données", "🗑️ Gestion Base"])
    
    with tab1:
        st.subheader("📊 Export des Données")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Exporter tout en JSON", type="primary"):
                data_export = {
                    'projets': st.session_state.projets,
                    'revenus': st.session_state.revenus,
                    'config_admin': st.session_state.config_admin,
                    'export_date': datetime.now().isoformat()
                }
                
                json_str = json.dumps(data_export, default=str, indent=2)
                st.download_button(
                    label="⬇️ Télécharger JSON",
                    data=json_str,
                    file_name=f"famille_finance_export_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📊 Exporter en Excel", type="secondary"):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    # Export projets
                    if st.session_state.projets:
                        df_projets = pd.DataFrame(st.session_state.projets)
                        df_projets.to_excel(writer, sheet_name='Projets', index=False)
                    
                    # Export revenus
                    if st.session_state.revenus:
                        df_revenus = pd.DataFrame(st.session_state.revenus)
                        df_revenus.to_excel(writer, sheet_name='Revenus', index=False)
                
                st.download_button(
                    label="⬇️ Télécharger Excel",
                    data=output.getvalue(),
                    file_name=f"famille_finance_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        st.info("💡 **Conseil:** Exportez régulièrement vos données pour sauvegarder votre travail.")
    
    with tab2:
        st.subheader("🗑️ Gestion de la Base de Données")
        
        st.warning("⚠️ **Attention:** Ces actions sont irréversibles. Exportez vos données avant de continuer.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Vider tous les projets", type="secondary"):
                if st.session_state.get('confirm_delete_projects', False):
                    st.session_state.projets = []
                    st.session_state.confirm_delete_projects = False
                    st.success("✅ Tous les projets ont été supprimés")
                    st.rerun()
                else:
                    st.session_state.confirm_delete_projects = True
                    st.warning("⚠️ Cliquez à nouveau pour confirmer")
        
        with col2:
            if st.button("🗑️ Vider tous les revenus", type="secondary"):
                if st.session_state.get('confirm_delete_revenues', False):
                    st.session_state.revenus = []
                    st.session_state.confirm_delete_revenues = False
                    st.success("✅ Tous les revenus ont été supprimés")
                    st.rerun()
                else:
                    st.session_state.confirm_delete_revenues = True
                    st.warning("⚠️ Cliquez à nouveau pour confirmer")
        
        if st.button("🗑️ Vider toute la base", type="secondary"):
            if st.session_state.get('confirm_delete_all', False):
                st.session_state.projets = []
                st.session_state.revenus = []
                st.session_state.confirm_delete_all = False
                st.success("✅ Toute la base a été vidée")
                st.rerun()
            else:
                st.session_state.confirm_delete_all = True
                st.error("⚠️ Cliquez à nouveau pour TOUT supprimer")

# Navigation et main
def main():
    """Fonction principale avec navigation"""
    init_session_state()
    
    # Sidebar avec navigation et filtres
    with st.sidebar:
        st.markdown("# 💰 Plan Financier Familial")
        
        # Changement de mindset
        st.markdown("""
        <div class="mindset-box" style="margin: 1rem 0; padding: 0.8rem;">
            <h4>🧠 Changement de Mindset</h4>
            <p><strong>William:</strong> "Comment développer des revenus qui travaillent sans moi ?"</p>
            <p><strong>Alix:</strong> "Quels actifs vais-je acquérir ce trimestre ?"</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Filtre global
        st.markdown("### 📅 Filtre Global")
        mois_options = ["Tout", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                       "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        st.session_state.mois_filtre = st.selectbox("Mois", mois_options)
        
        annee_options = ["Tout"] + [str(year) for year in range(2020, 2031)]
        st.session_state.annee_filtre = st.selectbox("Année", annee_options)
        
        # Navigation
        st.markdown("### 🧭 Navigation")
        page = st.radio("", [
            "📊 Dashboard",
            "📋 Vue Kanban Projets", 
            "💼 Gestion Projets",
            "💰 Revenus Variables",
            "🎯 Conseils 3 Mentors",
            "📈 Analytics & KPIs",
            "🚀 Progression Familiale",
            "👨‍👩‍👧‍👦 Éducation Enfants",
            "🔮 Vision 2030",
            "⚙️ Administration"
        ])
    
    # Affichage de la page sélectionnée
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "📋 Vue Kanban Projets":
        show_kanban_view()
    elif page == "💼 Gestion Projets":
        show_project_management()
    elif page == "💰 Revenus Variables":
        show_revenue_management()
    elif page == "🎯 Conseils 3 Mentors":
        show_mentors_page()
    elif page == "📈 Analytics & KPIs":
        show_analytics()
    elif page == "🚀 Progression Familiale":
        show_progression()
    elif page == "👨‍👩‍👧‍👦 Éducation Enfants":
        show_education()
    elif page == "🔮 Vision 2030":
        show_vision_2030()
    elif page == "⚙️ Administration":
        show_admin()

if __name__ == "__main__":
    main()
