import requests
import datetime
import sqlite3

gares = ['Paris Gare de Lyon', 'Paris Montparnasse', 'Paris Gare du Nord', 'Paris Saint-Lazare', 'Paris Est', 'Paris Austerlitz', 'Paris Bercy']
def format_date(x):
    return x[8:10]+'/'+x[5:7]+'/'+x[0:4]

connexion = sqlite3.connect('bdd.db')
curseur = connexion.cursor()
for annee in [2019,2020,2021,2022]: 
    for gare in gares: 
        params = {
            'rows' : '10000',
            'dataset': ['objets-trouves-restitution'],
            'sort': ['date'],
            'facet': ['date', 'gc_obo_gare_origine_r_name', 'gc_obo_nature_c', 'gc_obo_type_c'],
            'refine.date': annee,
            'refine.gc_obo_gare_origine_r_name': gare
            }
        url = "https://ressources.data.sncf.com/api/records/1.0/search/?"
        response = requests.get(url, params=params)
        data = response.json()
        for record in data['records']:
            type = record['fields']['gc_obo_type_c']
            nature = record['fields']['gc_obo_nature_c']
            date = datetime.datetime.fromtimestamp(record['fields']['date']).strftime('%d/%m/%Y')
            gare = record['fields']['gc_obo_gare_origine_r_name']
            curseur.execute("""
                 INSERT INTO objet 
                 VALUES (NULL, ?, ?, ?, ?)
                 """, (type, nature, format_date(date), gare))
    connexion.commit()
connexion.close()