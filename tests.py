from Archer import Archer
from randommap import *
from Unity import *

monde=Monde(30,160)
monde.creer_monde()

randomise(monde,2)

monde.spawn(Archer, "blue",1,2)
monde.spawn(Archer,"blue",2,2)
monde.spawn(Archer,"red",2,3)
monde.spawn(Archer,"red",3,3)

monde.update_unit_presence()


monde.afficher_console()