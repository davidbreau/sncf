import pandas as pd
import streamlit as st
import pydeck as pdk
import sqlite3

# Lire les données depuis la base de données
connexion = sqlite3.connect('bdd.db')
df_objet = pd.read_sql_query("SELECT * FROM objet", connexion)
df_gare = pd.read_sql_query("SELECT * FROM gare", connexion)
connexion.close()

# Création de la liste des années disponibles
annees = ['2019', '2020', '2021', '2022']

# Création de la liste des types d'objets disponibles
types_objet = df_objet['type'].unique()

# Sélection de l'année et du type d'objet avec des widgets Streamlit
annee_selectionnee = st.selectbox("Sélectionnez l'année :", annees, key=1)
types_selectionnes = st.multiselect("Sélectionnez le type d'objet :", types_objet, default=types_objet[:], key=3)

# Filtrage des données en fonction de la sélection de l'utilisateur
df_objet_filtre = df_objet[(df_objet['type'].isin(types_selectionnes)) & (df_objet['date'].str[-4:] == annee_selectionnee)]
df_gare_filtre = df_gare[['gare', 'lat', 'lon', 'frequentation_' + annee_selectionnee]]

# Jointure des deux tables sur la colonne 'gare'
df = pd.merge(df_objet_filtre, df_gare_filtre, on='gare')

# Regroupement des données par gare pour obtenir le nombre total d'objets trouvés
df_grouped = df.groupby(['gare', 'lat', 'lon', 'frequentation_' + annee_selectionnee]).size().reset_index(name='nombre_objets')

# Création de la couche de points 3D avec PyDeck
layer = pdk.Layer(
    'ScatterplotLayer',
    data=df_grouped,
    get_position='[lon, lat]',
    get_color='[nombre_objets, 0, 0, 160]',
    get_radius='[frequentation_' + annee_selectionnee + ']/100000',
    radius=0.5,
    elevation_scale=50,
    pickable=True,
    extruded=True,
)

# Création de la vue avec PyDeck
view_state = pdk.ViewState(
    latitude=df_grouped['lat'].mean(),
    longitude=df_grouped['lon'].mean(),
    zoom=10,
    pitch=50
)

# Création de la carte avec PyDeck
r = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style='mapbox://styles/mapbox/light-v9', tooltip={"text": "{gare}\n{nombre_objets} objets trouvés\n{frequentation_" + annee_selectionnee + "} voyageurs par jour"})

# Affichage de la carte avec Streamlit
st.pydeck_chart(r)
