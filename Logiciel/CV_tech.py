import AccesCV_Tech
import dearpygui.dearpygui as dpg
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import sqlite3
import webbrowser
import Scraper
import time
import os


class Acceuil:
    def __init__(self, where=0) -> None:
        
        dpg.create_context() #création de la fenêtre
        
        self.get_name_btn = []
        self.can_open_table = True
        self.path = self.GetPath(["bd","Profils.db"]) #chemin de la base de donnée
        self.name_table = ""
        self.current_table = ""
        self.data:list = []
        self.data_change = []
        self.data_now = []

        self.GetsIDConnection()

        dpg.create_viewport(title='CV-Tech', width=600, height=400, large_icon=r"C:\Users\VERITE\OneDrive\Desktop\LouisVerite\3_programmation\CV tech\logo\Logo_V2.ico", small_icon=r"C:\Users\VERITE\OneDrive\Desktop\LouisVerite\3_programmation\CV tech\logo\Logo_V2.ico") #initialisation de la fenêtre du logiciel
        dpg.set_viewport_resize_callback(self.Size_Window) #connection du fonction de récupération lors de la modification de la taille de la fenêtre mère

        #-----fenêtre interne qui contient tout-----
        with dpg.window(tag="primary wind"):
            #-----création d'une bare de menu-----
            with dpg.menu_bar(tag="nav bar 1"):
                dpg.add_menu_item(label="Plus d'information", callback=self.Link, user_data="https://okaroxgames42.wixsite.com/okarox/cv-tech")
                dpg.add_menu_item(label="Aide", callback=self.Link, user_data="https://okaroxgames42.wixsite.com/okarox")
                dpg.add_menu_item(label="Information personneles", callback=self.InformationPersonneles, user_data=False)
                
                with dpg.menu(label="Paramètre"):
                    with dpg.menu(label="Paramètre 1"):
                        dpg.add_menu_item(label="Paramètre 1.1", check=True)
                        dpg.add_menu_item(label="Paramètre 1.2")
                    with dpg.menu(label="Paramètre 2"):
                        dpg.add_menu_item(label="Paramètre 2.1", check=True)
                        dpg.add_menu_item(label="Paramètre 2.2")


            #-----création du menu de gauche-----
            with dpg.window(tag="windfils", label="Dossiers", no_resize=True, height=dpg.get_viewport_width()/2-20, width=dpg.get_viewport_width()*0.2, pos=(0,20), no_move=True, no_close=True, no_collapse=True):
                self.CountTable()
            with dpg.window(tag="windinformation", label="Informations", no_resize=True, height=dpg.get_viewport_width()/2, width=dpg.get_viewport_width()*0.2, pos=(0,dpg.get_viewport_width()/2), no_move=True, no_close=True, no_collapse=True):
                pass
            #-----création du menu de droite (fenêtre central")-----
            with dpg.window(tag="windinformationall", label="Informations générales", no_resize=True, height=200, width=dpg.get_viewport_width()*0.8, pos=(dpg.get_viewport_width()*0.2,20), no_move=True, no_close=True, no_collapse=True, no_scrollbar=True):
                pass
        
        if where == 1:
            self.InformationPersonneles(sender="sender", app_data="app_data", user_data=True)
        if where == 2:
            print("Une nouvelle version du logiciel est disponible.")
            with dpg.window(modal=True, no_resize=True, no_close=True):
                dpg.add_text(default_value="Une nouvelle version du logiciel doit être installer.\nCette dernière est obligatoire au bon fonctionnement du logiciel.\nMerci de l'installer en cliquant sur le boutton ci-dessous.")
                dpg.add_button(label="Mettre à jour le logiciel.", callback=self.UpdateLogiciel, user_data=1)
        if where == 3:
            with dpg.window(modal=True, no_resize=True, no_close=True):
                dpg.add_text(default_value="Une nouvelle version du driver doit être installer.\nCette dernière est obligatoire au bon fonctionnement du logiciel.\nMerci de l'installer en cliquant sur le boutton ci-dessous.")
                dpg.add_button(label="Mettre à jour le logiciel.", callback=self.UpdateLogiciel, user_data=2)
        dpg.set_primary_window("primary wind",value=True)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
    #-----fonction pour la modification des tailles des fenêtres-----
    def Size_Window(self, sender, app_data):
        #gauche haut
        if dpg.does_item_exist("windfils"):
            dpg.set_item_pos("windfils", (0,20))
            dpg.set_item_width("windfils", dpg.get_viewport_width()*0.2)
            dpg.set_item_height("windfils", dpg.get_viewport_height()/2-20)
        #gauche bas
        if dpg.does_item_exist("windinformation"):
            dpg.set_item_pos("windinformation", (0,dpg.get_viewport_height()/2))
            dpg.set_item_width("windinformation", dpg.get_viewport_width()*0.2)
            dpg.set_item_height("windinformation", dpg.get_viewport_height()/2)
        #mid
        if dpg.does_item_exist("windinformationall"):
            dpg.set_item_pos("windinformationall", (dpg.get_viewport_width()*0.2,20))
            dpg.set_item_width("windinformationall", dpg.get_viewport_width()*0.8)
            if self.current_table in ["btn more contact 0","btn more contact 1","btn more contact 2"]:
                dpg.set_item_height("windinformationall", dpg.get_viewport_height()-60)
                if dpg.does_item_exist("Table main"):
                    dpg.set_item_width("Table main", dpg.get_viewport_width()*0.8-40)
                    dpg.set_item_height("Table main", dpg.get_viewport_height()-110)
            else:
                dpg.set_item_height("windinformationall", dpg.get_viewport_height()-20)
                if dpg.does_item_exist("Table main"):
                    dpg.set_item_width("Table main", dpg.get_viewport_width()*0.8-40)
                    dpg.set_item_height("Table main", dpg.get_viewport_height()-90)    
    #-----récupération des informations sur les tables de la base de donnés-----
    def CountTable(self):
        connection = sqlite3.connect(self.path)
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table';")
            #result = cursor.fetchone()[0]
            tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        except Exception as e:
            print("Une erreur s'est produite : ", e)
        finally:
            cursor.close()
            connection.close()
            tables.pop(tables.index(('sqlite_sequence',)))
            tables.pop(tables.index(('CompanyInfo',)))
            
            dpg.add_button(tag="AddTable", label="Ajouter une table", callback=self.AddTable, parent="windfils")
            if dpg.does_item_exist("TableMangerFils"):
                dpg.delete_item("TableMangerFils")
            with dpg.table(parent="windfils", tag="TableMangerFils", header_row=True, policy=dpg.mvTable_SizingFixedFit, reorderable=True,
                    resizable=True, no_host_extendX=False, hideable=True,
                    borders_innerV=True, delay_search=True, borders_outerV=True, borders_innerH=True,
                    borders_outerH=True, scrollX=True, scrollY=True):
                dpg.add_table_column(tag="LeftPartFilsManager")
                dpg.add_table_column(tag="RightPartFilsManager")
                for i in tables:
                    with dpg.table_row(tag=f"row {i[0]}"):
                        dpg.add_button(tag=f"btn {i[0]}", label=f"{i[0]}.tb", callback=self.ShowTable)
                        dpg.add_button(tag=f"suppr {i[0]}", label=f"supprimer", callback=self.DeleteFile, user_data=f"{i[0]}")

    def AddTable(self):
        if dpg.does_item_exist("WindowCreateTable"):
            dpg.delete_item("WindowCreateTable")
        with dpg.window(tag="WindowCreateTable", label="Fenêtre d'ajout d'une table", no_collapse=True, modal=True, width=200, height=125):
            dpg.add_text(tag="TextAddTable",default_value="Nom de la table")
            dpg.add_input_text(tag="NameNewTable", default_value="")
            dpg.add_text(tag="ErrorMessageCreationTable", default_value="")
            dpg.add_button(label="Créer la nouvelle table", callback=self.CreateNewTable)
        
    def CreateNewTable(self, sender, app_data):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        name = "_".join(dpg.get_value('NameNewTable').split(" "))
        if (f"{name}",) not in tables and len(name) != 0:
            try:
                # Créer un curseur
                cursor = connection.cursor()
                
                # Créer une table
                sql = f"CREATE TABLE {name} (id INTEGER PRIMARY KEY, Prenom TEXT, Nom TEXT, LienCompte TEXT, Email TEXT, NomEmploiActuel TEXT, NomEntrepriseActuel TEXT, DuréeEntrepriseActuel TEXT, LieuEntrepriseActuel TEXT, LienCompanyActuel TEXT, SiteCompanyActuel TEXT, SecteurCompanyActuel TEXT, TailleEntrepriseActuel, NomEmploiAncien1 TEXT, NomEntrepriseAncien1 TEXT, DuréeEntrepriseAncien1 TEXT, LieuEntrepriseAncien1 TEXT, LienCompanyAncie1 TEXT, SiteCompanyAncien1 TEXT, SecteurCompanyAncien1 TEXT, TailleEntrepriseAncien1 TEXT, NomEmploiAncien2 TEXT, NomEntrepriseAncien2 TEXT, DuréeEntrepriseAncien2 TEXT, LieuEntrepriseAncien2 TEXT, LienCompanyAncien2 TEXT, SiteCompanyAncien2 TEXT, SecteurCompanyAncien2 TEXT, TailleEntrepriseAncien2 TEXT)"
                cursor.execute(sql)

                dpg.delete_item("AddTable")
                dpg.delete_item("TableMangerFils")
                self.CountTable()

            except Exception as e:
                print("Une erreur s'est produite CreateNewTable : ", e)
            finally:
                # Valider les modifications et fermer la connexion
                connection.commit()
                cursor.close()
                connection.close()
                dpg.delete_item("WindowCreateTable")
        else:
            dpg.set_value("ErrorMessageCreationTable", "Nom incorrect")

    def ShowTable(self, sender, app_data):
        if self.can_open_table:
            self.can_open_table = False
            n = str(sender).split(" ")
            self.name_table = n[1]
            self.data = self.GetTable(self.path, self.name_table)

            dpg.set_item_label("windinformation", f"Information {n[1]}")
            dpg.add_button(parent="windinformation", tag="btn close", label=f"Fermer le dossier {n[1]}", callback=self.CloseFils)
            dpg.add_button(parent="windinformation", tag="contact", label="Informations générales", callback=self.ShowMoreJob)
            dpg.add_button(parent="windinformation", tag="btn more contact 0", label="Emploi actuel", callback=self.ShowMoreJob)
            dpg.add_button(parent="windinformation", tag="btn more contact 1", label="Emploi passé 1", callback=self.ShowMoreJob)
            dpg.add_button(parent="windinformation", tag="btn more contact 2", label="Emploi passé 2", callback=self.ShowMoreJob)
            dpg.add_button(parent="windinformation", tag="add contact table", label="Télécharger via Excel", callback=self.UploadDataTable)
            dpg.add_button(parent="windinformation", tag="add contact search", label="Télécharger via une recherche", callback=self.callback)
            dpg.add_button(parent="windinformation", tag="add manual", label="Ajouter des contacts manuellement", callback=self.UploadDataManual)
            self.TableInformationAll()

    def GetTable(self, path, name_table):
        data = []
        try:
            connection = sqlite3.connect(path)
            cursor = connection.cursor()
            data = cursor.execute(f"SELECT * FROM {name_table}").fetchall()
        except Exception as e:
            print("Une erreur s'est produite GetTable : ", e)
        finally:
            cursor.close()
            connection.close()
            return data

    def TableInformationAll(self):
        if self.current_table != "TableInformatioAll":
            dpg.delete_item("Table main")
            dpg.delete_item("menu_bar_analyse")
            self.current_table = "TableInformationAll"
            nom_col = ["", "Prenom", "Nom", "Lien Compte", "Email", "Nom Emploi Actuel", "Nom Entreprise Actuel", "Nom Emploi Ancien 1", "Nom Emploi Ancien 2"]
            with dpg.table(parent="windinformationall", tag="Table main", header_row=True, policy=dpg.mvTable_SizingFixedFit, reorderable=True,
                    resizable=True, no_host_extendX=False, hideable=True,
                    borders_innerV=True, delay_search=True, borders_outerV=True, borders_innerH=True,
                    borders_outerH=True, scrollX=True, scrollY=True, height=dpg.get_viewport_height()-90,width=dpg.get_viewport_width()*0.8-40):
                for i in nom_col:
                    dpg.add_table_column(tag=f"col_{i}",label=i, width_fixed=True, no_resize=True)
                
                for i in range(len(self.data)):
                    self.data_change.append([])
                    self.data_now.append([])
                    for n in self.data[i]:
                        self.data_now[i].append(n)
                    with dpg.table_row(tag=self.data[i][0]):
                        dpg.add_button(label="Supprimer", width=len("Supprimer")*8, user_data=self.data[i][0], callback=self.DeleteRow) 
                        dpg.add_input_text(tag=f"1_{i}", default_value=self.data[i][1], user_data="Prenom", width=40*8, callback=self.GetChangeInformation)
                        dpg.add_input_text(tag=f"2_{i}", default_value=self.data[i][2], user_data="Nom", width=40*8, callback=self.GetChangeInformation)
                        dpg.add_button(label="Lien Linkedin", width=len("Lien Linkedin")*8, user_data=self.data[i][3], callback=self.Link)
                        dpg.add_input_text(tag=f"4_{i}", default_value=self.data[i][4], user_data="Email", width=40*8, callback=self.GetChangeInformation)
                        dpg.add_input_text(tag=f"5_{i}", default_value=self.data[i][5], user_data="NomEmploiActuel", width=40*8, callback=self.GetChangeInformation)
                        dpg.add_input_text(tag=f"6_{i}", default_value=self.data[i][6], user_data="NomEntrepriseActuel", width=40*8, callback=self.GetChangeInformation)
                        dpg.add_input_text(tag=f"9_{i}", default_value=self.data[i][13], user_data="NomEmploiAncienne1", width=40*8, callback=self.GetChangeInformation)
                        dpg.add_input_text(tag=f"13_{i}", default_value=self.data[i][21], user_data="NomEmploiAncienne2", width=40*8, callback=self.GetChangeInformation)

    def TableInformationMore(self, tipe, page):
        if self.current_table != tipe:
            dpg.delete_item("Table main")
            dpg.delete_item("menu_bar_analyse")
            self.current_table = tipe
            facteur = 0
            if page == 1:
                facteur = 8
            elif page == 2:
                facteur = 16
            nom_col = ["","Prenom", "Nom","Lien Compte", "Email", "Nom Emploi Actuel", "Nom Entreprise Actuel", "Durée Entreprise Actuel", "Lieu Entreprise Actuel", "Lien Entreprise Actuel", "Site Entreprise Actuel", "Secteur Entreprise Actuel", "Taille Entreprise Actuel", "Nom Emploi Ancien 1", "Nom Entreprise Ancien 1", "Durée Entreprise Ancien 1", "Lieu Entreprise Ancien 1", "Lien Entreprise Ancien 1", "Site Entreprise Ancien 1", "Secteur Entreprise Ancien 1", "Taille Entreprise Ancien 1", "Nom Emploi Ancien 2", "Nom Entreprise Ancien 2", "Durée Entreprise Ancien 2", "Lieu Entreprise Ancien 2", "Lien Entreprise Ancien 2", "Site Entreprise Ancien 2", "Secteur Entreprise Ancien 2", "Taille Entreprise Ancien 2"]
            with dpg.menu_bar(tag="menu_bar_analyse", parent="windinformationall"):
                with dpg.menu(label="Analytique"):
                    dpg.add_menu_item(tag="Analyse_taille_entreprise", label="Taille d'entreprise", callback=self.InformationAnalytiqueGraphique, user_data=nom_col[12+facteur])
                    dpg.add_menu_item(tag="Analyse_secteurs", label="Secteurs", callback=self.InformationAnalytiqueGraphique, user_data=nom_col[11+facteur])
                    dpg.add_menu_item(tag="Analyse_evolution", label="Evolution", callback=self.EvolutionPersonneTable)
            with dpg.table(parent="windinformationall", tag="Table main", header_row=True, policy=dpg.mvTable_SizingFixedFit, reorderable=True,
                    resizable=True, no_host_extendX=False, hideable=True,
                    borders_innerV=True, delay_search=True, borders_outerV=True, borders_innerH=True,
                    borders_outerH=True, scrollX=True, scrollY=True, height=dpg.get_viewport_height()-105,width=dpg.get_viewport_width()*0.8-40):
                
                dpg.add_table_column(tag=f"col_{nom_col[0]}",label=nom_col[0], width_fixed=True, no_resize=True)
                dpg.add_table_column(tag=f"col_{nom_col[1]}",label=nom_col[1], width_fixed=True, no_resize=True)
                dpg.add_table_column(tag=f"col_{nom_col[2]}",label=nom_col[2], width_fixed=True, no_resize=True)
                dpg.add_table_column(tag=f"col_{nom_col[3]}",label=nom_col[3], width_fixed=True, no_resize=True)
                dpg.add_table_column(tag=f"col_{nom_col[5+facteur]}",label=nom_col[5+facteur], width_fixed=True, no_resize=True)
                dpg.add_table_column(tag=f"col_{nom_col[6+facteur]}",label=nom_col[6+facteur], width_fixed=True, no_resize=True)
                dpg.add_table_column(tag=f"col_{nom_col[7+facteur]}",label=nom_col[7+facteur], width_fixed=True, no_resize=True)
                dpg.add_table_column(tag=f"col_{nom_col[8+facteur]}",label=nom_col[8+facteur], width_fixed=True, no_resize=True)
                dpg.add_table_column(tag=f"col_{nom_col[9+facteur]}",label=nom_col[9+facteur], width_fixed=True, no_resize=True)
                dpg.add_table_column(tag=f"col_{nom_col[10+facteur]}",label=nom_col[10+facteur], width_fixed=True, no_resize=True)
                dpg.add_table_column(tag=f"col_{nom_col[11+facteur]}",label=nom_col[11+facteur], width_fixed=True, no_resize=True)
                dpg.add_table_column(tag=f"col_{nom_col[12+facteur]}",label=nom_col[12+facteur], width_fixed=True, no_resize=True)
                
                for i in range(len(self.data)):
                    with dpg.table_row(tag=self.data[i][0]):
                        dpg.add_button(tag=f"0_{i}", label="Supprimer", width=len("Supprimer")*8, user_data=self.data[i][0], callback=self.DeleteRow) 
                        dpg.add_input_text(tag=f"1_{i}", default_value=self.data[i][1], user_data="Prenom", width=40*8, callback=self.GetChangeInformation)
                        dpg.add_input_text(tag=f"2_{i}", default_value=self.data[i][2], user_data="Nom", width=40*8, callback=self.GetChangeInformation)
                        dpg.add_button(label="Lien Linkedin", width=len("Lien Linkedin")*8, user_data=self.data[i][3], callback=self.Link)
                        dpg.add_input_text(tag=f"{5+facteur}_{i}", default_value=self.data[i][5+facteur], user_data=nom_col[5+facteur], width=40*8, callback=self.GetChangeInformation)
                        dpg.add_input_text(tag=f"{6+facteur}_{i}", default_value=self.data[i][6+facteur], user_data=nom_col[6+facteur], width=40*8, callback=self.GetChangeInformation)
                        dpg.add_input_text(tag=f"{7+facteur}_{i}", default_value=self.data[i][7+facteur], user_data=nom_col[7+facteur], width=40*8, callback=self.GetChangeInformation)
                        dpg.add_input_text(tag=f"{8+facteur}_{i}", default_value=self.data[i][8+facteur], user_data=nom_col[8+facteur], width=40*8, callback=self.GetChangeInformation)
                        dpg.add_button(label="Lien Linkedin", width=len(nom_col[9+facteur])*8, user_data=self.data[i][9+facteur], callback=self.Link)
                        dpg.add_button(label="Lien du site web", width=len(nom_col[10+facteur])*8, user_data=self.data[i][10+facteur], callback=self.Link)
                        dpg.add_input_text(tag=f"{11+facteur}_{i}", default_value=self.data[i][11+facteur], user_data=nom_col[11+facteur], width=40*8, callback=self.GetChangeInformation)
                        dpg.add_input_text(tag=f"{12+facteur}_{i}", default_value=self.data[i][12+facteur], user_data=nom_col[12+facteur], width=40*8, callback=self.GetChangeInformation)

    def TableByExcelTable(self, path, is_headless):
        try:
            connection = sqlite3.connect(self.path)
            cursor = connection.cursor()
            scraper_linkedin_mine = Scraper.Scraper_Linkedin(is_headless)
            if scraper_linkedin_mine.Login(self.GetsIDConnection()):
                for y in range(len(path)):
                    link = cursor.execute(f"SELECT * FROM {self.name_table} WHERE LienCompte = ?", (path[y][2],)).fetchall()
                    if len(link) == 0 and "https://www.linkedin.com/in/" in path[y][2]:
                        print(f"Ok c'est bon pour {path[y]}")
                        """try:
                            result = scraper_linkedin_mine.Process_experience(path[y][2])
                            if result != None:
                                emploi_passe = result[0]
                                like_passe = result[1]
                                new_information = (path[y][0], path[y][1], path[y][2], path[y][3], emploi_passe[0][0], emploi_passe[0][1], emploi_passe[0][2], emploi_passe[0][3], like_passe[0][0], like_passe[0][1], like_passe[0][2], like_passe[0][3], emploi_passe[1][0], emploi_passe[1][1], emploi_passe[1][2], emploi_passe[1][3], like_passe[1][0], like_passe[1][1], like_passe[1][2], like_passe[1][3], emploi_passe[2][0], emploi_passe[2][1], emploi_passe[2][2], emploi_passe[2][3], like_passe[2][0], like_passe[2][1], like_passe[2][2], like_passe[2][3],)
                                cursor.execute(f"INSERT INTO {self.name_table} (Prenom, Nom, LienCompte, Email, NomEmploiActuel, NomEntrepriseActuel, DuréeEntrepriseActuel, LieuEntrepriseActuel, LienCompanyActuel, SiteCompanyActuel, SecteurCompanyActuel, TailleEntrepriseActuel, NomEmploiAncien1, NomEntrepriseAncien1, DuréeEntrepriseAncien1, LieuEntrepriseAncien1, LienCompanyAncien1, SiteCompanyAncien1, SecteurCompanyAncien1, TailleEntrepriseAncien1, NomEmploiAncien2, NomEntrepriseAncien2, DuréeEntrepriseAncien2, LieuEntrepriseAncien2, LienCompanyAncien2 , SiteCompanyAncien2, SecteurCompanyAncien2 , TailleEntrepriseAncien2) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", new_information)
                                connection.commit()
                        except Exception as e:
                            print("Une erreur s'est produite TableByExcelTable get Linkedin : ", e)"""
            
        except Exception as e:
            print("Une erreur s'est produite TableByExcelTable fdsfsf : ", str(e))
            if """Message: no such element: Unable to locate element: {"method":"css selector","selector":"[id="remember-me-prompt__form-primary"]"}""" in str(e):
                print("loooakduqsdyqxgzexhughsxdisxfhsd")
            if dpg.does_item_exist("window_erreur_analyse_profil"):
                dpg.delete_item("window_erreur_analyse_profil")
            with dpg.window(tag="window_erreur_analyse_profil", modal=True):
                dpg.add_text(default_value="Une erreur s'est produite.\nMerci de vérifier vos identifiants Linkedin\nou votre connexion internet.")
        finally:
            cursor.close()
            connection.close()
            self.current_table = ""
            self.data = self.GetTable(self.path, self.name_table)
            self.TableInformationAll()

    def DeleteRow(self, sender, app_data, user_data):
        if dpg.does_item_exist("wind_delete_file"):
            dpg.delete_item("wind_delete_file")
        with dpg.window(tag="wind_delete_file", modal=True):
            dpg.add_text(default_value="Etes-vous sûre de vouloir supprimer cette table ?")
            dpg.add_button(label="Accepter", callback=self.DeleteRowProcess, user_data=user_data)
    
    def DeleteRowProcess(self, sender, app_data, user_data):
        dpg.delete_item("wind_delete_file")
        if user_data == "Delete_Just":
            dpg.delete_item(f"{sender.split('_')[1]}_row_manual")
        else:
            try:
                connection = sqlite3.connect(self.path)
                cursor = connection.cursor()
                data = cursor.execute(f"SELECT id FROM {self.name_table}").fetchall()
                
                cursor.execute(f"DELETE from {self.name_table} where id=?", (str(user_data),))
                dpg.delete_item(user_data)

            except Exception as e:
                print("Une erreur s'est produite del_info_more_job: ", e)
            finally:
                # Valider les modifications et fermer la connexion
                connection.commit()
                cursor.close()
                connection.close()

    def Link(self, sender, app_data, user_data):
        if sender == "btn_acheter_abonnement":
            dpg.show_item("window_information_personnel")
        webbrowser.open(user_data)
    
    def CloseFils(self, sender, app_data):
        dpg.set_item_label("windinformation", "")
        dpg.delete_item("menu_bar_info_all")
        dpg.delete_item("btn close")
        dpg.delete_item("btn more contact 0")
        dpg.delete_item("btn more contact 1")
        dpg.delete_item("btn more contact 2")
        dpg.delete_item("add contact table")
        dpg.delete_item("add contact search")
        dpg.delete_item("add manual")
        dpg.delete_item("Delete")
        dpg.delete_item("Table main")
        dpg.delete_item("contact")
        self.can_open_table = True
        self.Uptade()
        self.data_change = []

    def GetChangeInformation(self, sender, app_data):
        pos = str(sender).split("_")
        row = self.data_change[int(pos[1])]
        lol = str(dpg.get_value(sender))
        self.data_now[int(pos[1])][int(pos[0])] = lol
        if sender not in self.data_change[int(pos[1])]:
            self.data_change[int(pos[1])].append(sender)

    def Uptade(self):
        try:
            connection = sqlite3.connect(self.path)
            cursor = connection.cursor()
            nb_pop = 0
            data = cursor.execute(f"SELECT id FROM {self.name_table}").fetchall()
            nom_col = ["id", "Prenom", "Nom", "LienCompte", "Email", "NomEmploiActuel", "NomEntrepriseActuel", "DuréeEntrepriseActuel", "LieuEntrepriseActuel", "LienCompanyActuel", "SiteCompanyActuel", "SecteurCompanyActuel", "TailleEntrepriseActuel", "NomEmploiAncienne1", "NomEntrepriseAncienne1", "DuréeEntrepriseAncienne1", "LieuEntrepriseAncienne1", "LienCompanyAncienne1", "SiteCompanyAncienne1", "SecteurCompanyAncienne1", "TailleEntrepriseAncienne1", "NomEmploiAncienne2", "NomEntrepriseAncienne2", "DuréeEntrepriseAncienne2", "LieuEntrepriseAncienne2", "LienCompanyAncienne2", "SiteCompanyAncienne2", "SecteurCompanyAncienne2", "TailleEntrepriseAncienne2"]
            for i in range(len(self.data_change)):
                tuple_valu = []
                if len(self.data_change[i]) > 0:
                    for ii in range(len(self.data_change[i])):
                        pos = str(self.data_change[i][ii]).split("_")
                        tuple_valu.append([nom_col[int(pos[0])], self.data_now[int(pos[1])][int(pos[0])]])
                    resp = self.TxtUptade(tuple_valu, len(tuple_valu),self.data_now[i][0])
                    cursor.execute(resp[0], resp[1])
                    connection.commit()

        except Exception as e:
            print("Une erreur s'est produite Uptade test : ", e)
        finally:
            # Valider les modifications et fermer la connexion
            cursor.close()
            connection.close()

    def TxtUptade(self, val, size, col):
        if size == 1: return [f"""Update {self.name_table} set {val[0][0]} = ? where id = ?""", [val[0][1], col]]
        elif size == 2: return [f"""Update {self.name_table} set {val[0][0]} = ?, {val[1][0]} = ? where id = ?""", [val[0][1], val[1][1], col]]
        elif size == 3: return [f"""Update {self.name_table} set {val[0][0]} = ?, {val[1][0]} = ?, {val[2][0]} = ? where id = ?""", [val[0][1], val[1][1], val[2][1], col]]
        elif size == 4: return [f"""Update {self.name_table} set {val[0][0]} = ?, {val[1][0]} = ?, {val[2][0]} = ?, {val[3][0]} = ? where id = ?""", [val[0][1], val[1][1], val[2][1], val[3][1], col]]
        elif size == 5: return [f"""Update {self.name_table} set {val[0][0]} = ?, {val[1][0]} = ?, {val[2][0]} = ?, {val[3][0]} = ?, {val[4][0]} = ? where id = ?""", [val[0][1], val[1][1], val[2][1], val[3][1], val[4][1], col]]
        elif size == 6: return [f"""Update {self.name_table} set {val[0][0]} = ?, {val[1][0]} = ?, {val[2][0]} = ?, {val[3][0]} = ?, {val[4][0]} = ?, {val[5][0]} = ? where id = ?""", [val[0][1], val[1][1], val[2][1], val[3][1], val[4][1], val[5][1], col]]
        elif size == 7: return [f"""Update {self.name_table} set {val[0][0]} = ?, {val[1][0]} = ?, {val[2][0]} = ?, {val[3][0]} = ?, {val[4][0]} = ?, {val[5][0]} = ?, {val[6][0]} = ? where id = ?""", [val[0][1], val[1][1], val[2][1], val[3][1], val[4][1], val[5][1], val[6][1], col]]

    def ShowMoreJob(self, sender, app_data):
        if sender == "contact": self.TableInformationAll()
        elif sender == "btn more contact 0": self.TableInformationMore(str(sender), 0)
        elif sender == "btn more contact 1": self.TableInformationMore(str(sender), 1)
        elif sender == "btn more contact 2": self.TableInformationMore(str(sender), 2)
    
    def SelectInformationsAddContactExcel(self, sender, app_data:dict, user_data):
        dpg.delete_item("file_dialog_id")
        time.sleep(0.05)
        if dpg.does_item_exist("WindowSelectInformationsAddContactExcel"):
            dpg.delete_item("WindowSelectInformationsAddContactExcel")
        if dpg.does_item_exist("registry_value_format_or_not"):
            dpg.delete_item("registry_value_format_or_not")
        with dpg.value_registry(tag="registry_value_format_or_not"):
            dpg.add_bool_value(default_value=False, tag="bool_value_format", parent="registry_value_format_or_not")
            dpg.add_bool_value(default_value=True, tag="bool_value_headless", parent="registry_value_format_or_not")
        with dpg.window(tag="WindowSelectInformationsAddContactExcel", label="Fenêtre de séléction des informations", no_collapse=True, modal=True):
            dpg.add_checkbox(tag="est_format", source="bool_value_format", label="Votre fichier est-il formaté")
            dpg.add_checkbox(tag="est_headless", source="bool_value_headless", label="Voulez-vous cacher l'exécution ?")
            dpg.add_text(tag="TextSelectionAttriute",default_value="Renseignez les mots clés des emplois que vous recherchez")
            dpg.add_input_text(tag="InputAttribut")
            dpg.add_button(label="Créer la nouvelle table", callback=self.callback, user_data=app_data)

    def callback(self, sender, app_data:dict, user_data):
        try:
            dataframe = None
            ext = ""
            files_name = []
            key_word = dpg.get_value("InputAttribut").split(" ")
            is_format = dpg.get_value("bool_value_format")
            is_headless = dpg.get_value("bool_value_headless")

            dpg.delete_item("WindowSelectInformationsAddContactExcel")
            dpg.delete_item("registry_value_format_or_not")

            for i in user_data["selections"].keys():
                files_name.append(i)
            ext = "."+str(files_name[0].split(".")[-1])
            if ext == ".xlsx":
                dataframe = pd.read_excel(str(user_data["current_path"])+f"\{files_name[0]}")
            dpg.delete_item("file_dialog_id")
            lst_end = []
            if not is_format:
                for i in dataframe.iloc:
                    inter = str(i[0]).split(",")
                    if len(inter) > 5:
                        for ii in key_word:
                            if ii in inter[5]:
                                lst_end.append([inter[0], inter[1], inter[2], inter[3]])
                                break
            else:
                for i in range(1, dataframe.shape[0]):
                    if len(dataframe.iloc[i]) > 3:
                        lst_end.append([dataframe.iloc[i][0], dataframe.iloc[i][1], dataframe.iloc[i][2], dataframe.iloc[i][3]])
                    elif len(dataframe.iloc[i]) == 3:
                        lst_end.append([dataframe.iloc[i][0], dataframe.iloc[i][1], dataframe.iloc[i][2], "Nane"])
                    elif len(dataframe.iloc[i]) == 2:
                        lst_end.append([dataframe.iloc[i][0], dataframe.iloc[i][1], "Nane", "Nane"])
                    elif len(dataframe.iloc[i]) == 1:
                        lst_end.append([dataframe.iloc[i][0], "Nane", "Nane", "Nane"])
            self.TableByExcelTable(lst_end, is_headless)
        except Exception as e:
            print("Une erreur s'est produite Dowload : ", e)

    def GetSizeCompany(self, column_name:str):
        data = ["Nane"]
        print("column_name : ", column_name)
        column_name = "".join(column_name.split(" "))
        print("column_name : ", column_name)
        try:
            connection = sqlite3.connect(self.path)
            cursor = connection.cursor()
            data = cursor.execute(f"SELECT {column_name} FROM {self.name_table}").fetchall()
        except Exception as e:
            print("GetSizeCompany : ", e)
        finally:
            cursor.close()
            connection.close()
            return data

    def GetallQuantityMin(self, data, lst_inter_val=[], lst_inter_quantity=[]):
        lst_val:list = lst_inter_val
        lst_val_quantity = lst_inter_quantity
        for i in range(len(data)):
            inter = []
            if data[i][0] in lst_val:
                print(lst_val.index(data[i][0]))
                lst_val_quantity[lst_val.index(data[i][0])] += 1
            else:
                lst_val.append(data[i][0])
                lst_val_quantity.append(1)
        
        
        if lst_inter_val == ["0-1 employés", "2-10 employés", "11-50 employés", "51-200 employés", "201-500 employés", "501-1\u202f000 employés", "1\u202f001-5\u202f000 employés", "5\u202f001-10\u202f000 employés", "10\u202f001 employés et plus", "Nane"]:
            lst_val = ["0 - 1 employés", "2 - 10 employés", "11 - 50 employés", "51 - 200 employés", "201 - 500 employés", "501 - 1 000 employés", "1 001 - 5 000 employés", "5 001 - 10 000 employés", "10 001 employés et plus", "Nane"]

        return [lst_val, lst_val_quantity]

    def FindInformationLink(self, lst:list, info):
        return lst.index(info)

    def MaxValueLst(self, lst):
        value = 0
        for i in lst:
            if i > value:
                value = i
        return value + 3

    def InformationAnalytiqueGraphique(self, sender, app_data, user_data):
        number = 0
        data = None
        taille_entrepise = ["0-1 employés", "2-10 employés", "11-50 employés", "51-200 employés", "201-500 employés", "501-1\u202f000 employés", "1\u202f001-5\u202f000 employés", "5\u202f001-10\u202f000 employés", "10\u202f001 employés et plus", "Nane"]
        data = self.GetSizeCompany(user_data)

        if sender == "Analyse_taille_entreprise":
            print("ok")
            data = self.GetallQuantityMin(data, taille_entrepise, [0,0,0,0,0,0,0,0,0,0])
        else:
            data = self.GetallQuantityMin(data)
        time.sleep(0.05)
        if dpg.does_item_exist("Wind info graphique"):
            dpg.delete_item("Wind info graphique")
        with dpg.window(tag="Wind info graphique", label="Analytique", height=dpg.get_viewport_height()-50, width=dpg.get_viewport_width()-40, pos=(10,20), modal=True):

            with dpg.plot(label=user_data, height=-1, width=-1, no_mouse_pos=True):
                dpg.add_plot_axis(dpg.mvXAxis, no_gridlines=True, tag="x_axis", no_tick_marks=True, no_tick_labels=True)

                dpg.add_plot_legend(outside=True)

                # create y axis
                dpg.add_plot_axis(dpg.mvYAxis, label="Score", tag="y_axis")
                dpg.set_axis_limits("y_axis", 0, self.MaxValueLst(data[1]))
                for i in range(len(data[0])):
                    dpg.add_bar_series([i*200], [data[1][i]], weight=100, parent="y_axis", label=data[0][i])

    def EvolutionPersonneTable(self):
        print("Evolution nombre de profils dans la table")

    def UploadDataTable(self, sender, app_data):
        data = self.GetTable(self.GetPath(["bd", "Information.db"]), "IdentifiantConnexion")[0]
        result = self.CanConnect(data[3])
        print("result first : ", result)
        if result == 200:
            if dpg.does_item_exist("file_dialog_id"):
                dpg.delete_item("file_dialog_id")
            with dpg.file_dialog(directory_selector=False, show=True, callback=self.SelectInformationsAddContactExcel, tag="file_dialog_id", width=700 ,height=400, modal=True):
                dpg.add_file_extension(".xlsx", color=(0, 255, 0, 255), custom_text="[Excel]")
        elif result == 404:
            if dpg.does_item_exist("wind_connexion_internet_requise"):
                dpg.delete_item("wind_connexion_internet_requise")
            with dpg.window(tag="wind_connexion_internet_requise", modal=True):
                dpg.add_text(default_value="Merci de vous connecter à internet afin de pouvoir utiliser cette fonctionnalité")
        elif result == 403:
            self.InformationPersonneles(sender="sender", app_data="app_data", user_data=True)
    
    def UploadDataSearch(self, sender, app_data):
        print("UploadDataSearch : ",sender)
    
    def UploadDataManual(self, sender, app_data):
        if dpg.does_item_exist("get_number_value_append_manual"):
            dpg.delete_item("get_number_value_append_manual")
        with dpg.window(tag="get_number_value_append_manual", modal=True):
            dpg.add_text(default_value="Choisissez le nombre de profils à ajouter")
            dpg.add_input_int(tag="number_row_manual", default_value=1, min_value=1, max_value=100)
            dpg.add_button(label="Accepter",callback=self.TableUploadData)
    
    def TableUploadData(self, sender, app_data):
        nb_row = dpg.get_value("number_row_manual")
        dpg.delete_item("get_number_value_append_manual")
        time.sleep(0.1)
        if dpg.does_item_exist("wind_append_info_manual"):
            dpg.delete_item("wind_append_info_manual")
        time.sleep(0.05)
        if dpg.does_item_exist("registry_value_format_or_not"):
            dpg.delete_item("registry_value_format_or_not")
        with dpg.window(tag="wind_append_info_manual", modal=True):
            with dpg.value_registry(tag="registry_value_format_or_not"):
                dpg.add_bool_value(default_value=True, tag="bool_value_headless", parent="registry_value_format_or_not")
            with dpg.menu_bar(tag="menu_bar_start_append_manual", parent="wind_append_info_manual"):
                dpg.add_menu_item(tag="start_append_manual", label="Lancer l'analyse", callback=self.StartAnalyseInformation, user_data=nb_row)
                with dpg.menu(label="Paramètre"):
                    dpg.add_checkbox(tag="est_headless", source="bool_value_headless", label="Voulez-vous cacher l'exécution ?")
            with dpg.table(tag="table_append_profil_manual", header_row=True, policy=dpg.mvTable_SizingFixedFit, reorderable=True,
                    resizable=True, no_host_extendX=False, hideable=True,
                    borders_innerV=True, delay_search=True, borders_outerV=True, borders_innerH=True,
                    borders_outerH=True, scrollX=True, scrollY=True, height=dpg.get_viewport_height()-105,width=dpg.get_viewport_width()*0.8-40):
                
                dpg.add_table_column(tag=f"col_del_manual",label="Supprimer", width_fixed=True, no_resize=True)
                dpg.add_table_column(tag=f"col_prenom_manual",label="Prénom", width_fixed=True, no_resize=True)
                dpg.add_table_column(tag=f"col_nom_manual",label="Nom", width_fixed=True, no_resize=True)
                dpg.add_table_column(tag=f"col_lien_manual",label="Lien du compte Linkedin", width_fixed=True, no_resize=True)
                for i in range(nb_row):
                    with dpg.table_row(tag=f"{i}_row_manual"):
                        dpg.add_button(tag=f"0_{i}_manual", label="Supprimer", width=len("Supprimer")*8, user_data="Delete_Just", callback=self.DeleteRow) 
                        dpg.add_input_text(tag=f"1_{i}_manual", width=40*8)
                        dpg.add_input_text(tag=f"2_{i}_manual", width=40*8)
                        dpg.add_input_text(tag=f"3_{i}_manual", width=40*8)
    
    def StartAnalyseInformation(self, sender, app_data, user_data):
        data = []
        for i in range(user_data):
            if dpg.does_item_exist(f"1_{i}_manual"):
                data.append([dpg.get_value(f"1_{i}_manual"),dpg.get_value(f"2_{i}_manual"),dpg.get_value(f"3_{i}_manual")])
            else:
                break
        dpg.delete_item("wind_append_info_manual")
        is_headless = dpg.get_value("bool_value_headless")
        dpg.delete_item("wind_append_info_manual")
        dpg.delete_item("registry_value_format_or_not")
        print(data)
        self.TableByExcelTable(data, is_headless)
        print("start analyse")

    def DeleteFile(self, sender, app_data, user_data):
        if dpg.does_item_exist("wind_delete_file"):
            dpg.delete_item("wind_delete_file")
        with dpg.window(tag="wind_delete_file", modal=True):
            dpg.add_text(default_value="Etes-vous sûre de vouloir supprimer cette table ?")
            dpg.add_button(label="Accepter", callback=self.DeleteFileProcess, user_data=user_data)
    
    def DeleteFileProcess(self, sender, app_data, user_data):
        dpg.delete_item("wind_delete_file")
        try:
            connection = sqlite3.connect(self.path)
            cursor = connection.cursor()
            cursor.execute(f"DROP TABLE {user_data}")
            dpg.delete_item(f"row {user_data}")
            if user_data == self.name_table:
                self.CloseFils("","")
        except Exception as e:
            print("Une erreur s'est produite del_info_more_job: ", e)
        finally:
            # Valider les modifications et fermer la connexion
            connection.commit()
            cursor.close()
            connection.close()

    def InformationPersonneles(self, sender, app_data, user_data):
        if dpg.does_item_exist("window_information_personnel"):
            dpg.delete_item("window_information_personnel")
        data = self.GetTable(self.GetPath(["bd", "Information.db"]), "IdentifiantConnexion")[0]
        
        with dpg.window(tag="window_information_personnel", modal=True, no_resize=True, no_close=user_data):
            if user_data:
                with dpg.menu_bar(tag="nav_bar_information_personnel", parent="window_information_personnel"):
                    dpg.add_menu_item(tag="btn_acheter_abonnement",label="Acheter une licence", callback=self.Link, user_data="https://okaroxgames42.wixsite.com/okarox/cv-tech")
                dpg.add_text(tag="Libelé",default_value="Merci de vous connecter à un internet si cela n'est pas encore fait.\nNous devons procéder à une vérification.")
            dpg.add_text(tag="prenom_information_personnel",default_value="Prénom")
            dpg.add_input_text(tag="input_prenom_information_personnel", default_value=data[1])
            dpg.add_text(tag="nom_information_personnel",default_value="Nom")
            dpg.add_input_text(tag="input_nom_information_personnel", default_value=data[2])
            dpg.add_text(tag="email_information_personnel",default_value="Email de connexion")
            dpg.add_input_text(tag="input_email_information_personnel", default_value=data[3])
            dpg.add_text(tag="ErrorEmail",default_value="", show=False)
            dpg.add_text(tag="email_Linkedin_information_personnel",default_value="Email de Linkedin")
            dpg.add_input_text(tag="input_email_Linkedin_information_personnel", default_value=data[4])
            dpg.add_text(tag="Mot_de_passe_Linkedin_information_personnel",default_value="Mot de passe Linkedin")
            dpg.add_input_text(tag="input_Mot_de_passe_Linkedin_information_personnel", default_value=data[5], password=True)
            dpg.add_button(tag="accepter_information_personnel",label="Ajouter les informations d'identification", callback=self.CheckInformationPersonnel, user_data=user_data)
    
    def CheckInformationPersonnel(self, sender, app_data, user_data):
        if user_data:
            result = self.CanConnect(dpg.get_value("input_email_information_personnel"))
            print("result CheckInformationPersonnel : ", result)
            if result == 200:
                print("Cool")
                self.EnregistremetInformationPersonnel()
            if result == 403:
                dpg.set_value('ErrorEmail', "Problème de connexion")
                dpg.show_item('ErrorEmail')
            if result == 404:
                dpg.set_value('ErrorEmail', "Compte non trouvé")
                dpg.show_item('ErrorEmail')
        else:
            self.EnregistremetInformationPersonnel()

    def EnregistremetInformationPersonnel(self):
        try:
            connection = sqlite3.connect(self.GetPath(["bd", "Information.db"]))
            cursor = connection.cursor()
            information = (dpg.get_value("input_prenom_information_personnel"), dpg.get_value("input_nom_information_personnel"), dpg.get_value("input_email_information_personnel"), dpg.get_value("input_email_Linkedin_information_personnel"), dpg.get_value("input_Mot_de_passe_Linkedin_information_personnel"),1,)
            print(information)
            cursor.execute(f"Update IdentifiantConnexion set Prenom = ?, Nom = ?, Email_de_connexion = ?, Email_Linkedin = ?, Mot_de_passe_Linkedin = ? where id = ? ", information)
            connection.commit()
        except Exception as e:
            print("Une erreur s'est produite EnregistremetInformationPersonnel: ", e)
        finally:
            cursor.close()
            connection.close()
            dpg.delete_item("window_information_personnel")
    
    def CanConnect(self, email):
        print(dpg.get_value("input_email_information_personnel"))
        connexion = AccesCV_Tech.AccesCV_Tech(email)
        can_connect = connexion.CanUseSoftware()
        return can_connect

    def GetsIDConnection(self):
        try:
            connection = sqlite3.connect(self.GetPath(["bd", "Information.db"]))
            cursor = connection.cursor()
            data = cursor.execute(f"SELECT Email_Linkedin, Mot_de_passe_Linkedin FROM IdentifiantConnexion").fetchall()
        except Exception as e:
            print("Une erreur s'est produite GetsIDConnection: ", e)
        finally:
            cursor.close()
            connection.close()
            return data[0]

    def GetPath(self, name):
        path_inter:list = list(os.path.abspath("CV_Tech.py").split("\\"))
        path_inter.pop(-1)
        for i in name:
            path_inter.append(i)
        path_inter = "\\".join(path_inter)
        return path_inter

    def UpdateLogiciel(self,sender, app_data, user_data):
        print(end="Update")
        if user_data == 1:
            print(" Logiciel")
        elif user_data == 2:
            print(" driver")
        
