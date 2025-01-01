import time
from datetime import datetime
import timeit

from models.Position import Position
from models.maps.Tile import Tile
from models.model import Model
import models.unity
from models.World import World
from models.gameManager import GameManager
from models.unity.Villager import Villager


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
    fo = monde.get_ressources()["f"]
    v.drop_ressources()
    #v.collect(fo)
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
    gm.addUnitToMoveDict(community["s"]["eq1p4"], Position(10,20))
    print("Added 2nd unit to move dict")
    #gm.checkUnitsToMove()
    #Boucle pour tester le game manager

    gm.tick = timeit.default_timer()
    time.sleep(2)
    # Record the start time
    print("started main loop")
    elapsedTime = 0
    while True:
        print(elapsedTime)
        gm.checkUnitsToMove()
        gm.tick = timeit.default_timer()


    # monde.show_world()
