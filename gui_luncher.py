from views.world import World_GUI
# from views.Gui import *
from views.menu import PlayPauseMenu
from views.Gui import FenetreJeu
from views.game import Game
from controllers.gameManager import GameManager
from models.World import World
from models.model import Model
import tkinter as tk
import pygame as pg

class luncher:

    def __init__(self):
        self.root = tk.Tk()

    def main(self):
        running = True
        playing = True

        pg.init()
        pg.mixer.init()
        pg.display.set_caption("Age of Empires")
        icon = pg.image.load("./assets/images/logo.png")
        pg.display.set_icon(icon)
        screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        clock = pg.time.Clock()
        
        world = World(50, 50)
        
        village1 = Model("fabulous", world)
        village2 = Model("hiraculous", world)
        village1.initialize_villages(50,2,30, 10, gold=200, wood=10, food=300, town_center=1, keeps=2, houses=5, camps=3)
        village2.initialize_villages(4,50,6, 20, 1, gold=2, wood=1, food=3, barracks=1, archery_ranger=3, stables=3, farms=2)
        world.fill_ressources(10)
        game_manager = GameManager(1, world)
        game = Game(screen, clock, game_manager)
        # menu_manager = Menu_manager(screen, game)
        
        # world_gui = World_GUI(0, 30, 30, 100, 100, world)
        
        while running:
            
            while game.playing:
                game.run()
    

if __name__ == "__main__":
    luncher = luncher()
    luncher.main()
    # fen = FenetreJeu(luncher)
    # luncher.root.mainloop()