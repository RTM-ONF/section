import streamlit as st

st.title("Calculs hydrauliques sur section irrégulière")

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image("images/onf.png", width=200)

"""
Cet outil a été conçu pour faciliter la visualisation et le calcul des principales caractéristiques géométriques et hydrauliques d’une **section irrégulière**.

**L’utilisation de cette application implique l’acceptation pleine et entière des conditions accessibles en bas de cette page.**

Pour vous accompagner étape par étape, l’application se compose de plusieurs onglets :

#### 1. Importer une section

Importez votre fichier décrivant la section.

#### 2. Coordonnées et statistiques

Consultez les valeurs brutes de la géométrie ainsi que les principales statistiques.

#### 3. Visualiser la section

Explorez votre section sous forme de graphique interactif.

#### 4. Propriétés géométriques

Renseignez une hauteur d’eau pour afficher automatiquement le niveau d’eau sur la section et
les principales caractéristiques géométriques.

#### 5. Ecoulements liquides

Appliquez une ou plusieurs lois d'écoulements liquides à votre section.
"""

with st.expander("Avertissement – Clause de non-responsabilité"):
    st.markdown(
        """
        Cette application est fournie à titre informatif et pédagogique. Les calculs, estimations et résultats produits par ce logiciel sont basés sur des modèles, hypothèses et données qui peuvent comporter des approximations ou des simplifications.

        Malgré le soin apporté à son développement et à sa validation, aucune garantie n’est donnée quant à l’exactitude, l’exhaustivité ou l’actualité des informations et résultats fournis.

        En conséquence, les auteurs, développeurs et distributeurs de cette application ne sauraient être tenus responsables des erreurs, omissions ou des conséquences directes ou indirectes résultant de l’utilisation des informations, résultats ou recommandations fournis par ce logiciel.

        L’utilisateur demeure seul responsable de l’interprétation des résultats et de l’usage qu’il en fait. Il lui appartient notamment de vérifier la pertinence des hypothèses, des paramètres d’entrée et des résultats obtenus au regard de son contexte d’utilisation.

        Cette application ne se substitue en aucun cas à une expertise technique, scientifique ou professionnelle. Toute décision fondée sur les résultats fournis par ce logiciel relève de la seule responsabilité de l’utilisateur.

        L’utilisation de cette application implique l’acceptation pleine et entière des présentes conditions.
        """
    )