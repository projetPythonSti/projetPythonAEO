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
from save import *
import sys
import math
import time
import timeit
import colorsys
import contextlib
from term_ui import *

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
        self.save = Save()

    def run_term (self):
        speed = 10
        self.playing = True
        tup = self.init_term()
        term = tup[0]
        t = tup[1]
        del tup


        while self.playing :
            self.my_inputs(term,speed)

    def init_term(self):
        term = Terminal()
        with term.cbreak(), term.hidden_cursor(), term.fullscreen():
            t = time.time()
            return term,t


    def my_inputs (self, term,speed):
        with term.cbreak():
            val = ''
            while 1:
                val = term.inkey(timeout=0.0000000001)
                if not val:
                    self.Turn(speed,term)
                elif val.lower() == 'p':
                    self.pause(term)
                elif val.name == 'KEY_TAB':
                    self.stat(term)


                elif val.lower() == '+':
                    if speed < 20:
                        speed += 1
                    print(speed)
                elif val.lower() == '-':
                    if speed > 5:
                        speed -= 1
                    print(speed)




    def Turn (self,speed,term) :

        self.clock.tick(60)
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
        self.draw_term(term)

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


    def draw_term (self,term):

        #os.system('cls' if os.name == 'nt' else 'clear')
        sys.stdout.flush()
        #self.world.afficher_console()
        #print(term.home + term.clear)
        #self.world.show_world()
        affichage_term(term,self.world)
        #print("Durée de la partie " + str(self.game_duration) + "s ")


    def pause (self,term) :
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Nous sommes en pause : ")
        print("Appuyez sur q pour quitter")
        print("Appuyez sur s pour sauvegarder")
        print("Appuyez sur r pour reprendre")
        with term.cbreak():
            val2 = ''
            while val2.lower() != 'r':
                val2 = term.inkey()
                if val2.lower() == 'q':
                    quit()
                elif val2.lower() == 's':
                    self.save.save_term(self.world)


    def stat (self,term):
        #generate
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Nous sommes en pause : ")
        print("Appuyez sur q pour quitter")
        print("Appuyez sur r pour reprendre")
        with term.cbreak():
            val2 = ''
            while val2.lower() != 'r':
                val2 = term.inkey()
                if val2.lower() == 'q':
                    quit()
