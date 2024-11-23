from Archer import Archer
from randommap import *
from Unity import *
import time
import os, sys

monde=Monde(30,160)
monde.creer_monde()

randomise(monde,2)

a1 = Archer(1)
a2 = Archer(2)
a3 = Archer(3)
a1.position=(1,2)
a2.position=(2,2)
a3.position=(2,3)
monde.units.append(a1)
monde.units.append(a2)
monde.units.append(a3)

monde.update_unit_presence()

monde.afficher_console()