import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

def load_data():
    conn = sqlite3.connect('bdd.db')
    query = """
    SELECT o.date, t.temperature, COUNT(o.id) as nombre_objets
    FROM objet o
    JOIN temperature t ON o.date = t.date
    GROUP BY o.date, t.temperature
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = load_data()

st.title("Analyse des objets trouvés en fonction de la température")

fig = px.scatter(df, x='temperature', y='nombre_objets', trendline="ols")
st.plotly_chart(fig)

st.write("Est-ce que le nombre d'objets perdus est corrélé à la température d'après ce graphique?")
st.write("Si le graphique montre une tendance claire (ascendante ou descendante) entre la température et le nombre d'objets trouvés, il y a une corrélation entre les deux variables. Sinon, il n'y a pas de corrélation évidente.")


####################################################################################################


import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

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

fig = px.scatter(df_filtre, x='temperature', y='nombre_objets', trendline="ols")

st.write(fig)

results = px.get_trendline_results(fig)
ols_results = results.iloc[0]['px_fit_results']

st.write("Est-ce que le nombre d'objets perdus est corrélé à la température d'après ce graphique?")
st.write(f"La p-value pour cette relation est {ols_results.pvalues[1]:.6f}.")

if ols_results.pvalues[1] < 0.05:
    st.write("Oui, le nombre d'objets perdus est significativement corrélé à la température.")
else:
    st.write("Non, le nombre d'objets perdus n'est pas significativement corrélé à la température.")

