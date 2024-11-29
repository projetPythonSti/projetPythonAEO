from Archer import Archer
from randommap import *
from Unity import *
from town_center import TownCenter

print("\n\n\n\n\n")

monde=Monde(30,160)
monde.creer_monde()

randomise(monde,2)

monde.update_unit_presence()

monde.update_build_presence()

monde.afficher_console()