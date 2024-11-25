from Archer import Archer
from randommap import *
from Unity import *

monde=Monde(30,160)
monde.creer_monde()

randomise(monde,2)

monde.spawn(Archer,1,2)
monde.spawn(Archer,2,2)
monde.spawn(Archer,2,3)
monde.spawn(Archer,3,3)

monde.update_unit_presence()


monde.afficher_console()