import pygame as pg
import time
import os, sys

from game import Game
from game_term import Game_term
from randommap import *
from models.unity.Archer import *
import asyncio

from models.Position import Position
from models.maps.Tile import Tile
from models.model import Model
import models.unity
from models.World import World
from models.gameManager import GameManager
from models.unity.Villager import Villager
from datetime import datetime

def jeu_terminal (world, gm:GameManager):
    running = True
    playing = True
    clock = pg.time.Clock()
    game_term = Game_term(world,clock,gm)

    while running :

        while playing :
            game_term.run_term()



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
    """
    monde = World(100, 100)
    monde.creer_monde()
    randomise(monde, 3)

    a1 = Archer(1)
    a1.position = (1, 2)
    monde.units.append(a1)

    #main()
    jeu_terminal(monde)

    """
if __name__ == "__main__":
    monde = World(100, 100)
    village1 = Model("1", monde)
    village2 = Model("2", monde)
    village1.initialize_villages(1, 2, 3, gold=200, wood=100, food=300)
    village2.initialize_villages(4, 5, 6, gold=2, wood=1, food=3)
    v = Villager(village1)
    village1.add_unit(v)
    v.ressources_dict["w"] = 3
    v.ressources_dict["g"] = 2
    monde.fill_world()
    monde.fill_ressources(10)
    print(village1.population())
    print(monde.get_ressources())
    print("Before : ", village1.get_ressources())
    fo = monde.get_ressources()["fo"]["0"]
    v.drop_ressources()
    v.collect(fo)
    print("After : ", village1.get_ressources())
    print(v.ressources_dict)
    community = village1.get_community()
    # print(village2.population())
    #print(monde.get_ressources())
    #print(v)
    #print(community)
    gm = GameManager(speed=1, world=monde)
    print("Launched GameManager")
    gm.addUnitToMoveDict(v, Position(40, 40))
    print("Added unit to move dict")
    gm.addUnitToMoveDict(community["sm"]["eq1p4"], Position(10,20))
    print("Added 2nd unit to move dict")
    print(monde.filled_tiles)
    #print(gm.checkUnitsToMove())
    #Boucle pour tester le game manager
    n = 0
    #jeu_terminal(monde,gm)
    #monde.to_json("world.json")
    print("World saved to 'world.json'")



"""
    while n<500:
        gm.checkUnitsToMove()
        tick = datetime.now()
        n += 1
"""

