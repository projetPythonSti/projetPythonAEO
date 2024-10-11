#Créé par Max le 27/09/2024
from mressources import *
from .setup import TILE_SIZE

class Tuile:
    def __init__(self,id):
        self.id=id
        self.ressource=" " #" " représente une tuile sans ressources, sera remplacé par une instance de Ressource
        #il suffira de changer le __repr__ de Ressource pour afficher la lettre correspondant à la ressource
        self.unites={} #les cles seront les ids et les valeurs seront les instances Unite
        self.rect = [
            (id[0] * TILE_SIZE, id[1] * TILE_SIZE),
            (id[0] * TILE_SIZE + TILE_SIZE, id[1] * TILE_SIZE),
            (id[0] * TILE_SIZE + TILE_SIZE, id[1] * TILE_SIZE + TILE_SIZE),
            (id[0] * TILE_SIZE, id[1] * TILE_SIZE + TILE_SIZE)
        ]
        self.iso = [self.cart_to_iso(id[0],id[1]) for id[0],id[1] in self.rect]

    def __repr__(self):
        if self.unites!={}:
            return self.unites
        return self.ressource

    def cart_to_iso (self, x, y):
        iso_x = x-y
        iso_y = (x + y)/2
        return iso_x, iso_y

class Monde:
    def __init__(self,x,y): #x et y dimensions du monde
        self.x=x
        self.y=y
        self.dico={} #à chaque clé sera associé une Tuile
        #les clés du dico seront de la forme "(0,0)"
        self.creer_monde()

    def creer_monde(self): #remplit de Tuile le dico
        for x in range(self.x):
            for y in range(self.y):
                cle=(x,y)
                self.dico[cle]=Tuile(cle)

    def afficher_console(self):
        for x in range(self.x):
            for y in range(self.y):
                print(self.dico[(x,y)],end="")
            print("",end="\n")

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