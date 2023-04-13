import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.text('Afficher le nombre d’objets trouvés en fonction de la température sur un scatterplot. Est ce que le nombre d’objets perdus est corrélé à la temperature d\'après ce graphique?')

conn = sqlite3.connect('bdd.db')

# Récupérer les données des tables 'objet' et 'temperature'
query_objet = "SELECT type, nature, gare, date FROM objet"
df_objet = pd.read_sql_query(query_objet, conn)

query_temp = "SELECT temperature, date FROM temperature"
df_temp = pd.read_sql_query(query_temp, conn)

# Ajouter une colonne 'temperature' au dataframe 'df_objet'
df_objet = pd.merge(df_objet, df_temp, on='date')

# Créer un scatterplot avec 'temperature' en abscisse et le nombre d'objets trouvés en ordonnée
fig, ax = plt.subplots()
ax.scatter(df_objet['temperature'], df_objet.groupby('temperature')['type'].count())
ax.set_xlabel('Température')
ax.set_ylabel('Nombre d\'objets trouvés')

# Afficher le scatterplot dans Streamlit
st.pyplot(fig)

