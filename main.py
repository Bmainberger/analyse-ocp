import os
# Cette ligne installe l'outil de graphique automatiquement au lancement
os.system('pip install plotly')

import streamlit as st
import plotly.express as px

# Configuration
st.set_page_config(page_title="OCP Patrimoine - Expert", layout="wide")
st.title("🛡️ OCP Patrimoine - Bilan 360°")

# --- CLIENT ---
st.header("1 & 2. État Civil & Profession")
c1, c2 = st.columns(2)
with c1:
    nom = st.text_input("Nom & Prénom du Client")
    statut = st.selectbox("Statut Pro", ["Salarié", "TNS", "Dirigeant", "Retraité"])
with c2:
    sit = st.selectbox("Situation", ["Marié(e)", "Pacsé(e)", "Célibataire"])
    rev = st.number_input("Revenu Annuel Net (€)", min_value=0)

st.markdown("---")

# --- IMMOBILIER ---
st.header("3 & 4. Patrimoine Immobilier")
nb_i = st.number_input("Nombre de biens immobiliers", min_value=0, step=1)
total_immo = 0.0
for i in range(nb_i):
    val = st.number_input(f"Valeur vénale du bien n°{i+1} (€)", key=f"v_{i}")
    total_immo += val

st.markdown("---")

# --- FINANCIER & RETRAITE ---
st.header("5. Patrimoine Financier & Retraite")
st.info("Inclut : Assurance-Vie, PER, Madelin, PERCO, Article 83, Livrets")
nb_f = st.number_input("Nombre de comptes / contrats", min_value=0, step=1)
total_fin = 0.0
for k in range(nb_f):
    colf1, colf2 = st.columns(2)
    with colf1:
        typ = st.selectbox(f"Type contrat {k}", ["Assurance-Vie", "PER", "Madelin", "PEA", "Livret A", "PERCO", "Art. 83"], key=f"t_{k}")
    with colf2:
        solde = st.number_input(f"Solde du contrat {k} (€)", key=f"s_{k}")
        total_fin += solde

st.markdown("---")

# --- PRÉVOYANCE ---
st.header("6. Prévoyance & Emprunteur")
st.write("**Garanties professionnelles et personnelles**")
st.checkbox("Assurance Emprunteur (Décès, PTIA, IPT, ITT, Perte emploi)")
st.checkbox("Prévoyance (Rente Éducation, Rente Conjoint, IJ)")

st.markdown("---")

# --- SYNTHÈSE GLOBALE ---
st.header("9. Synthèse du Patrimoine Brut")
total_global = total_immo + total_fin
if total_global > 0:
    col_r, col_g = st.columns([1, 1])
    with col_r:
        st.metric("TOTAL IMMOBILIER", f"{total_immo:,.0f} €")
        st.metric("TOTAL FINANCIER", f"{total_fin:,.0f} €")
        st.subheader(f"Patrimoine Global : {total_global:,.0f} €")
    with col_g:
        # Création du graphique camembert
        fig = px.pie(names=["Immobilier", "Financier"], values=[total_immo, total_fin], hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Saisissez des montants pour générer le graphique de synthèse.")
