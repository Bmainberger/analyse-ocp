import streamlit as st
from datetime import date

# Définition des familles d'actifs d'après ta liste
familles_actifs = {
    "Liquidités & Disponibilités": ["Compte Courant", "Livret A", "LDDS", "LEP", "Compte à terme", "Trésorerie d'entreprise"],
    "Épargne Logement": ["PEL", "CEL"],
    "Enveloppes de Capitalisation": ["Assurance-Vie", "Contrat de Capitalisation", "PEA", "PEA-PME", "Compte-Titres"],
    "Épargne Retraite": ["PER Individuel", "PER Collectif", "PER Assurance", "PER Bancaire"],
    "Actifs Numériques": ["Crypto-actifs (Bitcoin, ETH...)", "Stablecoins"]
}

nb_fin = st.number_input("Nombre de comptes ou contrats financiers", min_value=0, step=1)
total_fin = 0.0

for k in range(int(nb_fin)):
    with st.expander(f"Contrat n°{k+1}", expanded=True):
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            # Choix de la famille selon tes instructions
            famille_choisie = st.selectbox("Famille d'actif", list(familles_actifs.keys()), key=f"fam_f_{k}")
            # Établissement & Date (indispensable pour l'audit)
            etablissement = st.text_input("Établissement (Banque/Assureur)", key=f"etab_f_{k}")
            date_ouv = st.date_input("Date d'ouverture", value=date(2020, 1, 1), key=f"date_f_{k}")

        with col_f2:
            # Type précis filtré par famille
            type_precis = st.selectbox("Type de contrat", familles_actifs[famille_choisie], key=f"type_f_{k}")
            # Valeur actuelle
            solde = st.number_input("Solde / Valeur actuelle (€)", min_value=0.0, key=f"solde_f_{k}")
            total_fin += solde

        with col_f3:
            # Mode de gestion
            st.selectbox("Mode de gestion", ["Gestion Libre", "Gestion Pilotée", "Gestion Sous Mandat"], key=f"gest_f_{k}")
            
            # Affichage dynamique des détails (Fonds Euro vs UC)
            if famille_choisie in ["Enveloppes de Capitalisation", "Épargne Retraite"]:
                if any(x in type_precis for x in ["Assurance-Vie", "PER", "Capitalisation"]):
                    repart_euro = st.slider("Répartition Fonds Euro (%)", 0, 100, 50, key=f"euro_f_{k}")
                    st.caption(f"Unités de Compte : {100 - repart_euro}%")
                else:
                    st.selectbox("Profil de risque", ["Prudent", "Équilibré", "Dynamique"], key=f"risk_f_{k}")

if total_fin > 0:
    st.metric("Total Épargne Financière", f"{total_fin:,.0f} €".replace(",", " "))
