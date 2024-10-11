#Créé par Max le 27/09/2024

from mmonde import *
from random import *

def somme(t1,t2): #somme((1,1),(2,2))=(3,3)
    total=()
    for i in range(0,len(t1)):
        total+=(t1[i]+t2[i],) #virgule permet d'avoir un tuple
    return total

def placer(monde,cle,ressource,chance=50): #place un cluster d'une ressource autour d'une tuile d'un monde
    #place le bloc initial
    monde.dico[cle].contains=ressource
    #place peut être à côté, récursif
    for i in range(-1,2):
        for j in range(-1,2):
            if(randint(0,100)<=chance): #50% réplication -16% à chaque réplication
                newkey=somme((i,j),cle)
                if newkey[0]>=0 and newkey[0]<monde.x and newkey[1]>=0 and newkey[1]<monde.y:
                    placer(monde,newkey,ressource,chance-16)
#randomise pourrait être remplacé par une fonction de la même forme pour chaque archetype de maps (arabia,
def randomise(monde,richesse): #prend un monde, place des clusters de ressources sur un cercle, +de clusters selon la richesse
    #blocs de wood
    for i in range(5+richesse*2):
        x=randint(0,monde.x-1)
        y=randint(0,monde.y-1)
        placer(monde,(x,y),wood)
        placer(monde,(monde.x-1-x,monde.y-1-y),wood) #symétrie centrale
    #blocs de gold
    for i in range(1 + richesse):
        x = randint(0, monde.x - 1)
        y = randint(0, monde.y - 1)
        placer(monde, (x, y), gold,30)
        placer(monde, (monde.x-1-x,monde.y-1-y), gold, 30)
    #gold au centre
    placer(monde, (monde.x // 2, monde.y // 2), gold, 80)

'''
print(somme((1,1),(2,2)))

'''

