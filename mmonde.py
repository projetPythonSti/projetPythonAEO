from mressources import *
from Unity import *

class Tile:
    def __init__(self,id): #id c'est le tuple (x,y)
        self.id=id
        self.contains=" " #représente une tuile sans ressources, sera remplacé par une instance de Ressource
        #il suffira de changer le __repr__ de Ressource pour afficher la lettre correspondant à la ressource
        self.unites=[] #a list might be more relevant

    def __repr__(self):
        if self.unites!=[]:
            return self.unites[0][0].lower() #lowered first letter of the first unit on the tile
        return self.contains #ressource

class Monde:
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
                print(self.dico[(x,y)].contains,end="")
            print("",end="\n")

    def update_unit_presence(self):
        for x in range(self.x): #resets every tile's unit list
            for y in range(self.y):
                self.dico[(x,y)].contains={}
        for u in self.units: #puts every unit in their tile's unit list
            key=intkey(u.position)
            self.dico[key].unites.append(u)

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