import sqlite3

connexion = sqlite3.connect('bdd.db')
curseur = connexion.cursor()

curseur.execute("""
                CREATE TABLE IF NOT EXISTS gare (
                    gare TEXT NOT NULL PRIMARY KEY,
                    lat FLOAT,
                    lon FLOAT,
                    frequentation_2019 INT,
                    frequentation_2020 INT,
                    frequentation_2021 INT,
                    frequentation_2022 INT
                )
                """)

curseur.execute("""
                CREATE TABLE IF NOT EXISTS temperature (
                    temperature FLOAT NOT NULL,
                    date TEXT NOT NULL PRIMARY KEY
                )
                """)

curseur.execute("""
                CREATE TABLE IF NOT EXISTS objet (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    nature TEXT NOT NULL,
                    date TEXT NOT NULL,
                    gare TEXT,
                    FOREIGN KEY (gare)
                        REFERENCES gare(gare),
                    FOREIGN KEY (date)
                        REFERENCES temperature(date)
                )
                """) ### /!\ si gare(gare) ne marche pas : essayer gare_id references gare(id)

connexion.commit()
connexion.close()
