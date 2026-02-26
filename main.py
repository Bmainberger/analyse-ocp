import streamlit as st
try:
    import plotly.express as px
except ImportError:
    st.error("Veuillez créer le fichier requirements.txt avec 'plotly' à l'intérieur.")

from datetime import date

# Configuration
st.set_page_config(page_title="OCP Patrimoine - Expert", layout="wide")
st.title("🛡️ OCP Patrimoine - Bilan 360°")

# --- SECTIONS 1 & 2 ---
st.header("1 & 2. État Civil & Profession")
c1, c2 = st.columns(2)
with c1:
    nom = st.text_input("Nom & Prénom du Client")
    statut_pro = st.selectbox("Statut Professionnel", ["Salarié", "TNS / Libéral", "Dirigeant", "Retraité"])
with c2:
    situation = st.selectbox("Situation Familiale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)"])
    revenus = st.number_input("Revenus Annuels Nets (€)", min_value=0, step=1000)

st.markdown("---")

# --- SECTIONS 3 & 4 : IMMOBILIER ---
st.header("3 & 4. Patrimoine Immobilier")
t1, t2 = st.tabs(["🏠 Physique (Pinel, LMNP...)", "🏢 Pierre-Papier (SCPI...)"])
total_immo = 0.0

with t1:
    nb_i = st.number_input("Nombre de biens immobiliers", min_value=0, step=1)
    for i in range(nb_i):
        with st.expander(f"Bien n°{i+1}", expanded=True):
            ci1, ci2 = st.columns(2)
            with ci1:
                st.selectbox(f"Type {i}", ["Résidence Principale", "Appartement", "Maison", "Terrain", "Parking"], key=f"ti_{i}")
                v = st.number_input(f"Valeur vénale (€) {i}", key=f"vi_{i}")
                total_immo += v
            with ci2:
                st.selectbox(f"Dispositif fiscal {i}", ["Nu (Classique)", "LMNP", "Pinel", "Malraux", "Monument Historique"], key=f"fi_{i}")

with t2:
    nb_scpi = st.number_input("Nombre de placements SCPI/SCI", min_value=0, step=1)
    for j in range(nb_scpi):
        with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
            cs1, cs2 = st.columns(2)
            with cs1:
                p_part = st.number_input(f"Prix de part (€) {j}", key=f"pp_{j}")
                n_part = st.number_input(f"Nombre de parts {j}", key=f"np_{j}")
            with cs2:
                val_calc = p_part * n_part
                st.number_input(f"Valeur totale (€) {j}", value=val_calc, key=f"vt_{j}")
                total_immo += val_calc

st.markdown("---")

# --- SECTION 5 : FINANCIER & RETRAITE ---
st.header("5. Patrimoine Financier & Retraite")
nb_f = st.number_input("Nombre de comptes / contrats", min_value=0, step=1)
total_fin = 0.0
for k in range(nb_f):
    with st.expander(f"Contrat n°{k+1}", expanded=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            typ_f = st.selectbox(f"Type {k}", ["Livret A / LDD", "Assurance-Vie", "PER", "PERCO / PEE", "Article 83", "Madelin", "PEA"], key=f"tf_{k}")
        with f2:
            solde = st.number_input(f"Solde (€) {k}", key=f"sf_{k}")
            total_fin += solde
        with f3:
            if typ_f in ["Assurance-Vie", "PER", "Madelin"]:
                st.selectbox(f"Gestion {k}", ["Mono-support", "Multi-support"], key=f"gu_{k}")

st.markdown("---")

# --- SECTION 6 : PRÉVOYANCE EXPERTE ---
st.header("6. Prévoyance & Protection")
nb_p = st.number_input("Nombre de contrats de prévoyance", min_value=0, step=1)
for p in range(nb_p):
    with st.expander(f"Contrat de Prévoyance n°{p+1}", expanded=True):
        cp1, cp2 = st.columns(2)
        with cp1:
            cat_p = st.selectbox(f"Type {p}", ["Garantie Décès", "IJ / Arrêt de travail", "Assurance Emprunteur", "Invalidité", "GAV / Dépendance"], key=f"cp_{p}")
        with cp2:
            st.number_input(f"Montant Garanti (€) {p}", key=f"mg_{p}")
        
        if cat_p == "Assurance Emprunteur":
            st.write("**Détails Garanties :**")
            g1, g2, g3 = st.columns(3)
            with g1: st.checkbox(f"Décès / PTIA {p}", value=True)
            with g2: st.checkbox(f"IPT / IPP {p}")
            with g3: st.checkbox(f"ITT / Perte emploi {p}")
        elif cat_p == "Garantie Décès":
            st.write("**Options de Rente :**")
            gr1, gr2 = st.columns(2)
            with gr1: st.checkbox(f"Rente Éducation {p}")
            with gr2: st.checkbox(f"Rente Conjoint {p}")

st.markdown("---")

# --- SYNTHÈSE FINALE ---
st.header("9. Synthèse du Patrimoine Brut")
pat_brut = total_immo + total_fin

if pat_brut > 0:
    col_res, col_chart = st.columns([1, 1])
    with col_res:
        st.metric("TOTAL IMMOBILIER", f"{total_immo:,.0f} €")
        st.metric("TOTAL FINANCIER", f"{total_fin:,.0f} €")
        st.subheader(f"Patrimoine Brut : {pat_brut:,.0f} €")
    
    with col_chart:
        try:
            fig = px.pie(names=["Immobilier", "Financier"], values=[total_immo, total_fin], hole=0.4)
            st.plotly_chart(fig)
        except:
            st.info("Graphique en cours de chargement...")
else:
    st.info("Veuillez saisir des actifs pour générer la synthèse.")
