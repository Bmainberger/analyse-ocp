import streamlit as st
from datetime import date

# 1. Configuration de la page
st.set_page_config(page_title="OCP Patrimoine - Bilan Complet", page_icon="🛡️", layout="wide")

st.title("🛡️ OCP Patrimoine - Bilan et Analyse Global")
st.markdown("---")

# --- INITIALISATION DES TOTAUX ---
total_brut_immo = 0.0
total_brut_fin = 0.0
total_passif = 0.0
total_charges_mensuelles = 0.0
revenus_mensuels_totaux = 0.0

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
        nom_conj = st.text_input("Nom du Conjoint", key="nom_conj")
        dnaiss_conj = st.date_input("Date de naissance conjoint", value=date(1980, 1, 1), key="dnaiss_conj")
    with c_col2:
        pre_conj = st.text_input("Prénom du Conjoint", key="pre_conj")
        st.text_input("Nationalité Conjoint", key="nat_conj")

st.markdown("---")

# --- SECTION 3 : REVENUS & BUDGET ---
st.header("3. Revenus, Charges & Capacité d'Épargne")
b1, b2, b3 = st.columns(3)

with b1:
    st.subheader("💰 Revenus Mensuels")
    rev_pro = st.number_input("Salaires / BNC / Dividendes (net)", min_value=0.0, key="rev_pro_m")
    rev_fonc = st.number_input("Revenus Fonciers (net)", min_value=0.0, key="rev_fonc_m")
    revenus_mensuels_totaux = rev_pro + rev_fonc
    st.info(f"Total Revenus : {revenus_mensuels_totaux:,.0f} € / mois")

with b2:
    st.subheader("💸 Charges Mensuelles")
    loyer_mens = st.number_input("Loyer / Charges Copro", min_value=0.0, key="loyer_m")
    impots_mens = st.number_input("Impôts (Mensualisés)", min_value=0.0, key="imp_m")
    vie_courante = st.number_input("Train de vie (Alim, Loisirs...)", min_value=0.0, key="vie_m")
    total_charges_mensuelles = loyer_mens + impots_mens + vie_courante

with b3:
    st.subheader("📊 Capacité d'Épargne")
    capacite_brute = revenus_mensuels_totaux - total_charges_mensuelles
    if capacite_brute > 0:
        st.metric("Reste à vivre", f"{capacite_brute:,.0f} €", delta="Positif")
    else:
        st.metric("Reste à vivre", f"{capacite_brute:,.0f} €", delta="Négatif", delta_color="inverse")
    st.caption("Note : Les mensualités de crédits seront déduites automatiquement dans la synthèse.")

st.markdown("---")

# --- SECTION 4 & 5 : PATRIMOINE IMMOBILIER ---
st.header("4 & 5. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier"])

with tab1:
    nb_biens = st.number_input("Nombre de biens immobiliers", min_value=0, key="nb_p_p")
    for i in range(int(nb_biens)):
        with st.expander(f"Bien n°{i+1}", expanded=True):
            v1, v2 = st.columns(2)
            with v1:
                st.selectbox(f"Type {i}", ["Résidence Principale", "Résidence Secondaire", "Investissement Locatif"], key=f"t_i_{i}")
                val_i = st.number_input(f"Valeur (€) {i}", min_value=0.0, key=f"v_i_{i}")
                total_brut_immo += val_i
            with v2:
                st.selectbox(f"Régime {i}", ["Nu", "LMNP", "Pinel"], key=f"f_i_{i}")

with tab2:
    nb_coll = st.number_input("Nombre de SCPI/SCI", min_value=0, key="nb_p_c")
    for j in range(int(nb_coll)):
        with st.expander(f"Placement Collectif n°{j+1}"):
            px_p = st.number_input(f"Prix part {j}", min_value=0.0, key=f"px_{j}")
            nb_p = st.number_input(f"Nb parts {j}", min_value=0.0, key=f"nb_{j}")
            total_brut_immo += (px_p * nb_p)

st.markdown("---")

# --- SECTION 6 : FINANCIER ---
st.header("6. Patrimoine Financier")
nb_fin = st.number_input("Nombre de contrats", min_value=0, key="nb_f")
for k in range(int(nb_fin)):
    with st.expander(f"Contrat n°{k+1}"):
        f1, f2 = st.columns(2)
        with f1:
            st.selectbox(f"Type {k}", ["Livret", "Assurance-Vie", "PEA", "PER"], key=f"tf_{k}")
            st.text_input(f"Banque {k}", key=f"bf_{k}")
        with f2:
            solde_f = st.number_input(f"Solde (€) {k}", min_value=0.0, key=f"sf_{k}")
            total_brut_fin += solde_f

st.markdown("---")

# --- SECTION 7 & 8 : PROTECTION & SANTÉ ---
st.header("7 & 8. Prévoyance & Santé")
s_org = st.text_input("Assureur Santé", key="s_org")
nb_prev = st.number_input("Nombre de contrats Prévoyance", min_value=0, key="nb_prev")
for p in range(int(nb_prev)):
    st.selectbox(f"Garantie {p}", ["Décès", "IJ", "Emprunteur"], key=f"gt_{p}")

st.markdown("---")

# --- SECTION 9 : PASSIF (CRÉDITS) ---
st.header("9. Passif & Mensualités")
nb_p_immo = st.number_input("Nombre de crédits immo", min_value=0, key="nb_p_i")
mensualites_totales = 0.0
for m in range(int(nb_p_immo)):
    with st.expander(f"Crédit n°{m+1}"):
        m1, m2 = st.columns(2)
        with m1:
            crd_p = st.number_input(f"Restant Dû {m}", min_value=0.0, key=f"crd_{m}")
            total_passif += crd_p
        with m2:
            mens_p = st.number_input(f"Mensualité {m}", min_value=0.0, key=f"mens_{m}")
            mensualites_totales += mens_p

st.markdown("---")

# --- SECTION 11 : OBJECTIFS ---
st.header("🎯 11. Objectifs")
obj_prioritaires = st.multiselect("Priorités", ["Retraite", "Fiscalité", "Transmission", "Revenus"], key="objs")

# --- CALCULS BARRE LATÉRALE ---
pat_brut = total_brut_immo + total_brut_fin
pat_net = pat_brut - total_passif
epargne_mensuelle_reelle = capacite_brute - mensualites_totales

st.sidebar.title("📊 Synthèse")
st.sidebar.metric("PATRIMOINE NET", f"{pat_net:,.0f} €".replace(",", " "))
st.sidebar.metric("CAPACITÉ ÉPARGNE", f"{epargne_mensuelle_reelle:,.0f} €/mois".replace(",", " "))

# --- RÉSUMÉ FINAL ---
if st.button("🚀 GÉNÉRER LE RÉSUMÉ FINAL"):
    st.header("📋 Résumé de l'Audit OCP")
    r1, r2 = st.columns(2)
    with r1:
        st.subheader("👤 Client")
        st.write(f"**Nom :** {nom_client} {prenom_client}")
        st.write(f"**Patrimoine Net :** {pat_net:,.0f} €".replace(",", " "))
    with r2:
        st.subheader("💰 Flux Mensuels")
        st.write(f"**Revenus :** {revenus_mensuels_totaux:,.0f} €")
        st.write(f"**Mensualités crédits :** {mensualites_totales:,.0f} €")
        st.metric("Épargne Mensuelle Réelle", f"{epargne_mensuelle_reelle:,.0f} €")
    
    st.success("Analyse terminée. Vous pouvez maintenant conseiller sur l'allocation de cette épargne !")
