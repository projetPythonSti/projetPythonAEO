#Créé par Max le 27/09/2024
from mressources import *
from Unity import *
from setup import TILE_SIZE

class Tile:
    def __init__(self,id): #id c'est le tuple (x,y)
        self.id=id
        self.contains=" " #représente une tuile sans ressources, sera remplacé par une instance de Ressource
        #il suffira de changer le __repr__ de Ressource pour afficher la lettre correspondant à la ressource
        self.unites=[] #a list might be more relevant
        self.rect = [
            (id[0] * TILE_SIZE, id[1] * TILE_SIZE),
            (id[0] * TILE_SIZE + TILE_SIZE, id[1] * TILE_SIZE),
            (id[0] * TILE_SIZE + TILE_SIZE, id[1] * TILE_SIZE + TILE_SIZE),
            (id[0] * TILE_SIZE, id[1] * TILE_SIZE + TILE_SIZE)
        ]

        #self.iso = [self.cart_to_iso(id[0], id[1]) for id[0], id[1] in self.rect]S

    def __repr__(self):
        if len(self.unites) != 0:
            return self.unites[0].name[0] #First letter of the first unit class name
        return self.contains

    def affichage_magique(self):
        if len(self.unites) != 0:
            return self.unites[0].name[0].lower() #First letter of the first unit class name
        return self.contains

    def cart_to_iso (self, x, y):
        iso_x = x-y
        iso_y = (x + y)/2
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


class World :
    def __init__(self,x,y): #x et y dimensions du monde
        self.x=x
        self.y=y
        self.dico={} #à chaque clé sera associé une Tuile
        #les clés du dico seront de la forme (x,y)
        self.units=[] #unités de toute la map

    def creer_monde(self): #remplit de Tuile le dico du monde
        for x in range(self.x):
            for y in range(self.y):
                cle=(x,y)
                self.dico[cle]=Tile(cle)

    def afficher_console(self):
        for x in range(self.x):
            for y in range(self.y):
                print(self.dico[(x,y)].affichage_magique(),end="")
            print("",end="\n")

    def update_unit_presence(self):
        for x in range(self.x): #resets every tile's unit list
            for y in range(self.y):
                self.dico[(x,y)].unites=[]
        for u in self.units: #puts every unit in their tile's unit list
            key=intkey(u.position)
            self.dico[key].unites.append(u)

def intkey(key): #turns a float key into an int key for dict indexation
    return (int(key[0]),int(key[1]))



monde=World(5,20)
monde.creer_monde()

'''
for i in range(1,3):
    for j in range(4,13):
        monde.dico[(i,j)]=Wood

for j in range(2,9):
    monde.dico[(4,j)]=Gold

monde.afficher_console()


'''
