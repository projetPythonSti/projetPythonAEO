from wcwidth import wcwidth

from models.AIPlayer import ResourceTypeENUM
from models.World import World
from random import randint

from models.buildings.town_center import TownCenter
from models.ressources.ressources import Wood,Gold
from models.unity.Villager import Villager


#function, returns the sum of two tuples
def sum_tuple(t1,t2):
    return (t1[0]+t2[0],t1[1]+t2[1])

"""
                24/01/2025@tahakhetib : J'ai ajouté des chose sur ce que @maxgigi à écrit
                    -Ajouté l'ajout des ressources dans le dictionnaire des ressources du monde
                        Afin que cela fonctionne correctement, j'ai également crée une nouvelle ressource à partir de celle passée en paramètre 
                        pour éviter qu'elle en écrase une autre dans le dictionnaire des ressources
"""


#function, on a world, places a cluster of one resource starting from a specific key
#it grows from the center, based on a replication chance and a fading factor
def cluster(world,resource,key,repl=50,fade=16): #key is a tuple please
    resKeys = list(world.ressources[resource.name].keys())
    newResource = None
    if resource.name == "w":
        newResource = Wood(world)
        newResource.position=Position(key[0],key[1])
        if len(resKeys)==0:
            pass
        else:
            newResource.uid = f"{int(resKeys[-1])+1}"
    elif resource.name == "g":
        newResource = Gold(world)
        newResource.position = Position(key[0], key[1])
        if len(resKeys) == 0:
            pass
        else:
            newResource.uid = f"{int(resKeys[-1]) + 1}"

    #checks position ok
    if key[0] >= 0 and key[0] < world.width and key[1] >= 0 and key[1] < world.height:
        #places the original resource
        world.tiles_dico[key].contains = newResource
        world.ressources[newResource.name][newResource.uid] = newResource
        #tries placing more next to it
        for i in range(-1,2):
            for j in range(-1,2):
                if randint(0,100)<repl:
                    newkey = sum_tuple(key,(i,j))
                    if newkey[0]>=0 and newkey[0]<world.width and newkey[1]>=0 and newkey[1]<world.height:
                        cluster(world,newResource,newkey,repl-fade)

#function that takes a big dict {"X":self.x, "Y": self.y, "q" : self.ressources_quantities, "n" : self.nb_joueur, "b" : self.ai_behavior, "t" : self.type_map }
#and returns a randomly generated World that follows the information

#function that takes a map name, returns a World
#supported maps : "Arabia", "GoldRush",
def random_world(dict):
    newworld = World(dict["X"],dict["Y"])
    maptype = dict["t"]
    wealth = int(newworld.width*newworld.height / 4800) # = 3 for a 120x120 , wealth allows resources to scale with map size
    if maptype == "g": #Most gold in the center
        for _ in range(0, wealth + 2):  # Some wood on the outskirts
            number = randint(1, 8)
            x = randint(0, newworld.width // number); y = randint(0, newworld.height // (9 - number))
            cluster(newworld, Wood(newworld), (x, y)); cluster(newworld, Wood(newworld), (newworld.width - x - 1, y))
            cluster(newworld, Wood(newworld), (newworld.width - x - 1, newworld.height - y - 1)); cluster(newworld, Wood(newworld), (x, newworld.height - y - 1))
        for _ in range(0, wealth + 2):  # Some lil wood
            x = randint(0, newworld.width // 3); y = randint(0, newworld.height // 3)
            cluster(newworld, Wood(newworld), (x, y), 50, 25); cluster(newworld, Wood(newworld), (newworld.width - x - 1, y), 50, 25)
            cluster(newworld, Wood(newworld), (newworld.width - x - 1, newworld.height - y - 1), 50, 25); cluster(newworld, Wood(newworld), (x, newworld.height - y - 1), 50, 25)
        for _ in range(0, wealth):  # Some gold in the center
            x = randint(newworld.width // 4, newworld.width//2); y = randint(newworld.height//4, newworld.height//2)
            cluster(newworld, Gold(newworld), (x, y), 50, 25); cluster(newworld, Gold(newworld), (newworld.width - x - 1, y), 50, 25)
            cluster(newworld, Gold(newworld), (newworld.width - x - 1, newworld.height - y - 1), 50, 25); cluster(newworld, Gold(newworld), (x, newworld.height - y - 1), 50, 25)
    else: #Arabia, Medium clusters of wood, open center
        for _ in range(0, wealth + 1):  # Some wood on the outskirts
            number = randint(1, 6)
            x = randint(0, newworld.width // number);
            y = randint(0, newworld.height // (7 - number))
            cluster(newworld, Wood(newworld), (x, y));
            cluster(newworld, Wood(newworld), (newworld.width - x - 1, y))
            cluster(newworld, Wood(newworld), (newworld.width - x - 1, newworld.height - y - 1));
            cluster(newworld, Wood(newworld), (x, newworld.height - y - 1))
        for _ in range(0, wealth + 4):  # Some lil wood
            x = randint(0, newworld.width // 2);
            y = randint(0, newworld.height // 2)
            cluster(newworld, Wood(newworld), (x, y), 50, 30);
            cluster(newworld, Wood(newworld), (newworld.width - x - 1, y), 50, 30)
            cluster(newworld, Wood(newworld), (newworld.width - x - 1, newworld.height - y - 1), 50, 30);
            cluster(newworld, Wood(newworld), (x, newworld.height - y - 1), 50, 30)
        for _ in range(0, wealth):  # Some gold around the world
            x = randint(0, int(newworld.width / 2.5));
            y = randint(0, int(newworld.height / 2.5))
            cluster(newworld, Gold(newworld), (x, y), 50, 25);
            cluster(newworld, Gold(newworld), (newworld.width - x - 1, y), 50, 25)
            cluster(newworld, Gold(newworld), (newworld.width - x - 1, newworld.height - y - 1), 50, 25);
            cluster(newworld, Gold(newworld), (x, newworld.height - y - 1), 50, 25)

    return newworld

#function that makes teams according to number and starting resources
from models.model import Model
def make_teams(dict,world):
    for n in range(1,dict["n"]+1):
        team = Model(str(n),world)
        if dict["q"]=="p": #Lean
            team.initialize_villages(gold=50,wood=200,food=50,villages=3)
        elif dict["q"]=="m": #Mean
            team.initialize_villages(gold=2000, wood=2000, food=2000,villages=3)
        else: #Marines
            team.initialize_villages(gold=20000, wood=20000, food=20000,villages=15)

#function that clears some space for the TCs and places those, and some starting villagers
from models.Position import Position
def place_tcs(dict,world):
    #values for placement
    x = randint(12, world.width//3-12)
    y = randint(12, world.height//3-12)
    ''' makes it so team1 doesn't always spawn top left, commented for debugging issues
    n = randint(1,4)
    if n%2==0:
        x=world.width-x
    if n>=3:
        y=world.height-y
    '''
    #clears space
    for j in range(y-2, y + 14):
        for i in range(x-2, x + 14):
            world.tiles_dico[(i,j)].contains=None
            world.tiles_dico[(world.width-i,world.height-j)].contains=None
            if dict["n"]>=3:
                world.tiles_dico[(i, world.height - j)].contains = None
            if dict["n"]>=4:
                world.tiles_dico[(world.width - i,j)].contains = None
            if dict["n"]>=5:
                world.tiles_dico[(world.width//2-i,j)].contains=None
            if dict["n"]>=6:
                world.tiles_dico[(world.width//2-i,world.height-j)].contains=None
            if dict["n"]>=7:
                world.tiles_dico[(i,world.height//2-j)].contains=None
            if dict["n"]>=8:
                world.tiles_dico[(world.width-i,world.height//2-j)].contains=None

    #places TCs
    tc1 = TownCenter(team=world.villages[0])
    tc1.position=Position(x+4,y+4)
    world.place_element(tc1)
    world.villages[0].community["T"][tc1.uid] = tc1
    tc2 = TownCenter(team=world.villages[1])
    tc2.position = Position(world.width-x-6,world.height-y-6)
    world.place_element(tc2)
    world.villages[1].community["T"][tc1.uid] = tc2
    if dict["n"]>=3:
        tc3 = TownCenter(team=world.villages[2])
        tc3.position = Position(x+4,world.height-y-6)
        world.place_element(tc3)
        world.villages[2].community["T"][tc3.uid] = tc3
    if dict["n"]>=4:
        tc4 = TownCenter(team=world.villages[3])
        tc4.position = Position(world.width-x-6,y+4)
        world.place_element(tc4)
        world.villages[3].community["T"][tc4.uid] = tc4
    if dict["n"]>=5:
        tc5 = TownCenter(team=world.villages[4])
        tc5.position = Position(world.width//2, y+4)
        world.place_element(tc5)
        world.villages[4].community["T"][tc5.uid] = tc5
    if dict["n"]>=6:
        tc6 = TownCenter(team=world.villages[5])
        tc6.position = Position(world.width//2, world.height - y - 6)
        world.place_element(tc6)
        world.villages[5].community["T"][tc6.uid] = tc6
    if dict["n"]>=7:
        tc7 = TownCenter(team=world.villages[6])
        tc7.position = Position(x+4, world.height//2)
        world.place_element(tc7)
        world.villages[6].community["T"][tc7.uid] = tc7
    if dict["n"]>=8:
        tc8 = TownCenter(team=world.villages[7])
        tc8.position = Position(world.width-x-6, world.height//2)
        world.place_element(tc8)
        world.villages[7].community["T"][tc8.uid] = tc8
    #re-places villagers (they got summoned by initialize villages but weren't assigned proper positions)
    j=y+1
    for id in world.villages[0].community["v"]:
        v = world.villages[0].community["v"][id]
        v.position=Position(x+1,j)
    j = world.height-y-1
    for id in world.villages[1].community["v"]:
        v = world.villages[1].community["v"][id]
        v.position = Position(world.width-x, j)
    if dict["n"] >= 3:
        j = world.height - y - 1
        for id in world.villages[2].community["v"]:
            v = world.villages[2].community["v"][id]
            v.position = Position(x+1, j)
    if dict["n"] >= 4:
        j = y+1
        for id in world.villages[3].community["v"]:
            v = world.villages[3].community["v"][id]
            v.position = Position(world.width-x, j)
    if dict["n"] >= 5:
        for id in world.villages[4].community["v"]:
            v = world.villages[4].community["v"][id]
            v.position = Position(world.width//2-2, y+2)
    if dict["n"] >= 6:
        for id in world.villages[5].community["v"]:
            v = world.villages[5].community["v"][id]
            v.position = Position(world.width//2-2, world.height-y)
    if dict["n"] >= 7:
        for id in world.villages[6].community["v"]:
            v = world.villages[6].community["v"][id]
            v.position = Position(x+2, world.height//2)
    if dict["n"] >= 8:
        for id in world.villages[7].community["v"]:
            v = world.villages[7].community["v"][id]
            v.position = Position(world.width-x, world.height//2)
    world.fill_world2() #serves units display








if __name__ == "__main__":
    test = random_world({"X":120,"Y":180,"t":"Arabia"})
    test.show_world()