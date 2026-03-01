import streamlit as st
from datetime import date

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="OCP Patrimoine - Diagnostic", page_icon="🛡️", layout="wide")

# Style Visuel OCP (Couleurs et Cartes)
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    div.stButton > button {
        background-color: #26e291; color: #1a2b49; border-radius: 8px;
        padding: 0.8em 2.5em; font-weight: bold; border: none; font-size: 1.1rem;
    }
    .hero-title { font-size: 3rem; font-weight: 800; color: #1a2b49; }
    .benefit-card { background-color: #f8fafc; padding: 20px; border-radius: 10px; border-left: 5px solid #26e291; height: 100%; }
    </style>
    """, unsafe_allow_html=True)

# Initialisation des états
if 'page' not in st.session_state:
    st.session_state['page'] = 'accueil'
if 'is_expert' not in st.session_state:
    st.session_state['is_expert'] = False

# --- BARRE LATÉRALE : ACCÈS PRIVILÉGIÉ (CLIENTS OU EXPERT) ---
with st.sidebar:
    st.title("🔐 Espace Privé")
    st.write("Si vous avez reçu un code d'accès OCP, saisissez-le ici :")
    code_saisi = st.text_input("Code confidentiel", type="password")
    
    if code_saisi == "ADMINOCP":
        st.session_state['is_expert'] = True
        st.success("👨‍💼 MODE EXPERT ACTIVÉ")
        st.session_state['page'] = 'formulaire' # Envoie l'expert direct au formulaire
    elif code_saisi == "OCP2026":
        st.session_state['is_expert'] = False
        st.info("✅ Accès Client Privilégié")
        st.session_state['page'] = 'formulaire' # Envoie le client direct au formulaire

# --- PAGE 1 : ACCUEIL PRESTIGE (POUR LES PROSPECTS DU WEB) ---
if st.session_state['page'] == 'accueil':
    st.markdown('<h1 class="hero-title">Prenez de la hauteur sur votre patrimoine.</h1>', unsafe_allow_html=True)
    st.subheader("Un diagnostic clair, complet et gratuit réalisé par OCP Patrimoine.")
    
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        st.markdown('<div class="benefit-card"><h3>🔭 Vision 360°</h3><p>Regroupez vos biens immobiliers, placements et dettes sur une seule interface.</p></div>', unsafe_allow_html=True)
    with col_b2:
        st.markdown('<div class="benefit-card"><h3>📈 Optimisation</h3><p>Identifiez les leviers pour réduire vos impôts et préparer votre transmission.</p></div>', unsafe_allow_html=True)
    with col_b3:
        st.markdown('<div class="benefit-card"><h3>🛡️ Sérénité</h3><p>Un diagnostic précis pour piloter votre avenir en toute confidentialité.</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.write("**Le Processus :** 1. Remplissez vos données (5 min) / 2. Analyse par votre conseiller / 3. Entretien de restitution.")
    
    if st.button("🚀 DÉMARRER MON BILAN GRATUIT"):
        st.session_state['page'] = 'formulaire'
        st.rerun()
    st.stop()

# --- PAGE 2 : LE FORMULAIRE DÉTAILLÉ (ACCÈS LIBRE OU CODE) ---
total_brut_immo = 0.0
total_brut_fin = 0.0
total_passif = 0.0
mensualites_totales = 0.0
reste_vivre_brut = 0.0

# 1. ÉTAT CIVIL & FAMILLE
st.header("1. État Civil & Famille")
c1, c2 = st.columns(2)
with c1:
    st.text_input("Nom du Client", key="nom_c")
    st.text_input("Prénom du Client", key="pre_c")
    st.date_input("Date de naissance", value=date(1980, 1, 1), key="dnaiss_c")
    st.text_input("Nationalité", key="nat_c")
with c2:
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"], key="sit_mat")
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, step=1, key="nb_e")

# 3. REVENUS & BUDGET
st.header("3. Profession & Revenus")
cp1, cp2, cp3 = st.columns(3)
with cp1:
    st.selectbox("Statut", ["Salarié", "TNS", "Dirigeant", "Retraité"], key="statut_pro")
    rev_annuel = st.number_input("Revenu net annuel (€)", min_value=0.0, key="rev_a")
with cp2:
    vie_mensuelle = st.number_input("Train de vie mensuel (€)", min_value=0.0, key="budget_vie")
    impots_mens = st.number_input("Impôts mensuels (€)", min_value=0.0, key="budget_impot")
with cp3:
    st.selectbox("TMI", ["0%", "11%", "30%", "41%", "45%"], key="tmi_c")
    rev_mensuel_estim = rev_annuel / 12
    reste_vivre_brut = rev_mensuel_estim - (vie_mensuelle + impots_mens)

# 4 & 5. PATRIMOINE IMMOBILIER (Le cœur de votre expertise)
st.header("4 & 5. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immo Physique", "🏢 Pierre-Papier (SCPI, GFV...)"])
with tab1:
    nb_biens = st.number_input("Nombre de biens physiques", min_value=0, key="nb_p_p")
    for i in range(int(nb_biens)):
        with st.expander(f"Bien n°{i+1}", expanded=True):
            col_i1, col_i2 = st.columns(2)
            val_i = col_i1.number_input(f"Valeur vénale (€) {i}", key=f"v_i_{i}")
            col_i2.selectbox(f"Régime {i}", ["Nu", "LMNP", "Pinel", "MH"], key=f"r_i_{i}")
            total_brut_immo += val_i
with tab2:
    nb_coll = st.number_input("Nombre de placements (SCPI, SCI, GFV...)", min_value=0, key="nb_p_c")
    for j in range(int(nb_coll)):
        with st.expander(f"Placement n°{j+1}", expanded=True):
            t_coll = st.selectbox(f"Type {j}", ["SCPI", "SCI", "GFV / GFI", "Club Deal"], key=f"type_c_{j}")
            c_c1, c_c2 = st.columns(2)
            px_p = c_c1.number_input(f"Prix part {j}", key=f"px_{j}")
            nb_p = c_c2.number_input(f"Nb parts {j}", key=f"nb_{j}")
            total_brut_immo += (px_p * nb_p)
            if t_coll == "SCPI": st.number_input(f"TOF % {j}", key=f"tof_{j}")
            elif t_coll == "GFV / GFI": st.text_input(f"Surface {j}", key=f"surf_{j}")

# 6. PATRIMOINE FINANCIER
st.header("6. Patrimoine Financier")
nb_fin = st.number_input("Nombre de contrats financiers", min_value=0, key="nb_f")
for k in range(int(nb_fin)):
    with st.expander(f"Contrat n°{k+1}"):
        f1, f2 = st.columns(2)
        f1.selectbox(f"Type {k}", ["Assurance-Vie", "PER", "PEA", "Livret"], key=f"tf_{k}")
        solde_f = f2.number_input(f"Solde (€) {k}", key=f"sf_{k}")
        total_brut_fin += solde_f

# 7. PRÉVOYANCE
st.header("7. Prévoyance & Protection")
nb_prev = st.number_input("Nombre de contrats prévoyance", min_value=0, key="nb_prev")
for p in range(int(nb_prev)):
    with st.expander(f"Prévoyance n°{p+1}"):
        p1, p2 = st.columns(2)
        p1.selectbox(f"Garantie {p}", ["Décès", "IJ", "Invalidité", "Emprunteur"], key=f"pt_{p}")
        p2.text_input(f"Bénéficiaires {p}", key=f"pb_{p}")

# 9. PASSIF
st.header("9. Passif & Endettement")
nb_pret = st.number_input("Nombre de crédits immobiliers", min_value=0, key="nb_pret")
for i in range(int(nb_pret)):
    with st.expander(f"Crédit n°{i+1}"):
        cp1, cp2 = st.columns(2)
        total_passif += cp1.number_input(f"Restant dû (€) {i}", key=f"crdu_{i}")
        mensualites_totales += cp2.number_input(f"Mensualité (€) {i}", key=f"m_{i}")

# --- ANALYSE EXPERT (RESERVÉ ADMINOCP) ---
if st.session_state['is_expert']:
    st.sidebar.markdown("---")
    st.sidebar.title("📊 Analyse Expert")
    pat_brut = total_brut_immo + total_brut_fin
    pat_net = pat_brut - total_passif
    st.sidebar.metric("PATRIMOINE NET", f"{pat_net:,.0f} €")
    st.sidebar.metric("ÉPARGNE/MOIS", f"{(reste_vivre_brut - mensualites_totales):,.0f} €")
    
    if st.button("🚀 GÉNÉRER LE BILAN EXPERT"):
        st.balloons()
        st.header("📋 Diagnostic Stratégique OCP")
        col_an1, col_an2 = st.columns(2)
        col_an1.metric("Poids Immobilier", f"{(total_brut_immo/pat_brut*100 if pat_brut>0 else 0):.1f}%")
        col_an2.metric("Taux d'endettement", f"{(mensualites_totales/(rev_mensuel_estim if rev_mensuel_estim>0 else 1)*100):.1f}%")

# BOUTON FINAL
st.markdown("---")
if st.button("📤 ENVOYER MON DOSSIER"):
    st.balloons()
    st.success("Dossier transmis avec succès à OCP Patrimoine. Un conseiller reviendra vers vous.")
