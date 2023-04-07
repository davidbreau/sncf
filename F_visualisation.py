import streamlit as st
import plotly.express as px
import sqlite3
import pandas as pd
from datetime import datetime


def fetch_data():
    conn = sqlite3.connect("bdd.db")
    query = """
        SELECT o.type, o.nature, o.date, o.gare, g.lat, g.lon, g.frequentation_2019, g.frequentation_2020, g.frequentation_2021, g.frequentation_2022
        FROM objet o
        INNER JOIN gare g ON o.gare = g.gare
        WHERE o.date BETWEEN '2019-01-01' AND '2022-12-31'
        ORDER BY o.date
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def calculate_weekly_sums(df):
    df["date"] = pd.to_datetime(df["date"])
    df["week_number"] = df["date"].dt.to_period("W")
    weekly_sums = df.groupby(["week_number", "type"])["type"].count().reset_index(name="count")
    return weekly_sums


def main():
    st.title("Objets trouvés et fréquentation des gares de Paris")

    df = fetch_data()
    weekly_sums = calculate_weekly_sums(df)

    object_types = weekly_sums["type"].unique()
    selected_types = st.multiselect("Sélectionnez les types d'objet à afficher", object_types, default=object_types)

    filtered_weekly_sums = weekly_sums[weekly_sums["type"].isin(selected_types)]

    fig = px.bar(filtered_weekly_sums, x="week_number", y="count", color="type", text="count",
                 title="Nombre d'objets trouvés par semaine (2019-2022)",
                 labels={"week_number": "Semaine", "count": "Nombre d'objets"},
                 category_orders={"week_number": sorted(weekly_sums["week_number"].unique())})

    st.plotly_chart(fig)

    # Carte de Paris
    years = ["2019", "2020", "2021", "2022"]
    selected_year = st.selectbox("Sélectionnez l'année", years)

    filtered_df = df[df["date"].dt.year == int(selected_year)]
    filtered_df = filtered_df[filtered_df["type"].isin(selected_types)]
    gare_counts = filtered_df.groupby("gare").size().reset_index(name="count")

    fig2 = px.scatter_mapbox(gare_counts,
                             lat="lat",
                             lon="lon",
                             hover_name="gare",
                             hover_data=["count"],
                             color="count",
                             size="count",
                             color_continuous_scale=px.colors.cyclical.IceFire,
                             size_max=30,
                             zoom=12,
                             mapbox_style="carto-positron")

    st.plotly_chart(fig2)


if __name__ == "__main__":
    main()