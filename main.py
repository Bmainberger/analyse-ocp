import streamlit as st
from datetime import date
from fpdf import FPDF

# --- FONCTION GÉNÉRATION PDF (RESERVÉE À L'EXPERT) ---
def generate_pdf(nom, prenom, p_net, p_brut, endettement, gap, notes):
    pdf = FPDF()
    pdf.add_page()
    # En-tête
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(29, 46, 77) # Bleu Marine OCP
    pdf.cell(0, 10, 'BILAN PATRIMONIAL STRATEGIQUE - OCP', 0, 1, 'C')
    pdf.ln(10)
    
    # Infos Client
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Client : {prenom} {nom}", 0, 1)
    pdf.cell(0, 10, f"Date du bilan : {date.today().strftime('%d/%m/%Y')}", 0, 1)
    pdf.ln(5)
    
    # Tableau des indicateurs
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(90, 10, 'Indicateur Cle', 1, 0, 'C')
    pdf.cell(90, 10, 'Valeur calculee', 1, 1, 'C')
    pdf.set_font('Arial', '', 11)
    pdf.cell(90, 10, 'Patrimoine Net', 1, 0)
    pdf.cell(90, 10, f"{p_net:,.0f} EUR", 1, 1)
    pdf.cell(90, 10, 'Taux d\'endettement', 1, 0)
    pdf.cell(90, 10, f"{endettement:.1f} %", 1, 1)
    pdf.cell(90, 10, 'Gap Retraite estime', 1, 0)
    pdf.cell(90, 10, f"{gap:,.0f} EUR / mois", 1, 1)
    pdf.ln(10)
    
    # Analyse Expert
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Synthese et Preconisations de l\'Expert :', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 10, notes if notes else "Analyse detaillee en attente de presentation.")
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="OCP Patrimoine - Bilan", page_icon="🛡️", layout="wide")

# Initialisation des compteurs financiers
t_immo = t_fin = t_passif = t_dispo = t_pro = 0.0

# --- BARRE LATÉRALE (ACCÈS EXPERT) ---
if 'is_expert' not in st.session_state: 
    st.session_state['is_expert'] = False

with st.sidebar:
    st.title("🔐 Espace Conseiller")
    code = st.text_input("Code Expert", type="password")
    if code == "ADMINOCP":
        st.session_state['is_expert'] = True
        st.success("Mode Expert Activé")
    elif code != "":
        st.error("Code refusé")

st.title("Votre Étude Patrimoniale Personnalisée")
st.write("Complétez les 11 modules ci-dessous pour une analyse complète.")

# --- LES 11 MODULES ---

# 1. État Civil
st.header("1. État Civil")
col1, col2 = st.columns(2)
with col1:
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
with col2:
    rev_annuel = st.number_input("Revenu net annuel global (€)", min_value=0.0)
    tmi = st.selectbox("Votre TMI actuelle", ["0%", "11%", "30%", "41%", "45%"])

# 2. Composition du Foyer
st.header("2. Composition du Foyer")
c_f1, c_f2 = st.columns(2)
c_f1.selectbox("Situation familiale", ["Célibataire", "Marié(e)", "PACSÉ(e)", "Union Libre", "Divorcé(e)"])
c_f2.number_input("Nombre d'enfants à charge", min_value=0, step=1)

# 3. Vos Objectifs
st.header("3. Vos Objectifs Prioritaires")
st.multiselect("Sélectionnez vos priorités", 
               ["Préparer la retraite", "Protéger ma famille", "Transmettre mon patrimoine", "Réduire mes impôts", "Générer des revenus", "Financer un projet immobilier"])

# 4 & 5. Immobilier (Résidences & Locatif)
st.header("4 & 5. Patrimoine Immobilier")
nb_immo = st.number_input("Combien de biens possédez-vous ?", min_value=0, step=1)
for i in range(int(nb_immo)):
    val = st.number_input(f"Valeur estimée du Bien {i+1} (€)", min_value=0.0, key=f"immo_{i}")
    t_immo += val

# 6. Actifs Financiers
st.header("6. Actifs Financiers (Placements)")
nb_fin = st.number_input("Combien de comptes ou contrats (AV, PEA, etc.) ?", min_value=0, step=1)
for i in range(int(nb_fin)):
    val_f = st.number_input(f"Valeur du placement {i+1} (€)", min_value=0.0, key=f"fin_{i}")
    t_fin += val_f

# 7. Épargne de Précaution
st.header("7. Épargne disponible (Livrets)")
t_dispo = st.number_input("Montant total de vos livrets (A, LDD, etc.) (€)", min_value=0.0)

# 8. Actifs Professionnels
st.header("8. Actifs Professionnels")
t_pro = st.number_input("Valeur estimée de votre outil pro / parts sociales (€)", min_value=0.0)

# 9. Passif (Dettes)
st.header("9. Vos Dettes (Crédits)")
nb_d = st.number_input("Nombre de crédits en cours ?", min_value=0, step=1)
for i in range(int(nb_d)):
    dette = st.number_input(f"Capital restant dû crédit {i+1} (€)", min_value=0.0, key=f"dette_{i}")
    t_passif += dette

# 10. Prévoyance
st.header("10. Prévoyance")
st.radio("Couverture prévoyance actuelle", ["Aucune", "Partielle", "Optimale"])
st.checkbox("Avez-vous une assurance décès ?")

# 11. Transmission
st.header("11. Transmission")
st.checkbox("Avez-vous déjà effectué des donations ?")
st.text_area("Dispositions particulières (testament, clause bénéficiaire...)")

# --- SECTION RÉSERVÉE À L'EXPERT (VISIBLE APRÈS CODE ADMINOCP) ---
if st.session_state['is_expert']:
    st.markdown("---")
    st.header("📊 CONSOLE D'ANALYSE EXPERT OCP")
    
    # Calculs automatiques
    p_brut = t_immo + t_fin + t_dispo + t_pro
    p_net = p_brut - t_passif
    endettement = (t_passif / p_brut * 100) if p_brut > 0 else 0
    gap_retraite = (rev_annuel / 12) * 0.45

    col_res1, col_res2, col
