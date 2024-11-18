import pygame as pg
import time
import os, sys
from game import Game
from randommap import *

def jeu_terminal (world):
    running = True
    playing = True
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((720, 720))
    clock = pg.time.Clock()
    game = Game(screen, clock,world)

    while running :

        while playing :
            game.run_console()



def main (world) :
    running = True
    playing = True

    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((0,0), )
    clock = pg.time.Clock()
    game = Game(screen, clock,world)


    while running :

        while playing :

            game.run()

if __name__ == "__main__" :
    monde = World(10, 10)
    monde.creer_monde()
    randomise(monde, 3)
    print("hi")
    #main()
    monde.afficher_console()
    main(monde)