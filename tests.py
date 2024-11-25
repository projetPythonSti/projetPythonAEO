from pathfinding import astar
from randommap import *
from Archer import *
from time import *
import numpy as np
monde=World(100, 100)
monde.creer_monde()

randomise(monde,10)

unit1=Archer(1, 1)
unit1.position=(0,0)
unit2=Archer(2,1)
unit2.position=(6,6)
unit3=Archer(3,1)
unit3.position=(5,6)
monde.units.append(unit1)
monde.units.append(unit2)
monde.units.append(unit3)
monde.afficher_console()

grid = monde.convertMapToGrid()
start = (0,0)
goal = (10,70)


route = astar(grid, start, goal)
print(route)

if route.__class__ == bool:
    print("Found no short path")
route = route + [start]
route = route[::-1]
print(f"position de {monde.units[0].name} : {monde.units[0].position}")
monde.units[0].move(goal, route)
print(f"position de {monde.units[0].name} : {monde.units[0].position}")
monde.afficher_console()
monde.afficher_route_console(route)