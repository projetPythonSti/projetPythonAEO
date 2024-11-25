from Archer import Archer
from randommap import *
from Unity import *
from town_center import TownCenter

print("\n\n\n\n\n")

monde=Monde(30,160)
monde.creer_monde()

randomise(monde,2)

a1b = monde.spawn_unit(Archer, "blue",1,2)
a2b = monde.spawn_unit(Archer,"blue",2,2)
a1r = monde.spawn_unit(Archer,"red",2,3)
a2r = monde.spawn_unit(Archer,"red",3,3)

monde.update_unit_presence()

tc1b = monde.spawn_building(TownCenter, "blue", 5,2)

monde.update_build_presence()

monde.afficher_console()