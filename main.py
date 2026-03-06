import streamlit as st
from datetime import date
import pandas as pd
from fpdf import FPDF

# --- 1. FONCTION PDF (Indépendante, ne touche pas aux modules) ---
def generate_pdf(nom, prenom, p_net, r_mens, endettement, gap, notes):
    try:
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
        pdf.cell(0, 10, f"Taux Endettement : {endettement:.1f} %", 0, 1)
        pdf.cell(0, 10, f"Manque a gagner retraite : {gap:,.0f} EUR/mois", 0, 1)
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, "Synthese de l'expert :", 0, 1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(0, 10, notes if notes else "Analyse en cours.")
        return pdf.output(dest='S').encode('latin-1', 'ignore')
    except:
        return None

# --- 2. CONFIGURATION ---
st.set_page_config(page_title="OCP Patrimoine", page_icon="🛡️", layout="wide")

# --- 3. INITIALISATION DES VARIABLES (Pour que les graphiques voient 0 au lieu de VIDE) ---
total_brut_immo = 0.0
total_brut_fin = 0.0
total_passif = 0.0
rev_annuel = 0.0
rev_foncier = 0.0

# --- 4. ACCÈS EXPERT ---
if 'is_expert' not in st.session_state: st.session_state['is_expert'] = False
with st.sidebar:
    st.title("🔐 Espace Expert")
    code_admin = st.text_input("Code confidentiel", type="password")
    if code_admin == "ADMINOCP": st.session_state['is_expert'] = True
    else: st.session_state['is_expert'] = False

# --- MODULES 1 À 11 (VOTRE INTERFACE CLIENT) ---
st.title("Votre stratégie patrimoniale commence ici.")
st.markdown("---")

st.header("1. État Civil & Situation Familiale")
c1, c2 = st.columns(2)
with c1:
    nom_client = st.text_input("Nom du Client", value="")
    prenom_client = st.text_input("Prénom du Client", value="")
    situation = st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)"])
with c2:
    nb_enfants = st.number_input("Nombre d'enfants", min_value=0, step=1)
    if situation in ["Marié(e)", "Pacsé(e)"]:
        prenom_conj = st.text_input("Prénom du Conjoint")

st.header("3. Revenus")
cr1, cr2 = st.columns(2)
rev_annuel = cr1.number_input("Revenu net annuel (€)", min_value=0.0, step=1000.0)
rev_foncier = cr2.number_input("Autres revenus mensuels (€)", min_value=0.0, step=100.0)

st.header("4, 5 & 6. Actifs (Immo & Financier)")
t_actifs1, t_actifs2 = st.tabs(["🏠 Immobilier", "💰 Placements"])
with t_actifs1:
    nb_immo = st.number_input("Nombre de biens immobiliers", min_value=0, step=1)
    for i in range(nb_immo):
        val = st.number_input(f"Valeur Bien {i+1} (€)", min_value=0.0, key=f"immo_{i}")
        total_brut_immo += val
with t_actifs2:
    nb_fin = st.number_input("Nombre de contrats financiers", min_value=0, step=1)
    for j in range(nb_fin):
        val_f = st.number_input(f"Solde Contrat {j+1} (€)", min_value=0.0, key=f"fin_{j}")
        total_brut_fin += val_f

st.header("9. Passif")
nb_pret = st.number_input("Nombre de crédits en cours", min_value=0, step=1)
for k in range(nb_pret):
    dette = st.number_input(f"Restant dû Crédit {k+1} (€)", min_value=0.0, key=f"dette_{k}")
    total_passif += dette

# --- MODULE 12 : CONSOLE EXPERT (CHIFFRES & GRAPHES RÉTABLIS) ---
if st.session_state['is_expert']:
    st.markdown("---")
    st.header("📊 ANALYSE STRATÉGIQUE BIG EXPERT")
    
    # Calculs de base
    p_brut = total_brut_immo + total_brut_fin
    p_net = p_brut - total_passif
    r_mens = (rev_annuel / 12) + rev_foncier
    tx_endett = (total_passif / p_brut * 100) if p_brut > 0 else 0.0
    retraite_est = r_mens * 0.55
    gap_val = r_mens - retraite_est
    
    # Indicateurs Visuels
    m1, m2, m3 = st.columns(3)
    m1.metric("Patrimoine Net", f"{p_net:,.0f} €")
    m2.metric("Revenu Mensuel", f"{r_mens:,.0f} €")
    m3.metric("Endettement", f"{tx_endett:.1f} %")

    # Onglets de Diagnostic
    tab_diag1, tab_diag2, tab_diag3 = st.tabs(["📈 Graphique", "☂️ Prévoyance", "👴 Retraite"])
    
    with tab_diag1:
        st.subheader("Répartition du Patrimoine")
        df_plot = pd.DataFrame({
            "Catégorie": ["Immobilier", "Financier"],
            "Montant": [total_brut_immo, total_brut_fin]
        })
        st.bar_chart(df_plot.set_index("Catégorie"))

    with tab_diag2:
        st.write("Analyse de la couverture décès et invalidité...")
        st.info("Module Prévoyance activé (Indicateurs basés sur les revenus)")

    with tab_diag3:
        st.write(f"Manque à gagner mensuel à la retraite : **{gap_val:,.0f} €**")
        st.warning(f"Capital nécessaire pour compenser : {gap_val * 250:,.0f} €")

    # SECTION FINALE : NOTES ET PDF
    st.markdown("---")
    st.subheader("📝 Édition du Rapport")
    expertise_notes = st.text_area("Note de synthèse pour le client :", height=150)
    
    if st.button("🔨 GÉNÉRER LE BILAN PDF"):
        pdf_data = generate_pdf(nom_client, prenom_client, p_net, r_mens, tx_endett, gap_val, expertise_notes)
        if pdf_data:
            st.download_button("📥 Télécharger le rapport PDF", data=pdf_data, file_name=f"Bilan_{nom_client}.pdf", mime="application/pdf")
        else:
            st.error("Erreur lors de la génération du PDF.")

# --- BOUTON ENVOI (SI PAS EXPERT) ---
if not st.session_state['is_expert']:
    st.markdown("---")
    st.button("🚀 TRANSMETTRE MON ÉTUDE")
