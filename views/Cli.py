import curses
from blessed import Terminal
import os, sys

class CLIView():
    
    def __init__(self):
        pass
    
    def affichage(self, stdscr):
        curses.curs_set(0)
        stdscr.clear()
        
        letter = list("abcde")
        current = 0
        while(current < len(letter)):
            stdscr.clear()
            stdscr.addstr(0,0,f"Lettre : {letter[current]}")
            stdscr.refresh()
            
            key = stdscr.getch()
            
            if(key == curses.KEY_DOWN):
                current += 1
            
            if current >= len(letter):
                break
        
        # stdscr.getch()

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
        print("Menu de création de partie \n \n")
        print("Appuyez sur q à tout moment pour revenir au menu de démarrage")
        print("Appuyez sur z à tout moment pour revenir à l'étape précédente \n \n")


    def set_size_map (self) :
        term = Terminal()
        print("Veuillez choisir la taille de la carte")
        print("Appuyez sur s pour revenir une petite carte")
        print("Appuyez sur m pour revenir une carte de taille moyenne")
        print("Appuyez sur l pour revenir une grande carte")
        with term.cbreak():
            val = ''
            while val.lower() != 's' or val.lower() != 'm' or val.lower() != 'l':
                val = term.inkey()
                if val.lower() == 'q' :
                    self.start_menu()
                if val.lower() == 'z' :
                    self.start_menu()
            if val.lower() == 's':
                self.set_ressources_quantity()
                pass #écrire du code pour set une petite map
            if val.lower() == 'm':
                self.set_ressources_quantity()
                pass #écrire du code pour set une moyenne map
            if val.lower() == 'l':
                self.set_ressources_quantity()
                pass #écrire du code pour set une large map





    def set_ressources_quantity (self) :
        term = Terminal()
        print("Veuillez choisir la taille de la carte")
        print("Appuyez sur s pour un petit nombre de ressource")
        print("Appuyez sur m pour un nombre moyen de ressource")
        print("Appuyez sur l pour un grand nombre de ressource")
        with term.cbreak():
            val = ''
            while val.lower() != 's' or val.lower() != 'm' or val.lower() != 'l':
                val = term.inkey()
                if val.lower() == 'q':
                    self.start_menu()
                if val.lower() == 'z':
                    self.set_size_map()
            if val.lower() == 's':
                self.set_nb_player()
                pass  # écrire du code pour set une petite map
            if val.lower() == 'm':
                self.set_nb_player()
                pass  # écrire du code pour set une moyenne map
            if val.lower() == 'l':
                self.set_nb_player()
                pass  # écrire du code pour set une large map

    def set_nb_player (self) :
        term = Terminal()
        print("Veuillez choisir le nombre de joueur")
        print("Entrez le nombre de joueur de la partie. Ce nombre doit être compris entre 2 et 8")
        with term.cbreak():
            val = ''
            while val.lower() != '2' or val.lower() != '3' or val.lower() != '4' or val.lower() != '5' or val.lower() != '6' or val.lower() != '7' or val.lower() != '8':
                val = term.inkey()
                if val.lower() == 'q':
                    self.start_menu()
                if val.lower() == 'z':
                    self.set_size_map()
            if val.lower() == '2':
                self.set_ai_behavior(2)
                pass  # écrire du code pour set 2 joueur
            if val.lower() == '3':
                self.set_ai_behavior(3)
                pass
            if val.lower() == '4':
                self.set_ai_behavior(4)
                pass
            if val.lower() == '5':
                self.set_ai_behavior(5)
                pass
            if val.lower() == '6':
                self.set_ai_behavior(6)
                pass
            if val.lower() == '7':
                self.set_ai_behavior(7)
                pass
            if val.lower() == '8':
                self.set_ai_behavior(8)
                pass

    def set_ai_behavior (self,n) :
        term = Terminal()
        if n == 1 :
            print("Veuillez choisir le comportement de l'ia du joueur 1")
            print("Truc sur les comportement de l'ia")
            with term.cbreak():
                val = ''


        # j'ai la flemme je rajouterais la suite plus tard
        pass
        #rajouté code

if __name__ == "__main__":
    cli = CLIView()
    curses.wrapper(cli.affichage)
    