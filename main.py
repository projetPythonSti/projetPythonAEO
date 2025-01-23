import pygame as pg
import time
import os, sys

from game import Game
from randommap import *
from Archer import *
import asyncio

def jeu_terminal (world):
    running = True
    playing = True
    clock = pg.time.Clock()
    game_term = Game(world, clock)

    while running :

        while playing :
            game_term.run()



def jeu_pygame (world) :
    running = True
    playing = True

    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
    clock = pg.time.Clock()
    game = Game(screen, clock,world)


    while running :

        while playing :

            game.run()

def main () :
    pass


if __name__ == "__main__" :
    monde = World(100, 100)
    monde.creer_monde()
    randomise(monde, 3)

    a1 = Archer(1)
    a1.position = (1, 2)
    monde.units.append(a1)

    #main()
    jeu_terminal(monde)

