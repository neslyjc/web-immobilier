"""
app.py
Web Immobilier
Release 1.2.0 (base)
"""

# ============================================================
# Web Immobilier
#
# Mission
# Transformer des données financières en informations utiles
# pour prendre une meilleure décision d'investissement.
# ============================================================


import streamlit as st

from config import (
    APP_NAME,
    APP_VERSION,
    PRIX_ACHAT_DEFAUT,
    MISE_DE_FONDS_DEFAUT,
    TAUX_HYPOTHECAIRE_DEFAUT,
    DUREE_HYPOTHEQUE_DEFAUT,
    DUREES_HYPOTHEQUE,
    REVENUS_ANNUELS_DEFAUT,  
    TAXES_MUNICIPALES_DEFAUT,
    TAXES_SCOLAIRES_DEFAUT,
    ASSURANCE_HABITATION_DEFAUT,
    AUTRES_DEPENSES_MENSUELLES_DEFAUT,
)

from calculs import (
    calcul_mise_de_fonds,
    calcul_montant_pret,
    calcul_prime_schl,
    calcul_versement_hypothecaire,
    format_argent,
)

from revenus import (
    calcul_revenus_mensuels,
    calcul_revenus_annuels,
)

from depenses import (
    calcul_taxes_annuelles,
    calcul_assurance_annuelle,
    calcul_depenses_mensuelles,
)

from analyse import (
    calcul_cashflow_mensuel,
    calcul_cashflow_annuel,
    calcul_mrb,
    calcul_capital_rembourse_premiere_annee,
)


st.set_page_config(page_title=APP_NAME, layout="wide")

# ============================================================
# Protection par mot de passe — accès réservé
# ============================================================
# Le mot de passe est conservé dans Streamlit Secrets
# sous la clé APP_PASSWORD. Il n'est jamais écrit dans le code.
def verifier_acces() -> bool:
    if st.session_state.get("authentifie", False):
        return True

    st.title(APP_NAME)
    st.caption(f"Release {APP_VERSION}")
    st.subheader("Accès réservé")

    champ_mot_de_passe, _ = st.columns([0.50, 0.50])

    st.markdown(
        """
        <style>
        /* Page de connexion : texte du champ et bouton Accéder */
        div[data-testid="stTextInput"] label p {
            font-size: 1.05rem !important;
            font-weight: 700 !important;
        }
        /* Bouton Connexion : ciblage exclusif */
        div.st-key-connexion_button button {
            width: 155px !important;
            min-width: 155px !important;
            max-width: 155px !important;
            padding: 0.55rem 1.25rem !important;
            background-color: #4A90E2 !important;
            color: white !important;
            border: 1px solid #4A90E2 !important;
        }
        div.st-key-connexion_button button p,
        div.st-key-connexion_button button span,
        div.st-key-connexion_button button div {
            font-size: 1.30rem !important;
            font-weight: 800 !important;
            line-height: 1.1 !important;
            color: white !important;
        }
        div.st-key-connexion_button button:hover {
            background-color: #357ABD !important;
            color: white !important;
            border-color: #357ABD !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with champ_mot_de_passe:
        mot_de_passe = st.text_input(
            "Veuillez entrer le mot de passe :",
            type="password",
            key="mot_de_passe",
        )

    with st.container(key="connexion_button"):
        if st.button("Connexion"):
            mot_de_passe_attendu = st.secrets.get("APP_PASSWORD", "")

            if not mot_de_passe_attendu:
                st.error(
                    "Le mot de passe de l'application n'est pas encore configuré "
                    "dans Streamlit Secrets."
                )
                st.stop()

            if mot_de_passe == mot_de_passe_attendu:
                st.session_state["authentifie"] = True
                st.rerun()
            else:
                st.error("Mot de passe incorrect.")

    return False


# Protection par mot de passe activée pour la mise en ligne.
if not verifier_acces():
    st.stop()

# ============================================================
# Style de présentation — Phase 1.2
# ============================================================
# La logique métier et les calculs restent inchangés.
# Ce bloc agit uniquement sur la présentation des résultats.
st.markdown("""
<style>
/* Test esthétique — Prix d'achat uniquement */
div[data-testid="stTextInput"] input {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
}

/* Signes - / + : cibler directement le texte du bouton.
   La taille du bouton lui-même reste inchangée. */
div[data-testid="stButton"] button p,
div[data-testid="stButton"] button span {
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    line-height: 1 !important;
}
/* Réduire légèrement la largeur visuelle de la zone de saisie */
section[data-testid="stSidebar"] {
    width: 100%;
}

/* Titres des cartes de résultats */
.resultat-titre {
    font-size: 1.05rem;
    font-weight: 700;
    line-height: 1.25;
    margin-bottom: 0.45rem;
}

/* Description principale : lisible et au moins aussi visible que le montant */
.resultat-description {
    font-size: 1.00rem;
    font-weight: 700;
    line-height: 1.25;
    margin-bottom: 0.15rem;
}

/* Montant : plus gros et en gras */
.resultat-valeur {
    font-size: 1.45rem;
    font-weight: 700;
    line-height: 1.20;
    margin-bottom: 0.20rem;
}

/* Commentaire secondaire : lisible, mais moins dominant */
.resultat-commentaire {
    font-size: 1.00rem;
    font-weight: 500;
    line-height: 1.30;
    margin-top: 0.05rem;
}

/* Petit montant secondaire, par exemple la prime SCHL */
.resultat-secondaire {
    display: inline-block;
    font-size: 1.230rem;
    font-weight: 700;
    margin-top: 0.20rem;
    padding: 0.18rem 0.45rem;
    border-radius: 0.35rem;
    background: #d9f5df;
}

/* Carte individuelle */
.resultat-carte {
    padding: 0.55rem 0.15rem 0.65rem 0.15rem;
    min-height: 5.2rem;
}

/* Évite que les longs libellés soient écrasés */
.resultat-description-long {
    max-width: 100%;
}

/* Verdict pleine largeur */
.verdict-carte {
    margin-top: 0.65rem;
    padding: 0.75rem 1rem;
    border-top: 1px solid #d8d8d8;
}

.verdict-titre {
    font-size: 1.35rem;
    font-weight: 700;
    margin-bottom: 0.15rem;
}

.verdict-valeur {
    font-size: 1.15rem;
    font-weight: 700;
    line-height: 1.25;
}

.verdict-raison {
    font-size: 0.88rem;
    font-weight: 500;
    line-height: 1.35;
    margin-top: 0.55rem;
}

/* Réduire l'espace vertical inutile entre les éléments */
div[data-testid="stVerticalBlock"] {
    gap: 0.35rem;
}

/* Harmoniser la colonne de saisie #1 avec les colonnes de résultats */
div[data-testid="stWidgetLabel"] p {
    font-size: 1.00rem !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
}

/* Options générales : cases à cocher visibles et lisibles. */
div[data-testid="stCheckbox"] label p {
    font-size: 1.00rem !important;
    font-weight: 700 !important;
}

/* Colonne #1 : libellés des champs en gras et lisibles.
   Streamlit place le libellé à l'intérieur de chaque widget :
   on cible donc directement les labels des widgets concernés. */
div[data-testid="stNumberInput"] [data-testid="stWidgetLabel"] p,
div[data-testid="stNumberInput"] [data-testid="stWidgetLabel"] *,
div[data-testid="stSelectbox"] [data-testid="stWidgetLabel"] p,
div[data-testid="stSelectbox"] [data-testid="stWidgetLabel"] *,
div[data-testid="stSlider"] [data-testid="stWidgetLabel"] p,
div[data-testid="stSlider"] [data-testid="stWidgetLabel"] * {
    font-size: 1.00rem !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
}

/* Sécurité pour les variantes de structure DOM de Streamlit */
div[data-testid="stNumberInput"] label,
div[data-testid="stNumberInput"] label *,
div[data-testid="stSelectbox"] label,
div[data-testid="stSelectbox"] label *,
div[data-testid="stSlider"] label,
div[data-testid="stSlider"] label * {
    font-weight: 700 !important;
}

/* Montants saisis : gras et légèrement plus visibles */
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"],
div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
}

/* Valeurs saisies : plus visibles, comme les données des résultats */
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
}

/* Durée de l'hypothèque : valeur sélectionnée en rouge,
   avec la même taille et le même poids visuel que les autres valeurs. */
div[data-testid="stSelectbox"] [role="combobox"],
div[data-testid="stSelectbox"] [role="combobox"] *,
div[data-testid="stSelectbox"] [role="combobox"] span {
    color: #ff4b4b !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
}

/* Taux hypothécaire (%) : valeur rouge et en gras */
div[data-testid="stNumberInput"]:has(input[aria-label="Taux hypothécaire (%)"]) input {
    color: #ff4b4b !important;
    font-weight: 700 !important;
}

/* Mise de fonds (%) : valeur rouge et en gras */
div[data-testid="stNumberInput"]:has(input[aria-label="Mise de fonds (%)"]) input {
    color: #ff4b4b !important;
    font-weight: 700 !important;
}

/* Texte des bornes du curseur */
div[data-testid="stSlider"] [data-testid="stTickBarMin"],
div[data-testid="stSlider"] [data-testid="stTickBarMax"] {
    font-size: 0.95rem !important;
}

/* ------------------------------------------------------------
   Responsive mobile : conserver les lignes Montant | - | +
   sur une seule ligne.
   On cible uniquement les blocs à 3 colonnes qui contiennent
   les boutons - / +, afin de ne pas modifier les autres
   colonnes de l'application sur téléphone.
   ------------------------------------------------------------ */
@media (max-width: 640px) {
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(3) div[data-testid="stButton"]) {
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: stretch !important;
    }

    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(3) div[data-testid="stButton"]) > div:nth-child(1) {
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(3) div[data-testid="stButton"]) > div:nth-child(2),
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(3) div[data-testid="stButton"]) > div:nth-child(3) {
        flex: 0 0 2.75rem !important;
        min-width: 2.75rem !important;
    }
}
</style>
""", unsafe_allow_html=True)


def deconnecter():
    st.session_state["authentifie"] = False
    st.session_state.pop("mot_de_passe", None)


def formater_revenu_sauvegarde(valeur):
    try:
        return f"{int(float(valeur)):,.0f}".replace(",", " ")
    except (TypeError, ValueError):
        return f"{int(REVENUS_ANNUELS_DEFAUT):,}".replace(",", " ")


def basculer_immeuble_revenu():
    actif = st.session_state.get("immeuble_a_revenu", True)
    if actif:
        valeur_sauvegardee = st.session_state.get(
            "revenus_annuels_avant_zero", REVENUS_ANNUELS_DEFAUT
        )
        st.session_state["revenus_annuels_texte"] = formater_revenu_sauvegarde(
            valeur_sauvegardee
        )
    else:
        valeur = st.session_state.get("revenus_annuels_texte", "")
        valeur = valeur.replace(" ", "").replace("\u00a0", "")
        try:
            valeur = float(valeur)
            if valeur > 0:
                st.session_state["revenus_annuels_avant_zero"] = valeur
        except ValueError:
            pass
        st.session_state["revenus_annuels_texte"] = "0"


# En-tête : titre à gauche, options au centre, Déconnexion à droite.
header_left, header_options, header_right = st.columns([0.30, 0.50, 0.20])

with header_left:
    st.title(APP_NAME)
    st.caption(f"Release {APP_VERSION}")

with header_options:
    st.checkbox(
        "Immeuble à Revenu",
        value=True,
        key="immeuble_a_revenu",
        on_change=basculer_immeuble_revenu,
    )
    st.checkbox(
        "Prime SCHL",
        value=True,
        key="prime_schl_active",
    )

with header_right:
    st.markdown("<div style='height:0.25rem;'></div>", unsafe_allow_html=True)
    st.button(
        "🔒 Déconnexion",
        key="bouton_deconnexion",
        on_click=deconnecter,
        use_container_width=True,
    )


gauche, droite = st.columns([0.58, 1.42])


with gauche:
    st.subheader("Financement")

    def champ_montant_avec_separateurs(label, default, step, key):
        def formater():
            valeur = st.session_state.get(key, "")
            valeur = valeur.replace(" ", "").replace("\u00a0", "")
            if valeur:
                try:
                    st.session_state[key] = f"{float(valeur):,.0f}".replace(",", " ")
                except ValueError:
                    pass

        def valeur():
            brut = st.session_state.get(key, "").replace(" ", "").replace("\u00a0", "")
            try:
                return int(float(brut))
            except ValueError:
                return 0

        def moins():
            st.session_state[key] = f"{max(0, valeur() - step):,}".replace(",", " ")

        def plus():
            st.session_state[key] = f"{valeur() + step:,}".replace(",", " ")

        if key not in st.session_state:
            st.session_state[key] = f"{int(default):,}".replace(",", " ")

        st.markdown(
            f'<div style="font-size:1.05rem;font-weight:700;line-height:1.25;'
            f'margin-bottom:0.65rem;">{label}</div>',
            unsafe_allow_html=True,
        )

        c_val, c_minus, c_plus = st.columns([0.86, 0.07, 0.07])

        with c_val:
            texte = st.text_input(
                label,
                key=key,
                on_change=formater,
                label_visibility="collapsed",
            )

        with c_minus:
            st.button("−", key=f"{key}_moins", on_click=moins, use_container_width=True)

        with c_plus:
            st.button("+", key=f"{key}_plus", on_click=plus, use_container_width=True)

        try:
            return float(texte.replace(" ", "").replace("\u00a0", "") or 0)
        except ValueError:
            st.error(f"Veuillez entrer un montant valide pour « {label} ».")
            return 0.0

    # Test local : Prix d'achat en texte avec séparateur de milliers.
    # Les boutons - / + modifient la valeur par tranches de 10 000 $,
    # puis la valeur reste affichée avec les espaces de séparation.
    def formater_prix_achat():
        valeur = st.session_state.get("prix_achat_texte", "")
        valeur_nettoyee = valeur.replace(" ", "").replace("\u00a0", "")
        if not valeur_nettoyee:
            return
        try:
            nombre = float(valeur_nettoyee)
            st.session_state["prix_achat_texte"] = f"{nombre:,.0f}".replace(",", " ")
        except ValueError:
            pass

    def valeur_prix_achat():
        valeur = st.session_state.get("prix_achat_texte", "")
        valeur = valeur.replace(" ", "").replace("\u00a0", "")
        try:
            return int(float(valeur))
        except ValueError:
            return 0

    def prix_achat_moins():
        valeur = max(0, valeur_prix_achat() - 10000)
        st.session_state["prix_achat_texte"] = f"{valeur:,}".replace(",", " ")

    def prix_achat_plus():
        valeur = valeur_prix_achat() + 10000
        st.session_state["prix_achat_texte"] = f"{valeur:,}".replace(",", " ")

    if "prix_achat_texte" not in st.session_state:
        st.session_state["prix_achat_texte"] = (
            f"{int(PRIX_ACHAT_DEFAUT):,}".replace(",", " ")
        )

    # Libellé séparé pour aligner les boutons exactement sur la barre de saisie.
    st.markdown(
        '<div style="font-size:1.05rem;font-weight:700;line-height:1.25;'
        'margin-bottom:0.65rem;">Prix d\'achat ($)</div>',
        unsafe_allow_html=True,
    )

    col_prix, col_moins, col_plus = st.columns([0.86, 0.07, 0.07])

    with col_prix:
        prix_achat_texte = st.text_input(
            "Prix d'achat ($)",
            key="prix_achat_texte",
            on_change=formater_prix_achat,
            label_visibility="collapsed",
        )

    with col_moins:
        st.button(
            "−",
            key="prix_achat_moins",
            on_click=prix_achat_moins,
            use_container_width=True,
        )

    with col_plus:
        st.button(
            "+",
            key="prix_achat_plus",
            on_click=prix_achat_plus,
            use_container_width=True,
        )

    try:
        prix_achat = float(
            prix_achat_texte.replace(" ", "").replace("\u00a0", "")
        )
    except ValueError:
        prix_achat = 0.0
        st.error("Veuillez entrer un montant valide.")
    
    if not st.session_state.get("immeuble_a_revenu", True):
        st.session_state["revenus_annuels_texte"] = "0"

    revenus_annuels = champ_montant_avec_separateurs(
        "Revenus bruts annuels ($)", REVENUS_ANNUELS_DEFAUT, 1000, "revenus_annuels_texte"
    )

    if not st.session_state.get("immeuble_a_revenu", True):
        revenus_annuels = 0.0
    
    mise_pct = st.number_input(
        "Mise de fonds (%)",
        min_value=5.0,
        max_value=100.0,
        value=float(MISE_DE_FONDS_DEFAUT),
        step=0.25,
        format="%.2f",
    )

    duree = st.selectbox(
        "Durée de l'hypothèque (ans)",
        DUREES_HYPOTHEQUE,
        index=DUREES_HYPOTHEQUE.index(DUREE_HYPOTHEQUE_DEFAUT),
    )

       
    taux = st.number_input(
        "Taux hypothécaire (%)",
        min_value=0.0,
        value=float(TAUX_HYPOTHECAIRE_DEFAUT),
        step=0.05,
    )
    
    
    taxes_municipales = champ_montant_avec_separateurs(
        "Taxes municipales ($/année)", TAXES_MUNICIPALES_DEFAUT, 100, "taxes_municipales_texte"
    )
  

    taxes_scolaires = champ_montant_avec_separateurs(
        "Taxes scolaires ($/année)", TAXES_SCOLAIRES_DEFAUT, 50, "taxes_scolaires_texte"
    )
  
    
    assurance = champ_montant_avec_separateurs(
        "Assurance habitation ($/mois)", ASSURANCE_HABITATION_DEFAUT, 25, "assurance_texte"
    )
        
    
    autres_depenses_mensuelles = champ_montant_avec_separateurs(
        "Autres dépenses ($/mois)", AUTRES_DEPENSES_MENSUELLES_DEFAUT, 25, "autres_depenses_texte"
    )
    
    
mise = calcul_mise_de_fonds(prix_achat, mise_pct)

pret = calcul_montant_pret(prix_achat, mise)

revenus_mensuels = calcul_revenus_mensuels(
    revenus_annuels
)


taxes_annuelles = calcul_taxes_annuelles(
    taxes_municipales,
    taxes_scolaires,
)

assurance_annuelle = calcul_assurance_annuelle(
    assurance
)

depenses_mensuelles = calcul_depenses_mensuelles(
    taxes_annuelles,
    assurance_annuelle,
    autres_depenses_mensuelles,
)


taux_schl_calcule, prime_schl_calcule, montant_finance_calcule = calcul_prime_schl(
    pret,
    mise_pct
)

if st.session_state.get("prime_schl_active", True):
    taux_schl = taux_schl_calcule
    prime_schl = prime_schl_calcule
    montant_finance = montant_finance_calcule
else:
    taux_schl = 0.0
    prime_schl = 0.0
    montant_finance = pret

paiement = calcul_versement_hypothecaire(
    montant_finance,
    taux,
    duree
)

cashflow_mensuel = calcul_cashflow_mensuel(
    revenus_mensuels,
    paiement,
    depenses_mensuelles,
)


cashflow_annuel = calcul_cashflow_annuel(
    cashflow_mensuel
)

capital_annuel, capital_mensuel = (
    calcul_capital_rembourse_premiere_annee(
        montant_finance,
        taux,
        duree
    )
)


mrb = calcul_mrb(prix_achat, revenus_annuels) if revenus_annuels > 0 else None


with droite:
    st.subheader("Résultats")

    # ==========================================================
    # Fonction d'affichage des résultats
    # ==========================================================
    # Cette fonction ne modifie aucune donnée ni aucun calcul.
    # Elle sert uniquement à uniformiser la typographie.
    def afficher_resultat(
        icone,
        description,
        valeur,
        commentaire=None,
        secondaire=None,
        rouge=False,
    ):
        valeur_classe = "resultat-valeur"
        valeur_style = ' style="color:#d62728;"' if rouge else ""

        html = f"""
        <div class="resultat-carte">
            <div class="resultat-description">{icone} {description}</div>
            <div class="{valeur_classe}"{valeur_style}>{valeur}</div>
        """

        if commentaire:
            html += f'<div class="resultat-commentaire">{commentaire}</div>'

        if secondaire:
            html += f'<div class="resultat-secondaire">{secondaire}</div>'

        html += "</div>"

        st.markdown(html, unsafe_allow_html=True)

    # ==========================================================
    # Colonnes des résultats
    # ==========================================================
    col_financement, col_depenses, col_revenus, col_analyse = st.columns(4)

    with col_financement:

        st.markdown("### 🏦 Financement")

        afficher_resultat(
            "💰",
            "Mise de fonds",
            format_argent(mise),
            "Apport personnel initial",
        )

        afficher_resultat(
            "💵",
            "Montant du prêt",
            format_argent(pret),
            "Montant emprunté auprès de la banque",
        )

        afficher_resultat(
            "🏦",
            "Prime SCHL",
            f"{taux_schl:.2f} %",
            "Assurance prêt hypothécaire",
            f"+ {format_argent(prime_schl)}",
        )

        afficher_resultat(
            "💳",
            "Montant financé",
            format_argent(montant_finance),
            "Total du financement",
        )

    with col_depenses:

        st.markdown("### 💸 Dépenses")

        afficher_resultat(
            "🏠",
            "Paiement mensuel (hypothèque)",
            format_argent(paiement),
            "Paiement hypothécaire mensuel",
        )

        afficher_resultat(
            "🏛️",
            "Taxes annuelles",
            format_argent(taxes_annuelles),
            "Taxes municipales et scolaires",
        )

        afficher_resultat(
            "🛡️",
            "Assurance annuelle",
            format_argent(assurance_annuelle),
            "Assurance habitation annuelle",
        )

        afficher_resultat(
            "💸",
            "Dépenses mensuelles (hors hypothèque)",
            format_argent(depenses_mensuelles),
            "Autres dépenses mensuelles",
        )

    with col_revenus:

        st.markdown("### 💰 Revenus")

        afficher_resultat(
            "📅",
            "Revenus mensuels",
            format_argent(revenus_mensuels),
            "Revenus locatifs mensuels",
        )

        afficher_resultat(
            "🏢",
            "Revenus annuels",
            format_argent(revenus_annuels),
            "Revenus locatifs annuels",
        )

    with col_analyse:
        st.markdown("### 📊 Analyse")

        afficher_resultat(
            "💵",
            "Cash Flow mensuel",
            format_argent(cashflow_mensuel),
            "Flux de trésorerie mensuel",
            rouge=cashflow_mensuel < 0,
        )

        afficher_resultat(
            "📅",
            "Cash Flow annuel",
            format_argent(cashflow_annuel),
            "Flux de trésorerie annuel",
            rouge=cashflow_annuel < 0,
        )

        afficher_resultat(
            "🏦",
            "Capital remboursé (mensuel)",
            format_argent(capital_mensuel),
            "Capital remboursé chaque mois",
        )

        afficher_resultat(
            "🏦",
            "Capital remboursé (annuel)",
            format_argent(capital_annuel),
            "Capital remboursé chaque année",
        )

        afficher_resultat(
            "📈",
            "Multiplicateur de revenu brut (MRB)",
            f"{mrb:.2f}" if mrb is not None else "N/A",
            "Multiplicateur de revenu brut",
        )

    # ==========================================================
    # Conclusion — données de cash flow uniquement
    # ==========================================================
    st.markdown('<div class="verdict-carte">', unsafe_allow_html=True)
    st.markdown(
        '<div class="verdict-titre">📊 Conclusion</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="verdict-valeur" style="color:#d62728;">Cash Flow mensuel : {format_argent(cashflow_mensuel)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="verdict-valeur" style="color:#d62728;">Cash Flow annuel     : {format_argent(cashflow_annuel)}</div>', 
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

