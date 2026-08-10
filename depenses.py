"""
===========================================================
Web Immobilier
Module : depenses.py
Version : 1.3.0
===========================================================

Gestion des dépenses d'un immeuble locatif.

Version 1.0
-----------
L'utilisateur saisit :

    - Taxes municipales (annuelles)
    - Taxes scolaires (annuelles)
    - Assurance habitation (mensuelle)

Le module calcule automatiquement :

    - Total des taxes annuelles
    - Assurance annuelle
    - Dépenses annuelles
    - Dépenses mensuelles
"""

# ==========================================================
# CONSTANTES
# ==========================================================

NB_MOIS_PAR_AN = 12


# ==========================================================
# CALCULS
# ==========================================================

def calcul_taxes_annuelles(
    taxes_municipales: float,
    taxes_scolaires: float
) -> float:
    """
    Retourne le total des taxes annuelles.
    """

    return taxes_municipales + taxes_scolaires


def calcul_assurance_annuelle(
    assurance_mensuelle: float
) -> float:
    """
    Convertit une assurance mensuelle
    en montant annuel.
    """

    return assurance_mensuelle * NB_MOIS_PAR_AN


def calcul_depenses_annuelles(
    taxes_municipales: float,
    taxes_scolaires: float,
    assurance_mensuelle: float
) -> float:
    """
    Retourne le total annuel des dépenses.
    """

    taxes = calcul_taxes_annuelles(
        taxes_municipales,
        taxes_scolaires
    )

    assurance = calcul_assurance_annuelle(
        assurance_mensuelle
    )

    return taxes + assurance

   
    
def calcul_depenses_mensuelles(
    taxes_annuelles: float,
    assurance_annuelle: float,
    autres_depenses_mensuelles: float
) -> float:
    
    """
    Calcule les dépenses mensuelles
    à partir des taxes annuelles
    et de l'assurance annuelle.
    """

      
    depenses_mensuelles = (
        (taxes_annuelles / NB_MOIS_PAR_AN)
        + (assurance_annuelle / NB_MOIS_PAR_AN)
        + autres_depenses_mensuelles
    )

    return depenses_mensuelles


# ==========================================================
# FORMATAGE
# ==========================================================

def format_argent(valeur: float) -> str:
    """
    Retourne un montant formaté.

    Exemple :

        15000

    devient

        15 000 $
    """

    return f"{valeur:,.0f} $".replace(",", " ")


# ==========================================================
# TESTS
# ==========================================================

if __name__ == "__main__":

    taxes_municipales = 6500
    taxes_scolaires = 500
    assurance_mensuelle = 150

    depenses_annuelles = calcul_depenses_annuelles(
        taxes_municipales,
        taxes_scolaires,
        assurance_mensuelle
    )

    print("=" * 50)
    print("Module depenses.py")
    print("=" * 50)

    print(
        "Taxes annuelles :",
        format_argent(
            calcul_taxes_annuelles(
                taxes_municipales,
                taxes_scolaires
            )
        )
    )

    print(
        "Assurance annuelle :",
        format_argent(
            calcul_assurance_annuelle(
                assurance_mensuelle
            )
        )
    )

    print(
        "Dépenses annuelles :",
        format_argent(
            depenses_annuelles
        )
    )

#    print(
#       "Dépenses mensuelles :",
#        format_argent(
#            calcul_depenses_mensuelles(
#                depenses_annuelles
#            )
#        )
#    )
    
    
    autres_depenses_mensuelles = 0

    taxes_annuelles = calcul_taxes_annuelles(
        taxes_municipales,
        taxes_scolaires
    )

    assurance_annuelle = calcul_assurance_annuelle(
        assurance_mensuelle
    )

    depenses_mensuelles = calcul_depenses_mensuelles(
        taxes_annuelles,
        assurance_annuelle,
        autres_depenses_mensuelles
    )

    print(
        "Dépenses mensuelles :",
        format_argent(depenses_mensuelles)
    )