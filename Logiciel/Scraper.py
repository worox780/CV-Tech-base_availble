from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
from time import sleep
import validators
from bs4 import BeautifulSoup as bs
import requests
import wget

"""name_file = input("nom du fichier")
wget.download(f"https://github.com/worox780/CV-Tech-base_availble/raw/main/{name_file}")"""


class Scraper_Linkedin:
    def __init__(self, is_headless:bool) -> None:
        option = webdriver.ChromeOptions()
        option.headless = is_headless
        self.driver = webdriver.Chrome(options=option)
        self.wait = WebDriverWait(self.driver, 60)

    def Process_experience(self, link_give):
        print("start : " + str(link_give))
        self.driver.get(link_give)
        link = str(self.driver.current_url) + "details/experience"
        self.driver.get(link)
        txt_experience_major:list = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "li.pvs-list__paged-list-item.artdeco-list__item.pvs-list__item--line-separated.pvs-list__item--one-column")))
        soup = bs(str(self.driver.page_source), 'lxml')
        experience = soup.find_all("li", class_="pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column")
        print("experience : ", len(experience))
        if len(experience) == 0:
            return [[["Nane","Nane","Nane","Nane"],["Nane","Nane","Nane","Nane"],["Nane","Nane","Nane","Nane"]],[["Nane","Nane","Nane","Nane"],["Nane","Nane","Nane","Nane"],["Nane","Nane","Nane","Nane"]]]

        
        link_experience_major = self.driver.find_elements(By.CSS_SELECTOR, "li>div>div>div>a[href]")

        resp1 = experience

        final_experience = []
        final_company = []

        count_turn = 0
        add = 0

        for i in range(len(resp1)):
            print("turn : " + str(i))
            if count_turn >= 3:
                break
            
            resp = resp1[count_turn].select("li>div>div>div>ul>li>div")
            if len(list(resp)) > 0:
                title_company = resp1[count_turn].find(class_="display-flex flex-row justify-space-between")
                title_company:str = str(title_company.text).split("\n")
                rang = 0
                for n in range(len(title_company)):
                    if title_company[n - rang] == "" or title_company[n - rang] == " ":
                        title_company.pop(n - rang)
                        rang += 1
                title_company:list = list(title_company[0])
                size_title_company:int = len(title_company)
                for m in range(size_title_company//2, size_title_company):
                    title_company.pop(size_title_company//2)
                title_company = "".join(title_company)
                lst_type_emploi = ['CDI', 'Indépendant', 'Freelance', 'CDD', 'Stage', 'Contrat en alternance', 'Intermittent du spectacle', 'CDI temps partiel', 'Service Civique', 'CDD temps partiel', 'VIE/VIA', 'Fonctionnaire', 'Intérimaire']
                resp = resp1[count_turn].select("li>div>div>div>ul>li>div>div>div>div>a")
                for ii in resp:
                    final_experience.append([])
                    lol = str(ii.text).split("\n")
                    rang = 0
                    for n in range(len(lol)):
                        if lol[n - rang] == "":
                            lol.pop(n - rang)
                            rang += 1
                    for n in range(len(lol)):
                        lst_tempo = list(lol[n])
                        for m in range(len(lol[n])//2, len(lol[n])):
                            lst_tempo.pop(len(lol[n])//2)
                        lst_tempo = "".join(lst_tempo)
                        lol[n] = lst_tempo
                    rang = 0
                    for n in range(len(lol)):
                        if lol[n - rang] == "":
                            lol.pop(n - rang)
                            rang += 1
                    if lol[1] in lst_type_emploi:
                        lol[1] = f"{title_company} . {lol[1]}"
                    else:
                        lol.insert(1, title_company)

                    for addinfo in range(len(lol), 4):
                        lol.append("Nane")
                    
                    if len(lol) > 1:
                        lol.insert(1, link_experience_major[i].get_attribute("href"))

                    final_experience[add] = lol
                    count_turn += 1
                    add += 1
                    if add >= 3:
                        break
            else:
                resp = resp1[count_turn].find(class_="display-flex flex-row justify-space-between")
                final_experience.append([])
                for ii in resp:
                    lol = str(ii.text).split("\n")
                    rang = 0
                    for n in range(len(lol)):
                        if lol[n - rang] == "":
                            lol.pop(n - rang)
                            rang += 1
                    for n in range(len(lol)):
                        lst_tempo = list(lol[n])
                        for m in range(len(lol[n])//2, len(lol[n])):
                            lst_tempo.pop(len(lol[n])//2)
                        result = "".join(lst_tempo)
                        lol[n] = result
                    rang = 0
                    for n in range(len(lol)):
                        if lol[n - rang] == "":
                            lol.pop(n - rang)
                            rang += 1
                    if lol != []:
                        if len(lol) <= 1:
                            link_experience_major.insert(i, "Nane")
                            lol.insert(1, link_experience_major[i])
                        else:
                            lol.insert(1, link_experience_major[i].get_attribute("href"))
                        final_experience[add] = lol
                        count_turn += 1
                        add += 1
        
        for i in range(len(final_experience)):
            if len(final_experience[i]) == 1:
                final_experience[i] = ["Nane","Nane","Nane","Nane"]
        for i in range(len(final_experience)):
            if not validators.url(final_experience[i][1]) and final_experience[i][0] != "Nane":
                final_company.append(["Nane", "Nane", "Nane", "Nane"])
                final_experience[i].pop(1)
            else:
                final_company.append(self.Process_Company(final_experience[i][1]))
                final_experience[i].pop(1)
        for i in range(len(final_experience)):
            for ii in range(len(final_experience[i]), 4):
                final_experience[i].append("Nane")
        for i in range(len(final_experience), 3):
            final_experience.append(["Nane","Nane","Nane","Nane"])
            final_company.append(["Nane", "Nane", "Nane", "Nane"])
        return [final_experience, final_company]

    def Process_Company(self, link_give:str):
        self.driver.get(link_give + "about/")
        
        soup = bs(str(self.driver.page_source), 'html.parser')
        lst_result:dict = {"Page Linkedin":str(self.driver.current_url),"Site web":"Nane", "Secteur":"Nane", "Taille de l’entreprise":"Nane"}
        resp = soup.select("main>div>div>div>div>section>dl")
        if len(resp) > 0:
            resp = resp[0].text
            lst_key = ["Site web", "Secteur", "Taille de l’entreprise"]

            resp = resp.split("\n")

            rang = 0

            for ii in range(len(resp)):
                is_ = True
                for iii in resp[ii - rang]:
                    if iii != " ":
                        is_ = False
                        break
                if is_:
                    resp.pop(ii - rang)
                    rang += 1

            for i in range(len(resp)):
                inter = resp[i].split(" ")
                rang = 0
                for ii in range(len(inter)):
                    if inter[ii - rang] == "":
                        inter.pop(ii - rang)
                        rang += 1
                inter = " ".join(inter)
                resp[i] = inter

            if "Site web" in resp: lst_result["Site web"] = resp[resp.index("Site web")+1]
            if "Secteur" in resp: lst_result["Secteur"] = resp[resp.index("Secteur")+1]
            if "Taille de l’entreprise" in resp: lst_result["Taille de l’entreprise"] = resp[resp.index("Taille de l’entreprise")+1]
            
            return[lst_result["Page Linkedin"], lst_result["Site web"], lst_result["Secteur"], lst_result["Taille de l’entreprise"]]
        else:
            return["Nane", "Nane", "Nane", "Nane"]

    def Login(self, id) -> None:
        if actions.login(self.driver, id[0], id[1]): # if email and password isnt given, it'll prompt in terminal
            print("login")
        else:
            return False


"""scraper_linkedin_mine = Scraper_Linkedin(False)
scraper_linkedin_mine.Login(("louisverite01123@gmail.com", "Harry@thme!tique56"))
print(scraper_linkedin_mine.Process_experience("https://www.linkedin.com/in/louis-verite-626a11263/"))
print("done")"""