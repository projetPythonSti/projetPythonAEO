from randommap import *

monde=Monde(30,30)
monde.creer_monde()

randomise(monde,3)
while True:
    monde.afficher_console()
    time.sleep(0.5)