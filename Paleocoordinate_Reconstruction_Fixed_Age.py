# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 14:47:05 2026

@author: nthar
"""

"""
Author: Nicolas Tharaud : nicolas.tharaud@lsce.ipsl.fr
Description:
------------
Ce script permet de reconstruire des coordonnées paléogéographiques
(latitude et longitude dans le passé) à partir de coordonnées modernes,
pour un âge de reconstruction FIXE (unique pour tous les points).

La reconstruction est réalisée via l'API officielle de GPlates en utilisant
le modèle de plaques tectoniques MULLER2022.

-------------------------------------------------------------------------------
FORMAT DU FICHIER D'ENTRÉE (.txt)
-------------------------------------------------------------------------------

Le fichier d'entrée doit être un fichier texte (.txt) contenant les
coordonnées modernes de points géographiques.

Le fichier doit contenir AU MINIMUM deux colonnes avec les noms EXACTS :

    modlon   modlat

Description des colonnes :
- modlon : Longitude actuelle (en degrés décimaux, WGS84)
- modlat : Latitude actuelle (en degrés décimaux, WGS84)

Les colonnes doivent être séparées par des espaces ou des tabulations.
Une ligne d'en-tête est attendue et sera ignorée par le script.

Exemple de fichier Modern_Location.txt :

modlon  modlat
6.40    45.20
130.80  -12.50
-20.30  60.00

-------------------------------------------------------------------------------
SORTIE
-------------------------------------------------------------------------------

Le script génère un fichier texte contenant les coordonnées modernes
et les coordonnées paléogéographiques reconstruites :

    Paleo_Location.txt

Colonnes de sortie :
- modlat : Latitude moderne
- modlon : Longitude moderne
- pallat : Latitude reconstruite à l'âge donné
- pallon : Longitude reconstruite à l'âge donné

La description du code suivant a été générée par l'IA ChatGPT 
===============================================================================
"""


### ======================== Libraries =========================== ###

import numpy as np
import requests
import time


### ======================== Input File =========================== ###

# Chargement du fichier texte contenant les coordonnées modernes
# skiprows=1 permet d'ignorer la ligne d'en-tête
data = np.loadtxt("Modern_Location.txt", skiprows=1)

# Séparation des colonnes
modlon = data[:, 0]   # Longitude moderne
modlat = data[:, 1]   # Latitude moderne


### ======================== Output Containers =========================== ###

# Listes pour stocker les coordonnées paléogéographiques reconstruites
pallon = []  # Longitude paléo
pallat = []  # Latitude paléo


### ======================== GPlates Parameters =========================== ###

# URL de l'API GPlates pour la reconstruction de points
url = "https://gws.gplates.org/reconstruct/reconstruct_points/"

# Âge de reconstruction (en millions d'années)
age = 17

# Modèle tectonique utilisé
model = "MULLER2022"


### ======================== Timing =========================== ###

# Démarrage du chronométrage
start_time = time.time()


### ======================== Reconstruction Loop =========================== ###

# Boucle sur chaque point moderne
for lon, lat in zip(modlon, modlat):

    # Paramètres envoyés à l'API GPlates
    # Attention à l'ordre : longitude, latitude
    params = {"points": f"{lon},{lat}", "time": age, "model": model}

    # Envoi de la requête HTTP
    response = requests.get(url, params=params)

    try:
        # Conversion de la réponse JSON
        data_json = response.json()
        print(f"Réponse pour ({lon}, {lat}) : {data_json}")

        # Vérification de la présence de coordonnées reconstruites
        if "coordinates" in data_json:
            coords_list = data_json["coordinates"]

            if isinstance(coords_list, list) and len(coords_list) > 0:
                # Extraction des coordonnées paléo
                plon, plat = coords_list[0]
                pallon.append(plon)
                pallat.append(plat)
                continue  # On passe au point suivant

        # Cas où la reconstruction n'est pas valide
        print(f"Données manquantes ou invalides pour ({lon}, {lat})")
        pallon.append(np.nan)
        pallat.append(np.nan)

    except Exception as e:
        # Gestion des erreurs
        print(f"Erreur pour ({lon}, {lat}) : {e}")
        pallon.append(np.nan)
        pallat.append(np.nan)

    # Pause pour éviter de surcharger le serveur GPlates
    time.sleep(0.1)


### ======================== Export Results =========================== ###

# Sauvegarde des résultats dans un nouveau fichier texte
# Nom du fichié à adapter
with open("Paleo_Location.txt", "w") as f:
    # Écriture de l'en-tête
    f.write("modlat modlon pallat pallon\n")

    # Écriture ligne par ligne
    for lat, lon, plat, plon in zip(modlat, modlon, pallat, pallon):
        f.write(f"{lat:.2f} {lon:.2f} {plat:.2f} {plon:.2f}\n")


### ======================== Timing End =========================== ###

# Fin du chronométrage
end_time = time.time()
elapsed = end_time - start_time

print("Reconstruction terminée : fichier Paleo_Location.txt créé.")
print(f"Durée d'exécution : {elapsed:.2f} secondes.")
### ====================================================================== ###