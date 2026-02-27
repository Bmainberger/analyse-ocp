import streamlit as st
from datetime import date

# Configuration de la page
st.set_page_config(page_title="OCP Patrimoine - Analyse", page_icon="🛡️", layout="wide")

st.title("🛡️ OCP Patrimoine - Bilan et Analyse")
st.markdown("---")

# --- SECTION 1 : ÉTAT CIVIL & FAMILLE ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)
with col1:
    st.text_input("Nom du Client", key="nom_client")
    st.text_input("Prénom du Client", key="prenom_client")
    st.date_input("Date de naissance", value=date(1980, 1, 1), key="dnaiss_client")
    st.text_input("Lieu de naissance", key="lieu_naissance")
with col2:
    st.text_input("Nationalité", key="nationalite") 
    st.selectbox("Situation Matrimoniale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"], key="situation")
    nb_enfants = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1, key="nb_enfants")

if nb_enfants > 0:
    st.write("📅 **Détail des enfants :**")
    c_enf = st.columns(3)
    for i in range(int(nb_enfants)):
        with c_enf[i % 3]:
            st.date_input(f"Date de naissance Enfant n°{i+1}", value=date(2010, 1, 1), key=f"dnaiss_enf_{i}")

st.markdown("---")

# --- SECTION 2 : COORDONNÉES ---
st.header("2. Coordonnées")
c_coo1, c_coo2, c_coo3 = st.columns([2, 1, 1])
with c_coo1:
    st.text_input("Adresse postale complète", key="adresse")
with c_coo2:
    st.text_input("Téléphone", key="telephone")
with c_coo3:
    st.text_input("Email", key="email")

st.markdown("---")

# --- SECTION 3 : PROFESSION & REVENUS ---
st.header("3. Situation Professionnelle & Revenus")
cp1, cp2, cp3 = st.columns(3)
with cp1:
    st.selectbox("Statut Professionnel", ["Salarié", "TNS / Libéral", "Dirigeant", "Fonctionnaire", "Retraité", "Sans activité"], key="statut_pro")
    st.text_input("Profession / Intitulé du poste", key="profession")
with cp2:
    st.number_input("Revenu net annuel (€)", min_value=0, key="revenu_annuel")
    st.number_input("Autres revenus (€)", min_value=0, key="autres_revenus")
with cp3:
    st.selectbox("Tranche Marginale d'Imposition (TMI)", ["0%", "11%", "30%", "41%", "45%"], key="tranche_impo")
    st.number_input("Âge de retraite prévu", min_value=50, max_value=80, value=64, key="age_retraite")

st.markdown("---")

# --- SECTION 4 & 5 : PATRIMOINE IMMOBILIER ---
st.header("4 & 5. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier (SCPI, SCI, GFV...)"])

with tab1:
    nb_biens = st.number_input("Nombre de biens immobiliers physiques", min_value=0, key="nb_biens")
    for i in range(int(nb_biens)):
        with st.expander(f"Bien n°{i+1}", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox(f"Type de bien {i+1}", ["Résidence Principale", "Résidence Secondaire", "Appartement", "Maison", "Terrain", "Parking / Garage", "Immeuble de rapport"], key=f"type_i_{i}")
                st.number_input(f"Valeur vénale (€) {i+1}", min_value=0, key=f"val_i_{i}")
            with c2:
                st.selectbox(f"Régime fiscal {i+1}", ["Droit Commun (Nu)", "LMNP", "LMP", "Pinel", "Malraux", "Monument Historique"], key=f"fisc_i_{i}")
                st.radio(f"Crédit en cours ? {i+1}", ["Non", "Oui"], key=f"cred_i_{i}")

with tab2:
    nb_coll = st.number_input("Nombre de placements collectifs", min_value=0, key="nb_coll")
    for j in range(int(nb_coll)):
        with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
            t_coll = st.selectbox(f"Type de support", ["SCPI", "SCI", "OPCI", "GFV", "GFI", "Club Deal"], key=f"type_c_{j}")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.text_input("Nom du support", key=f"nom_c_{j}")
                st.selectbox("Mode de détention", ["Pleine Propriété", "Nue-Propriété", "Usufruit", "Via Assurance-Vie", "Via PER"], key=f"det_c_{j}")
            with c2:
                val_estim = st.number_input("Valeur estimée (€)", min_value=0, key=f"liq_c_{j}")
                rev_annuel = st.number_input("Revenus annuels nets (€)", min_value=0, key=f"rev_c_{j}")
            with c3:
                if val_estim > 0:
                    st.metric("Rendement estimé", f"{(rev_annuel / val_estim) * 100:.2f} %")
                if t_coll == "SCPI":
                    st.number_input("TOF (%)", min_value=0.0, max_value=100.0, key=f"tof_c_{j}")

st.markdown("---")

# --- SECTION 6 : PATRIMOINE FINANCIER (TES 5 FAMILLES) ---
st.header("6. Patrimoine Financier")

familles_actifs = {
    "Liquidités & Disponibilités": ["Compte Courant", "Livret A", "LDDS", "LEP", "Compte à terme", "Trésorerie d'entreprise"],
    "Épargne Logement": ["PEL", "CEL"],
    "Enveloppes de Capitalisation": ["Assurance-Vie", "Contrat de Capitalisation", "PEA", "PEA-PME", "Compte-Titres"],
    "Épargne Retraite": ["PER Individuel", "PER Collectif", "PER Assurance", "PER Bancaire"],
    "Actifs Numériques": ["Crypto-actifs (Bitcoin, ETH...)", "Stablecoins"]
}

nb_fin = st.number_input("Nombre de comptes ou contrats financiers", min_value=0, step=1, key="nb_fin_total")
total_fin = 0.0

for k in range(int(nb_fin)):
    with st.expander(f"Contrat n°{k+1}", expanded=True):
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            famille_choisie = st.selectbox("Famille d'actif", list(familles_actifs.keys()), key=f"fam_f_{k}")
            st.text_input("Établissement (Banque/Assureur)", key=f"etab_f_{k}")
            st.date_input("Date d'ouverture", value=date(2020, 1, 1), key=f"date_f_{k}")
        with col_f2:
            type_precis = st.selectbox("Type de contrat", familles_actifs[famille_choisie], key=f"type_f_{k}")
            solde = st.number_input("Solde / Valeur actuelle (€)", min_value=0.0, key=f"solde_f_{k}")
            total_fin += solde
        with col_f3:
            st.selectbox("Mode de gestion", ["Gestion Libre", "Gestion Pilotée", "Gestion Sous Mandat"], key=f"gest_f_{k}")
            if famille_choisie in ["Enveloppes de Capitalisation", "Épargne Retraite"]:
                if any(x in type_precis for x in ["Assurance-Vie", "PER", "Capitalisation"]):
                    repart_euro = st.slider("Répartition Fonds Euro (%)", 0, 100, 50, key=f"euro_f_{k}")
                    st.caption(f"Unités de Compte : {100 - repart_euro}%")

if total_fin > 0:
    st.metric("Total Épargne Financière", f"{total_fin:,.0f} €".replace(",", " "))

st.markdown("---")

# --- SECTION 7 & 8 : PRÉVOYANCE & SANTÉ ---
st.header("7 & 8. Prévoyance & Santé")
col_s1, col_s2 = st.columns(2)
with col_s1:
    st.subheader("Prévoyance")
    st.selectbox("Garantie principale", ["Décès", "Rente Éducation", "IJ (Revenu)", "Invalidité", "Emprunteur"], key="prev_g")
    st.number_input("Capital/Montant garanti (€)", min_value=0, key="prev_m")
with col_s2:
    st.subheader("Santé")
    st.text_input("Mutuelle / Assureur", key="sante_assur")
    st.select_slider("Niveau de couverture", options=["100%", "200%", "300%", "400%+"], key="sante_couv")

st.markdown("---")
st.success("Analyse prête et sécurisée !")
