import CV_tech
import AccesCV_Tech
import sqlite3
import os

"""
Code pour le lancement du logiciel

code 0:
    RAS
code 1:
    Il manque des informations de connexions
code 2:
    Mise à jour du logiciel à faire. Doit être effectué.
code 3:
    Mise à jour du driver. Doit être effectué.
"""


def GetPath():
    path_inter:list = list(os.path.abspath("main.py").split("\\"))
    path_inter.pop(-1)
    path_inter.append("bd")
    path_inter.append("Information.db")
    path_inter = "\\".join(path_inter)
    return path_inter

def IsUptadeSoftware(data):
    if len(data) == 0: return 1
    reponse = AccesCV_Tech.MiseAJour(logiciel=data[1], driver=data[2]).InformationGenerale()

    if reponse == 200: return 0
    if reponse == 101: return 2
    if reponse == 102: return 3

if __name__ == "__main__":
    path = GetPath()
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        data = cursor.execute("SELECT email_de_connexion,Version_Logiciel,Version_Driver FROM IdentifiantConnexion WHERE id = 1").fetchone()
    except:
        print("error")
    finally:
        cursor.close()
        connection.close()

        CV_tech.Acceuil(where=IsUptadeSoftware(data))
