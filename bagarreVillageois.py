from time import *

from models.unity.Archer import Archer
from models.Pathfinding import Pathfinding
from randommap import *
from models.unity.Villager import *
from models.buildings.town_center import TownCenter
from mmonde import *


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
    for t in monde.units:
        if u.team!=t.team:
            u.target=t
            break
#each cycle, every villager either moves towards its target or attacks it (if at range)
while 1:
    sleep(2)
    monde.afficher_console()
    for u in monde.units:
        #if not at range
        if dist(u.position,u.target.position)>0.5:
            u.move_easy(u.target.position)
        #if at range
        else:
            u.attack(u.target)
    #also, dead units should be removed, and alive units should retarget
