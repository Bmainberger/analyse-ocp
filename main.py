import streamlit as st
import plotly.express as px
from datetime import date

# Configuration
st.set_page_config(page_title="OCP Patrimoine - Expert", layout="wide")
st.title("🛡️ OCP Patrimoine - Bilan 360°")

# --- SECTION 1 & 2 : CLIENT ---
st.header("1 & 2. État Civil & Profession")
c1, c2 = st.columns(2)
with c1:
    nom = st.text_input("Nom & Prénom")
    statut_pro = st.selectbox("Statut Pro", ["Salarié", "TNS (Madelin)", "Dirigeant", "Retraité"])
with c2:
    situation = st.selectbox("Situation", ["Célibataire", "Marié(e)", "Pacsé(e)"])
    revenus = st.number_input("Revenu Annuel Net (€)", min_value=0)

st.markdown("---")

# --- SECTIONS 3 & 4 : IMMOBILIER ---
st.header("3 & 4. Patrimoine Immobilier")
t_immo1, t_immo2 = st.tabs(["🏠 Physique (Pinel, LMNP...)", "🏢 Pierre-Papier (SCPI...)"])
total_immo = 0.0

with t_immo1:
    nb_i = st.number_input("Nombre de biens physiques", min_value=0)
    for i in range(nb_i):
        with st.expander(f"Bien n°{i+1}"):
            col_i1, col_i2 = st.columns(2)
            with col_i1:
                st.selectbox(f"Type", ["Résidence Principale", "Appartement", "Maison", "Terrain", "Parking"], key=f"ti_{i}")
                val = st.number_input(f"Valeur (€)", key=f"vi_{i}")
                total_immo += val
            with col_i2:
                st.selectbox(f"Régime", ["Nu", "LMNP", "Pinel", "Malraux", "MH"], key=f"ri_{i}")

with t_immo2:
    nb_c = st.number_input("Nombre de SCPI/SCI", min_value=0)
    for j in range(nb_c):
        with st.expander(f"Placement n°{j+1}"):
            p_part = st.number_input("Prix de part", key=f"pp_{j}")
            n_part = st.number_input("Nb de parts", key=f"np_{j}")
            v_retrait = p_part * n_part
            st.write(f"Valeur calculée : **{v_retrait:,.0f} €**")
            total_immo += v_retrait

st.markdown("---")

# --- SECTION 5 : FINANCIER & RETRAITE ---
st.header("5. Patrimoine Financier & Retraite")
nb_f = st.number_input("Nombre de comptes/contrats", min_value=0)
total_fin = 0.0
for k in range(nb_f):
    with st.expander(f"Contrat n°{k+1}"):
        f1, f2, f3 = st.columns(3)
        with f1:
            typ = st.selectbox("Type", ["Livret A", "LDD/PEL", "Assurance-Vie", "PER", "PERCO / PEE", "Article 83", "Madelin"], key=f"tf_{k}")
        with f2:
            solde = st.number_input("Solde (€)", key=f"sf_{k}")
            total_fin += solde
        with f3:
            if "Assurance-Vie" in typ or "PER" in typ or "Madelin" in typ:
                st.selectbox("Support", ["Mono-support", "Multi-support"], key=f"su_{k}")

st.markdown("---")

# --- SECTION 6 : PRÉVOYANCE EXPERTE ---
st.header("6. Prévoyance & Assurance Emprunteur")
nb_p = st.number_input("Nombre de contrats Prévoyance", min_value=0)
for p in range(nb_p):
    with st.expander(f"Contrat n°{p+1}"):
        cat = st.selectbox("Type de risque", ["Décès", "IJ / Arrêt de travail", "Invalidité", "Assurance Emprunteur", "Dépendance / GAV"], key=f"cp_{p}")
        if cat == "Assurance Emprunteur":
            st.number_input("Quotité (%)", value=100, key=f"q_{p}")
            st.multiselect("Garanties incluses", ["Décès", "PTIA", "IPT", "IPP", "ITT", "Perte d'emploi"], default=["Décès", "PTIA"], key=f"g_{p}")
        else:
            st.number_input("Capital/Rente garanti (€)", key=f"cap_{p}")
            st.multiselect("Détails Rentes", ["Rente Éducation", "Rente Conjoint"], key=f"re_{p}")

st.markdown("---")

# --- SECTION 8 & 9 : SYNTHÈSE & GRAPHIQUE ---
st.header("9. Synthèse du Patrimoine Brut")
if (total_immo + total_fin) > 0:
    data = {"Catégorie": ["Immobilier", "Financier"], "Valeur": [total_immo, total_fin]}
    fig = px.pie(data, values='Valeur', names='Catégorie', hole=0.4, color_discrete_sequence=['#1f77b4', '#ff7f0e'])
    
    col_g1, col_g2 = st.columns([1, 2])
    with col_g1:
        st.metric("TOTAL IMMOBILIER", f"{total_immo:,.0f} €")
        st.metric("TOTAL FINANCIER", f"{total_fin:,.0f} €")
        st.metric("PATRIMOINE GLOBAL", f"{(total_immo + total_fin):,.0f} €", delta_color="normal")
    with col_g2:
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Saisissez des actifs pour voir la synthèse.")
