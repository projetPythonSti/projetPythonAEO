from time import perf_counter

from Archer import Archer
from pathfinding import Pathfinding
from randommap import *
from Unity import *
from town_center import TownCenter

import time

print("\n\n\n\n\n")

#creates a 30 by 160 world composed of 30x160 tiles
monde=Monde(30,160)
monde.creer_monde()

#puts resources and town centers and villagers on the map
#two players symmetrical map
randomise(monde,0)

monde.update_unit_presence()

monde.update_build_presence()

monde.afficher_console()

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

''' me trying to find nicer path for units
for i in len(route)-2: #search for turns
    if (route[i][0]!=route[i+1][0] and route[i+1][1]!=route[i+2][1]) or \
        (route[i][1]!=route[i+1][1] and route[i+1][0]!=route[i+2][0]):
'''