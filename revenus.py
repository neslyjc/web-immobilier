"""
===========================================================
Web Immobilier
Module : revenus.py
Version : 1.3.0
===========================================================

Gestion des revenus d'un immeuble locatif.

Version 1.0
-----------
L'utilisateur saisit uniquement le montant des
revenus bruts annuels.

Le module calcule automatiquement :

    - Revenus mensuels
    - Revenus annuels
"""

# ==========================================================
# CONSTANTES
# ==========================================================

NB_MOIS_PAR_AN = 12


# ==========================================================
# CALCULS
# ==========================================================

def calcul_revenus_mensuels(revenus_annuels: float) -> float:
    """
    Convertit les revenus annuels en revenus mensuels.
    """
    return revenus_annuels / NB_MOIS_PAR_AN


def calcul_revenus_annuels(revenus_mensuels: float) -> float:
    """
    Convertit les revenus mensuels en revenus annuels.
    """
    return revenus_mensuels * NB_MOIS_PAR_AN


# ==========================================================
# FORMATAGE
# ==========================================================

def format_argent(valeur: float) -> str:
    """
    Retourne un montant formaté.

    Exemple :
        108000 devient 108 000 $
    """
    return f"{valeur:,.0f} $".replace(",", " ")


# ==========================================================
# TESTS
# ==========================================================

if __name__ == "__main__":

    revenus_annuels = 108000

    print("=" * 50)
    print("Module revenus.py")
    print("=" * 50)

    print(
        "Revenus annuels :",
        format_argent(revenus_annuels)
    )

    print(
        "Revenus mensuels :",
        format_argent(
            calcul_revenus_mensuels(revenus_annuels)
        )
    )