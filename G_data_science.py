import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px


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

st.text('Quelle est la médiane du nombre d’objets trouvés en fonction de la saison? Il y a t il une correlation entre ces deux variables d\'après le graphique?')
df