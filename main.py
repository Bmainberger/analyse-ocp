import streamlit as st
from datetime import date
import pandas as pd
from fpdf import FPDF

# --- 1. FONCTION PDF ---
def generate_pdf(nom, prenom, p_net, r_mens, endettement, gap, notes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'BILAN PATRIMONIAL STRATEGIQUE - OCP', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Client : {prenom} {nom}", 0, 1)
    pdf.cell(0, 10, f"Date : {date.today().strftime('%d/%m/%Y')}", 0, 1)
    pdf.ln(5)
    pdf.cell(0, 10, f"Patrimoine Net : {p_net:,.0f} EUR", 0, 1)
    pdf.cell(0, 10, f"Revenu Mensuel : {r_mens:,.0f} EUR", 0, 1)
    pdf.cell(0, 10, f"Taux Endettement : {endettement:.1f} %", 0, 1)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "Synthese de l'Expert :", 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 10, notes if notes else "Analyse realisee par OCP.")
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 2. CONFIGURATION ---
st.set_page_config(page_title="OCP Patrimoine", page_icon="🛡️", layout="wide")

# --- 3. INITIALISATION ---
total_brut_immo = 0.0
total_brut_fin = 0.0
total_passif = 0.0

# --- 4. ACCÈS EXPERT ---
if 'is_expert' not in st.session_state:
    st.session_state['is_expert'] = False

with st.sidebar:
    st.title("🔐 Espace Expert")
    code_admin = st.text_input("Code confidentiel", type="password")
    if code_admin == "ADMINOCP":
        st.session_state['is_expert'] = True
    else:
        st.session_state['is_expert'] = False

st.title("Votre stratégie patrimoniale commence ici.")
st.markdown("---")

# --- MODULE 1 : ÉTAT CIVIL ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)
with col1:
    nom_client = st.text_input("Nom du Client", key="nom_c")
    prenom_client = st.text_input("Prénom du Client", key="pre_c")
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)"], key="sit_mat")
with col2:
    nb_enfants = st.number_input("Nombre d'enfants", min_value=0, step=1, key="nb_e")
    if situation in ["Marié(e)", "Pacsé(e)"]:
        st.text_input("Prénom du Conjoint", key="pre_conj")

# --- MODULE 3 : REVENUS ---
st.header("3. Situation Professionnelle & Revenus")
cp1, cp2 = st.columns(2)
rev_annuel = cp1.number_input("Revenu net annuel (€)", min_value=0.0, key="rev_a")
rev_foncier = cp2.number_input("Autres revenus mensuels (€)", min_value=0.0, key="rev_f")

# --- MODULES 4, 5, 6 : ACTIFS ---
st.header("4, 5 & 6. Patrimoine Immobilier & Financier")
tab1, tab2 = st.tabs(["🏠 Immobilier", "🏢 Placements Financiers"])

with tab1:
    nb_biens = st.number_input("Nombre de biens physiques", min_value=0, key="nb_p_p")
    for i in range(int(nb_biens)):
        with st.expander(f"Bien n°{i+1}", expanded=True):
            val_i = st.number_input(f"Valeur vénale (€) - Bien {i+1}", min_value=0.0, key=f"val_i_{i}")
            total_brut_immo += val_i

with tab2:
    nb_fin = st.number_input("Nombre de contrats financiers", min_value=0, key="nb_f_f")
    for j in range(int(nb_fin)):
        with st.expander(f"Contrat n°{j+1}", expanded=True):
            m_f = st.number_input(f"Solde (€) - Contrat {j+1}", min_value=0.0, key=f"m_f_{j}")
            total_brut_fin += m_f

# --- MODULE 9 : PASSIF ---
st.header("9. Passif & Endettement")
nb_pret = st.number_input("Nombre de crédits", min_value=0, key="nb_p_immo")
for k in range(int(nb_pret)):
    with st.expander(f"Crédit n°{k+1}"):
        crdu = st.number_input(f"Restant Dû (€) - Crédit {k+1}", min_value=0.0, key=f"crdu_p_{k}")
        total_passif += crdu

# --- MODULE 12 : ANALYSE EXPERT ---
if st.session_state['is_expert']:
    st.markdown("---")
    st.header("📊 ANALYSE STRATÉGIQUE BIG EXPERT")
    
    p_brut = total_brut_immo + total_brut_fin
    p_net = p_brut - total_passif
    r_mens = (rev_annuel / 12) + rev_foncier
    tx_endett = (total_passif / p_brut * 100) if p_brut > 0 else 0.0
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Patrimoine Net", f"{p_net:,.0f} €")
    c2.metric("Revenu Mensuel", f"{r_mens:,.0f} €")
    c3.metric("Endettement", f"{tx_endett:.1f} %")

    t_a, t_b, t_c, t_d = st.tabs(["🛡️ Structure & Risques", "💸 Fiscalité", "☂️ Prévoyance", "👴 Retraite"])
    
    with t_a:
        st.write("**Répartition des Actifs**")
        if p_brut > 0:
            df_st = pd.DataFrame({"Pilier
