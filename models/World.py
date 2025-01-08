import numpy as np
import json

from models.buildings.town_center import TownCenter
from models.maps.Tile import  Tile
from models.model import Model  # delete it after finish testing the class World
from models.unity.Villager import Villager  # delete it after finish testing the class World
from models.ressources.ressources import Gold, Wood, Food, Ressource
from collections import defaultdict
import random as rd
import os

from models.Position import Position

class World:


    """
        22/12/2024 : J'ai apporté des modifications à ce fichier @tahakhetib sur ce que @amadou_yaya_diallo a écrit
            - Réglé les erreurs d'exécution lors de l'appel à la fonction remove_element, passage de monde à self
            - changé la manière dont on traite les tiles remplies
            - Décommenté la fonction convertMapToGrid afin de la réutiliser avec GameManager
        26/12/2024@tahakhetib : J'ai apporté des modifs sur ce que @amadou_yaya_diallo
            - Changé le type de l'attribut filled_tiles vers un dictionnaire
            - Modifié les fonctions place_element() et remove_element() pour qu'elle s'adapte au changement de filled_tiles
        02/01/2025@tahakhetib : J'ai apporté des modifications sur ce que @amadou_yaya_diallo a écrit
            - Passé le type des éléments du dictionnaire de tiles_dico à Tiles
        08/01/2025@mgirardo : J'ai inversé x et y pour corriger show_world(). ATTENTION à VOS X ET Y
    """
    def __init__(self, width, height):  # dict of villages in the world
        self.width = width
        self.height = height
        self.villages = list() #c'est les équipes
        self.ressources = defaultdict(dict)
        self.tiles_dico = defaultdict(int)  # à chaque clé sera associé une Tuile
        self.filled_tiles = defaultdict(tuple)  #
        self.initialise_world()
        # les clés du dico seront de la forme (x,y)
        # self.units  #every unit on the map, a list seems better to me

    def initialise_world(self): #emplit de Tuile le dico du monde
        for x in range(self.width):
            for y in range(self.height):
                self.tiles_dico[(x,y)] = Tile()

    def add_village(self, village):
        self.villages.append(village)

    def fill_ressources(self, max_ressource):
        for i in range(rd.randint(0, max_ressource)):
           self.ressources["w"][str(i)] = Wood(world=self)

        for i in range(rd.randint(0, max_ressource//2)):
           self.ressources["g"][str(i)] = Gold(world=self)

        # for i in range(rd.randint(0, max_ressource)):
        #    self.ressources["f"][str(i)] = Food(world=self)

        self.place_ressources()

    def get_ressources(self):
        return self.ressources

    def place_ressources(self):
        for w, g in zip(self.ressources["w"].values(), self.ressources["g"].values()):
            self.place_element(w)
            self.place_element(g)
            # self.place_element(fo)


    def fill_world(self):
        village1, village2 = self.villages
        # iterating on 2 dict at the same time
        for pop1, pop2 in zip(village1.population().values(), village2.population().values()):
            for v1, v2 in zip(pop1.values(), pop2.values()):
                self.place_element(v1)
                self.place_element(v2)

    def show_world(self): #
        for y in range(self.height):
            for x in range(self.width):
                print(self.tiles_dico[(x, y)], end="")
            print("", end="\n")

    # shows a part of the world, works with two position found in the game's loop
    def show_precise_world(self,upleft:Position,downright:Position):
        print()
        if upleft.getY()>0:
            print(' '+(downright.getX()-upleft.getX())*'ʌ')
        for y in range(upleft.getY(),downright.getY(),1):
            if upleft.getX()>0:
                print('<', end='')
            for x in range(upleft.getX(),downright.getX(),1):
                print(self.tiles_dico[(x, y)], end="")
            if downright.getX()<self.width:
                print('>', end='')
            print("", end="\n")
        if downright.getY()<self.height:
            print(' '+(downright.getX()-upleft.getX())*'v')
        print("upleft.getX = ", upleft.getX(), " upleft.getY = ", upleft.getY())


    '''
    def show_precise_world(self,upleft:Position,downright:Position):
        print()
        if upleft.getX()>0:
            print(' '+(downright.getY()-upleft.getY())*'ʌ')
        for x in range(upleft.getX(),downright.getX(),1):
            if upleft.getY()>0:
                print('<',end='')
            for y in range(upleft.getY(),downright.getY(),1):
                print(self.tiles_dico[(x, y)], end="")
            if downright.getY()<self.width:
                print('>',end='')
            print("", end="\n")
        if downright.getX()<self.height:
            print(' '+(downright.getY()-upleft.getY())*'v')
        # print(f"downright.getX() == {downright.getX()} self.height == {self.height}",end=' ')
        print("upleft.getX = ",upleft.getX()," upleft.getY = ",upleft.getY())
    '''

    def place_element(self, element):
        place = (element.position.getX(), element.position.getY())
        if (place not in self.filled_tiles.values()):
            self.tiles_dico[place].set_contains(element)
            self.filled_tiles[place] = place
            # update the view of the element

    def remove_element(self, element):
        place = (element.position.getX(), element.position.getY())
        self.tiles_dico[place].set_contains(None)
        self.filled_tiles.pop(place)
        if (type(element) == Ressource or type(element) == Wood or type(element) == Food or type(element) == Gold):
            self.ressources[element.name.lower()].pop(str(element.uid))

        # update the view of the element

    # def afficher_console(self):
    #     # self.update_unit_presence() #updates this everytime we print the map
    #     for x in range(self.x):
    #         for y in range(self.y):
    #             print(self.dico[(x, y)].affiche(),end="") #This one works
    #         print("",end="\n")

    # def afficher_route_console(self,route):
    #     self.update_unit_presence() #updates this everytime we print the map
    #     for x in range(self.x):
    #         for y in range(self.y):
    #             if (x,y) in route:
    #                 print("-", end="")
    #             else:
    #                 print(self.dico[(x, y)].affiche(),end="") #This one works

    #         print("",end="\n")

    # def update_unit_presence(self):
    #     for x in range(self.x): #resets every tile's unit list
    #         for y in range(self.y):
    #             self.dico[(x,y)].unites=[]
    #     for u in self.units: #puts every unit in their tile's unit list
    #         key= self.intkey(u.position)
    #         self.dico[key].unites.append(u)

    def convertMapToGrid(self):
        array_shape = (self.width+1, self.height+1)
        binary_array = np.zeros(array_shape, dtype=int)
        for i, (key, value) in enumerate(self.tiles_dico.items()):
            binary_array[key[0], key[1]] = 0 if value.contains == None else 1
        return binary_array

    """Les deux fonction qui suivent sont utilisées pour la sauvegarde et ne sont pas à utiliser seule """
    def to_dict (self):
        return {"width" : self.width, "height" : self.height, "villages" : { v.name : v.to_dict() for v in self.villages }, "ressources" : { k1 : {k2 : self.ressources[k1][k2].to_dict() for k2 in self.ressources[k1].keys()} for k1 in self.ressources.keys()}}

    def to_json(self, file_name=None):
        """Convert object to JSON and optionally save to file."""
        data = self.to_dict()
        if file_name:
            with open("saves/"+file_name, "w") as f:
                json.dump(data, f, indent=4)
        return json.dumps(data, indent=4)

    #def intkey(key): #turns a float key into an int key for dict indexation
    #     return (int(key[0]),int(key[1]))


if __name__ == "__main__":
    monde = World(100, 100)
    village1 = Model("fabulous", monde)
    village2 = Model("hiraculous", monde)
    village1.initialize_villages(1,2,3, gold=200, wood=400, food=300, town_center=1, keeps=2, houses=5, camps=3)
    village2.initialize_villages(4,5,6, gold=2, wood=1, food=3, barracks=1, archery_ranger=3, stables=3, farms=2)
    v = Villager(village1)
    village1.add_unit(v)
    v.ressources_dict["w"] = 3
    v.ressources_dict["g"] = 2
    town_center = TownCenter(village1)
    village1.add_unit(town_center)
    monde.fill_world()
    monde.fill_ressources(10)
    print(village1.population())
    print(monde.get_ressources())
    print("Before : ", village1.get_ressources())
    fo = monde.get_ressources()["fo"]["0"]
    v.drop_ressources()
    v.collect(fo)
    print("After : ", village1.get_ressources())
    print(v.ressources_dict)
    # print(village2.population())
    # print(monde.get_ressources())
    # print(sorted(monde.filled_tiles, key=lambda x: x[0]), len(monde.filled_tiles))
    monde.show_world()
    # village1.remove_unit(town_center)
    # print(town_center.get_occupied_tiles())
    # print(sorted(set(monde.filled_tiles) & set(town_center.get_occupied_tiles()), key=lambda x: (x[0], x[1])))
    monde.remove_element(town_center)
    print("After removing town center")
    monde.show_world()
