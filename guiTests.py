import pygame as pg
from game import Game
from randommap import *

from models.gameManager import GameManager

from views.start_menu import *

#Le world en paramètre est voué à disparaitre
def jeu_terminal (world, gm:GameManager):
    running = True
    playing = True

    # MENU

    menu = Menu()
    dico = menu.start_menu()

    """
    IMPORTANT NEED FONCTION TRANSFORME MON DICO EN MONDE
    """

    clock = pg.time.Clock()
    game_term = Game(world, clock, gm)

    while running :

        while playing :
            game_term.run()



def jeu_pygame (world) :
    running = True
    playing = True

    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
    clock = pg.time.Clock()
    game = Game(screen, clock,world)


    while running :

        while playing :

            game.run()

def main () :
    pass

if __name__ == "__main__":
    monde = random_world({"X":120,"Y":180,"t":"Arabia"})
    village1 = Model("1", monde)
    village2 = Model("2", monde)
    village1.initialize_villages(1, 2, 3, gold=200, wood=100, food=300)
    village2.initialize_villages(4, 5, 6, gold=2, wood=1, food=3)
    v = Villager(village1)
    village1.add_unit(v)
    v.ressources_dict["w"] = 3
    v.ressources_dict["g"] = 2
    monde.fill_world()
    monde.fill_ressources(10)
    print(village1.population())
    print(monde.get_ressources())
    print("Before : ", village1.get_ressources())
    print("After : ", village1.get_ressources())
    print(v.ressources_dict)
    community = village1.get_community()
    # print(village2.population())
    #print(monde.get_ressources())
    #print(v)
    #print(community)
    gm = GameManager(speed=1, world=monde)
    print("Launched GameManager")
    gm.addUnitToMoveDict(v, Position(40, 40))
    print("Added unit to move dict")
    gm.addUnitToMoveDict(community["v"]["eq1p6"], Position(10,20))
    print("Added 2nd unit to move dict")
    print(monde.filled_tiles)
    #print(gm.checkUnitsToMove())
    #Boucle pour tester le game manager
    n = 0
    jeu_terminal(monde,gm)
    #monde.to_json("world.json")
    #print("World saved to 'world.json'")



"""
    while n<500:
        gm.checkUnitsToMove()
        tick = datetime.now()
        n += 1
"""

