import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import sqlite3
import pydeck as pdk

####################
#################### HISTOGRAMME
####################

# Lire les données depuis la base de données
connexion = sqlite3.connect('bdd.db')
df = pd.read_sql_query("SELECT * FROM objet", connexion)

# Convertir la colonne 'date' en format datetime
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

# Créer une liste des types d'objet uniques
types_objet = df['type'].unique()

st.title("Nombre d'objets trouvés par semaine (total)")
# Sélectionner les types d'objet à afficher
selected_types = st.multiselect('Sélectionner les types d\'objet à afficher', types_objet, default=types_objet[:])

# Filtrer les données en fonction des types d'objet sélectionnés
df_filtered = df[df['type'].isin(selected_types)]


# Regrouper les données par semaine et compter le nombre d'objets trouvés
df_weekly = df_filtered.groupby(pd.Grouper(key='date', freq='W')).count()['id'].reset_index()

# Créer un histogramme avec Plotly
fig = px.bar(df_weekly, x='date', y='id', color='id', color_continuous_scale='Plasma')

# Afficher le graphique avec Streamlit
st.plotly_chart(fig)

####################
#################### CARTE
####################

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

st.title("Nombre d'objets trouvés par année pour 1 million de voyageurs")
types = df_objet['type'].unique().tolist()
types_selectionnes = st.multiselect("Sélectionnez les types d'objets :", types, default=types[:], key=3)

# Filtrage des données en fonction de la sélection de l'utilisateur
df_objet_filtre = df_objet[(df_objet['type'].isin(types_selectionnes)) & (df_objet['date'].str[-4:] == annee_selectionnee)]
df_gare_filtre = df_gare[['gare', 'lat', 'lon', 'frequentation_' + annee_selectionnee]]
df_gare = df_gare.sort_values('gare').reset_index().drop(columns='index')
# Calcul du nombre d'objets trouvés des types sélectionnés pour chaque gare
df_nb_objets_par_gare = df_objet_filtre.groupby('gare')['id'].count().reset_index().rename(columns={'id': 'nb_objets'})

# Calcul du ratio fréquentation / nombre d'objets trouvés
df_gare['ratio_freq_objets'] = round((df_nb_objets_par_gare.nb_objets * 1_000_000) / df_gare['frequentation_' + annee_selectionnee])

import colorcet as cc

def plasma_color(value, min_value, max_value):
    value_normalized = (value - min_value) / (max_value - min_value)
    color_index = int(value_normalized * 255)
    hex_color = cc.palette["CET_CBD2"][color_index]
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    return list(rgb_color)

# Calcul du ratio fréquentation / nombre d'objets trouvés
df_gare['ratio_freq_objets'] = round((df_nb_objets_par_gare.nb_objets * 1_000_000 / df_gare['frequentation_' + annee_selectionnee]))

# Générer les couleurs Plasma pour chaque gare en fonction du ratio
min_ratio = df_gare['ratio_freq_objets'].min()
max_ratio = df_gare['ratio_freq_objets'].max()
df_gare['plasma_color'] = df_gare['ratio_freq_objets'].apply(lambda x: plasma_color(x, min_ratio, max_ratio))
df_gare['rgb_color'] = df_gare['plasma_color'].apply(lambda x: tuple(x))

# Création de la carte de Paris avec les barres représentant le ratio
view_state = pdk.ViewState(
    longitude=df_gare['lon'].mean(),
    latitude=df_gare['lat'].mean(),
    zoom=12,
    pitch=45
)
layer = pdk.Layer(
    'ColumnLayer',
    data=df_gare,
    get_position='[lon, lat]',
    get_elevation='ratio_freq_objets',
    elevation_scale=25,
    get_fill_color='rgb_color',
    pickable=True,
    auto_highlight=True,
    extruded=True,
    coverage=0.2
)
tooltip = {
    "html": "<b>Gare :</b> {gare}<br/><b>Nombre d'objets trouvés sur 1 million de voyageurs :</b> {ratio_freq_objets} objets",
    "style": {"backgroundColor": "black", "color": "white"}
}
r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
st.pydeck_chart(r)













# # Création de la carte de Paris avec les barres représentant le ratio
# view_state = pdk.ViewState(
#     longitude=df_gare['lon'].mean(),
#     latitude=df_gare['lat'].mean(),
#     zoom=12,
#     pitch=45
# )
# layer = pdk.Layer(
#     'ColumnLayer',
#     data=df_gare,
#     get_position='[lon, lat]',
#     get_elevation='ratio_freq_objets',
#     elevation_scale=10,
#     # get_fill_color='[255 * (1 - ratio_freq_objets), 0, 255 * ratio_freq_objets]',
#     get_fill_color='[255, ratio_freq_objets, ratio_freq_objets, 175]',
#     pickable=True,
#     auto_highlight=True,
#     extruded=True,
#     coverage=0.2
# )
# tooltip = {
#     "html": "<b>Gare :</b> {gare}<br/><b>Nombre d'objets trouvés sur 1 million de voyageurs :</b> {ratio_freq_objets} objets",
#     "style": {"backgroundColor": "black", "color": "white"}
# }
# r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
# st.pydeck_chart(r)
