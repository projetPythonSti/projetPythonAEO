import pygame as pg
from blessed import Terminal
from models.Position import Position
from models.AIPlayer import AIPlayer
from models.save import *
import sys
import time
import timeit

#########################################
## Jeu
#########################################

class Game :
    """
                23/01/2025@tahakhetib : J'ai apporté des modifications à ce fichier  sur ce que @etan-test-1 a écrit
                    - Ajouté la liste des IA (players) aux attributs du jeu et leur activité à chaque tour
                        Idée pour plus tard : Pour éviter la surchage du système, au lieu de lancer toutes les IA à chaque frame, plutôt lancer une IA par frame ?

            """

    def __init__(self, world, clock, gm, players: list[AIPlayer]):

        self.ltick = time.time()
        self.gm = gm
        self.players = players
        self.clock = clock
        self.speed = 1
        self.world = world
        self.upleft = Position(0,0) #changes by player arrow keys, should always start upper left of the map (0,0)
        self.downright = Position(0, 0) #changes by itself to fit the screen
        self.playing = False
        self.game_duration = 0
        self.save = Save()
        self.ffff = False
        self.pygame_on = False


# Boucle Principale
    def run (self):
        self.playing = True
        tup = self.init_term()
        term = tup[0]
        t = tup[1]
        del tup

        while self.playing :
            self.my_inputs_turn (term)



    def my_inputs_turn (self, term):
        with term.cbreak():
            val = ''
            while 1:
                val = term.inkey(timeout=0.0000000001)
                if not val:
                    self.turn(term)
                elif val.lower() == 'p':
                    self.pause(term)
                elif val.name == 'KEY_TAB':
                    self.stat(term)

                #a changer
                elif val.lower() == '+':
                    if self.speed < 10:
                        self.speed += 1
                elif val.lower() == '-':
                    if self.speed >= 1 :
                        self.speed -= 1


                elif val == 'z':
                    if self.upleft.getY()>0:
                        self.upleft.setY(self.upleft.getY()-1)
                elif val == 'q':
                    if self.upleft.getX()>0:
                        self.upleft.setX(self.upleft.getX()-1)
                elif val == 's':
                    if self.upleft.getY()<self.world.height:
                        self.upleft.setY(self.upleft.getY()+1)
                elif val == 'd':
                    if self.upleft.getX()<self.world.width:
                        self.upleft.setX(self.upleft.getX()+1)
                elif val == 'Z':
                    self.upleft.setY(self.upleft.getY()-4)
                    if self.upleft.getY()<0:
                        self.upleft.setY(0)
                elif val == 'Q':
                    self.upleft.setX(self.upleft.getX()-4)
                    if self.upleft.getX()<0:
                        self.upleft.setX(0)
                elif val == 'S':
                    self.upleft.setY(self.upleft.getY()+4)
                    if self.upleft.getY()>self.world.height:
                        self.upleft.setY(self.world.height)
                elif val == 'D':
                    self.upleft.setX(self.upleft.getX()+4)
                    if self.upleft.getX()>self.world.width:
                        self.upleft.setX(self.world.width)
                elif val.name == 'KEY_UP':
                    if self.upleft.getY()>0:
                        self.upleft.setY(self.upleft.getY()-1)
                elif val.name == 'KEY_LEFT':
                    if self.upleft.getX()>0:
                        self.upleft.setX(self.upleft.getX()-1)
                elif val.name == 'KEY_DOWN':
                    if self.upleft.getY()<self.world.height:
                        self.upleft.setY(self.upleft.getY()+1)
                elif val.name == 'KEY_RIGHT':
                    if self.upleft.getX()<self.world.width:
                        self.upleft.setX(self.upleft.getX()+1)

                elif val.name == 'KEY_F1' or val.name == 'KEY_F2' or val.name == 'KEY_F3' or val.name == 'KEY_F4':
                    self.ffff = not self.ffff



    def turn (self,term) :
        self.clock.tick(60)
        now = time.time()
        delta = now - self.ltick
        ig_delta = delta * self.speed
        self.game_duration = self.game_duration + ig_delta
        self.ltick = now
        # t.sleep(2)
        #self.world.units[0].position = (self.world.units[0].position[0] + 1, self.world.units[0].position[1])
        # self.events()
        # self.update()
        for a in self.players:
            a.playTurn()
        self.gm.checkUnitsToMove()
        self.gm.tick = timeit.default_timer()

        self.draw_term(term)
        """
        Peut changer si besoin 
        """
        if self.pygame_on :
            self.draw_pygame()
        if self.gm.save:
            pass
        if self.term_on:
            self.draw_term


### Fonction intermédiaire

    def init_term(self):
        term = Terminal()
        with term.cbreak(), term.hidden_cursor(), term.fullscreen():
            t = time.time()
            return term,t

    def draw_term (self,term):

        sys.stdout.flush()
        if self.ffff :
            self.resources_term(term)

        else :
            self.downright=Position(min(self.upleft.getX()+term.width-2,self.world.width),min(self.upleft.getY()+term.height-3,self.world.height)) #lil minuses here to fit everything nicely
            print(self.world.return_precise_world(self.upleft,self.downright))
            #prevents going too much right and down
            if self.downright.getX()-self.upleft.getX()<term.width-2 and self.world.width>term.width:
                self.upleft.setX(self.world.width-term.width+2)
            elif self.world.width < term.width:
                self.upleft.setX(0)
            if self.downright.getY()-self.upleft.getY()<term.height-3 and self.world.height>term.height:
                self.upleft.setY(self.world.height-term.height+3)
            elif self.world.height<term.height:
                self.upleft.setY(0)


    def draw_pygame (self):
        pass
        ### A REMPLIR
    
    def load_game(self, game):
        pass
    
    def load_game(self):
        pass

    def resources_term(self,term):
        sys.stdout.flush()
        infos=""
        for village in self.world.villages:
            infos+="Village "+village.name+" ;"
            infos+=" Wood:"+str(village.ressources["w"])+" Gold:"+str(village.ressources["g"])+" Food:"+str(village.ressources["f"])
            infos+=" Population:"+str(village.peopleCount)+'/'
            infos+='\n'
        infos += '\n' * (term.height - len(self.world.villages) - 2)
        print(infos)


    def pause (self,term) :
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Nous sommes en pause : ")
        print("Appuyez sur q pour quitter")
        print("Appuyez sur s pour sauvegarder")
        print("Appuyez sur r pour reprendre")
        print(f"IN GAME TIME : {self.game_duration}")
        print(f"SPEED : {self.speed}")
        with term.cbreak():
            val2 = ''
            while val2.lower() != 'r':
                val2 = term.inkey()
                if val2.lower() == 'q':
                    quit()
                elif val2.lower() == 's':
                    self.save.save_term(self.world)


    def stat (self,term):
        #generate html
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
