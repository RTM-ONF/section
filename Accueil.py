import streamlit as st

st.title("Calculs hydrauliques sur section irrégulière")

"""
Cet outil a été conçu pour faciliter l’exploration, la visualisation et le calcul des principales caractéristiques géométriques et hydrauliques d’une **section irrégulière**.

Pour vous accompagner étape par étape, l’application se compose de plusieurs onglets :

### 1. Importer une section

Importez votre fichier décrivant la section.

### 2. Coordonnées et statistiques basiques

Consultez les valeurs brutes de la géométrie ainsi que leurs statistiques essentielles.

### 3. Visualiser la section

Explorez votre section sous forme de graphique interactif.

### 4. Propriétés géométriques

Renseignez une hauteur d’eau pour afficher automatiquement le niveau d’eau sur la section et
les caractéristiques géométriques clés.

### 5. Relation hauteur débit

Générez les courbes de débit en fonction de la hauteur d’eau selon plusieurs modèles hydrauliques.
"""