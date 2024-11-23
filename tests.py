from randommap import *
import time
import os, sys

monde=World(30, 160)
monde.creer_monde()

randomise(monde,3)

monde.afficher_console()

