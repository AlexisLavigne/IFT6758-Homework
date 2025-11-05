"""
Ce devoir est basé sur [le cours de science des données de Greg Baker à SFU

Toutes les zones qui nécessitent des travaux sont marquées d'une étiquette "TODO".
"""

import numpy as np


def city_lowest_precipitation(totals: np.array) -> int:
    """
    Étant donné un tableau 2D où chaque ligne représente une ville, et chaque colonne est un mois de janvier 
    à décembre d'une année particulière, retourne la ville avec les précipitations totales les plus faibles.
    """
    return np.sum(totals, axis=1).argmin()


def avg_precipitation_month(totals: np.array, counts: np.array) -> np.array:
    """
    Déterminez les précipitations moyennes à ces endroits pour chaque mois. Ce sera le total
    précipitations pour chaque mois (axe 0), divisé par le total des observations pour ce mois.
    """
    precipitation_per_month = np.sum(totals, axis=0)
    counts_per_month = np.sum(counts, axis=0)
    avg_precipitation_per_month = precipitation_per_month / counts_per_month
    return avg_precipitation_per_month


def avg_precipitation_city(totals: np.array, counts: np.array) -> np.array:
    """
    Faites de même pour les villes: donnez les précipitations moyennes (précipitations quotidiennes moyennes sur le mois) 
    pour chaque ville.
    """
    precipitation_per_city = np.sum(totals, axis=1)
    counts_per_city = np.sum(counts, axis=1)
    avg_precipitation_per_city = precipitation_per_city / counts_per_city
    return avg_precipitation_per_city


def quarterly_precipitation(totals: np.array) -> np.array:
    """
    Calculez les précipitations totales pour chaque trimestre dans chaque ville (c'est-à-dire les totaux pour chaque station sur des groupes de trois mois). Vous pouvez supposer que le nombre de colonnes sera divisible par 3.

    Astuce: Utilisez la fonction de reshape pour reformer en un tableau 4n sur 3, additionner et reformer en n sur 4.
    """
    if totals.shape[1] != 12:
        raise NotImplementedError("Le tableau d'entrée n'a pas 12 mois!")

    n = totals.shape[0]
    totals = totals.reshape(4*n, 3)
    quarterly_totals = totals.sum(axis=1)
    return quarterly_totals.reshape(n, 4)


def main():
    data = np.load("data/monthdata.npz")
    totals = data["totals"]
    counts = data["counts"]

    # You can use this to steer your code
    print(f"Rangée avec la précipitations la plus faible:\n{city_lowest_precipitation(totals)}")
    print(f"La précipitation moyenne par mois:\n{avg_precipitation_month(totals, counts)}")
    print(f"La précipitation moyenne par ville:\n{avg_precipitation_city(totals, counts)}")
    print(f"La précipitations trimestrielle:\n{quarterly_precipitation(totals)}")


if __name__ == "__main__":
    main()
