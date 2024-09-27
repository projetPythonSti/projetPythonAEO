#Créé par Max le 27/09/2024

from mmonde import *
from random import *

def somme(t1,t2): #somme((1,1),(2,2))=(3,3)
    total=()
    for i in range(0,len(t1)):
        total+=(t1[i]+t2[i],) #virgule permet d'avoir un tuple
    return total

def placer(monde,cle,ressource): #place un cluster d'une ressource autour d'une tuile
    #place le bloc initial
    monde.dico[cle]=ressource
    #place peut être à côté, récursif
    for i in range(-1,2):
        for j in range(-1,2):
            if(randint(0,100)>85):
                placer(monde,somme((i,j),cle),ressource)

def randomise(monde): #prend un monde, fait placer() plusieurs fois sur des cercles autour du centre
    x_centre=monde.x//2
    y_centre=monde.y//2

'''
print(somme((1,1),(2,2)))

'''