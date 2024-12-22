import time
import os, sys

from game import Game
from game_term import Game_term
from randommap import *
from models.unity.Archer import *
import asyncio

def jeu_terminal (world):
    running = True
    playing = True
    game_term = Game_term(world)

    while running :

        while playing :
            game_term.run_term()



def jeu_pygame (world) :
    running = True
    playing = True


    game = Game(world)


    while running :

        while playing :

            game.run()

def main () :
    pass


if __name__ == "__main__" :
    monde = World(100, 100)
    monde.creer_monde()
    randomise(monde, 3)

    a1 = Archer(1,1)
    a1.position = (1, 2)
    monde.units.append(a1)

    #main()
    jeu_terminal(monde)

