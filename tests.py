#Créé par Max le 27/09/2024

from randommap import *

monde=Monde(120,120)
monde.creer_monde()

randomise(monde,2)
placer(monde,(60,60),gold,80)

monde.afficher_console()