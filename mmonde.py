from mressources import *
from Unity import *
import numpy as np
from models.buildings.buildings import *

from utils.setup import TILE_SIZE

class Tile:
    def __init__(self,id): #id c'est le tuple (x,y)
        self.id=id
        self.contains= " " #représente une tuile sans ressources, sera remplacé par une instance de Ressource
        #il suffira de changer le __repr__ de Ressource pour afficher la lettre correspondant à la ressource
        self.unites=[]

    def __repr__(self):
        if self.unites!=[]:
            return self.unites[0].name[0].lower() #lowered first letter of the first unit on the tile
        return self.contains #ressource

    def affiche(self): #magic method repr wasn't doing me right, made a non-magic method    #KillAllWizards
        if self.unites!=[]:
            return self.unites[0].name[0].lower() #lowered first letter of the first unit on the tile
        return self.contains #ressource

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

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
        self.units = []  # unités de toute la map
        self.buildings = []  # batiments de toute la map

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

    #thoses two bastards below should only be used in extreme cases
    #in an ideal world, units and buildings will update themselves
    def update_unit_presence(self):
        for x in range(self.x): #resets every tile's unit list
            for y in range(self.y):
                self.dico[(x,y)].unites=[]
        for u in self.units: #puts every unit in their tile's unit list
            key=floatkey_to_intkey(position_to_tuple(u.position))
            self.dico[key].unites.append(u)
    #this one fucker shall not be used, for it tempers with the actual gameplay
    def update_build_presence(self):
        for u in self.buildings: #puts every building in the tile's contain they are in
            for v in u.tiles_occupied:
                key=floatkey_to_intkey(position_to_tuple(u.position))
                self.dico[v].contains = u

    def convertMapToGrid(self):
        array_shape = (self.x, self.y)
        binary_array = np.zeros(array_shape, dtype=int)
        for i, (key, value) in enumerate(self.dico.items()):
            binary_array[key[0], key[1]] = 0 if value.contains == " " else 1
        return binary_array

    def spawn_unit(self, unitclass, team, x, y):
        new_unit = unitclass(1, team)
        new_unit.position = Position(x, y)
        self.units.append(new_unit)
        return new_unit

    def spawn_building(self, buildclass, team, x, y):
        new_build = buildclass()
        new_build.position = Position(x, y)
        new_build.grid_x = new_build.position.getX()
        new_build.grid_y = new_build.position.getY()
        new_build.update_tiles_occupied()
        self.buildings.append(new_build)
        return new_build

def floatkey_to_intkey(key): #turns a float key into an int key for dict indexation
    return (int(key[0]),int(key[1]))

def position_to_tuple(position):
    return (position.getX(),position.getY())

from math import sqrt

def dist(pos1,pos2): #gives the distance between two positions
    return sqrt(abs(pos2.getX()-pos1.getX())**2+abs(pos2.getY()-pos1.getY())**2)

def closest_position(my_pos,list_pos): #finds the closest position between a position and a list of position
    closest = list_pos[0]
    for i in list_pos[1:]:
        if dist(my_pos,i) < dist(my_pos,closest): #position plus proche trouvée
            closest = i
    return closest

print("dist entre 0,0 et 2,2 = ",dist(Position(0,0),Position(2,2)))
print("dist entre 4,4 et 2,2 = ",dist(Position(4,4),Position(2,2)))
print("position la plus proche à 2,2 est ",position_to_tuple(closest_position(Position(2,2),[Position(0,0),Position(1,3),Position(5,5)])))