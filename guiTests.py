import pygame as pg
import time
import os, sys

from Archer import Archer
from game import Game
from randommap import *

def jeu_terminal (world):
    running = True
    playing = True
    clock = 0
    game = Game(None, clock,world)

    while running :

        while playing :
            game.run_console()



def main (world) :
    running = True
    playing = True

    #pg.init()
    #pg.mixer.init()
    screen = pg.display.set_mode((0,0), )
    clock = pg.time.Clock()
    game = Game(None, clock,world)


    while running :

        while playing :

            game.run()

if __name__ == "__main__" :
    monde = World(100, 100)
    monde.creer_monde()
    randomise(monde, 3)

    a1 = Archer(1,1)
    a1.position = (1, 2)
    monde.units.append(a1)
    #main()
    jeu_terminal(monde)
