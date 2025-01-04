import timeit
from datetime import datetime

import pygame as pg
import sys
from mmonde import World
from utils.setup import TILE_SIZE
import os, sys
import time as t
import datetime as dt
from models.unity.Archer import *
import asyncio
from pynput import keyboard
from blessed import Terminal

#########################################
## Jeu
#########################################

class Game_term :

    def __init__(self, world,clock, gm):
        self.ltick = datetime.now()
        self.gm = gm
        self.clock = clock
        self.speed = 1
        self.world = world
        self.playing = False
        self.game_duration = 0

    def run_term (self):
        speed = 10
        self.playing = True

        while self.playing :
            term = Terminal()
            print("press 'q' to quit.")
            with term.cbreak():
                val = ''
                while val.lower() != 'q':
                    val = term.inkey(timeout=0.00001)
                    if not val:
                        self.Turn(speed)
                    elif val.lower() == '+':
                        if speed < 20:
                            speed += 1
                        print(speed)
                    elif val.lower() == '-':
                        if speed > 5:
                            speed -= 1
                        print(speed)
                    elif val.lower() == 'p':
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("Nous sommes en pause : ")
                        print("Appuyez sur z pour quitter")
                        print("Appuyez sur r pour reprendre")
                        with term.cbreak():
                            val2 = ''
                            while val2.lower() != 'r':
                                val2 = term.inkey()
                                if val2.lower() == 'z' :
                                    quit()
                    elif val.lower() == 'q':
                        quit()

                print(f'bye!{term.normal}')



    def Turn (self,speed) :
        self.clock.tick(0.5 * (speed/10))
        now = datetime.now()
        delta = now - self.ltick
        ig_delta = delta * self.speed
        self.game_duration = self.game_duration + ig_delta.seconds
        self.ltick = now
        # t.sleep(2)
        #self.world.units[0].position = (self.world.units[0].position[0] + 1, self.world.units[0].position[1])
        # self.events()
        # self.update()
        self.gm.checkUnitsToMove()
        self.gm.tick = timeit.default_timer()
        print(self.world.filled_tiles)
        #self.world.update_unit_presence()
        self.draw_term()

    def Horloge(self):
        pass

    def events (self): #inutile il me semble

        """
            def on_press(key):
            try:
                print('alphanumeric key {0} pressed'.format(key.char))
            except AttributeError:
                print('special key {0} pressed'.format(
                    key))

        def on_release(key):
            print('{0} released'.format(key))
            if key == keyboard.Key.esc:
                # Stop listener
                return False
        """

    def update(self):
        pass


    def draw_term (self):
        term = Terminal()

        os.system('cls' if os.name == 'nt' else 'clear')
        #self.world.afficher_console()
        with term.location(0,term.height-1):
            #print(term.home + term.clear)
            self.world.show_world()

            print("Durée de la partie " + str(self.game_duration) + "s ")







