import CV_tech
import AccesCV_Tech
import dearpygui.dearpygui as dpg
import sqlite3
import webbrowser
import time
import os

class ConnexionPage:
    def __init__(self, path) -> None:
        self.path = path
        
        with dpg.window(tag="window_information_personnel", modal=True, no_resize=True):
            with dpg.menu_bar(tag="nav bar 1"):
                dpg.add_menu_item(label="Acheter une licence", callback=self.License)
            dpg.add_text(tag="1",default_value="Prénom")
            dpg.add_input_text(tag="input_prenom")
            dpg.add_text(tag="2",default_value="Nom")
            dpg.add_input_text(tag="input_nom")
            dpg.add_text(tag="3",default_value="Email de connexion")
            dpg.add_input_text(tag="input_email")
            dpg.add_text(tag="5",default_value="", show=False)
            dpg.add_button(tag="4",label="Ajouter les informations d'identification", callback=self.CanConnect)
        

    def DeleteAll(self):
        dpg.delete_item("1")
        dpg.delete_item("2")
        dpg.delete_item("3")
        dpg.delete_item("4")
        dpg.delete_item("input_prenom")
        dpg.delete_item("input_nom")
        dpg.delete_item("input_email")
    
    def CallBack(self):
        if dpg.get_value("input_email") != "":
            try:
                connection = sqlite3.connect(self.path)
                cursor = connection.cursor()
                information = (dpg.get_value("input_prenom"), dpg.get_value("input_nom"), dpg.get_value("input_email"),1,)
                cursor.execute(f"Update IdentifiantConnexion set Prenom = ?, Nom = ?, email_de_connexion = ? where id = ? ", information)
                connection.commit()
            finally:
                cursor.close()
                connection.close()
                self.DeleteAll()
                dpg.set_value('5', "Compte trouvé")
                dpg.add_text(default_value="Merci de relancer le logiciel", parent="primary wind")
                dpg.add_button(label="Fermer le logiciel", parent="primary wind", callback=self.Quit)
    
    def CanConnect(self, sender, app_data):
        connexion = AccesCV_Tech.AccesCV_Tech(dpg.get_value("input_email"))
        can_connect = connexion.CanUseSoftware()
        if can_connect == 200:
            self.CallBack()
        if can_connect == 404:
            dpg.set_value('5', "Problème de connexion")
            dpg.show_item('5')
        if can_connect == 403:
            dpg.set_value('5', "Compte non-trouvé")
            dpg.show_item('5')

    def License(self, sender, app_data):
        webbrowser.open_new("https://okaroxgames42.wixsite.com/okarox/cv-tech")

    def Quit(self, sender, app_data):
        dpg.destroy_context()