from models.buildings.town_center import TownCenter
import randommap
from views.world import World_GUI
# from views.Gui import *
from views.menu import PlayPauseMenu
from views.Gui import FenetreJeu
from views.game import Game
from controllers.gameManager import GameManager
from models.World import World
from models.model import Model
from models.AIPlayer import AIPlayer, PlayStyleEnum
import tkinter as tk
import pygame as pg

class luncher:

    def __init__(self):
        self.root = tk.Tk()

    def main(self):
        running = True
        # playing = True

        pg.init()
        pg.mixer.init()
        pg.display.set_caption("Age of Empires")
        icon = pg.image.load("./assets/images/logo.png")
        pg.display.set_icon(icon)
        screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        clock = pg.time.Clock()
        
        world = randommap.random_world({"X":120, "Y": 120, "t": "Arabia"})
        print(world.ressources)
        village1 = Model("1", world)
        village2 = Model("2", world)
        #50,2,30, 10, gold=200, wood=10, food=300, 
        village1.initialize_villages(50,2,30, 10, gold=200, wood=10, food=300,keeps=10, houses=5)
        village2.initialize_villages( 4, 2, 30 , 10, food=100, camps=2, barracks=2, archery_ranger=2)
        #4,50,6, 20, gold=2, wood=1, stables=3, 
        # village1.initialize_villages(houses=1)
        # village2.initialize_villages(houses=1)
        world.fill_world()
        world.fill_ressources(90)
        game_manager = GameManager(1, world)
        game = Game(screen, clock, game_manager)
        playersList  = []
        for a in world.villages:
            tc = TownCenter(a)
            world.place_element(tc)
            world.villages[0].community["T"][tc.uid] = tc
            playersList.append(AIPlayer(a,world, PlayStyleEnum["p"].value,100, game_manager,))
        game.players = playersList
    
        while running:
            
            while game.playing:
                game.run()
    

if __name__ == "__main__":
    luncher = luncher()
    luncher.main()
    # fen = FenetreJeu(luncher)
    # luncher.root.mainloop()