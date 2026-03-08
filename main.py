import streamlit as st
from datetime import date
from fpdf import FPDF 

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="OCP Patrimoine", page_icon="🛡️", layout="wide")

# INITIALISATION DE TOUTES LES VARIABLES (MÉMOIRE)
keys = ['nom_c', 'pre_c', 'rev_a', 'sit_mat', 'nb_e', 'statut_pro', 'immo_brut', 'fin_brut', 'passif_t', 'com_client', 'is_expert']
for key in keys:
    if key not in st.session_state:
        st.session_state[key] = "" if "c" in key or "mat" in key or "pro" in key else 0.0

# --- RÉCUPÉRATION DES DONNÉES DEPUIS LE LIEN (URL) ---
query_params = st.query_params
if "nom" in query_params: st.session_state['nom_c'] = query_params["nom"]
if "prenom" in query_params: st.session_state['pre_c'] = query_params["prenom"]
if "rev" in query_params: st.session_state['rev_a'] = float(query_params["rev"])
if "sit" in query_params: st.session_state['sit_mat'] = query_params["sit"]
if "enf" in query_params: st.session_state['nb_e'] = int(query_params["enf"])
if "pro" in query_params: st.session_state['statut_pro'] = query_params["pro"]
if "immo" in query_params: st.session_state['immo_brut'] = float(query_params["immo"])
if "fin" in query_params: st.session_state['fin_brut'] = float(query_params["fin"])
if "det" in query_params: st.session_state['passif_t'] = float(query_params["det"])
if "txt" in query_params: st.session_state['com_client'] = query_params["txt"]

# --- 2. ACCÈS EXPERT ---
with st.sidebar:
    st.title("🔐 Espace Expert")
    code_admin = st.text_input("Code confidentiel", type="password")
    st.session_state['is_expert'] = (code_admin == "ADMINOCP")
    if st.session_state['is_expert']: st.success("Mode Expert Activé")

# --- 3. FORMULAIRE PRINCIPAL ---
st.title("Bilan Patrimonial OCP")

# SECTION 1 : ÉTAT CIVIL
st.header("1. État Civil & Famille")
col1, col2 = st.columns(2)
with col1:
    st.text_input("Nom", key="nom_c")
    st.text_input("Prénom", key="pre_c")
with col2:
    st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"], key="sit_mat")
    st.number_input("Nombre d'enfants", min_value=0, step=1, key="nb_e")

# SECTION 2 : FINANCES (Affichage direct pour l'expert)
st.header("2. Situation Financière")
f1, f2, f3 = st.columns(3)
with f1:
    st.selectbox("Statut Pro", ["Salarié", "TNS", "Dirigeant", "Retraité"], key="statut_pro")
    st.number_input("Revenu Annuel (€)", key="rev_a")
with f2:
    # Valeur par défaut injectée depuis l'URL pour l'expert
    val_immo = st.number_input("Patrimoine Immobilier (€)", value=float(st.session_state.get('immo_brut', 0)))
    val_fin = st.number_input("Patrimoine Financier (€)", value=float(st.session_state.get('fin_brut', 0)))
with f3:
    val_det = st.number_input("Dettes / Crédits (€)", value=float(st.session_state.get('passif_t', 0)))

st.header("3. Projets & Commentaires")
st.text_area("Notes du client", key="com_client", height=150)

# --- 4. CALCULS ET PDF ---
pat_brut = val_immo + val_fin
pat_net = pat_brut - val_det

if st.session_state['is_expert']:
    st.markdown("---")
    st.subheader("📊 Synthèse Expert")
    st.metric("PATRIMOINE NET", f"{pat_net:,.0f} €")
    note_expert = st.text_area("Votre analyse stratégique", key="syn_expert")

    if st.button("📄 GÉNÉRER LE BILAN PDF PROFESSIONNEL"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, f"BILAN PATRIMONIAL : {st.session_state.pre_c} {st.session_state.nom_c}", ln=True, align='C')
        
        pdf.set_font("Arial", '', 12)
        pdf.ln(10)
        pdf.cell(200, 10, f"Situation : {st.session_state.sit_mat} | {st.session_state.nb_e} enfant(s)", ln=True)
        pdf.cell(200, 10, f"Statut Pro : {st.session_state.statut_pro} | Revenus : {st.session_state.rev_a:,.0f} EUR/an", ln=True)
        pdf.ln(5)
        pdf.cell(200, 10, f"Patrimoine Immobilier : {val_immo:,.0f} EUR", ln=True)
        pdf.cell(200, 10, f"Patrimoine Financier : {val_fin:,.0f} EUR", ln=True)
        pdf.cell(200, 10, f"Dettes totales : {val_det:,.0f} EUR", ln=True)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, f"PATRIMOINE NET : {pat_net:,.0f} EUR", ln=True)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, "Commentaires Client :", ln=True)
        pdf.set_font("Arial", 'I', 11)
        pdf.multi_cell(0, 10, st.session_state.com_client)
        
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, "Analyse OCP :", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 10, note_expert if note_expert else "Bilan en cours d'analyse.")
        
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button("📥 Télécharger le Bilan PDF", data=pdf_output, file_name=f"Bilan_{st.session_state.nom_c}.pdf")

# --- 5. ENVOI FINAL (POUR LE CLIENT) ---
if not st.session_state['is_expert']:
    st.markdown("---")
    # CONSTRUCTION DU LIEN COMPLET (Encode les espaces et textes)
    base_url = "https://analyse-ocp-hzixep8mm6jdekmfu5ur2h.streamlit.app/?"
    params = (
        f"nom={st.session_state.nom_c}&prenom={st.session_state.pre_c}&rev={st.session_state.rev_a}"
        f"&sit={st.session_state.sit_mat}&enf={st.session_state.nb_e}&pro={st.session_state.statut_pro}"
        f"&immo={val_immo}&fin={val_fin}&det={val_det}"
        f"&txt={st.session_state.com_client.replace(' ', '%20')}"
    )
    lien_total = base_url + params
    
    corps_mail = f"NOUVEAU DOSSIER : {st.session_state.nom_c}\nLien direct : {lien_total}"
    
    bouton_html = f"""<form action="https://formsubmit.co/bmainberger@ocp-patrimoine.com" method="POST">
            <input type="hidden" name="DOSSIER" value="{corps_mail}">
            <button type="submit" style="background-color: #1d2e4d; color: white; padding: 20px; width: 100%; border-radius: 8px; cursor: pointer; font-weight: bold; border:none;">🚀 TRANSMETTRE MON ÉTUDE</button>
        </form>"""
    st.markdown(bouton_html, unsafe_allow_html=True)
