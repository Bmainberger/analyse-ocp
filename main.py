import streamlit as st
from datetime import date
import pandas as pd
from fpdf import FPDF

# --- FONCTION GÉNÉRATION PDF (AJOUT SANS MODIFIER LE RESTE) ---
def generate_pdf(nom, prenom, p_net, r_mens, endettement, gap, notes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(29, 46, 77)
    pdf.cell(0, 10, 'BILAN PATRIMONIAL STRATEGIQUE - OCP', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Client : {prenom} {nom}", 0, 1)
    pdf.cell(0, 10, f"Date : {date.today().strftime('%d/%m/%Y')}", 0, 1)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(60, 10, 'Indicateur', 1, 0, 'C')
    pdf.cell(60, 10, 'Valeur', 1, 1, 'C')
    pdf.set_font('Arial', '', 11)
    pdf.cell(60, 10, 'Patrimoine Net', 1, 0)
    pdf.cell(60, 10, f"{p_net:,.0f} EUR", 1, 1)
    pdf.cell(60, 10, 'Revenu Mensuel', 1, 0)
    pdf.cell(60, 10, f"{r_mens:,.0f} EUR", 1, 1)
    pdf.cell(60, 10, 'Taux Endettement', 1, 0)
    pdf.cell(60, 10, f"{endettement:.1f} %", 1, 1)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Synthese de l\'Expert :', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 10, notes if notes else "Analyse en cours.")
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# 1. CONFIGURATION & STYLE (VOTRE STYLE ORIGINAL)
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

# 2. INITIALISATION DES COMPTEURS (VOS CALCULS)
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
    nom_client = st.text_input("Nom du Client", key="nom_c")
    prenom_client = st.text_input("Prénom du Client", key="pre_c")
    date_naissance = st.date_input("Date de naissance", value=date(1980, 1, 1), key="dnaiss_c")
    lieu_naissance = st.text_input("Lieu de naissance", key="lieu_c")
    nationalite = st.text_input("Nationalité", key="nat_c") 

with col2:
    st.subheader("Situation")
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"], key="sit_mat")
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1, key="nb_e")

if situation in ["Marié(e)", "Pacsé(e)"]:
    st.markdown("---")
    st.subheader("Informations du Conjoint")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        nom_conj =
