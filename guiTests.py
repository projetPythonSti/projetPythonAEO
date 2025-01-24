import pygame as pg
import time
import os, sys

from game import Game
from models.AIPlayer import AIPlayer, PlayStyleEnum
from randommap import *
from models.unity.Archer import *
from models.Position import Position
from models.maps.Tile import Tile
from models.model import Model
import models.unity
from models.World import World
from controllers.gameManager import GameManager
from models.unity.Villager import Villager
from datetime import datetime
from views.start_menu import *

from models.Position import Position
import randommap


def fillAIPlaystyle(world:World, aiBehavior,gameLevel , gm:GameManager, debug=False):
    aiList = []

    for a in range(len(world.villages)):
        aiList.append(AIPlayer(world.villages[a-1],world,PlayStyleEnum[aiBehavior[a-1]].value,100, gm,debug=debug, writeToDisk=False))
    return aiList


def jeu_terminal (world, gm:GameManager, debug=False):
    running = True
    playing = True

    # MENU
    #return {"X": self.x, "Y": self.y, "q": self.ressources_quantities, "n": self.nb_joueur, "b": self.ai_behavior,
            # "t": self.type_map}

    menu = Menu()
    dico = menu.start_menu()
    clock = pg.time.Clock()
    playersList = fillAIPlaystyle(world, gm=gm, gameLevel=100, aiBehavior=dico["b"],debug=debug)
    game_term = Game(world,clock,gm, players=playersList)
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
    game = Game(screen, clock,world, [])


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
    monde = randommap.random_world({"X":120, "Y":120, "t": "GoldRush"})
    village1 = Model("1", monde)
    village2 = Model("2", monde)
    village1.initialize_villages(1, 2, 3,villages=50, gold=200, wood=100, food=300)
    village2.initialize_villages(4, 5, 6,villages=50,gold=2, wood=1, food=3)
    v = Villager(village1)
    village1.add_unit(v)
    v.ressources_dict["w"] = 3
    v.ressources_dict["g"] = 2
    monde.fill_world()
    monde.fill_ressources(10)
    print(village1.population())
    print(monde.get_ressources())
    print("Before : ", village1.get_ressources())
    print("After : ", village1.get_ressources())
    print(v.ressources_dict)
    community = village1.get_community()
    # print(village2.population())
    #print(monde.get_ressources())
    #print(v)
    #print(community)
    gm = GameManager(speed=1, world=monde, debug=False)
    print("Launched GameManager")
    #m.addUnitToMoveDict(v, Position(40, 40))
    print("Added unit to move dict")
    #gm.addUnitToMoveDict(community["v"]["eq1p6"], Position(10,20))
    print("Added 2nd unit to move dict")
    tc = TownCenter(team=village1)
    tc2= TownCenter(team=village2)
    monde.place_element(tc)
    monde.place_element(tc2)
    monde.villages[0].community["T"][tc.uid] = tc
    monde.villages[1].community["T"][tc2.uid] = tc2
    #print(monde.filled_tiles)
    #Boucle pour tester le game manager
    n = 0
    jeu_terminal(monde,gm, False)



"""
    while n<500:
        gm.checkUnitsToMove()
        tick = datetime.now()
        n += 1
"""

