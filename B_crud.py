import sqlite3



########################################################################################################
########################################### CREATE #####################################################
########################################################################################################

def creer_gare(gare:str) -> None:
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                 INSERT INTO gare 
                 VALUES (NULL, ?)
                 """, (gare))
    connexion.commit()
    connexion.close()


# def creer_objet( type:str, nature:str, date:str, gare:str) -> None:
    # curseur.execute("""
    #              INSERT INTO objet 
    #              VALUES (NULL, ?, ?, ?, ?)
    #              """, (type, nature, date, gare))
# creer_objet = ("""
#                  INSERT INTO objet 
#                  VALUES (NULL, ?, ?, ?, ?)
#                  """, (type, nature, date, gare))


########################################################################################################
########################################### READ #######################################################
########################################################################################################

########################################################################################################
########################################### UPDATE #####################################################
########################################################################################################

def update_geo_gare(gare:str, lat:float, lon: float) -> None:
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE gare
                        SET lat = ?, lon = ?
                        WHERE gare = ?
                    """, (lat, lon, gare))  
    connexion.commit()
    connexion.close()
    
def update_frequentation_gare(gare:str, freq2019:int, freq2020:int, freq2021:int, freq2022: int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE gare
                        SET frequentation_2019 = ?, frequentation_2020 = ?, frequentation_2021 = ?, frequentation_2022 = ?
                        WHERE gare = ?
                    """, (freq2019, freq2020, freq2021, freq2022, gare))  
    connexion.commit()
    connexion.close()

########################################################################################################
########################################### DELETE #####################################################
########################################################################################################

def supprimer_objets():
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    DELETE FROM objet
                    """)
    connexion.commit()
    connexion.close()

