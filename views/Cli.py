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
        term = Terminal()
        print("Menu de création de partie \n \n")
        print("Appuyez sur q pour revenir au menu de démarrage")
        print("Appuyez sur z a tout moment pour revenir à l'étape précédente \n \n")

        with term.cbreak():
            pass

    def set_size_map (self) :
        term = Terminal()
        with term.cbreak():
            pass

    def set_ressources_quantity (self) :
        pass

    def set_nb_player (self) :
        pass

    def set_ai_behavior (self) :

        pass
        #rajouté code

if __name__ == "__main__":
    cli = CLIView()
    curses.wrapper(cli.affichage)
    