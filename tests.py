#Créé par Max le 27/09/2024
from randommap import *

monde=Monde(30,160)
monde.creer_monde()

randomise(monde,3)

monde.afficher_console()