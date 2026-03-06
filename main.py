import streamlit as st
from datetime import date
import pandas as pd

# 1. CONFIGURATION & STYLE
st.set_page_config(page_title="OCP Patrimoine", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #1d2e4d;
        color: white;
        font-size: 20px;
        font-weight: bold;
        width: 100%;
        border-radius: 5px;
        border: none;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. INITIALISATION DES COMPTEURS
total_brut_immo = 0.0
total_brut_fin = 0.0
total_passif = 0.0
mensualites_totales = 0.0

# 3. GESTION ACCÈS EXPERT
if 'is_expert' not in st.session_state:
    st.session_state['is_expert'] = False

with st.sidebar:
    st.title("🔐 Espace Expert")
    code_admin = st.text_input("Code confidentiel", type="password")
    if code_admin == "ADMINOCP":
        st.session_state['is_expert'] = True
        st.success("Mode Expert Activé")
    else:
        st.session_state['is_expert'] = False

# 4. LANDING PAGE
st.title("Votre stratégie patrimoniale commence ici.")
col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
    st.info("🔭 **Vision 360°**\n\nRegroupez tout votre patrimoine.")
with col_b2:
    st.info("📈 **Optimisation**\n\nRéduisez vos impôts.")
with col_b3:
    st.info("🛡️ **Sérénité**\n\nDiagnostic par un expert.")

st.markdown("---")

# --- SECTION 1 : ÉTAT CIVIL & FAMILLE ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Le Client")
    nom_client = st.text_input("Nom du Client")
    prenom_client = st.text_input("Prénom du Client")
    date_naissance = st.date_input("Date de naissance", value=date(1980, 1, 1))
    lieu_naissance = st.text_input("Lieu de naissance")
    nationalite = st.text_input("Nationalité") 

with col2:
    st.subheader("Situation")
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"])
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1)

if situation in ["Marié(e)", "Pacsé(e)"]:
    st.markdown("---")
    st.subheader("Informations du Conjoint")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        nom_conj = st.text_input("Nom du Conjoint")
        dnaiss_conj = st.date_input("Date de naissance conjoint", value=date(1980, 1, 1))
    with c_col2:
        pre_conj = st.text_input("Prénom du Conjoint")

if nb_enfants > 0:
    st.write("📅 **Détail des enfants :**")
    c_enf = st.columns(3)
    for i in range(int(nb_enfants)):
        with c_enf[i % 3]:
            st.date_input(f"Date de naissance Enfant n°{i+1}", value=date(2010, 1, 1), key=f"enf_{i}")

st.markdown("---")

# --- SECTION 2 : COORDONNÉES ---
st.header("2. Coordonnées")
c_coo1, c_coo2, c_coo3 = st.columns([2, 1, 1])
with c_coo1:
    st.text_input("Adresse postale complète")
with c_coo2:
    st.text_input("Téléphone")
with c_coo3:
    st.text_input("Email")

st.markdown("---")

# --- SECTION 3 : PROFESSION & REVENUS ---
st.header("3. Situation Professionnelle & Revenus")
cp1, cp2, cp3 = st.columns(3)
with cp1:
    st.selectbox("Statut Professionnel", ["Salarié", "TNS / Libéral", "Dirigeant", "Fonctionnaire", "Retraité", "Sans activité"])
    st.text_input("Profession / Intitulé du poste")
with cp2:
    rev_annuel = st.number_input("Revenu net annuel (€)", min_value=0.0)
    rev_foncier = st.number_input("Autres revenus (Foncier, etc.) (€)", min_value=0.0)
with cp3:
    st.selectbox("Tranche Marginale d'Imposition (TMI)", ["0%", "11%", "30%", "41%", "45%"])
    age_ret = st.number_input("Âge de départ à la retraite prévu", min_value=50, max_value=80, value=64)

st.subheader("📊 3. bis Budget & Capacité d'Épargne")
b_col1, b_col2 = st.columns(2)
with b_col1:
    st.number_input("Train de vie mensuel (€)", min_value=0.0)
    st.number_input("Loyer ou Charges (€)", min_value=0.0)
with b_col2:
    st.number_input("Impôts mensuels (€)", min_value=0.0)
    rev_mensuel_estim = (rev_annuel + rev_foncier) / 12
    st.info(f"Revenus mensuels estimés : {rev_mensuel_estim:,.0f} €")

st.markdown("---")

# --- SECTION 4 & 5 : PATRIMOINE IMMOBILIER ---
st.header("4 & 5. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier"])
with tab1:
    nb_biens = st.number_input("Nombre de biens immobiliers physiques", min_value=0)
    for i in range(int(nb_biens)):
        with st.expander(f"Bien n°{i+1}", expanded=True):
            val_i = st.number_input(f"Valeur vénale (€) - {i+1}", min_value=0.0)
            total_brut_immo += val_i

with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs (SCPI, etc.)", min_value=0)
    for j in range(int(nb_coll)):
        with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
            px_p = st.number_input(f"Prix de part (€) - {j+1}", min_value=0.0)
            nb_p = st.number_input(f"Nombre de parts - {j+1}", min_value=0.0)
            total_brut_immo += (px_p * nb_p)

st.markdown("---")

# --- SECTION 6 : PATRIMOINE FINANCIER ---
st.header("6. Patrimoine Financier")
nb_fin = st.number_input("Nombre de comptes/contrats financiers", min_value=0)
for k in range(int(nb_fin)):
    with st.expander(f"Contrat n°{k+1}"):
        m_f = st.number_input(f"Solde (€) - {k+1}", min_value=0.0)
        total_brut_fin += m_f

st.markdown("---")

# --- SECTION 7 : PRÉVOYANCE ---
st.header("7. Prévoyance & Protection")
nb_prev_input = st.number_input("Nombre de contrats de prévoyance", min_value=0)
for p in range(int(nb_prev_input)):
    with st.expander(f"Contrat Prévoyance n°{p+1}"):
        st.selectbox(f"Type - {p+1}", ["Décès", "IJ / Invalidité", "Homme clé"])
        st.number_input(f"Montant Garanti (€) - {p+1}")

st.markdown("---")

# --- SECTION 8 : SANTÉ ---
st.header("8. Santé / Mutuelle")
col_s1, col_s2 = st.columns(2)
with col_s1:
    st.text_input("Organisme / Assureur")
with col_s2:
    st.number_input("Cotisation annuelle (€)", min_value=0.0)

st.markdown("---")

# --- SECTION 9 : PASSIF ---
st.header("9. Passif & Endettement")
nb_pret_immo = st.number_input("Nombre de crédits immobiliers", min_value=0)
for i in range(int(nb_pret_immo)):
    with st.expander(f"Crédit Immo n°{i+1}"):
        crdu = st.number_input(f"Capital Restant Dû (€) - {i+1}", min_value=0.0)
        total_passif += crdu
        m_mens = st.number_input(f"Mensualité (€) - {i+1}", min_value=0.0)
        mensualites_totales += m_mens

st.markdown("---")

# --- SECTION 10 : REMARQUES ---
st.header("📝 10. Vos Remarques & Questions")
st.text_area("Avez-vous des précisions à nous apporter sur votre situation ?")

st.markdown("---")

# --- SECTION 11 : OBJECTIFS ---
st.header("🎯 11. Objectifs & Priorités")
col_obj1, col_obj2 = st.columns(2)
with col_obj1:
    st.multiselect("Quels sont vos objectifs principaux ?", 
                   ["Retraite", "Réduction d'impôts", "Protection famille", "Transmission", "Complément de revenus", "Achat résidence principale"])
with col_obj2:
    st.select_slider("Horizon d'investissement", options=["Court terme", "Moyen terme", "Long terme", "Transmission"])
    st.select_slider("Profil de risque", options=["Prudent", "Équilibré", "Dynamique", "Offensif"])

st.markdown("---")

# --- SECTION 12 : RÉSUMÉ RÉSERVÉ À L'EXPERT ---
if st.session_state['is_expert']:
    st.header("📊 ANALYSE STRATÉGIQUE BIG EXPERT")
    
    p_brut = total_brut_immo + total_brut_fin
    p_net = p_brut - total_passif
    r_mensuel_expert = (rev_annuel + rev_foncier) / 12
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Patrimoine Net", f"{p_net:,.0f} €".replace(",", " "))
    c2.metric("Revenu Mensuel", f"{r_mensuel_expert:,.0f} €".replace(",", " "))
    c3.metric("Ratio d'Endettement", f"{(total_passif/p_brut*100) if p_brut > 0 else 0:.1f} %")

    st.markdown("### 🎯 Diagnostics")
    tab_a, tab_b, tab_c, tab_d = st.tabs(["🛡️ Structure & Risques", "💸 Fiscalité", "☂️ Prévoyance", "👴 Retraite"])
    
    with tab_a:
        col_diag1, col_diag2 = st.columns(2)
        with col_diag1:
            st.write("**Forces & Points d'attention**")
            if p_net > 300000: st.success("✅ Patrimoine net significatif")
            if total_brut_fin < (r_mensuel_expert * 6): st.error("❌ Épargne de précaution insuffisante")
            if (total_passif/p_brut if p_brut > 0 else 0) > 0.40: st.warning("⚠️ Endettement > 40%")
        with col_diag2:
            st.write("**Répartition des Actifs**")
            df_st = pd.DataFrame({
                "Pilier": ["Immo", "Financier"],
                "Valeur": [total_brut_immo, total_brut_fin]
            })
            st.bar_chart(df_st.set_index("Pilier"))

    with tab_d:
        retraite_est = r_mensuel_expert * 0.55
        gap_val = r_mensuel_expert - retraite_est
        st.write(f"Manque à gagner mensuel estimé : **{gap_val:,.0f} €**")
        st.write(f"Capital à constituer pour compenser : **{gap_val * 250:,.0f} €**")

# BOUTON D'ENVOI FINAL (CÔTÉ CLIENT)
if not st.session_state['is_expert']:
    st.markdown("---")
    st.markdown("""
        <form action="https://formsubmit.co/bmainberger@ocp-patrimoine.com" method="POST">
            <button type="submit">🚀 TRANSMETTRE MON ÉTUDE</button>
        </form>
    """, unsafe_allow_html=True)
