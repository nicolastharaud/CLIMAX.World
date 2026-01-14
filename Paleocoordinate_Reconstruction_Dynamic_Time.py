# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 14:37:19 2026

@author: nthar
"""

"""
Author: Nicolas Tharaud : nicolas.tharaud@lsce.ipsl.fr
Description:
------------
Ce script permet de reconstruire les coordonnées paléogéographiques
(latitude et longitude dans le passé) à partir de coordonnées actuelles
et d'un âge donné (en millions d'années), en utilisant l'API officielle
de GPlates et le modèle de plaques tectoniques MULLER2022.

Les coordonnées reconstruites sont ajoutées aux données d'entrée et
exportées dans un nouveau fichier.

-------------------------------------------------------------------------------
FORMAT DU FICHIER D'ENTRÉE (.txt)
-------------------------------------------------------------------------------

Le fichier d'entrée doit être un fichier texte (.txt) et contenir AU MINIMUM 
les trois colonnes suivantesavec les noms EXACTS :

    ModLat   ModLon   Age

Description des colonnes :
- ModLat : Latitude actuelle du point (en degrés décimaux, WGS84)
- ModLon : Longitude actuelle du point (en degrés décimaux, WGS84)
- Age    : Âge de reconstruction en millions d'années (Ma)

Les séparateurs décimaux peuvent être :
- un point (.)
- ou une virgule (,)

Exemple de fichier Coord.txt :

ModLat  ModLon  Age
45.2    6.4     10
-12,5   130,8   100
60.0    -20.3   50

-------------------------------------------------------------------------------
SORTIE
-------------------------------------------------------------------------------

Le script génère un nouveau fichier contenant les colonnes originales
et deux nouvelles colonnes :

- PalLat : Latitude reconstruite à l'âge donné
- PalLon : Longitude reconstruite à l'âge donné

La description du code suivant a été générée par l'IA ChatGPT 
===============================================================================
"""

### ======================== Libraries =========================== ###

import pandas as pd
import numpy as np
import requests # communication avec l'API GPlates
import time
from tqdm import tqdm # affichage d'une barre de progression


### ======================== Input File =========================== ###

# Lecture du fichier txt
# Adapter le séparateur (sep) si besoin
data = pd.read_csv("Coord.txt", sep=r"\s+", engine="python")


### ======================== Output Containers =========================== ###

# Listes qui stockeront les coordonnées paléogéographiques reconstruites
pallat = []  # Latitudes paléo
pallon = []  # Longitudes paléo


### ======================== GPlates Parameters =========================== ###

# Modele de reconstruction tectonique utilisé
model = "MULLER2022"

# URL de l'API GPlates pour la reconstruction de points
url = "https://gws.gplates.org/reconstruct/reconstruct_points/"


### ======================== Reconstruction Loop =========================== ###

# Boucle sur chaque ligne du fichier d'entrée
# tqdm permet de suivre l'avancement du traitement
for idx, row in tqdm(data.iterrows(), total=len(data), desc="Reconstruction"):
    try:
        # Conversion des valeurs en float
        # La méthode replace permet de gérer les virgules comme séparateur décimal
        lat = float(str(row['ModLat']).replace(',', '.'))
        lon = float(str(row['ModLon']).replace(',', '.'))
        age = float(str(row['Age']).replace(',', '.'))

        # Paramètres envoyés à l'API GPlates
        # Attention : l'ordre est longitude, latitude
        params = {"points": f"{lon},{lat}", "time": age, "model": model}

        # Envoi de la requête HTTP à l'API
        response = requests.get(url, params=params)

        # Conversion de la réponse au format JSON
        data_json = response.json()

        # Vérification que des coordonnées reconstruites sont retournées
        if "coordinates" in data_json and data_json["coordinates"]:
            # Extraction des coordonnées paléo
            plon, plat = data_json["coordinates"][0]
            pallon.append(plon)
            pallat.append(plat)
        else:
            # Cas où l'API ne retourne aucune reconstruction
            print(f"Aucune coordonnée paléo pour ({lon}, {lat}) à {age} Ma")
            pallon.append(np.nan)
            pallat.append(np.nan)

    except Exception as e:
        # Gestion des erreurs (données invalides, problème API, etc.)
        print(f"Erreur à la ligne {idx}: {e}")
        pallon.append(np.nan)
        pallat.append(np.nan)

    # Pause pour éviter de surcharger l'API GPlates
    time.sleep(0.1)


### ======================== Export Results =========================== ###

# Ajout des colonnes de coordonnées reconstruites au tableau original
data['PalLat'] = pallat
data['PalLon'] = pallon

# Sauvegarde des résultats dans un nouveau fichier
# Nom du fichier de sortie peut être adapté
data.to_csv("Coords_Reconstructed.txt", index=False, sep="\t") 

print("Reconstruction terminée : fichier Coords_Reconstructed.txt créé.")
### ====================================================================== ###