from importlib.resources import Resource

import pygame as pg
import sys

import mressources
from mmonde import World
from mressources import Ressource
from setup import TILE_SIZE
import os, sys
from consoledraw import Console
import time

class Game :

    def __init__(self, screen, clock,world):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size() if screen is not None else 0,0
        self.world = world

    def run (self):
        self.playing = True
        while self.playing:
            self.clock.tick(3)
            self.events()
            self.update()
            self.draw()

    def run_console (self):
        self.playing = True
        while self.playing:
            #self.clock.tick(3)
            #self.events()
            self.update()
            self.draw_term()

    def events (self):
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

    def draw (self) :
        self.screen.fill((0,0,0))
        for x in range (self.world.x):
            for y in range(self.world.y):
                sq = self.world.dico[(x,y)].rect
                rect = pg.Rect(sq[0][0], sq[0][1], TILE_SIZE,TILE_SIZE)
                if (self.world.dico[(x,y)].contains == " "):
                    pg.draw.rect(self.screen, (23,0,255),rect,1)
                    if (len(self.world.dico[(x,y)].unites) != 0):
                        pg.draw(self.screen, (23,0,255), rect)
                elif(self.world.dico[(x,y)].contains.__class__ == mressources.Wood):
                    pg.draw.rect(self.screen, (255,0,0),rect,1)
                elif(self.world.dico[(x,y)].contains.__class__ == mressources.Gold):
                    pg.draw.rect(self.screen, (0,255,0),rect,1)
                elif(self.world.dico[(x,y)].contains.__class__ == mressources.Food):
                    pg.draw.rect(self.screen,(100,210,255),rect,width=1)




        pg.display.flip()

    def draw_term (self):
        self.world.afficher_console()
        os.system('cls' if os.name == 'nt' else 'clear')




