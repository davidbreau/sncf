import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import sqlite3

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

# Récupération des données de la table objet
query_objet = "SELECT * FROM objet"
df_objet = pd.read_sql_query(query_objet, connexion)

# Récupération des données de la table gare
query_gare = "SELECT * FROM gare"
df_gare = pd.read_sql_query(query_gare, connexion)

# Fermeture de la connexion à la base de données
connexion.close()

# Création de la liste des années disponibles
annees = ['2019', '2020', '2021', '2022']

# Création de la liste des types d'objets disponibles
types = df_objet['type'].unique().tolist()

# Sélection de l'année et du type d'objet avec des widgets Streamlit
annee_selectionnee = st.selectbox("Sélectionnez l'année :", annees, key=1)
types_selectionnes = st.multiselect("Sélectionnez le type d'objet :", types, default=types[:], key=3)

# Filtrage des données en fonction de la sélection de l'utilisateur
df_objet_filtre = df_objet[(df_objet['type'].isin(types_selectionnes)) & (df_objet['date'].str[-4:] == annee_selectionnee)]
df_gare_filtre = df_gare[['gare', 'lat', 'lon', 'frequentation_' + annee_selectionnee]]

# Jointure des deux tables sur la colonne 'gare'
df = pd.merge(df_objet_filtre, df_gare_filtre, on='gare')

# Regroupement des données par gare pour obtenir le nombre total d'objets trouvés
df_grouped = df.groupby(['gare', 'lat', 'lon', 'frequentation_' + annee_selectionnee]).size().reset_index(name='nombre_objets')

# Affichage de la carte avec Plotly Express en utilisant des barres 3D et le style Plasma pour la couleur
fig = px.scatter_3d(df_grouped, x="lat", y="lon", z="nombre_objets", color="nombre_objets", color_continuous_scale='Plasma', text="gare", size="frequentation_" + annee_selectionnee, size_max=30)
fig.update_traces(marker=dict(line=dict(width=0.5, color='Black')), selector=dict(mode='markers'))
fig.update_layout(scene=dict(xaxis_title="Latitude", yaxis_title="Longitude", zaxis_title="Nombre d'objets trouvés"),
                  margin=dict(l=0, r=0, b=0, t=0),
                  coloraxis_colorbar=dict(title="Nombre d'objets trouvés"),
                  title="Répartition des objets trouvés par gare et fréquentation en " + annee_selectionnee)

# Afficher le graphique avec Streamlit
st.plotly_chart(fig)
