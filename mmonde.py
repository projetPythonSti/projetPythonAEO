from ressources.mressources import *
from unity.Unity import *
import numpy as np

from utils.setup import TILE_SIZE



class Tile_gui (Tile) :
    def __init__(self, id):
        self.rect = [
            (id[0] * TILE_SIZE, id[1] * TILE_SIZE),
            (id[0] * TILE_SIZE + TILE_SIZE, id[1] * TILE_SIZE),
            (id[0] * TILE_SIZE + TILE_SIZE, id[1] * TILE_SIZE + TILE_SIZE),
            (id[0] * TILE_SIZE, id[1] * TILE_SIZE + TILE_SIZE)
        ]

        self.iso = [self.cart_to_iso(id[0], id[1]) for id[0], id[1] in self.rect]


class World:
    def __init__(self,x,y): #x et y dimensions du monde
        self.x=x
        self.y=y
        self.dico={} #à chaque clé sera associé une Tuile
        #les clés du dico seront de la forme (x,y)
        self.units=[] #every unit on the map, a list seems better to me

    def creer_monde(self): #remplit de Tuile le dico du monde
        for x in range(self.x):
            for y in range(self.y):
                cle=(x,y)
                self.dico[cle]=Tile(cle)

    def afficher_console(self):
        self.update_unit_presence() #updates this everytime we print the map
        for x in range(self.x):
            for y in range(self.y):
                print(self.dico[(x, y)].affiche(),end="") #This one works
            print("",end="\n")

    def afficher_route_console(self,route):
        self.update_unit_presence() #updates this everytime we print the map
        for x in range(self.x):
            for y in range(self.y):
                if (x,y) in route:
                    print("-", end="")
                else:
                    print(self.dico[(x, y)].affiche(),end="") #This one works

            print("",end="\n")
            
    def update_unit_presence(self):
        for x in range(self.x): #resets every tile's unit list
            for y in range(self.y):
                self.dico[(x,y)].unites=[]
        for u in self.units: #puts every unit in their tile's unit list
            key=intkey(u.position)
            self.dico[key].unites.append(u)

    def convertMapToGrid(self):
        array_shape = (self.x, self.y)
        binary_array = np.zeros(array_shape, dtype=int)
        for i, (key, value) in enumerate(self.dico.items()):
            binary_array[key[0], key[1]] = 0 if value.contains == " " else 1
        return binary_array

def intkey(key): #turns a float key into an int key for dict indexation
    return (int(key[0]),int(key[1]))

'''
monde=Monde(5,20)
monde.creer_monde()

for i in range(1,3):
    for j in range(4,13):
        monde.dico[(i,j)]=wood

for j in range(2,9):
    monde.dico[(4,j)]=gold

monde.afficher_console()
'''