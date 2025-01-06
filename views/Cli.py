import curses
import time

class CLIView:
    def __init__(self, monde, stdscr, game_manager):
        self.monde = monde
        self.stdscr = stdscr
        self.height = monde.height
        self.width = monde.width
        self.running = False
        self.game_manager = game_manager
        self.init_curses()

    def init_curses(self):
        """Initialisation de l'écran curses"""
        curses.curs_set(0)  # Masque le curseur
        self.stdscr.nodelay(1)  # Ne bloque pas l'exécution
        self.stdscr.timeout(100)  # Rafraîchit tous les 100ms
        self.stdscr.clear()  # Efface l'écran
        self.stdscr.refresh()

    def display_world(self):
        height, width = self.stdscr.getmaxyx()  # Obtient les dimensions du terminal
        for y in range(self.height):
            if y >= height - 1:  # Si on atteint la fin de l'écran, on arrête de dessiner
                break
            for x in range(self.width):
                if x >= width - 1:  # Si on dépasse la largeur de l'écran, on arrête
                    break
                self.display_tile(x, y)  # Affiche la tuile à la position (x, y)
            self.stdscr.addstr("\n")  # Passe à la ligne suivante, mais vérifie que l'on est encore dans les limites de la fenêtre

    def display_tile(self, x, y):
        """Affiche une seule tuile"""
        tile = self.monde.tiles_dico[(x, y)]
        # Utilisation de la méthode str pour obtenir une représentation textuelle de la tuile
        content = str(tile)  # Vous pouvez remplacer par la méthode spécifique pour obtenir un symbole
        self.stdscr.addstr(content)

    def update_element_position(self, element, old_position):
        """Met à jour la position d'un élément"""
        if old_position != element.position:
            # Efface l'ancienne position
            self.clear_tile(old_position)
            # Met à jour la vue pour la nouvelle position
            self.place_element(element)

    def remove_element(self, element):
        """Supprime un élément de la vue"""
        position = (element.position.getX(), element.position.getY())
        self.clear_tile(position)

    def place_element(self, element):
        """Place un élément sur la grille"""
        position = (element.position.getX(), element.position.getY())
        # Récupère la position de la tuile
        tile = self.monde.tiles_dico[position]
        # Mettez ici le code pour obtenir un caractère qui représente l'élément
        symbol = "X"  # Par exemple, un "X" pour un élément placé
        self.stdscr.addstr(position[1], position[0], symbol)  # Affiche à la position donnée

    def clear_tile(self, position):
        """Efface une tuile donnée"""
        self.stdscr.addstr(position[1], position[0], "-")  # Efface la position

    def refresh(self):
        """Rafraîchit l'écran"""
        self.stdscr.refresh()

    def update(self):
        """Met à jour la vue du monde"""
        self.stdscr.clear()
        self.display_world()
        self.refresh()

    def main_loop(self):
        """Boucle principale de la vue CLI"""
        self.running = True
        while self.running:
            self.update()  # Rafraîchit l'affichage à chaque itération

            # Exécuter un test d'action sur le monde
            # Simulation d'une modification de position d'un élément pour la démonstration
            time.sleep(1)  # Pause d'une seconde pour voir les changements
            try:
                self.monde.remove_element(self.monde.villages[0].population()['a']['0'])  # Supprime le premier village
            except Exception as e:
                pass
            
            for element in self.game_manager.moving_units:
                self.update_element_position(element, element.position)
            # Exemple d'action sur un élément : déplacer un village
            # (Ce serait déclenché par un événement dans votre jeu, ici nous le simulons)
            # if self.monde.villages:
            #     village = self.monde.villages[0].population()['a']['0']  # Exemple, on déplace le premier village
            #     old_position = village.position
            #     village.position.setX(village.position.getX() + 1)  # Déplacement à droite
            # self.update_element_position(village, old_position)
            
            # Gestion des entrées du clavier, par exemple pour quitter la boucle
            key = self.stdscr.getch()
            if key == ord('q'):  # Quitte si on appuie sur "q"
                self.running = False
