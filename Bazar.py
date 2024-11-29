import time
import os, sys


def affichage(tab,x,y) :
    for i in range(x):
        for j in range(y):
            print(tab[i][j], "|",end="")
        print()
    print()

"""
tab = [[0,0],[0,0]]
affichage(tab,2,2)
sys.stdout.flush()
time.sleep(1)

os.system('clear')

tab = [[0,0],[0,1]]
affichage(tab,2,2)
sys.stdout.flush()
time.sleep(1)

os.system('clear')

tab = [[0,0],[1,0]]
affichage(tab,2,2)
"""


"""
print("Progression :   0%", end="")
for i in range(1, 101):
    sys.stdout.flush()
    time.sleep(0.1)
    print("\b" * 4, str(i).rjust(3), "%", sep="", end="")
print()
"""

print("test",end="")
time.sleep(1)
for i in range(0, 101):
    print("\rProgression :", str(i).rjust(3) + "%", end="")
    sys.stdout.flush()
    time.sleep(0.1)
print()

#######
## 1er version asynchro (fonctionne pas)
######

import pygame as pg
import sys
from mmonde import World
from setup import TILE_SIZE
import os, sys
import time
from Archer import *
import asyncio

class Game_term :

    def __init__(self, clock, world):
        self.clock = clock
        self.world = world
        self.playing = False

    async def run_term (self):
        self.playing = True
        while self.playing:
            self.clock.tick(0.5)
            self.world.units[0].position = (self.world.units[0].position[0]+1,self.world.units[0].position[1])
            self.events()
            self.update()
            self.world.update_unit_presence()
            self.draw_term()

    def events (self): #inutile il me semble
        for event in pg.event.get():
            if event.type == pg.QUIT :
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def update(self):
        pass

    def draw_term (self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.world.afficher_console()

    async def pause (self) :
        while self.playing:
            test = input()
            if test == 'p' :
                self.playing = False
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Vous êtes en pause : ")
                print("Appuyez sur 'q' pour quitter ou appuyer sur 'r' pour reprendre")
                inp = input()
                while (inp !='r') or (inp != 'q') :
                    print("Mauvais input")
                    print("Appuyez sur 'q' pour quitter ou appuyer sur 'r' pour reprendre")


                if inp == 'r':
                    print("La partie va reprendre dans 3 sec")
                    time.sleep(3)
                    self.playing = True

                elif inp == 'q':
                    print("La partie va se terminer dans 3 sec")
                    time.sleep(3)
