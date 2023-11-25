import requests
from bs4 import BeautifulSoup as bs
import json


"""
Code de retour pour la maintenance

code 100:
    code 101 -> Mise à jour du logiciel
    code 102 -> Mise à jour du driver
code 200:
    code 200 -> tâche réussite (connection serveur, logiciel à jour)
code 400:
    code 403 -> Accès serveur refusé
    code 404 -> Problème de connexion internet
"""


class AccesCV_Tech:
    def __init__(self, email:str, logiciel:int, driver:int) -> None:
        self.link = "https://github.com/worox780/CV-Tech-base_availble/blob/main/InformationAbonnement.txt"
        self.code_json:dict
        self.email:str = email
        self.abonnement:str
        self.code_json = self.Connect()
    
    def Connect(self) -> dict:
        return FonctionGenerale.CodeJsonPageGithub(self.link)
    
    def CanUseSoftware(self):
        if self.code_json[1] == 404:
            return 404
        for i in self.code_json[0]:
            inter = i.split(" ----- ")[0]
            if self.email == inter:
                return 200
        return 403
    
class FonctionGenerale:
    def CodeJsonPageGithub(url) -> dict:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return [json.loads(response.content)["payload"]["blob"]["rawLines"], 200]
        except:
            return ["", 404]

class MiseAJour:
    def __init__(self, logiciel:int, driver:int) -> None:
        self.logiciel:str = str(logiciel)
        self.driver:str = str(driver)
        
    def InformationGenerale(self):
        response:list = FonctionGenerale.CodeJsonPageGithub("https://github.com/worox780/CV-Tech-base_availble/blob/main/InformationGenerale.txt")
        if response[1] == 200:
            if self.driver != response[0][1]:
                return 102
            elif self.logiciel != response[0][0]:
                return 101
            else:
                return 200
        else:
            return 404




"""connect = MiseAJour(0.1,119.0)
print(connect.InformationGenerale())"""