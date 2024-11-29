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
randomise(monde,2)

monde.update_unit_presence()

monde.update_build_presence()

monde.afficher_console()

print("\n\n\n\n\n")


path = Pathfinding(monde.convertMapToGrid(),(0,0),(monde.x-1,monde.y-1))
start = time.time()
route = path.astar()
end = time.time() - start
monde.afficher_route_console(route)
print(end)