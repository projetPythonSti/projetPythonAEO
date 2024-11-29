from Archer import Archer
from randommap import *
from Unity import *
from town_center import TownCenter

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