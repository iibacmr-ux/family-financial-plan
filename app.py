import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
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
        --space-16: 16px;
        --space-24: 24px;
        --radius-lg: 12px;
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02);
    }
    
    /* Reset Streamlit par défaut */
    .main .block-container {
        padding: 2rem 1rem;
        max-width: none;
        background-color: var(--color-background);
    }
    
    /* Sidebar personnalisée */
    .css-1d391kg {
        background-color: var(--color-surface) !important;
    }
    
    /* Navigation Radio Buttons */
    .nav-radio {
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: var(--space-16);
        margin-bottom: var(--space-16);
        box-shadow: var(--shadow-sm);
    }
    
    .nav-radio h3 {
        color: var(--color-primary);
        font-size: 1.5rem;
        margin-bottom: var(--space-16);
        text-align: center;
        font-weight: 600;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: var(--space-24);
        box-shadow: var(--shadow-sm);
        text-align: center;
        transition: all 0.3s ease;
        margin-bottom: var(--space-16);
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .kpi-positive { color: var(--color-success); }
    .kpi-negative { color: var(--color-error); }
    .kpi-warning { color: var(--color-warning); }
    
    /* Project Cards */
    .project-card {
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: var(--space-24);
        margin-bottom: var(--space-16);
        box-shadow: var(--shadow-sm);
    }
    
    .project-type-actif {
        background: rgba(33, 128, 141, 0.1);
        color: var(--color-success);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .project-type-passif {
        background: rgba(192, 21, 47, 0.1);
        color: var(--color-error);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .project-type-formation {
        background: rgba(98, 108, 113, 0.1);
        color: var(--color-info);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    /* Phase Badges */
    .phase-stabilisation {
        background: rgba(192, 21, 47, 0.15);
        color: var(--color-error);
        border: 1px solid rgba(192, 21, 47, 0.25);
    }
    
    .phase-transition {
        background: rgba(168, 75, 47, 0.15);
        color: var(--color-warning);
        border: 1px solid rgba(168, 75, 47, 0.25);
    }
    
    .phase-expansion {
        background: rgba(33, 128, 141, 0.15);
        color: var(--color-success);
        border: 1px solid rgba(33, 128, 141, 0.25);
    }
    
    /* Alertes */
    .alert-success {
        background: rgba(33, 128, 141, 0.1);
        border: 1px solid rgba(33, 128, 141, 0.3);
        border-radius: var(--radius-lg);
        padding: var(--space-16);
        margin: var(--space-16) 0;
        color: var(--color-success);
    }
    
    .alert-warning {
        background: rgba(168, 75, 47, 0.1);
        border: 1px solid rgba(168, 75, 47, 0.3);
        border-radius: var(--radius-lg);
        padding: var(--space-16);
        margin: var(--space-16) 0;
        color: var(--color-warning);
    }
    
    .alert-error {
        background: rgba(192, 21, 47, 0.1);
        border: 1px solid rgba(192, 21, 47, 0.3);
        border-radius: var(--radius-lg);
        padding: var(--space-16);
        margin: var(--space-16) 0;
        color: var(--color-error);
    }
    
    /* Mindset Box */
    .mindset-box {
        background: rgba(34, 197, 94, 0.08);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: var(--space-16);
        margin: var(--space-16) 0;
    }
    
    .mindset-reminder {
        margin-bottom: 12px;
        font-size: 0.9rem;
    }
    
    .mindset-reminder strong {
        color: var(--color-primary);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 0.5rem;
        }
        
        .kpi-card {
            padding: var(--space-16);
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DONNEES ET LOGIQUE METIER
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
                'montant_utilise_reel': 0,
                'cash_flow_mensuel': 0,
                'statut': 'En cours',
                'echeance': date(2025, 6, 30),
                'roi_attendu': 12,
                'description': 'Acquisition terrain pour location future',
                'suivi_mensuel': []
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
                'description': 'Voyage familial cohésion',
                'suivi_mensuel': []
            },
            {
                'id': 3,
                'nom': 'Scolarité enfants',
                'type': 'Investissement formation',
                'montant_total': 6500000,
                'budget_alloue_mensuel': 542000,
                'montant_utilise_reel': 542000,
                'cash_flow_mensuel': -542000,
                'statut': 'En cours',
                'echeance': date(2025, 12, 31),
                'roi_attendu': 25,
                'description': 'Éducation Uriel, Naelle, Nell-Henri',
                'suivi_mensuel': []
            },
            {
                'id': 4,
                'nom': 'Projet IIBA',
                'type': 'Actif générateur',
                'montant_total': 2786480,
                'budget_alloue_mensuel': 100000,
                'montant_utilise_reel': 50000,
                'cash_flow_mensuel': 232000,
                'statut': 'Développement',
                'echeance': date(2025, 9, 30),
                'roi_attendu': 18,
                'description': 'Business génération revenus passifs',
                'suivi_mensuel': []
            }
        ]
    
    if 'revenus_variables' not in st.session_state:
        st.session_state.revenus_variables = [
            {
                'nom': 'Salaire William',
                'montant_mensuel': 800000,
                'type': 'Salaire',
                'regulier': True
            },
            {
                'nom': 'Revenus IIBA',
                'montant_mensuel': 232000,
                'type': 'Business',
                'regulier': False
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

def get_mentor_advice(project_type, project_name):
    """Génère les conseils des 3 mentors"""
    advice = {}
    
    if project_type == 'Actif générateur':
        advice['kiyosaki'] = f"✅ Excellent ! Ce projet génère des revenus passifs et vous rapproche du quadrant I (Investisseur). Continuez à multiplier ces actifs."
        advice['buffett'] = f"🔍 Assurez-vous de comprendre parfaitement ce business et son potentiel long terme. La compréhension est clé."
        advice['ramsey'] = f"💪 Si ce projet ne vous endette pas excessivement, c'est un excellent investissement pour votre indépendance."
        
    elif project_type == 'Passif':
        advice['kiyosaki'] = f"⚠️ Attention ! Ce passif retire de l'argent de votre poche chaque mois. Est-il vraiment nécessaire ?"
        advice['buffett'] = f"🤔 Quel est le coût d'opportunité ? Cet argent pourrait-il être mieux investi ailleurs ?"
        advice['ramsey'] = f"🚨 Vérifiez que cet investissement respecte votre budget 50/30/20 et n'endette pas votre famille."
        
    else:  # Formation
        advice['kiyosaki'] = f"📚 L'éducation est un actif qui génère des revenus futurs plus élevés. Investissement dans le capital humain approuvé !"
        advice['buffett'] = f"🎯 Le meilleur investissement est en vous-même et votre famille. Cet avantage concurrentiel durera toute votre vie."
        advice['ramsey'] = f"✅ L'éducation est toujours rentable à long terme, tant qu'elle respecte votre budget équilibré."
    
    return advice

# ============================================================================
# SIDEBAR NAVIGATION AVEC RADIO BUTTONS
# ============================================================================

def render_sidebar():
    """Affiche la sidebar avec navigation radio"""
    with st.sidebar:
        st.markdown('<div class="nav-radio">', unsafe_allow_html=True)
        st.markdown("### 💰 Plan Financier Familial")
        st.markdown("*Alix & William - Vers l'Indépendance 2030*")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Navigation avec radio buttons
        pages = [
            "📊 Dashboard Principal",
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
        
        # Mindset reminders
        st.markdown('<div class="mindset-box">', unsafe_allow_html=True)
        st.markdown("### 🧠 Mindset Reminders")
        
        mindset_items = [
            ("🏦 **Kiyosaki**", "Les riches acquièrent des actifs, les pauvres des passifs"),
            ("📈 **Buffett**", "Prix raisonnable + qualité exceptionnelle = succès"),
            ("💪 **Ramsey**", "Vivez selon vos moyens, investissez la différence")
        ]
        
        for title, desc in mindset_items:
            st.markdown(f"""
            <div class="mindset-reminder">
                <strong>{title}</strong>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Phase actuelle
        kpis = calculer_kpis()
        phase = kpis['phase_actuelle'].lower()
        
        st.markdown(f"""
        <div class="phase-{phase}" style="padding: 12px; border-radius: 8px; text-align: center; margin-top: 16px;">
            <strong>🎯 Phase: {kpis['phase_actuelle'].upper()}</strong>
        </div>
        """, unsafe_allow_html=True)
        
    return selected_page

# ============================================================================
# PAGES DE L'APPLICATION
# ============================================================================

def show_dashboard():
    """Page Dashboard Principal"""
    st.title("📊 Dashboard Principal")
    
    # Phase et date
    kpis = calculer_kpis()
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(f"🎯 Phase Actuelle: {kpis['phase_actuelle']}")
    
    with col2:
        st.write(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
    
    # KPIs Grid
    st.subheader("💡 Indicateurs Clés (KPIs)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cash_flow_class = "kpi-negative" if kpis['cash_flow_mensuel'] < 0 else "kpi-positive"
        st.markdown(f"""
        <div class="kpi-card">
            <h4>💸 Cash Flow Mensuel</h4>
            <div class="kpi-value {cash_flow_class}">{format_currency(kpis['cash_flow_mensuel'])}</div>
            <small>{"⚠️ Négatif" if kpis['cash_flow_mensuel'] < 0 else "✅ Positif"}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        ratio_class = "kpi-negative" if kpis['ratio_actifs_passifs'] < 20 else "kpi-warning" if kpis['ratio_actifs_passifs'] < 40 else "kpi-positive"
        st.markdown(f"""
        <div class="kpi-card">
            <h4>⚖️ Ratio Actifs/Passifs</h4>
            <div class="kpi-value {ratio_class}">{kpis['ratio_actifs_passifs']:.1f}%</div>
            <small>📉 {"Critique" if kpis['ratio_actifs_passifs'] < 20 else "Moyen" if kpis['ratio_actifs_passifs'] < 40 else "Bon"}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        revenus_class = "kpi-negative" if kpis['revenus_passifs_pct'] < 15 else "kpi-warning" if kpis['revenus_passifs_pct'] < 30 else "kpi-positive"
        st.markdown(f"""
        <div class="kpi-card">
            <h4>💰 Revenus Passifs</h4>
            <div class="kpi-value {revenus_class}">{kpis['revenus_passifs_pct']:.1f}%</div>
            <small>🎯 Objectif: 30%</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Évolution Cash Flow (Simulation)")
        
        # Simulation données 12 derniers mois
        import numpy as np
        mois = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')
        cash_flow_evolution = np.random.normal(kpis['cash_flow_mensuel'], 500000, len(mois))
        
        fig = px.line(
            x=mois, 
            y=cash_flow_evolution,
            title="Cash Flow Mensuel (FCFA)",
            labels={'x': 'Mois', 'y': 'Cash Flow (FCFA)'}
        )
        fig.add_hline(y=0, line_dash="dash", annotation_text="Équilibre")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Répartition Actifs vs Passifs")
        
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
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Quadrants Familiaux
    st.markdown("---")
    st.subheader("🎯 Quadrants Familiaux (Kiyosaki)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="project-card">
            <h4>👨 William</h4>
            <p><strong>Actuel:</strong> E (Employé)</p>
            <p><strong>Cible:</strong> B (Business Owner)</p>
            <p><em>Actions: Développer IIBA + side-business</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="project-card">
            <h4>👩 Alix</h4>
            <p><strong>Actuel:</strong> S (Self-employed)</p>
            <p><strong>Cible:</strong> I (Investor)</p>
            <p><em>Actions: Focus immobilier + formations</em></p>
        </div>
        """, unsafe_allow_html=True)

def show_project_management():
    """Page Gestion Projets avec CRUD complet"""
    st.title("💼 Gestion des Projets")
    
    # Bouton Ajouter Projet
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Nouveau Projet", type="primary"):
            st.session_state.show_add_form = True
    
    # Formulaire d'ajout (modal-like)
    if st.session_state.get('show_add_form', False):
        show_add_project_form()
    
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
    
    # Affichage des projets
    st.subheader(f"📋 Projets ({len(projets_filtered)})")
    
    if projets_filtered:
        for projet in projets_filtered:
            show_project_card(projet)
    else:
        st.info("Aucun projet ne correspond aux filtres sélectionnés.")

def show_add_project_form():
    """Formulaire d'ajout de projet"""
    st.markdown("### ➕ Nouveau Projet")
    
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
        
        description = st.text_area("Description détaillée", height=100)
        
        col1, col2, col3 = st.columns(3)
        
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
                    'description': description,
                    'suivi_mensuel': []
                }
                
                st.session_state.projets.append(nouveau_projet)
                st.session_state.show_add_form = False
                st.success(f"✅ Projet '{nom}' créé avec succès !")
                st.rerun()
            else:
                st.error("⚠️ Veuillez remplir tous les champs obligatoires.")

def filter_projects(filter_type, filter_status, filter_priority, sort_by):
    """Filtre et trie les projets"""
    projets = st.session_state.projets.copy()
    
    # Filtrage
    if filter_type != "Tous":
        projets = [p for p in projets if p['type'] == filter_type]
    
    if filter_status != "Tous":
        projets = [p for p in projets if p['statut'] == filter_status]
    
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

def show_project_card(projet):
    """Affiche une carte projet avec options CRUD"""
    type_class = {
        'Actif générateur': 'project-type-actif',
        'Passif': 'project-type-passif', 
        'Investissement formation': 'project-type-formation'
    }
    
    # Calculs
    delta_budget = projet['montant_total'] - projet['montant_utilise_reel']
    progress = (projet['montant_utilise_reel'] / projet['montant_total']) * 100 if projet['montant_total'] > 0 else 0
    
    # Couleur statut
    status_color = {
        'Planifié': '🔵',
        'En cours': '🟡', 
        'Développement': '🟠',
        'Réalisé': '🟢',
        'Suspendu': '🔴'
    }
    
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="project-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <h3>{projet['nom']}</h3>
                    <span class="{type_class[projet['type']]}">{projet['type']}</span>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 16px; margin-bottom: 16px;">
                    <div style="text-align: center;">
                        <small>BUDGET TOTAL</small><br>
                        <strong>{format_currency(projet['montant_total'])}</strong>
                    </div>
                    <div style="text-align: center;">
                        <small>UTILISÉ</small><br>
                        <strong>{format_currency(projet['montant_utilise_reel'])}</strong>
                    </div>
                    <div style="text-align: center;">
                        <small>DELTA</small><br>
                        <strong>{format_currency(delta_budget)}</strong>
                    </div>
                    <div style="text-align: center;">
                        <small>CASH FLOW/MOIS</small><br>
                        <strong style="color: {'green' if projet['cash_flow_mensuel'] > 0 else 'red' if projet['cash_flow_mensuel'] < 0 else 'gray'}">
                            {format_currency(projet['cash_flow_mensuel'])}
                        </strong>
                    </div>
                </div>
                
                <div style="margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                        <span>Progression: {progress:.1f}%</span>
                        <span>{status_color.get(projet['statut'], '⚪')} {projet['statut']}</span>
                    </div>
                    <div style="background: #f0f0f0; border-radius: 10px; height: 8px; margin-top: 8px;">
                        <div style="background: #1FB8CD; height: 100%; border-radius: 10px; width: {progress}%;"></div>
                    </div>
                </div>
                
                <p style="font-size: 0.9rem; color: #666; margin-bottom: 16px;">
                    {projet['description']}
                </p>
                
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #888;">
                    <span>📅 Échéance: {projet['echeance'].strftime('%d/%m/%Y')}</span>
                    <span>📊 ROI: {projet['roi_attendu']}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("✏️ Modifier", key=f"edit_{projet['id']}"):
                st.session_state.edit_project_id = projet['id']
                st.rerun()
        
        with col3:
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
                    st.rerun()
    
    # Conseils des mentors
    advice = get_mentor_advice(projet['type'], projet['nom'])
    
    with st.expander(f"🎯 Conseils des 3 Mentors pour: {projet['nom']}"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🏢 Robert Kiyosaki")
            st.info(advice['kiyosaki'])
        
        with col2:
            st.markdown("#### 💎 Warren Buffett") 
            st.info(advice['buffett'])
        
        with col3:
            st.markdown("#### 💪 Dave Ramsey")
            st.info(advice['ramsey'])

def show_revenue_management():
    """Page Gestion des Revenus Variables"""
    st.title("💰 Gestion des Revenus Variables")
    
    st.markdown("""
    Cette section permet de gérer les revenus qui fluctuent chaque mois 
    (salaires supplémentaires, revenus business IIBA, loyers, etc.)
    """)
    
    # Formulaire ajout revenu
    with st.expander("➕ Ajouter un Revenu Variable"):
        with st.form("add_revenue_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nom_revenu = st.text_input("Nom du revenu", placeholder="ex: Bonus William")
                type_revenu = st.selectbox("Type", ["Salaire", "Business", "Loyer", "Investissement", "Autre"])
            
            with col2:
                montant_mensuel = st.number_input("Montant ce mois (FCFA)", min_value=0, step=10000)
                regulier = st.checkbox("Revenu régulier ?", help="Cocher si le montant est prévisible chaque mois")
            
            if st.form_submit_button("✅ Ajouter Revenu", type="primary"):
                nouveau_revenu = {
                    'nom': nom_revenu,
                    'montant_mensuel': montant_mensuel,
                    'type': type_revenu,
                    'regulier': regulier
                }
                st.session_state.revenus_variables.append(nouveau_revenu)
                st.success(f"Revenu '{nom_revenu}' ajouté !")
                st.rerun()
    
    # Affichage revenus actuels
    st.subheader("💼 Revenus Mensuels Actuels")
    
    if st.session_state.revenus_variables:
        for i, revenu in enumerate(st.session_state.revenus_variables):
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
                if st.button("🗑️", key=f"del_rev_{i}"):
                    st.session_state.revenus_variables.pop(i)
                    st.rerun()
        
        # Total
        total_revenus = sum(r['montant_mensuel'] for r in st.session_state.revenus_variables)
        st.markdown(f"### **Total Revenus: {format_currency(total_revenus)}**")
        
    else:
        st.info("Aucun revenu variable configuré.")
    
    # Graphique évolution
    st.subheader("📈 Évolution des Revenus")
    
    # Simulation données historiques
    import numpy as np
    mois = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')
    total_actuel = sum(r['montant_mensuel'] for r in st.session_state.revenus_variables)
    
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
            
            st.subheader(f"💡 Conseils pour: {project['nom']}")
            
            advice = get_mentor_advice(project['type'], project['nom'])
            
            # Affichage des conseils
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="mentor-card">
                    <h3>🏢 Robert Kiyosaki</h3>
                    <p><strong>"Père Riche, Père Pauvre"</strong></p>
                    <p><em>Focus: Quadrants du Cash Flow (E-S-B-I)</em></p>
                </div>
                """, unsafe_allow_html=True)
                st.info(advice['kiyosaki'])
            
            with col2:
                st.markdown("""
                <div class="mentor-card">
                    <h3>💎 Warren Buffett</h3>
                    <p><strong>"L'Oracle d'Omaha"</strong></p>
                    <p><em>Focus: Valeur Long Terme & Compréhension</em></p>
                </div>
                """, unsafe_allow_html=True)
                st.info(advice['buffett'])
            
            with col3:
                st.markdown("""
                <div class="mentor-card">
                    <h3>💪 Dave Ramsey</h3>
                    <p><strong>"Total Money Makeover"</strong></p>
                    <p><em>Focus: Discipline & Baby Steps</em></p>
                </div>
                """, unsafe_allow_html=True)
                st.info(advice['ramsey'])
            
            # Synthèse consensus
            st.markdown("### 🤝 Synthèse Consensus des 3 Mentors")
            
            if project['type'] == 'Actif générateur':
                st.markdown("""
                <div class="alert-success">
                <strong>✅ ACCORD UNANIME</strong>: Ce projet est excellent pour votre indépendance financière.<br>
                • <strong>Kiyosaki</strong>: Développe vos revenus passifs<br>
                • <strong>Buffett</strong>: Investissement long terme compréhensible<br>  
                • <strong>Ramsey</strong>: Si financé sans dette excessive<br><br>
                <strong>Action recommandée</strong>: Poursuivre le projet en respectant votre budget.
                </div>
                """, unsafe_allow_html=True)
            
            elif project['type'] == 'Passif':
                st.markdown("""
                <div class="alert-warning">
                <strong>⚠️ ATTENTION REQUISE</strong>: Les 3 mentors recommandent la prudence.<br>
                • <strong>Kiyosaki</strong>: Questionner si c'est vraiment nécessaire<br>
                • <strong>Buffett</strong>: Analyser le coût d'opportunité<br>
                • <strong>Ramsey</strong>: Vérifier que c'est dans votre budget 50/30/20<br><br>
                <strong>Action recommandée</strong>: Réduire ou reporter si possible.
                </div>
                """, unsafe_allow_html=True)
            
            else:  # Formation
                st.markdown("""
                <div class="alert-success">
                <strong>📚 INVESTISSEMENT APPROUVÉ</strong>: Tous soutiennent l'éducation.<br>
                • <strong>Kiyosaki</strong>: Meilleur ROI pour le capital humain<br>
                • <strong>Buffett</strong>: Avantage concurrentiel permanent<br>
                • <strong>Ramsey</strong>: Priorité familiale dans budget équilibré<br><br>
                <strong>Action recommandée</strong>: Maintenir l'investissement éducatif.
                </div>
                """, unsafe_allow_html=True)
    
    else:
        st.info("Aucun projet disponible. Ajoutez des projets dans la section 'Gestion Projets'.")

def show_analytics():
    """Page Analytics & KPIs"""
    st.title("📈 Analytics & KPIs Avancés")
    
    kpis = calculer_kpis()
    
    # Graphiques avancés
    col1, col2 = st.columns(2)
    
    with col1:
        # Évolution projetée vers indépendance financière
        years = [2025, 2026, 2027, 2028, 2029, 2030]
        independence_progress = [5, 15, 30, 50, 75, 100]
        
        fig = px.line(
            x=years, y=independence_progress,
            title="🎯 Projection Indépendance Financière",
            labels={'x': 'Année', 'y': 'Indépendance (%)'}
        )
        fig.add_hline(y=50, line_dash="dash", annotation_text="Seuil Liberté Partielle")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gauge chart pour les revenus passifs
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = kpis['revenus_passifs_pct'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Revenus Passifs (%)"},
            delta = {'reference': 30},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#1FB8CD"},
                'steps': [
                    {'range': [0, 25], 'color': "#ffebee"},
                    {'range': [25, 50], 'color': "#fff3e0"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 30}
            }
        ))
        fig.update_layout(height=300)
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
            format_currency(kpis['cash_flow_mensuel']),
            f"{kpis['ratio_actifs_passifs']:.1f}%",
            f"{kpis['revenus_passifs_pct']:.1f}%",
            f"{kpis['fonds_urgence_mois']} mois",
            f"{kpis['nombre_actifs']} actifs",
            kpis['phase_actuelle'],
            f"{kpis['baby_step_actuel']}/7"
        ],
        'Objectif 2026': [
            '+500,000 FCFA',
            '40%',
            '30%', 
            '6 mois',
            '5 actifs',
            'Transition',
            '4-5/7'
        ],
        'Statut': [
            '🔴' if kpis['cash_flow_mensuel'] < 0 else '🟢',
            '🔴' if kpis['ratio_actifs_passifs'] < 20 else ('🟡' if kpis['ratio_actifs_passifs'] < 40 else '🟢'),
            '🔴' if kpis['revenus_passifs_pct'] < 15 else ('🟡' if kpis['revenus_passifs_pct'] < 30 else '🟢'),
            '🔴' if kpis['fonds_urgence_mois'] < 3 else '🟢',
            '🔴' if kpis['nombre_actifs'] < 3 else '🟢',
            '🔴' if kpis['phase_actuelle'] == 'Stabilisation' else ('🟡' if kpis['phase_actuelle'] == 'Transition' else '🟢'),
            '🔴' if kpis['baby_step_actuel'] < 3 else ('🟡' if kpis['baby_step_actuel'] < 5 else '🟢')
        ]
    }
    
    df_kpis = pd.DataFrame(kpi_data)
    st.dataframe(df_kpis, use_container_width=True, hide_index=True)
    
    # Alertes financières
    st.subheader("🚨 Alertes Financières")
    
    if kpis['fonds_urgence_mois'] < 3:
        st.markdown("""
        <div class="alert-error">
        <strong>Fonds d'urgence critique:</strong> Vous devez constituer un fonds d'urgence de 6 mois (19,692,000 FCFA)
        </div>
        """, unsafe_allow_html=True)
    
    if kpis['cash_flow_mensuel'] < 0:
        st.markdown("""
        <div class="alert-warning">
        <strong>Cash flow négatif:</strong> Réduisez vos passifs ou augmentez vos actifs générateurs
        </div>
        """, unsafe_allow_html=True)
    
    if kpis['ratio_actifs_passifs'] < 20:
        st.markdown("""
        <div class="alert-warning">
        <strong>Ratio actifs/passifs critique:</strong> Réorientez vos investissements vers plus d'actifs générateurs
        </div>
        """, unsafe_allow_html=True)

def show_progression():
    """Page Progression Familiale"""
    st.title("🚀 Progression Familiale vers l'Indépendance")
    
    # Baby Steps Dave Ramsey
    st.subheader("👶 Baby Steps Dave Ramsey - Progression")
    
    baby_steps = [
        ("Fonds d'urgence starter 1 000$ (665k FCFA)", 1),
        ("Éliminer toutes dettes (sauf immobilier)", 2),  
        ("Fonds d'urgence complet 3-6 mois", 3),
        ("Investir 15% revenus pour retraite", 4),
        ("Épargne université enfants", 5),
        ("Rembourser hypothèque anticipé", 6),
        ("Construire richesse et donner", 7)
    ]
    
    kpis = calculer_kpis()
    current_step = kpis['baby_step_actuel']
    
    for step_desc, step_num in baby_steps:
        if step_num < current_step:
            status_icon = "✅"
            status_class = "alert-success"
        elif step_num == current_step:
            status_icon = "🔄"
            status_class = "alert-warning"
        else:
            status_icon = "⏳"
            status_class = "alert-error"
            
        st.markdown(f"""
        <div class="{status_class}">
            <strong>{status_icon} Étape {step_num}:</strong> {step_desc}
        </div>
        """, unsafe_allow_html=True)
    
    # Phases d'évolution
    st.subheader("📈 Phases vers l'Indépendance Financière")
    
    phase_actuelle = kpis['phase_actuelle']
    
    phases_info = {
        'Stabilisation': {
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
            'duree': "6-12 mois",
            'color': 'error'
        },
        'Transition': {
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
            'duree': "12-18 mois",
            'color': 'warning'
        },
        'Expansion': {
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
            'duree': "18+ mois",
            'color': 'success'
        }
    }
    
    col1, col2, col3 = st.columns(3)
    
    for i, (phase_name, col) in enumerate(zip(phases_info.keys(), [col1, col2, col3])):
        with col:
            is_current = (phase_actuelle == phase_name)
            phase_info = phases_info[phase_name]
            
            status_text = "🎯 PHASE ACTUELLE" if is_current else phase_name.upper()
            alert_class = f"alert-{phase_info['color']}"
            
            st.markdown(f"""
            <div class="{alert_class}">
                <strong>{status_text}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            if is_current:
                st.markdown("**Actions prioritaires:**")
                for action in phase_info['actions']:
                    st.write(f"• {action}")
                
                st.markdown("**Objectifs:**")
                for objectif in phase_info['objectifs']:
                    st.write(f"• {objectif}")
                
                st.info(f"**Durée estimée:** {phase_info['duree']}")

def show_children_education():
    """Page Éducation Financière des Enfants"""
    st.title("👨‍👩‍👧‍👦 Éducation Financière des Enfants")
    
    enfants = [
        {
            'nom': 'Uriel',
            'age': 14,
            'emoji': '👦',
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
            ],
            'activites': [
                'Jeu de société Cashflow for Kids de Kiyosaki',
                'Simulation investissement avec argent virtuel',
                'Création d\'un petit business (art, tutorat)',
                'Participation aux discussions financières familiales',
                'Lecture: "Père Riche Père Pauvre pour les jeunes"'
            ]
        },
        {
            'nom': 'Naelle', 
            'age': 7,
            'emoji': '👧',
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
            ],
            'activites': [
                'Jeux de comptage et reconnaissance monnaie',
                'Tirelire transparente pour voir l\'argent grandir',
                'Sorties shopping éducatives (comparer prix)',
                'Histoires et livres sur l\'argent pour enfants',
                'Récompenses pour épargne et bons choix'
            ]
        },
        {
            'nom': 'Nell-Henri',
            'age': 5,
            'emoji': '👶',
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
            ],
            'activites': [
                'Jeux de rôle "magasin" et "banque"',
                'Comptines et chansons sur l\'argent',
                'Images et dessins pour expliquer épargne',
                'Récompenses visuelles pour attendre/épargner',
                'Participation aux courses (porter, choisir)'
            ]
        }
    ]
    
    # Affichage des enfants
    for enfant in enfants:
        with st.container():
            st.markdown(f"## {enfant['emoji']} {enfant['nom']} ({enfant['age']} ans)")
            st.markdown(f"**Niveau:** {enfant['niveau']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🎓 Concepts à enseigner")
                for concept in enfant['concepts']:
                    st.write(f"• {concept}")
                
                st.markdown("### 🎯 Objectifs 2025")
                for objectif in enfant['objectifs_2025']:
                    st.write(f"• {objectif}")
            
            with col2:
                st.markdown("### 🎮 Activités recommandées")
                for activite in enfant['activites']:
                    st.write(f"• {activite}")
            
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
        st.markdown(f"**{mois}:** {activite}")

def show_vision_2030():
    """Page Vision Familiale 2030"""
    st.title("🔮 Vision Familiale 2030")
    st.subheader("🇨🇭 Objectif: Toute la famille en Suisse avec indépendance financière")
    
    # Timeline 2025-2030
    st.markdown("### 📅 Roadmap Stratégique 2025-2030")
    
    milestones = {
        '2025': 'Stabilisation finances + finalisation actifs Cameroun',
        '2026': 'Transition - développement revenus passifs',
        '2027': 'Expansion - multiplication actifs générateurs',
        '2028': 'Préparation déménagement famille',
        '2029': 'Installation progressive en Suisse',
        '2030': 'Indépendance financière complète'
    }
    
    for year, milestone in milestones.items():
        progress = ((int(year) - 2025) / 5) * 100
        
        if year == '2025':
            color = "error"
            status = "EN COURS"
        elif year in ['2026', '2027']:
            color = "warning"
            status = "PLANIFIÉ"
        else:
            color = "success"
            status = "OBJECTIF"
            
        st.markdown(f"""
        <div class="alert-{color}">
            <strong>{year} - {status}</strong><br>
            {milestone}
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(progress / 100)
    
    # Projets enfants 2030
    st.markdown("### 👨‍👩‍👧‍👦 Projets Enfants - Situation 2030")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🎓 Uriel (19 ans)")
        st.info("""
        **Situation:** Université Suisse - Budget 200k CHF/an
        
        **Préparation requise:**
        - Dossier université suisse (2027-2028)
        - Maîtrise français/allemand
        - Portfolio artistique international
        - Budget: 200k CHF/an (133M FCFA/an)
        """)
    
    with col2:
        st.markdown("#### 📚 Naelle (12 ans)")  
        st.info("""
        **Situation:** Collège international - Budget 50k CHF/an
        
        **Préparation requise:**
        - Intégration système scolaire suisse (2028)
        - Apprentissage allemand précoce
        - Adaptation sociale et culturelle
        - Budget: 50k CHF/an (33M FCFA/an)
        """)
    
    with col3:
        st.markdown("#### 🏫 Nell-Henri (10 ans)")
        st.info("""
        **Situation:** École primaire Suisse - Budget 30k CHF/an
        
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
        
        # Gap à combler
        revenus_actuels = 200000  # Estimation actuelle
        gap = revenus_passifs_mensuels - revenus_actuels
        
        st.metric("Gap à combler", f"{gap:,.0f} FCFA/mois")

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
    else:
        st.title("🚧 Page en construction")
        st.info("Cette fonctionnalité sera disponible dans la prochaine version.")

if __name__ == "__main__":
    main()
