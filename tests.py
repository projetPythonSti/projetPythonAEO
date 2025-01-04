from time import perf_counter

from models.unity.Archer import Archer
from models.Pathfinding import Pathfinding
from randommap import *
from Unity import *
from models.buildings.town_center import TownCenter
from mmonde import *

import time

print("\n\n\n\n\n")

#creates a 30 by 160 world composed of 30x160 tiles
monde=World(30,160)
monde.creer_monde()

#puts resources and town centers and villagers on the map
#two players symmetrical map
randomise(monde,0)

monde.update_unit_presence()

monde.update_build_presence()

monde.afficher_console()

#tests move_easy
from time import sleep
print("\n\n\n\n\n")
vill1 = monde.spawn_unit(Villager,"blue",0,0)
for _ in range(5):
    sleep(2)
    vill1.move_easy(Position(3,2))
    print(vill1.position.getX(),vill1.position.getY())
    monde.update_unit_presence()
    monde.afficher_console()


'''
print("\n\n\n\n\n")

path = Pathfinding(monde.convertMapToGrid(),(0,0),(monde.x-1,monde.y-1))
start = time.time()
route = path.astar()
end = time.time()
monde.afficher_route_console(route)
end2 = time.time()
print(f"Astar took {end-start} seconds")
print(f"Affichage took {end2-end} seconds")
print(route[::-1])
'''