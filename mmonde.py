#Créé par Max le 27/09/2024
from mressources import *

class Tuile:
    def __init__(self,id):
        self.id=id
        self.ressource=" " #" " représente une tuile sans ressources, sera remplacé par une instance de Ressource
        #il suffira de changer le __repr__ de Ressource pour afficher la lettre correspondant à la ressource
        self.unites={} #les cles seront les ids et les valeurs seront les instances Unite

    def __repr__(self):
        if  len(self.unites) != 0:
            return self.unites
        return self.ressource

class Monde:
    def __init__(self,x,y): #x et y dimensions du monde
        self.x=x
        self.y=y
        self.dico={} #à chaque clé sera associé une Tuile
        #les clés du dico seront de la forme "0,0"

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