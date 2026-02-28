import streamlit as st
from datetime import date
import json

# 1. Configuration de la page
st.set_page_config(page_title="OCP Patrimoine - Audit Global & Sauvegarde", page_icon="🛡️", layout="wide")

# --- LOGIQUE DE SAUVEGARDE ---
def save_data(data):
    return json.dumps(data, default=str, indent=4)

if 'data' not in st.session_state:
    st.session_state['data'] = {}

st.sidebar.title("💾 Gestion des Dossiers")
uploaded_file = st.sidebar.file_uploader("Charger un ancien dossier (.json)", type=["json"])

if uploaded_file is not None:
    st.session_state['data'] = json.load(uploaded_file)
    st.sidebar.success("✅ Dossier chargé !")

# Fonction pour simplifier la récupération des données
def g(key, default=""):
    return st.session_state['data'].get(key, default)

st.title("🛡️ OCP Patrimoine - Bilan et Analyse Global")
st.markdown("---")

# --- INITIALISATION DES TOTAUX ---
total_brut_immo = 0.0
total_brut_fin = 0.0
total_passif = 0.0
mensualites_totales = 0.0

# --- SECTION 1 : ÉTAT CIVIL & FAMILLE ---
st.header("1. État Civil & Situation Familiale")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Le Client")
    nom_c = st.text_input("Nom du Client", value=g('nom_c'), key="nom_c")
    pre_c = st.text_input("Prénom du Client", value=g('pre_c'), key="pre_c")
    d_n = g('dnaiss_c', "1980-01-01")
    dnaiss_c = st.date_input("Date de naissance", value=date.fromisoformat(d_n) if isinstance(d_n, str) else d_n, key="dnaiss_c")
    lieu_c = st.text_input("Lieu de naissance", value=g('lieu_c'), key="lieu_c")
    nat_c = st.text_input("Nationalité", value=g('nat_c'), key="nat_c") 

with col2:
    st.subheader("Situation")
    sit_opts = ["Célibataire", "Marié(e)", "Pacsé(e)", "Divorcé(e)", "Veuf/Veuve"]
    sit_val = g('sit_mat', "Célibataire")
    sit_mat = st.selectbox("Situation Matrimoniale", sit_opts, index=sit_opts.index(sit_val) if sit_val in sit_opts else 0, key="sit_mat")
    nb_e = st.number_input("Nombre d'enfants à charge", min_value=0, max_value=15, step=1, value=int(g('nb_e', 0)), key="nb_e")

pre_conj, nom_conj = "", ""
if sit_mat in ["Marié(e)", "Pacsé(e)"]:
    st.markdown("---")
    st.subheader("Informations du Conjoint")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        nom_conj = st.text_input("Nom du Conjoint", value=g('nom_conj'), key="nom_conj")
        d_nc = g('dnaiss_conj', "1980-01-01")
        dnaiss_conj = st.date_input("Date de naissance conjoint", value=date.fromisoformat(d_nc) if isinstance(d_nc, str) else d_nc, key="dnaiss_conj")
        lieu_conj = st.text_input("Lieu de naissance conjoint", value=g('lieu_conj'), key="lieu_conj")
    with c_col2:
        pre_conj = st.text_input("Prénom du Conjoint", value=g('pre_conj'), key="pre_conj")
        nat_conj = st.text_input("Nationalité Conjoint", value=g('nat_conj'), key="nat_conj")

if nb_e > 0:
    st.write("📅 **Détail des enfants :**")
    c_enf = st.columns(3)
    for i in range(int(nb_e)):
        with c_enf[i % 3]:
            d_ne = g(f"dnaiss_enf_{i}", "2010-01-01")
            st.date_input(f"Enfant n°{i+1}", value=date.fromisoformat(d_ne) if isinstance(d_ne, str) else d_ne, key=f"dnaiss_enf_{i}")

st.markdown("---")

# --- SECTION 2 : COORDONNÉES ---
st.header("2. Coordonnées")
c_coo1, c_coo2, c_coo3 = st.columns([2, 1, 1])
with c_coo1:
    adr_p = st.text_input("Adresse postale complète", value=g('adr_p'), key="adr_p")
with c_coo2:
    tel_p = st.text_input("Téléphone", value=g('tel_p'), key="tel_p")
with c_coo3:
    mail_p = st.text_input("Email", value=g('mail_p'), key="mail_p")

st.markdown("---")

# --- SECTION 3 : PROFESSION & REVENUS ---
st.header("3. Situation Professionnelle & Revenus")
cp1, cp2, cp3 = st.columns(3)
with cp1:
    stat_opts = ["Salarié", "TNS / Libéral", "Dirigeant", "Fonctionnaire", "Retraité", "Sans activité"]
    stat_val = g('statut_pro', "Salarié")
    statut_pro = st.selectbox("Statut Professionnel", stat_opts, index=stat_opts.index(stat_val) if stat_val in stat_opts else 0, key="statut_pro")
    poste_pro = st.text_input("Profession / Intitulé du poste", value=g('poste_pro'), key="poste_pro")
with cp2:
    rev_a = st.number_input("Revenu net annuel (€)", min_value=0.0, value=float(g('rev_a', 0.0)), key="rev_a")
    rev_f = st.number_input("Autres revenus (Foncier, etc.) (€)", min_value=0.0, value=float(g('rev_f', 0.0)), key="rev_f")
with cp3:
    tmi_opts = ["0%", "11%", "30%", "41%", "45%"]
    tmi_val = g('tmi_c', "30%")
    tmi_c = st.selectbox("Tranche Marginale d'Imposition (TMI)", tmi_opts, index=tmi_opts.index(tmi_val) if tmi_val in tmi_opts else 2, key="tmi_c")
    age_ret = st.number_input("Âge de départ à la retraite prévu", min_value=50, max_value=80, value=int(g('age_ret', 64)), key="age_ret")

# --- SECTION 3 BIS : BUDGET ---
st.subheader("📊 3. bis Budget & Capacité d'Épargne")
b_col1, b_col2 = st.columns(2)
with b_col1:
    budget_vie = st.number_input("Train de vie mensuel (€)", min_value=0.0, value=float(g('budget_vie', 0.0)), key="budget_vie")
    budget_loyer = st.number_input("Loyer ou Charges de copro (€)", min_value=0.0, value=float(g('budget_loyer', 0.0)), key="budget_loyer")
with b_col2:
    budget_impot = st.number_input("Impôts mensuels (€)", min_value=0.0, value=float(g('budget_impot', 0.0)), key="budget_impot")
    rev_mensuel_estim = (rev_a + rev_f) / 12
    reste_vivre_brut = rev_mensuel_estim - (budget_vie + budget_loyer + budget_impot)
    st.info(f"Revenus mensuels estimés : {rev_mensuel_estim:,.0f} €")

st.markdown("---")

# --- SECTION 4 & 5 : PATRIMOINE IMMOBILIER ---
st.header("4 & 5. Patrimoine Immobilier")
tab1, tab2 = st.tabs(["🏠 Immobilier Physique", "🏢 Pierre-Papier"])
with tab1:
    nb_p_p = st.number_input("Nombre de biens physiques", min_value=0, value=int(g('nb_p_p', 0)), key="nb_p_p")
    for i in range(int(nb_p_p)):
        with st.expander(f"Bien n°{i+1}", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox(f"Type {i}", ["Résidence Principale", "Résidence Secondaire", "Appartement", "Maison", "Terrain", "Parking", "Immeuble de rapport"], key=f"type_i_{i}")
                val_i = st.number_input(f"Valeur vénale (€) {i}", min_value=0.0, value=float(g(f"val_i_{i}", 0.0)), key=f"val_i_{i}")
                total_brut_immo += val_i
            with c2:
                st.selectbox(f"Régime fiscal {i}", ["Droit Commun (Nu)", "LMNP", "LMP", "Pinel", "Malraux", "Monument Historique"], key=f"fisc_i_{i}")
                st.radio(f"Crédit en cours ? {i}", ["Non", "Oui"], key=f"cred_i_{i}")

with tab2:
    nb_p_c = st.number_input("Nombre de placements collectifs", min_value=0, value=int(g('nb_p_c', 0)), key="nb_p_c")
    for j in range(int(nb_p_c)):
        with st.expander(f"Placement Collectif n°{j+1}", expanded=True):
            t_coll = st.selectbox(f"Type support {j}", ["SCPI", "SCI", "OPCI", "GFV / GFI", "Club Deal"], key=f"type_c_{j}")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.text_input(f"Nom {j}", value=g(f"nom_c_{j}"), key=f"nom_c_{j}")
                st.selectbox(f"Mode de détention {j}", ["Pleine Propriété", "Nue-Propriété", "Usufruit", "Via Assurance-Vie", "Via PER"], key=f"det_c_{j}")
            with c2:
                px_c = st.number_input(f"Prix part {j}", min_value=0.0, value=float(g(f"px_c_{j}", 0.0)), key=f"px_c_{j}")
                nb_c = st.number_input(f"Nb parts {j}", min_value=0.0, value=float(g(f"nb_c_{j}", 0.0)), key=f"nb_c_{j}")
                val_liq = px_c * nb_c
                st.write(f"Valeur estimée : {val_liq:,.0f} €")
                total_brut_immo += val_liq
            with c3:
                if t_coll == "SCPI":
                    st.number_input(f"TOF (%) {j}", min_value=0.0, max_value=100.0, value=float(g(f"tof_c_{j}", 0.0)), key=f"tof_c_{j}")
                elif t_coll == "GFV / GFI":
                    st.text_input(f"Surface {j}", value=g(f"surf_c_{j}"), key=f"surf_c_{j}")

st.markdown("---")

# --- SECTION 6 : PATRIMOINE FINANCIER ---
st.header("6. Patrimoine Financier")
nb_f_f = st.number_input("Nombre de contrats financiers", min_value=0, value=int(g('nb_f_f', 0)), key="nb_f_f")
for k in range(int(nb_f_f)):
    with st.expander(f"Contrat n°{k+1}"):
        f1, f2, f3 = st.columns(3)
        with f1:
            st.selectbox(f"Type {k}", ["Livret", "Assurance-Vie", "PER", "PEA", "Compte-Titres"], key=f"typ_f_{k}")
            st.text_input(f"Établissement {k}", value=g(f"banque_f_{k}"), key=f"banque_f_{k}")
        with f2:
            m_f = st.number_input(f"Solde (€) {k}", min_value=0.0, value=float(g(f"m_f_{k}", 0.0)), key=f"m_f_{k}")
            total_brut_fin += m_f
            d_f = g(f"date_f_{k}", "2020-01-01")
            st.date_input(f"Date d'adhésion {k}", value=date.fromisoformat(d_f) if isinstance(d_f, str) else d_f, key=f"date_f_{k}")
        with f3:
            st.selectbox(f"Support {k}", ["Mono-support", "Multi-support", "Gestion Pilotée"], key=f"gest_f_{k}")

st.markdown("---")

# --- SECTION 7 : PRÉVOYANCE ---
st.header("7. Prévoyance & Protection")
nb_p_v = st.number_input("Nombre de contrats prévoyance", min_value=0, value=int(g('nb_p_v', 0)), key="nb_p_v")
for p in range(int(nb_p_v)):
    with st.expander(f"Contrat Prévoyance n°{p+1}"):
        p1, p2, p3 = st.columns(3)
        with p1:
            type_p = st.selectbox(f"Garantie {p}", ["Décès (Capital)", "Rente Éducation", "Rente Conjoint", "IJ (Revenu)", "Invalidité", "Emprunteur"], key=f"p_t_{p}")
        with p2:
            st.number_input(f"Montant Garanti (€) {p}", value=float(g(f"p_m_{p}", 0.0)), key=f"p_m_{p}")
            if type_p == "Emprunteur":
                st.number_input(f"Quotité (%) {p}", min_value=0, max_value=100, value=int(g(f"p_q_{p}", 100)), key=f"p_q_{p}")
        with p3:
            st.text_input(f"Bénéficiaires {p}", value=g(f"p_b_{p}"), key=f"p_b_{p}")

st.markdown("---")

# --- SECTION 8 : SANTÉ ---
st.header("8. Santé / Mutuelle")
s1, s2, s3 = st.columns(3)
with s1:
    s_org = st.text_input("Assureur Santé", value=g('s_org'), key="s_org")
    st.selectbox("Type", ["Individuel", "Collectif", "Madelin"], key="s_typ")
    d_se = g('s_ech', "2026-12-31")
    st.date_input("Échéance", value=date.fromisoformat(d_se) if isinstance(d_se, str) else d_se, key="s_ech")
with s2:
    st.number_input("Cotisation (€)", min_value=0.0, value=float(g('s_cot', 0.0)), key="s_cot")
    st.selectbox("Périodicité", ["Mensuelle", "Trimestrielle", "Annuelle"], key="s_per")
    st.select_slider("Couverture", options=["100%", "200%", "300%", "400%+", "Frais réels"], key="s_niv")
with s3:
    st.multiselect("Personnes couvertes", ["Client", "Conjoint", "Enfant(s)"], default=["Client"], key="s_couv")
    st.text_area("Notes", value=g('s_notes'), key="s_notes")

st.markdown("---")

# --- SECTION 9 : PASSIF ---
st.header("9. Passif & Endettement")
tab_p1, tab_p2 = st.tabs(["🏠 Crédits Immobiliers", "💳 Crédits Conso"])
with tab_p1:
    nb_p_immo = st.number_input("Nb crédits immo", min_value=0, value=int(g('nb_p_immo', 0)), key="nb_p_immo")
    for i in range(int(nb_p_immo)):
        with st.expander(f"Crédit Immo n°{i+1}"):
            cp1, cp2, cp3 = st.columns(3)
            with cp1:
                st.text_input(f"Banque {i}", value=g(f"ban_p_{i}"), key=f"ban_p_{i}")
                st.selectbox(f"Type {i}", ["Amortissable", "In Fine", "Relais"], key=f"typ_p_{i}")
            with cp2:
                crdu = st.number_input(f"Restant Dû {i}", min_value=0.0, value=float(g(f"crdu_p_{i}", 0.0)), key=f"crdu_p_{i}")
                total_passif += crdu
                st.number_input(f"Taux {i}", min_value=0.0, value=float(g(f"taux_p_{i}", 0.0)), key=f"taux_p_{i}")
            with cp3:
                m_mens = st.number_input(f"Mensualité {i}", min_value=0.0, value=float(g(f"mens_p_{i}", 0.0)), key=f"mens_p_{i}")
                mensualites_totales += m_mens
                d_fip = g(f"fin_p_{i}", "2030-01-01")
                st.date_input(f"Date fin {i}", value=date.fromisoformat(d_fip) if isinstance(d_fip, str) else d_fip, key=f"fin_p_{i}")

with tab_p2:
    nb_p_conso = st.number_input("Nb autres crédits", min_value=0, value=int(g('nb_p_conso', 0)), key="nb_p_conso")
    for j in range(int(nb_p_conso)):
        with st.expander(f"Dette n°{j+1}"):
            cc1, cc2 = st.columns(2)
            with cc1:
                st.selectbox(f"Nature {j}", ["Prêt Personnel", "LOA / LLD", "Crédit Renouvelable", "Dette familiale"], key=f"nat_c_p2_{j}")
            with cc2:
                solde_d = st.number_input(f"Reste à payer {j}", min_value=0.0, value=float(g(f"solde_c_p2_{j}", 0.0)), key=f"solde_c_p2_{j}")
                total_passif += solde_d

st.markdown("---")

# --- SECTION 11 : OBJECTIFS ---
st.header("🎯 11. Objectifs & Priorités")
col_obj1, col_obj2 = st.columns(2)
with col_obj1:
    obj_multi = st.multiselect("Objectifs principaux ?", ["Préparer la Retraite", "Réduire la fiscalité", "Protéger la famille", "Transmettre un capital", "Développer l'immobilier", "Revenus immédiats"], key="obj_multi")
with col_obj2:
    st.select_slider("Horizon", options=["Court terme", "Moyen terme", "Long terme", "Transmission"], key="horizon_p")
    st.select_slider("Profil de risque", options=["Prudent", "Équilibré", "Dynamique", "Offensif"], key="profil_r")

# --- CALCULS & SIDEBAR ---
pat_net = total_brut_immo + total_brut_fin - total_passif
capa_epargne = reste_vivre_brut - mensualites_totales
st.sidebar.metric("PATRIMOINE NET", f"{pat_net:,.0f} €".replace(",", " "))
st.sidebar.metric("ÉPARGNE LIBRE", f"{capa_epargne:,.0f} €/mois")

# --- BOUTON SAUVEGARDE & RÉSUMÉ ---
st.markdown("---")
col_s1, col_s2 = st.columns(2)
with col_s1:
    if st.button("🚀 GÉNÉRER LE RÉSUMÉ"):
        st.success("Analyse OCP terminée !")
        st.metric("Net Patrimonial", f"{pat_net:,.0f} €")
        st.metric("Épargne Réelle", f"{capa_epargne:,.0f} €")
with col_s2:
    # On capture toutes les valeurs pour la sauvegarde
    save_btn = st.download_button(
        label="📥 Télécharger la Sauvegarde OCP",
        data=json.dumps({k: v for k, v in st.session_state.items() if k != 'data'}, default=str, indent=4),
        file_name=f"OCP_{nom_c}_{pre_c}.json",
        mime="application/json"
    )

st.info("Outil complet. Les données saisies peuvent être sauvegardées en bas de page.")
