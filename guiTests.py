import pygame as pg
import time
import os, sys
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
    monde = World(10, 10)
    monde.creer_monde()
    randomise(monde, 3)
    #main()
    #monde.afficher_console()
    jeu_terminal(monde)