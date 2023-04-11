import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import sqlite3

# Lire les données depuis la base de données
connexion = sqlite3.connect('bdd.db')
df = pd.read_sql_query("SELECT * FROM objet", connexion)

# Convertir la colonne 'date' en format datetime
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

# Créer une liste des types d'objet uniques
types_objet = df['type'].unique()

# Sélectionner les types d'objet à afficher
selected_types = st.multiselect('Sélectionner les types d\'objet à afficher', types_objet)

# Filtrer les données en fonction des types d'objet sélectionnés
df_filtered = df[df['type'].isin(selected_types)]

# Sélectionner les données entre 2019 et 2022
df_filtered = df_filtered[(df_filtered['date'] >= '2019-01-01') & (df_filtered['date'] <= '2022-12-31')]

# Regrouper les données par semaine et compter le nombre d'objets trouvés
df_weekly = df_filtered.groupby(pd.Grouper(key='date', freq='W')).count()['id'].reset_index()

# Créer un histogramme avec Plotly
fig = px.bar(df_weekly, x='date', y='id')

# Afficher le graphique avec Streamlit
st.plotly_chart(fig)
