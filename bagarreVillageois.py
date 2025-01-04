from time import perf_counter

from models.unity.Archer import Archer
from models.Pathfinding import Pathfinding
from randommap import *
from Unity import *
from models.buildings.town_center import TownCenter
from mmonde import *

import time

print("\n\n\n\n\n")

#creates a 12 by 12 world for demonstration purposes
monde=World(12,12)
monde.creer_monde()
#surrounds the world with wood for better console visibility
for i in range(0,12):
    monde.dico[(i,0)].contains = Wood()
    monde.dico[(0, i)].contains = Wood()
    monde.dico[(i, 11)].contains = Wood()
    monde.dico[(11, i)].contains = Wood()
#spawns 2 teams of 5 villagers each
for i in range(5):
    monde.spawn_unit(Villager, "blue", 3+i, 2)
    monde.spawn_unit(Villager, "red", 4+i, 9)
monde.afficher_console()
#villagers should now target one of the opposing team villagers
for u in monde.units:
    ()
#each cycle, every villager either moves towards its target or attacks it (if at range)
#also, they should check if their target is alive. If not,

