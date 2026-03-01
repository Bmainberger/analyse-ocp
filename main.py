import streamlit as st
from datetime import date

# 1. CONFIGURATION
st.set_page_config(page_title="OCP Patrimoine", page_icon="🛡️", layout="wide")

# Style OCP
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #26e291; color: #1a2b49; border-radius: 8px;
        padding: 0.7em 2.5em; font-weight: bold; border: none;
    }
    .stHeader { color: #1a2b49; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ OCP Patrimoine : Diagnostic Complet")

# --- SECTION 1 : ÉTAT CIVIL ---
st.header("1. État Civil & Situation Familiale")
c1, c2 = st.columns(2)
with c1:
    st.text_input("Nom du Client", key="nom_c")
    st.text_input("Prénom du Client", key="pre_c")
    st.date_input("Date de naissance", value=date(1980, 1, 1), key="dnaiss_c")
with c2:
    st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"], key="sit_mat")
    st.number_input("Nombre d'enfants à charge", min_value=0, step=1, key="nb_e")

# --- SECTION 2 : COORDONNÉES ---
st.header("2. Coordonnées")
cc1, cc2, cc3 = st.columns([2, 1, 1])
cc1.text_input("Adresse postale complète", key="adr_p")
cc2.text_input("Téléphone", key="tel_p")
cc3.text_input("Email", key="mail_p")

# --- SECTION 3 : SITUATION PROFESSIONNELLE ---
st.header("3. Situation Professionnelle & Revenus")
cp1, cp2, cp3 = st.columns(3)
with cp1:
    st.selectbox("Statut Professionnel", ["Salarié", "TNS / Libéral", "Dirigeant", "Retraité"], key="statut_pro")
    st.text_input("Profession / Poste", key="poste_pro")
with cp2:
    st.number_input("Revenu net annuel (€)", min_value=0.0, key="rev_a")
    st.number_input("Autres revenus (€)", min_value=0.0, key="rev_f")
with cp3:
    st.selectbox("TMI (%)", ["0%", "11%", "30%", "41%", "45%"], key="tmi_c")
    st.number_input("Âge de retraite prévu", min_value=50, max_value=80, value=64, key="age_ret")

# --- SECTION 4 & 5 : PATRIMOINE IMMOBILIER ---
st.header("4 & 5. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier (SCPI, SCI, GFV...)"])

with tab1:
    nb_p = st.number_input("Nombre de biens immobiliers physiques", min_value=0, value=1, key="nb_p_p")
    for i in range(int(nb_p)):
        with st.expander(f"Bien Immobilier n°{i+1}", expanded=True):
            st.selectbox(f"Usage {i}", ["Résidence Principale", "Résidence Secondaire", "Locatif Nu", "LMNP", "Terrain"], key=f"usage_p_{i}")
            st.number_input(f"Valeur estimée (€) {i}", min_value=0.0, key=f"val_p_{i}")

with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0, value=1, key="nb_p_c")
    for j in range(int(nb_coll)):
        with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
            t_coll = st.selectbox(f"Type de support {j}", ["SCPI", "SCI", "GFV / GFI", "OPCI"], key=f"type_c_{j}")
            ca, cb, cc = st.columns(3)
            with ca:
                st.text_input(f"Nom du support {j}", key=f"nom_c_{j}")
                st.selectbox(f"Mode de détention {j}", ["Pleine Propriété", "Nue-Propriété", "Usufruit", "Via Assurance-Vie", "Via PER"], key=f"det_c_{j}")
            with cb:
                px_p = st.number_input(f"Prix de part (€) {j}", min_value=0.0, step=1.0, key=f"px_c_{j}")
                nb_parts = st.number_input(f"Nombre de parts {j}", min_value=0.0, step=1.0, key=f"nb_c_{j}")
            with cc:
                if t_coll == "SCPI": st.number_input(f"TOF (%) {j}", key=f"tof_c_{j}")
                elif t_coll == "GFV / GFI": st.text_input(f"Surface / Exploitation {j}", key=f"surf_c_{j}")
            st.write(f"Valeur estimée : {px_p * nb_parts:,.0f} €")

# --- SECTION 6 : PATRIMOINE FINANCIER ---
st.header("6. Patrimoine Financier")
nb_f = st.number_input("Nombre de comptes/contrats financiers", min_value=0, value=1, key="nb_fin")
for k in range(int(nb_f)):
    with st.expander(f"Contrat n°{k+1}", expanded=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            st.selectbox(f"Type {k}", ["Livret", "Assurance-Vie", "PER", "PEA", "Compte-Titres"], key=f"f_type_{k}")
