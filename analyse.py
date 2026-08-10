"""
analyse.py
Web Immobilier
Release 1.0.0
"""

from calculs import (
    calcul_mise_de_fonds,
    calcul_montant_pret,
    calcul_versement_hypothecaire,
)



# ==========================================================
# CONSTANTES
# ==========================================================

NB_MOIS_PAR_AN = 12

SEUIL_EXCELLENT = 500.0
SEUIL_BON = 0.0
SEUIL_ANALYSER = -500.0


# ==========================================================
# FONCTIONS
# ==========================================================

def calcul_cashflow_mensuel(
    revenus_mensuels: float,
    paiement_hypotheque: float,
    depenses_mensuelles: float
) -> float:
    """
    Calcule le Cash Flow mensuel.
    """

    return (
        revenus_mensuels
        - paiement_hypotheque
        - depenses_mensuelles
    )


def calcul_cashflow_annuel(
    cashflow_mensuel: float
) -> float:
    """
    Calcule le Cash Flow annuel.
    """

    return cashflow_mensuel * NB_MOIS_PAR_AN


def calcul_mrb(
    prix_achat: float,
    revenus_annuels: float
) -> float:
    """
    Calcule le MRB.
    """

    return prix_achat / revenus_annuels

   
def calcul_verdict(
    cashflow_mensuel: float
) -> tuple[str, list[str]]:
    """
    Détermine le verdict et les raisons
    de l'analyse.
    """

    raisons = []

  
    if cashflow_mensuel > 0:

        verdict = "🟢 Excellent"

        raisons.append(
            "Cash Flow mensuel positif."
        )

    elif cashflow_mensuel >= -1000:

        verdict = "🟡 À analyser"

        raisons.append(
            "Cash Flow mensuel négatif, mais acceptable."
        )

        raisons.append(
            "Vérifiez que vous pouvez supporter ce déficit mensuel."
        )

    else:

        verdict = "🔴 Risque financier élevé"

        raisons.append(
            "Cash Flow mensuel inférieur à -1 000 $."
        )

        raisons.append(
            "Évaluez attentivement votre capacité financière."
        )
        
    return verdict, raisons


# ==========================================================
# Création de patrimoine
# ==========================================================
     
    
def calcul_capital_rembourse_premiere_annee(
    montant_finance: float,
    taux_annuel: float,
    amortissement_annees: int
) -> tuple[float, float]:
    """
    Calcule le capital remboursé durant la première année.
    """

    taux_mensuel = taux_annuel / 100 / 12

    paiement = calcul_versement_hypothecaire(
        montant_finance,
        taux_annuel,
        amortissement_annees
    )

    solde = montant_finance

    capital_annuel = 0.0

    capital_mensuel = 0.0
    
    
    for mois in range(12):

        interets = solde * taux_mensuel

        capital = paiement - interets
        
        capital_annuel += capital

        solde -= capital
        
      

    capital_mensuel = capital_annuel / 12

    return capital_annuel, capital_mensuel      

    
    
       

# ==========================================================
# TESTS
# ==========================================================

if __name__ == "__main__":

    print("=" * 55)
    print("Module analyse.py")
    print("=" * 55)

    prix_achat = 1_000_000

    mise_pct = 10.0

    taux = 4.25

    duree = 30

    revenus_annuels = 50_000

    revenus_mensuels = revenus_annuels / NB_MOIS_PAR_AN

    depenses_mensuelles = 946    
    
    
    mise = calcul_mise_de_fonds(
        prix_achat,
        mise_pct
    )

    montant_finance = calcul_montant_pret(
        prix_achat,
        mise
    )

    paiement_hypotheque = calcul_versement_hypothecaire(
        montant_finance,
        taux,
        duree
    )
   

    cashflow_mensuel = calcul_cashflow_mensuel(
        revenus_mensuels,
        paiement_hypotheque,
        depenses_mensuelles
    )

    cashflow_annuel = calcul_cashflow_annuel(
        cashflow_mensuel
    )

    mrb = calcul_mrb(
        prix_achat,
        revenus_annuels
    )

   
    verdict, raisons = calcul_verdict(
        cashflow_mensuel
    )

    print(f"Cash Flow mensuel : {cashflow_mensuel:,.0f} $")
    print(f"Cash Flow annuel  : {cashflow_annuel:,.0f} $")
    print(f"MRB               : {mrb:.2f}")
      
    print(f"Verdict...........: {verdict}")

    print("Raisons")

    for raison in raisons:
        print(f"  • {raison}")
        
        
    capital_annuel, capital_mensuel = (
        calcul_capital_rembourse_premiere_annee(
            montant_finance,
            taux,
            duree
        )
    )

    print()
    print("Capital remboursé")
    print("-----------------")

    print(f"Capital remboursé annuel  : {capital_annuel:,.0f} $")
    print(f"Capital remboursé mensuel : {capital_mensuel:,.0f} $")
