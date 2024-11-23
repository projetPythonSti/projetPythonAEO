import pygame as pg
import sys
from mmonde import World
from setup import TILE_SIZE
import os, sys
import time

class Game_term :

    def __init__(self, clock, world):
        self.clock = clock
        self.world = world

    def run_term (self):
        self.playing = True
        while self.playing:
            self.clock.tick(0.5)
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

    def draw_term (self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.world.afficher_console()




