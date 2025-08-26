# Plan Financier Stratégique - Pages Complètes
# Extension pour les pages manquantes de l'application Streamlit

def show_mentor_advice():
    st.title("🎯 Conseil des 3 Mentors Financiers")
    
    # Sélection d'un projet
    projets = st.session_state.data['projets']
    project_names = [p['nom'] for p in projets]
    
    if project_names:
        selected_project = st.selectbox("Choisir un projet pour conseil détaillé", project_names)
        
        if selected_project:
            project = next(p for p in projets if p['nom'] == selected_project)
            
            st.subheader(f"💡 Conseils pour: {project['nom']}")
            
            advice = get_mentor_advice(project['type'], project['montant'], project['nom'])
            
            # Affichage des conseils avec le design original
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
    st.title("📈 Analytics & KPIs Avancés")
    
    calculer_kpis()
    kpis = st.session_state.data['kpis']
    
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
    st.dataframe(df_kpis, use_container_width=True)
    
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
    
    if kpis['regle_50_30_20']['besoins'] > 50:
        st.markdown("""
        <div class="alert-warning">
        <strong>Règle 50/30/20 non respectée:</strong> Réajustez votre répartition budgétaire
        </div>
        """, unsafe_allow_html=True)

def show_progression():
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
    
    current_step = st.session_state.data['kpis']['baby_step_actuel']
    
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
    
    phase_actuelle = st.session_state.data['kpis']['phase_actuelle']
    
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
    
    # Indicateurs de succès
    st.markdown("### 📈 Indicateurs de Succès Vision 2030")
    
    success_categories = {
        'Financier 💰': [
            '12M+ FCFA/mois revenus passifs',
            'Patrimoine net 2+ milliards FCFA', 
            'Indépendance financière complète',
            'Fonds éducation enfants sécurisé'
        ],
        'Familial 👨‍👩‍👧‍👦': [
            'Famille unie et stabilisée en Suisse',
            'Enfants intégrés système éducatif',
            'Maîtrise langues locales',
            'Réseau social et professionnel établi'
        ],
        'Éducatif 🎓': [
            'Uriel: diplôme universitaire suisse',
            'Naelle: excellence scolaire adaptée',
            'Nell-Henri: intégration réussie',
            'Tous: éducation financière solide'
        ],
        'Personnel 🌟': [
            'William: transition E→B réussie',
            'Alix: expertise investissements',
            'Santé familiale optimale', 
            'Épanouissement personnel de tous'
        ]
    }
    
    col1, col2 = st.columns(2)
    
    categories_items = list(success_categories.items())
    
    with col1:
        for category, metrics in categories_items[:2]:
            st.markdown(f"#### {category}")
            for metric in metrics:
                st.write(f"✅ {metric}")
    
    with col2:
        for category, metrics in categories_items[2:]:
            st.markdown(f"#### {category}")
            for metric in metrics:
                st.write(f"✅ {metric}")

# Ajouter ces nouvelles fonctions au main()
def main():
    # Chargement CSS
    load_css()
    
    # Sidebar
    selected_page = render_sidebar()
    
    # Routing des pages
    if selected_page == "📊 Dashboard Principal":
        show_dashboard()
    elif selected_page == "💼 Gestion Projets X":
        show_project_management()
    elif selected_page == "🎯 Conseils 3 Mentors":
        show_mentor_advice()
    elif selected_page == "📈 KPIs & Analytics":
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
