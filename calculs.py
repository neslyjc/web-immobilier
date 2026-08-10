"""
calculs.py
Web Immobilier
Release 1.2.0 (base)
"""

from math import pow

def format_argent(valeur: float) -> str:
    """Retourne un montant au format canadien."""
    return f"{valeur:,.0f} $".replace(",", " ")

def calcul_mise_de_fonds(prix_achat: float, pourcentage: float) -> float:
    return prix_achat * (pourcentage / 100)

def calcul_montant_pret(prix_achat: float, mise_de_fonds: float) -> float:
    return prix_achat - mise_de_fonds

def calcul_versement_hypothecaire(montant_pret: float,
                                  taux_annuel: float,
                                  duree_annees: int) -> float:
    """
    Équivalent de la fonction Excel PMT.
    Retourne le versement mensuel.
    """
    taux = taux_annuel / 100 / 12
    nb = duree_annees * 12
    if taux == 0:
        return montant_pret / nb
    facteur = pow(1 + taux, nb)
    return montant_pret * (taux * facteur) / (facteur - 1)

# Les fonctions suivantes seront complétées dans les prochaines versions.

def calcul_prime_schl(*args, **kwargs):
    raise NotImplementedError("À compléter dans la Release 1.2")

def calcul_mrb(*args, **kwargs):
    raise NotImplementedError("À compléter dans une prochaine Release")

def calcul_cash_flow(*args, **kwargs):
    raise NotImplementedError("À compléter dans une prochaine Release")


# ----------------------------------------------------------
# SCHL
# ----------------------------------------------------------

def calcul_taux_schl(mise_de_fonds_pct: float) -> float:
    """
    Retourne le taux de prime SCHL selon le pourcentage
    de mise de fonds.
    """

    if mise_de_fonds_pct >= 20:
        return 0.00
    elif mise_de_fonds_pct >= 15:
        return 2.80
    elif mise_de_fonds_pct >= 10:
        return 3.10
    else:
        return 4.00


def calcul_prime_schl(montant_pret: float,
                      mise_de_fonds_pct: float) -> tuple:
    """
    Retourne :
        taux SCHL
        montant de la prime
        montant financé
    """

    taux = calcul_taux_schl(mise_de_fonds_pct)

    prime = montant_pret * taux / 100

    montant_finance = montant_pret + prime

    return taux, prime, montant_finance
    
    