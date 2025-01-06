from blessed import Terminal
import os, sys

class Menu :

    def __init__(self):
        self.x = None
        self.y = None
        self.ressources_quantities = None
        self.nb_joueur = 0
        self.ai_behavior = ()

#MENU DE DEMARRAGE
    def start_menu (self) :
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
                    self.map_creation_menu()

                else :
                    # ajouté code
                    pass

    def map_creation_menu (self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Menu de création de partie \n ")
        print("Appuyez sur q à tout moment pour revenir au menu de démarrage")
        print("Appuyez sur z à tout moment pour revenir à l'étape précédente \n ")
        self.set_size_map()


    def set_size_map (self) :
        term = Terminal()
        print("Veuillez choisir la taille de la carte")
        print("Appuyez sur p pour revenir une petite carte")
        print("Appuyez sur m pour revenir une carte de taille moyenne")
        print("Appuyez sur g pour revenir une grande carte \n")

        """
        val = input()
        while val != 's' and val!= 'm' and val!='l' and val!='z' and val!='q':
            val = input()

        if val == 's' :
            self.x = 120
            self.y = 120
            self.start_menu()
            
        if val == 'm' :
            self.x = 240
            self.y = 240
            self.start_menu()
            
        if val == 'l' :
            self.x = 360
            self.y = 360
            self.start_menu()
        
        if val == 'q' :
            self.start_menu()
        
        if val == 'z' :
            self.start_menu()"""


        with term.cbreak():
            val = ''
            while val.lower() != 's' or val.lower() != 'm' or val.lower() != 'l':
                val = term.inkey()
                if val.lower() == 'q' :
                    self.start_menu()
                if val.lower() == 'z' :
                    self.start_menu()
                if val.lower() == 'p':
                    self.set_ressources_quantity()
                    pass #écrire du code pour set une petite map
                if val.lower() == 'm':
                    self.set_ressources_quantity()
                    pass #écrire du code pour set une moyenne map
                if val.lower() == 'g':
                    self.set_ressources_quantity()
                    pass #écrire du code pour set une large map


    def set_ressources_quantity (self) :


        os.system('cls' if os.name == 'nt' else 'clear')
        term = Terminal()
        print("Veuillez choisir l'abondance des ressources (bois et gold) sur la carte")
        print("Appuyez sur p pour un petit nombre de ressource (lean)")
        print("Appuyez sur m pour un nombre moyen de ressource (mean)")
        print("Appuyez sur g pour un grand nombre de ressource (marines) \n")
        with term.cbreak():
            val = ''
            while val.lower() != 's' or val.lower() != 'm' or val.lower() != 'l':
                val = term.inkey()
                if val.lower() == 'q':
                    self.start_menu()
                if val.lower() == 'z':
                    self.set_size_map()
                if val.lower() == 'p':
                    self.ressources_quantities = 'p'
                    self.set_nb_player()

                if val.lower() == 'm':
                    self.ressources_quantities = 'm'
                    self.set_nb_player()

                if val.lower() == 'g':
                    self.ressources_quantities = 'g'
                    self.set_nb_player()


    def set_nb_player (self) :
        term = Terminal()
        print("Veuillez choisir le nombre de joueur")
        print("Entrez le nombre de joueur de la partie. Ce nombre doit être compris entre 2 et 8 \n")
        with term.cbreak():
            val = ''
            while val.lower() != '2' or val.lower() != '3' or val.lower() != '4' or val.lower() != '5' or val.lower() != '6' or val.lower() != '7' or val.lower() != '8':
                val = term.inkey()

                if val.lower() == 'q':
                    self.start_menu()

                if val.lower() == 'z':
                    self.set_size_map()

                if val.lower() == '2':
                    self.nb_joueur = 2
                    self.set_ai_behavior(2)

                if val.lower() == '3':
                    self.nb_joueur = 3
                    self.set_ai_behavior(3)

                if val.lower() == '4':
                    self.nb_joueur = 4
                    self.set_ai_behavior(4)

                if val.lower() == '5':
                    self.nb_joueur = 5
                    self.set_ai_behavior(5)

                if val.lower() == '6':
                    self.nb_joueur = 6
                    self.set_ai_behavior(6)

                if val.lower() == '7':
                    self.nb_joueur = 7
                    self.set_ai_behavior(7)

                if val.lower() == '8':
                    self.nb_joueur = 8
                    self.set_ai_behavior(8)

    def set_ai_behavior (self, n) :
        term = Terminal()
        print("Veuillez le comportement des IA ")
        if n == 1 :
            print("Veuillez choisir le comportement de l'ia du joueur 1")
            print("Truc sur les comportement de l'ia")
            with term.cbreak():
                val = ''


        # j'ai la flemme je rajouterais la suite plus tard
        # verif1
        pass
        #rajouté code

    def return_value(self):
        return {"X":self.x, "Y": self.y, "q" : self.ressources_quantities, "n" : self.nb_joueur, "b" : self.ai_behavior}
