import json
import os
import time

def save (world,file_name) :

    if file_name:
        if os.path.exists("saves/" + file_name):
            print(
                "Il y a déjà une sauvegarde de ce nom. Si vous voulez garder ce nom pour cette sauvegarde, l'ancienne sauvegarde du même non sera écrasé. \n Voulez vous vraiment continuer ? \n")
            rep = input("Appuyez sur o pour écraser et n pour revenir en arrière : ")
            while rep != "o" and rep != "n":
                print("Entrer invalide !")
                rep = input("Appuyez sur o pour écraser et n pour revenir en arrière : ")
            if rep == "o":
                world.to_json(file_name)
                print(f"Vous avez enregistre votre sauvegarde sous le nom : {file_name}")
                time.sleep(2)
            else:
                print("Rien n'a été sauvegarder.")
                time.sleep(2)
                return None
    else :
        world.to_json(file_name)

#Fonction intermédiaire
def json_to_dict (path) :
    file = open(path)
    world_dict = json.load(file)
    return world_dict

#Fonction intermédiaire
def dict_to_world (world_dict):
    pass
    # initialiser le monde avec les bons paramètres

#Fonction intermédiaire
def list_files_in_directory(directory):
    """Affiche les fichiers dans le répertoire spécifié."""
    liste_fichier = []
    # Liste tout le contenu du dossier
    for entry in os.listdir(directory):
        # Vérifie si c'est un fichier
        if os.path.isfile(os.path.join(directory, entry)):
            liste_fichier.append(entry)
            print(entry)
    return liste_fichier

def load () :
    print ("Voici la liste des fichiers :")
    list_save = list_files_in_directory("saves")
    chosen_save = input("Entrer un nom de sauvegarde pour charger une partie :")
    while chosen_save not in list_save :
        print("Entrer invalide! Vérifiez que vous avez écrit correctement le nom de la sauvegarde de votre choix. Il faut respect les minuscules et les majuscules).")
        chosen_save = input("Entrer un nom de sauvegarde pour charger une partie :")
    dico = json_to_dict(chosen_save)
    dict_to_world(dico)