import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import sqlite3
import pydeck as pdk

# Connexion à la base de données
connexion = sqlite3.connect('bdd.db')

# Récupération des données de la table objet
query_objet = "SELECT * FROM objet"
df_objet = pd.read_sql_query(query_objet, connexion)

# Récupération des données de la table gare
query_gare = "SELECT * FROM gare"
df_gare = pd.read_sql_query(query_gare, connexion)

# Fermeture de la connexion à la base de données
connexion.close()

# Sélection de l'année et du type d'objet avec des widgets Streamlit
annees = ['2019', '2020', '2021', '2022']
annee_selectionnee = st.selectbox("Sélectionnez l'année :", annees, key=1)

types = df_objet['type'].unique().tolist()
types_selectionnes = st.multiselect("Sélectionnez le type d'objet :", types, default=types[:], key=3)

# Filtrage des données en fonction de la sélection de l'utilisateur
df_objet_filtre = df_objet[(df_objet['type'].isin(types_selectionnes)) & (df_objet['date'].str[-4:] == annee_selectionnee)]
df_gare_filtre = df_gare[['gare', 'lat', 'lon', 'frequentation_' + annee_selectionnee]]

# Calcul du nombre d'objets trouvés des types sélectionnés pour chaque gare
df_nb_objets_par_gare = df_objet_filtre.groupby('gare')['id'].count().reset_index().rename(columns={'id': 'nb_objets'})

# # Jointure des deux tables sur la colonne 'gare'
# df = df_objet_filtre.merge(df_nb_objets_par_gare, df_gare_filtre, on='gare')

# Calcul du ratio fréquentation / nombre d'objets trouvés
df_gare['ratio_freq_objets'] = df_gare['frequentation_' + annee_selectionnee] / df_nb_objets_par_gare.nb_objets

# Création de la carte de Paris avec les barres représentant le ratio
st.write('Carte de Paris avec les barres représentant le ratio fréquentation / nombre d\'objets trouvés :')
view_state = pdk.ViewState(
    longitude=df_gare['lon'].mean(),
    latitude=df_gare['lat'].mean(),
    zoom=10
)
layer = pdk.Layer(
    'ColumnLayer',
    data=df_gare,
    get_position='[lon, lat]',
    get_elevation='ratio_freq_objets/100',
    elevation_scale=1,
    get_fill_color='[255 * ratio_freq_objets, 255 * (1 - ratio_freq_objets), 0]',
    pickable=True,
    auto_highlight=True,
    extruded=True,
    coverage=1
)
tooltip = {
    "html": "<b>Gare :</b> {gare}<br/><b>Ratio fréquentation / objets trouvés :</b> {ratio_freq_objets:.2f}",
    "style": {"backgroundColor": "white", "color": "black"}
}
r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
st.pydeck_chart(r)