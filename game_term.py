from datetime import datetime

import sys
from mmonde import World
import os, sys
import time as t
import datetime as dt
from models.unity.Archer import *
import asyncio
from pynput import keyboard

################################
## Partie input
################################

pause = False

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))

    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    global pause
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        pause = True
        return False

    if key == keyboard.Key.esc:
        pause = True


#########################################
## Jeu
#########################################

class Game_term :

    def __init__(self, world):
        self.ltick = datetime.now()
        self.clock = 1
        self.speed = 1
        self.world = world
        self.playing = False
        self.game_duration = 0

    def run_term (self):
        self.playing = True
        while self.playing:

            #self.clock.tick(0.5)
            now = datetime.now()
            delta = now - self.ltick
            ig_delta = delta * self.speed
            self.game_duration = self.game_duration + ig_delta.seconds
            self.ltick = now

            #t.sleep(2)
            self.world.units[0].position = (self.world.units[0].position[0]+1,self.world.units[0].position[1])
            #self.events()
            #self.update()
            self.world.update_unit_presence()



            self.draw_term()

    def Horloge(self):
        pass

    def events (self): #inutile il me semble

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

    def update(self):
        pass


    def draw_term (self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.world.afficher_console()
        print("Durée de la partie " + str(self.game_duration) + "s ")







