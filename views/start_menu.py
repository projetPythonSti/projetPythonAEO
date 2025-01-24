from blessed import Terminal
from save import *
import os, sys

class Menu :
    """
            23/01/2025@tahakhetib : J'ai apporté des modifications à ce fichier  sur ce que @etan-test-1 a écrit
                - Ajouté le retour du dictionnaire vers la boucle de jeu afin d'extraire les informations nécessaires à la création des IA,

        """
    def __init__(self):
        self.x = None
        self.y = None
        self.type_map = None
        self.ressources_quantities = None
        self.nb_joueur = 0
        self.ai_behavior = []

#MENU DE DEMARRAGE
    def start_menu (self) :
        self.reset()
        os.system('cls' if os.name == 'nt' else 'clear')
        term = Terminal()
        print("Menu de démarrage : ")
        print("Appuyez sur q pour quitter le jeu")
        print("Appuyez sur n pour créer une nouvelle partie")
        print("Appuyez sur c charger une partie sauvegardé")
        with term.cbreak():
            val = ''
            while val.lower() != 'n' or val.lower() != 'c':
                val = term.inkey()
                if val.lower() == 'q':
                    quit()

                if val.lower() =='n' :
                    self.set_size_map()
                    break

                if val.lower() == 'c' :
                    nsave = Save()
                    nsave.load_term()
                    break
            return self.return_value()

    def set_size_map (self) :
        os.system('cls' if os.name == 'nt' else 'clear')
        term = Terminal()
        print("Menu de création de partie \n ")
        print("Appuyez sur q à tout moment pour revenir au menu de démarrage")
        print("Appuyez sur z à tout moment pour revenir à l'étape précédente \n ")

        print("Veuillez choisir la taille de la carte")
        print("Appuyez sur p pour revenir une petite carte")
        print("Appuyez sur m pour revenir une carte de taille moyenne")
        print("Appuyez sur g pour revenir une grande carte \n")
        with term.cbreak():
            val = ''
            while val.lower() != 's' or val.lower() != 'm' or val.lower() != 'l':
                val = term.inkey()
                if val.lower() == 'q' :
                    self.start_menu()
                    break
                if val.lower() == 'z' :
                    self.start_menu()
                    break
                if val.lower() == 'p':
                    self.x = 120
                    self.y = 120
                    self.set_type_map()
                    break

                if val.lower() == 'm':
                    self.x = 240
                    self.y = 240
                    self.set_type_map()
                    break

                if val.lower() == 'g':
                    self.x = 360
                    self.y = 360
                    self.set_type_map()
                    break

    def set_type_map (self) :
        os.system('cls' if os.name == 'nt' else 'clear')
        term = Terminal()
        print("Menu de création de partie \n ")
        print("Appuyez sur q à tout moment pour revenir au menu de démarrage")
        print("Appuyez sur z à tout moment pour revenir à l'étape précédente \n ")

        print("Veuillez choisir le type de carte")
        print("Appuyez sur g pour une map de type Gold Rush (or au centre de la carte)")
        print("Appuyez sur r pour une map random")

        with term.cbreak():
            val = ''
            while val.lower() != 's' or val.lower() != 'm' or val.lower() != 'l':
                val = term.inkey()
                if val.lower() == 'q' :
                    self.start_menu()
                    break
                if val.lower() == 'z' :
                    self.start_menu()
                    break
                if val.lower() == 'g':
                    self.type_map = 'g'
                    self.set_ressources_quantity()
                    break

                if val.lower() == 'r':
                    self.type_map = 'r'
                    self.set_ressources_quantity()
                    break

    def set_ressources_quantity (self) :
        os.system('cls' if os.name == 'nt' else 'clear')
        term = Terminal()
        print("Menu de création de partie \n ")
        print("Appuyez sur q à tout moment pour revenir au menu de démarrage")
        print("Appuyez sur z à tout moment pour revenir à l'étape précédente \n ")

        print("Veuillez choisir l'abondance de ressource des joueurs en début de partie ")
        print("Appuyez sur p pour un petit nombre de ressource pour chaque joueur(lean)")
        print("Appuyez sur m pour un nombre moyen de ressource pour chaque joueur(mean)")
        print("Appuyez sur g pour un grand nombre de ressource pour chaque joueur(marines) \n")
        with term.cbreak():
            val = ''
            while val.lower() != 's' or val.lower() != 'm' or val.lower() != 'l':
                val = term.inkey()
                if val.lower() == 'q':
                    self.start_menu()
                    break
                if val.lower() == 'z':
                    self.set_size_map()
                    break
                if val.lower() == 'p':
                    self.ressources_quantities = 'p'
                    self.set_nb_player()
                    break

                if val.lower() == 'm':
                    self.ressources_quantities = 'm'
                    self.set_nb_player()
                    break

                if val.lower() == 'g':
                    self.ressources_quantities = 'g'
                    self.set_nb_player()
                    break


    def set_nb_player (self) :

        os.system('cls' if os.name == 'nt' else 'clear')
        term = Terminal()
        print("Menu de création de partie \n ")
        print("Appuyez sur q à tout moment pour revenir au menu de démarrage")
        print("Appuyez sur z à tout moment pour revenir à l'étape précédente \n ")

        print("Veuillez choisir le nombre de joueur")
        print("Entrez le nombre de joueur de la partie. Ce nombre doit être compris entre 2 et 8 \n")
        with term.cbreak():
            val = ''
            while val.lower() != '2' or val.lower() != '3' or val.lower() != '4' or val.lower() != '5' or val.lower() != '6' or val.lower() != '7' or val.lower() != '8':
                val = term.inkey()

                if val.lower() == 'q':
                    return self.set_ai_behavior()
                    break

                if val.lower() == 'z':
                    self.set_ai_behavior()
                    break

                if val.lower() == '2':
                    self.nb_joueur = 2
                    self.set_ai_behavior()
                    break

                if val.lower() == '3':
                    self.nb_joueur = 3
                    self.set_ai_behavior()
                    break

                if val.lower() == '4':
                    self.nb_joueur = 4
                    self.set_ai_behavior()
                    break

                if val.lower() == '5':
                    self.nb_joueur = 5
                    self.set_ai_behavior()
                    break

                if val.lower() == '6':
                    self.nb_joueur = 6
                    self.set_ai_behavior()
                    break

                if val.lower() == '7':
                    self.nb_joueur = 7
                    self.set_ai_behavior()
                    break

                if val.lower() == '8':
                    self.nb_joueur = 8
                    self.set_ai_behavior()
                    break

    def set_ai_behavior (self) :
        os.system('cls' if os.name == 'nt' else 'clear')
        term = Terminal()
        print("Menu de création de partie \n ")
        print("Appuyez sur q à tout moment pour revenir au menu de démarrage")
        print("Appuyez sur z à tout moment pour revenir à l'étape précédente \n ")

        print("Veuillez le comportement des IA ")
        print("Appuyez sur a pour une IA agressive")
        print("Appuyez sur p pour une IA passive")
        print("Appuyez sur b pour une IA bâtisseuse")

        with term.cbreak():
            n = 0
            val = ''
            while val.lower() != 'a' or val.lower() != 'p' or val.lower() != 'b' :
                print(f"Veuillez choisir le comportement de l'ia du joueur {n+1}")
                val = term.inkey()
                if val.lower() == 'q':
                    self.start_menu()
                    break
                if val.lower() == 'z':
                    self.set_size_map()
                    break
                if val.lower() == 'a':
                    self.ai_behavior.append('a')
                    n = n + 1
                    if n >= self.nb_joueur :
                        break

                if val.lower() == 'p':
                    self.ai_behavior.append('p')
                    n = n + 1
                    if n >= self.nb_joueur :
                        break
                if val.lower() == 'b':
                    self.ai_behavior.append('b')
                    n = n + 1
                    if n >= self.nb_joueur :
                        break

            #self.return_value()


    def return_value(self):
        return {"X":self.x, "Y": self.y, "q" : self.ressources_quantities, "n" : self.nb_joueur, "b" : self.ai_behavior, "t" : self.type_map }

    def reset(self):
        self.x = None
        self.y = None
        self.type_map = None
        self.ressources_quantities = None
        self.nb_joueur = 0
        self.ai_behavior = []