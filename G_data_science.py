import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    conn = sqlite3.connect("bdd.db")
    query = """
    SELECT objet.date, objet.gare, objet.type, objet.nature, gare.lat, gare.lon, temperature.temperature
    FROM objet
    JOIN gare ON objet.gare = gare.gare
    JOIN temperature ON objet.date = temperature.date
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def prepare_data(df):
    df['nombre_objets'] = 1
    df_filtre = df.groupby(['gare', 'temperature'])['nombre_objets'].sum().reset_index()
    return df_filtre

st.title("Analyse des objets trouvés en fonction de la température")

df = load_data()
df_filtre = prepare_data(df)

fig = px.scatter(df_filtre, x='temperature', y='nombre_objets', color='temperature', color_continuous_scale='Plasma')
st.write(fig)

st.write("Est-ce que le nombre d'objets perdus est corrélé à la température d'après ce graphique?")



#################################################################


st.title("Distribution du nombre d'objets trouvés par saison")

#la fonction d'attribution des saisons sur chaque objet étant longue, un csv a été enregistré
#afin d'alléger la génération de ce streamlit
df = pd.read_csv('liste_objets_avec_saison.csv')
# Création du sélecteur d'année
annee = st.selectbox("Sélectionnez l'année", ["2019", "2020", "2021", "2022"])

# Filtrage des données en fonction de l'année sélectionnée
df_filtre = df[df['date'].str[-4:] == annee]

# Calcul du nombre d'objets trouvés pour chaque saison et chaque type
counts = df_filtre.groupby(['saison', 'type']).size().reset_index(name='count')


# Création du boxplot avec Plotly Express
box = px.box(counts, x='saison', y='count', color='saison', color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(box)