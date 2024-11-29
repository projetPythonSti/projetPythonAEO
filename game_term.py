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

    def run_term (self):
        self.playing = True
        while self.playing:
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

    def pause (self) :
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




