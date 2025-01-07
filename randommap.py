# Old functions to generate maps
'''
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
        placer(monde,(x,y),Wood())
        placer(monde,(monde.x-1-x,monde.y-1-y),Wood()) #symétrie centrale
    #blocs de gold
    for i in range(1 + richesse):
        x = randint(0, monde.x - 1)
        y = randint(0, monde.y - 1)
        placer(monde, (x, y), Gold(),30)
        placer(monde, (monde.x-1-x,monde.y-1-y), Gold(), 30)
    #gold au centre
    placer(monde, (monde.x // 2, monde.y // 2), Gold(), 80)
'''

from models.World import World
from random import randint
from models.ressources.ressources import Wood,Gold

#function, returns the sum of two tuples
def sum_tuple(t1,t2):
    return (t1[0]+t2[0],t1[1]+t2[1])

#function, on a world, places a cluster of one resource starting from a specific key
#it grows from the center, based on a replication chance and a fading factor
def cluster(world,resource,key,repl=50,fade=16): #key is a tuple please
    #places the original resource
    world.tiles_dico[key].contains = resource
    #tries placing more next to it
    for i in range(-1,2):
        for j in range(-1,2):
            if randint(0,100)<repl:
                newkey = sum_tuple(key,(i,j))
                if newkey[0]>=0 and newkey[0]<world.width and newkey[1]>=0 and newkey[1]<world.height:
                    cluster(world,resource,newkey,repl-fade)

#function that takes a big dict {"X":self.x, "Y": self.y, "q" : self.ressources_quantities, "n" : self.nb_joueur, "b" : self.ai_behavior, "t" : self.type_map }
#and returns a randomly generated World that follows the information
def random_world(dict):
    newworld = World(dict["X"],dict["Y"])
    maptype = dict["t"]
    wealth = int(newworld.width*newworld.height / 3600) # = 4 for a 120x120 , wealth allows resources to scale with map size
    if maptype == "Arabia": #Medium clusters of wood, open center
        for _ in range(0,wealth+2): #Some wood on the outskirts
            number = randint(1,8)
            x = randint(0,newworld.width//number) ; y = randint(0,newworld.height//(9-number))
            cluster(newworld,Wood(newworld),(x,y)) ; cluster(newworld,Wood(newworld),(newworld.width-x-1,y))
            cluster(newworld,Wood(newworld),(newworld.width-x-1,newworld.height-y-1)) ; cluster(newworld,Wood(newworld),(x,newworld.height-y-1))
        for _ in range(0,wealth+2): #Some lil wood
            x = randint(0,newworld.width//3) ; y = randint(0,newworld.height//3)
            cluster(newworld,Wood(newworld),(x,y),50,25) ; cluster(newworld,Wood(newworld),(newworld.width-x-1,y),50,25)
            cluster(newworld,Wood(newworld),(newworld.width-x-1,newworld.height-y-1),50,25) ; cluster(newworld,Wood(newworld),(x,newworld.height-y-1),50,25)
        for _ in range(0,wealth): #Some gold
            x = randint(0,int(newworld.width/2.5)) ; y = randint(0,int(newworld.height/2.5))
            cluster(newworld,Gold(newworld),(x,y),50,25) ; cluster(newworld,Gold(newworld),(newworld.width-x-1,y),50,25)
            cluster(newworld,Gold(newworld),(newworld.width-x-1,newworld.height-y-1),50,25) ; cluster(newworld,Gold(newworld),(x,newworld.height-y-1),50,25)
    elif maptype == "GoldRush": #Most gold in the center
        ()
    else:
        ()

    return newworld

test = random_world({"X":120,"Y":120,"q":3,"t":"Arabia"})
#test.show_world()

cluster(test,Wood(test),(5,5))
test.show_world()