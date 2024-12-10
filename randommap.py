from mmonde import *
from random import *
from models.buildings.town_center import TownCenter
from models.unity.Archer import Archer
from Unity import *
from models.unity.Villager import Villager

def somme(t1,t2): #somme((1,1),(2,2))=(3,3)
    total=()
    for i in range(0,len(t1)):
        total+=(t1[i]+t2[i],) #virgule permet d'avoir un tuple
    return total

def placer(monde,cle,ressource,chance=50,reduction=16): #place un cluster d'une ressource autour d'une tuile d'un monde
    #place le bloc initial
    monde.dico[cle].contains=ressource
    #place peut être à côté, récursif
    for i in range(-1,2):
        for j in range(-1,2):
            if(randint(0,100)<=chance): #50% réplication -16% à chaque réplication
                newkey=somme((i,j),cle)
                if newkey[0]>=0 and newkey[0]<monde.x and newkey[1]>=0 and newkey[1]<monde.y:
                    placer(monde,newkey,ressource,chance-reduction)
#randomise pourrait être remplacé par une fonction de la même forme pour chaque archetype de maps (arabia,
def randomise(monde,richesse): #prend un monde, place des clusters de ressources sur un cercle, +de clusters selon la richesse
    #blocs de wood
    for i in range(5+richesse*2):
        x=randint(0,monde.x-1)
        y=randint(0,monde.y-1)
        placer(monde,(x,y),Wood())
        placer(monde,(monde.x-1-x,monde.y-1-y),Wood()) #symétrie centrale
    #blocs de gold
    for i in range(1 + richesse):
        x = randint(0, monde.x - 1)
        y = randint(0, monde.y - 1)
        placer(monde, (x, y), Gold(),30)
        placer(monde, (monde.x-1-x,monde.y-1-y), Gold(), 30, 9)
    #gold au centre
    placer(monde, (monde.x // 2, monde.y // 2), Gold(), 80,40)
    #clear some space for town centers, far from center
    x = randint(1, (monde.x - 1) // 3)
    y = randint(1, (monde.y - 1) // 3)
    for i in range(-1,5):
        for j in range(-1,5):
            monde.dico[x+i,y+j].contains=" "
            monde.dico[monde.x-x-i-1, monde.y-y-j-1].contains = " "
    #towns centers not adjacent to borders
    monde.spawn_building(TownCenter,"blue",x,y)
    monde.spawn_building(TownCenter, "red", monde.x-x-4, monde.y-y-4)
    #villagers adjacent to town centers
    monde.spawn_unit(Archer,"blue",x,y+4)
    monde.spawn_unit(Archer, "blue", x + 1, y+4)
    monde.spawn_unit(Archer, "blue", x + 2, y+4)
    monde.spawn_unit(Archer, "red", monde.x-x-4, monde.y-y-5)
    monde.spawn_unit(Archer, "red", monde.x-x-3, monde.y-y-5)
    monde.spawn_unit(Archer, "red", monde.x-x-2, monde.y-y-5)

'''
print(somme((1,1),(2,2)))

'''

