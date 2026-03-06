import streamlit as st
from datetime import date
import pandas as pd
from fpdf import FPDF
import base64

# --- FONCTION GÉNÉRATION PDF ---
def generate_pdf(nom, prenom, p_net, p_brut, endettement, gap_retraite, notes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(29, 46, 77) # Bleu Marine OCP
    pdf.cell(0, 10, 'BILAN PATRIMONIAL STRATEGIQUE - OCP', 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Client : {prenom} {nom}", 0, 1)
    pdf.cell(0, 10, f"Date : {date.today().strftime('%d/%m/%Y')}", 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(90, 10, 'Indicateur', 1, 0, 'C')
    pdf.cell(90, 10, 'Valeur', 1, 1, 'C')
    pdf.set_font('Arial', '', 11)
    pdf.cell(90, 10, 'Patrimoine Net', 1, 0)
    pdf.cell(90, 10, f"{p_net:,.0f} EUR", 1, 1)
    pdf.cell(90, 10, 'Taux Endettement', 1, 0)
    pdf.cell(90, 10, f"{endettement:.1f} %", 1, 1)
    pdf.ln(10)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Synthese Expert :', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 10, notes if notes else "Aucune note specifiee.")
    
    # Encodage sécurisé pour le téléchargement
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- CONFIGURATION STREAMLIT ---
st.set_page_config(page_title="OCP Patrimoine", page_icon="🛡️", layout="wide")

# Style du bouton principal
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #1d2e4d; color: white; font-size: 20px; font-weight: bold; width: 100%; border-radius: 5px; height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialisation des variables de calcul
total_brut_immo = total_brut_fin = total_passif = 0.0

# --- GESTION DU MODE EXPERT ---
if 'is_expert' not in st.session_state: 
    st.session_state['is_expert'] = False

with st.sidebar:
    st.title("🔐 Espace Expert")
    code_entre = st.text_input("Code d'accès", type="password")
    if code_entre == "ADMINOCP":
        st.session_state['is_expert'] = True
        st.success("Mode Expert Activé")
    elif code_entre != "":
        st.error("Code incorrect")

st.title("Votre stratégie patrimoniale commence ici.")
st.markdown("---")

# --- FORMULAIRE CLIENT ---
st.header("1. État Civil")
c1, c2 = st.columns(2)
with c1:
    nom_client = st.text_input("Nom du client", key="nom_c")
    prenom_client = st.text_input("Prénom du client", key="pre_c")
with c2:
    rev_annuel = st.number_input("Revenu net annuel (EUR)", min_value=0.0, key="rev_a")
    tmi_c = st.selectbox("TMI fiscale", ["0%", "11%", "30%", "41%", "45%"])

st.header("4 & 5. Immobilier")
nb_immo = st.number_input("Nombre de biens immobiliers", min_value=0, step=1)
for i in range(int(nb_immo)):
    val = st.number_input(f"Valeur estimée du Bien {i+1}", min_value=0.0, key=f"im_{i}")
    total_brut_immo += val

st.header("6. Actifs Financiers")
nb_fin = st.number_input("Nombre de comptes/placements", min_value=0, step=1)
for i in range(int(nb_fin)):
    val_f = st.number_input(f"Solde du placement {i+1}", min_value=0.0, key=f"fin_{i}")
    total_brut_fin += val_f

st.header("9. Passif (Dettes)")
nb_dettes = st.number_input("Nombre de crédits en cours", min_value=0, step=1)
for i in range(int(nb_dettes)):
    dette = st.number_input(f"Capital restant dû crédit {i+1}", min_value=0.0, key=f"det_{i}")
    total_passif += dette

# --- AFFICHAGE RÉSERVÉ À L'EXPERT ---
if st.session_state['is_expert']:
    st.markdown("---")
    st.header("📊 CONSOLE D'ANALYSE EXPERT OCP")
    
    p_brut = total_brut_immo + total_brut_fin
    p_net = p_brut - total_passif
    tx_endettement = (total_passif / p_brut * 100) if p_brut > 0 else 0
    gap = (rev_annuel / 12) * 0.45 # Estimation simplifiée du gap retraite

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Patrimoine Net", f"{p_net:,.0f} €")
    col_m2.metric("Taux d'endettement", f"{tx_endettement:.1f} %")
    col_m3.metric("Gap Retraite estimé", f"{gap:,.0f} € / mois")

    final_expert_notes = st.text_area("Observations et préconisations de l'expert :", height=150)

    # Bouton de génération PDF
    if st.button("🔨 GÉNÉRER LE RAPPORT PDF PROFESSIONNEL"):
        try:
            pdf_bytes = generate_pdf(nom_client, prenom_client, p_net, p_brut, tx_endettement, gap, final_expert_notes)
            st.download_button(
                label="📥 Télécharger le Bilan (PDF)",
                data=pdf_bytes,
                file_name=f"Bilan_Patrimonial_{nom_client}.pdf",
                mime="application/pdf"
            )
            st.success("Le rapport a été généré avec succès !")
        except Exception as e:
            st.error(f"Erreur lors de la génération : {e}")

# --- PIED DE PAGE (Public) ---
if not st.session_state['is_expert']:
    st.markdown("---")
    st.write("Veuillez remplir les informations ci-dessus, puis cliquez sur le bouton pour transmettre votre étude.")
    st.markdown(f'<form action="https://formsubmit.co/bmainberger@ocp-patrimoine.com" method="POST"><button type="submit" style="background-color: #1d2e4d; color: white; padding: 15px; width: 100%; border-radius: 5px; border: none; font-weight: bold; cursor: pointer;">🚀 TRANSMETTRE MON ÉTUDE À MON CONSEILLER</button></form>', unsafe_allow_html=True)
