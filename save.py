import json
import os
import time
# self.path mettre

import os
import pickle
import platform

from models.World import *


class Save:
    def __init__(self):
        self.generate_default_path()

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def save(self, world,file_name, path=None):
        self.generate_default_path()
        datas = [world]
        if path: self.save_path = path
        file = open(self.save_path + file_name, 'wb')
        pickle.dump(datas, file)
        file.close()

    def generate_default_path(self):
        system = platform.system()
        self.save_path = os.getcwd()
        if system == "Windows":
            self.save_path += "\\assets\\data\\saves\\"
        else:
            self.save_path += "/assets/data/saves/"

    """
        pay attention to load à saved file, note a file of another extention
    """

    """
    def load(self,file_name, path=None):
        self.generate_default_path()
        if path:
            self.save_path = path
        else:
            self.save_path += "/save"
        if self.backup_exist():
            file = open(self.save_path, 'rb')
            datas = pickle.load(file)
            file.close()
            return datas
    
    def backup_exist(self, path=None):
        if path: self.save_path = path
        return os.path.exists(self.save_path + "/save") 
    """

    def load(self, file_name, path=None):
        #Juste besoin d'une fonction ultra naïve pas sûr que les lignes suivantes soient nécessaire
        self.generate_default_path()
        if path:
            self.save_path = path
        else:
            self.save_path += "/save"

        file = open(self.save_path + file_name, 'rb')
        datas = pickle.load(file)
        file.close()
        return datas



    def save_term(self, world):
        file_name = input("Veuillez choisir le nom de votre sauvegarde :")
        print(f"{file_name} , est-ce bien le nom que vous voulez ?")
        confirmation = input(f"o pour oui et n pour non :")
        while confirmation != 'o':
            file_name = input("Veuillez choisir un nouveau nom pour votre sauvegarde :")
            print(f"{file_name} , est-ce bien le nom que vous voulez ?")
            confirmation = input(f"o pour oui et n pour non :")

        if file_name:
            if os.path.exists("assets/data/saves/" + file_name):
                print(
                    "Il y a déjà une sauvegarde de ce nom. Si vous voulez garder ce nom pour cette sauvegarde, l'ancienne sauvegarde du même non sera écrasé. \nVoulez vous vraiment continuer ? \n")
                rep = input("Appuyez sur o pour écraser et n pour annuler : ")
                while rep != "o" and rep != "n":
                    print("Entrer invalide !")
                    rep = input("Appuyez sur o pour écraser et n pour revenir en arrière : ")
                if rep == "o":
                    self.save(world,file_name,"assets/data/saves/")
                    print(f"Vous avez enregistre votre sauvegarde sous le nom : {file_name}")
                    time.sleep(2)
                else:
                    print("Rien n'a été sauvegarder.")
                    time.sleep(2)
                    return None
            else:
                self.save(world,file_name,"assets/data/saves/")

    def list_files_in_directory(self, directory):
        """Affiche les fichiers dans le répertoire spécifié."""
        liste_fichier = []
        # Liste tout le contenu du dossier
        for entry in os.listdir(directory):
            # Vérifie si c'est un fichier
            if os.path.isfile(os.path.join(directory, entry)):
                liste_fichier.append(entry)
                print(entry)
        return liste_fichier

    def load_term (self):
        print("Voici la liste des fichiers de sauvegardes :")
        list_save = self.list_files_in_directory("assets/data/saves/")
        chosen_save = input("Entrer un nom de sauvegarde pour charger une partie :")
        while chosen_save not in list_save:
            print(
                "Entrer invalide! Vérifiez que vous avez écrit correctement le nom de la sauvegarde de votre choix. Il faut respect les minuscules et les majuscules ainsi que les extensions.")
            chosen_save = input("Entrer un nom de sauvegarde pour charger une partie :")
        self.load(chosen_save,"assets/data/saves/")


if __name__ == "__main__":
    save = Save()
    mworld = World(10,10)
    save.load_term()