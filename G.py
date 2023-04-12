import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

def load_data():
    conn = sqlite3.connect("bdd.db")
    query = """
    SELECT objet.date, objet.gare, objet.type, objet.nature, gare.lat, gare.lon, gare.temperature
    FROM objet
    JOIN gare ON objet.gare = gare.gare
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

fig = px.scatter(df_filtre, x='temperature', y='nombre_objets', trendline="ols")

st.write(fig)

results = px.get_trendline_results(fig)
ols_results = results.query("px_fit_name == 'ols'").px_fit_results.iloc[0]

st.write("Est-ce que le nombre d'objets perdus est corrélé à la température d'après ce graphique?")
st.write(f"La p-value pour cette relation est {ols_results.pvalues['x']:.6f}.")

if ols_results.pvalues['x'] < 0.05:
    st.write("Oui, le nombre d'objets perdus est significativement corrélé à la température.")
else:
    st.write("Non, le nombre d'objets perdus n'est pas significativement corrélé à la température.")