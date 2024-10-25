import pygame as pg
import sys
from mmonde import World
from setup import TILE_SIZE
import os, sys
import time

class Game :

    def __init__(self, screen, clock,world):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
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
            self.clock.tick(3)
            self.events()
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
                pg.draw.rect(self.screen, (0,0,255),rect,1)

        pg.display.flip()

    def draw_term (self):
        self.world.afficher_console()
        os.system('cls' if os.name == 'nt' else 'clear')




