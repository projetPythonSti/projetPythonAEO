import numpy as np
from models.maps.Tile import  Tile
from models.model import Model  # delete it after finish testing the class World
from models.unity.Villager import Villager  # delete it after finish testing the class World
from models.ressources.ressources import Gold, Wood, Food, Ressource
from collections import defaultdict
import random as rd


class World:


    """
        22/12/2024 : J'ai apporté des modifications à ce fichier @tahakhetib sur ce que @amadou_yaya_diallo a écrit
            - Réglé les erreurs d'exécution lors de l'appel à la fonction remove_element, passage de monde à self
            - changé la manière dont on traite les tiles remplies
            - Décommenté la fonction convertMapToGrid afin de la réutiliser avec GameManager
        26/12/2024@tahakhetib : J'ai apporté des modifs sur ce que @amadou_yaya_diallo
            - Changé le type de l'attribut filled_tiles vers un dictionnaire
            - Modifié les fonctions place_element() et remove_element() pour qu'elle s'adapte au changement de filled_tiles
    """
    def __init__(self, width, height):  # dict of villages in the world
        self.width = width
        self.height = height
        self.villages = list()
        self.ressources = defaultdict(dict)
        self.tiles_dico = defaultdict(int)  # à chaque clé sera associé une Tuile
        self.filled_tiles = defaultdict(tuple)  #
        self.initialise_world()
        # les clés du dico seront de la forme (x,y)
        # self.units  #every unit on the map, a list seems better to me

    def initialise_world(self):  # emplit de Tuile le dico du monde
        for x in range(self.width + 1):
            for y in range(self.height + 1):
                self.tiles_dico[(x, y)] = Tile()

    def add_village(self, village):
        self.villages.append(village)

    def fill_ressources(self, max_ressource):
        for i in range(rd.randint(0, max_ressource)):
            self.ressources["w"][str(i)] = Wood(world=self)

        for i in range(rd.randint(0, max_ressource // 2)):
            self.ressources["g"][str(i)] = Gold(world=self)

        for i in range(rd.randint(0, max_ressource)):
            self.ressources["fo"][str(i)] = Food(world=self)

        self.place_ressources()

    def get_ressources(self):
        return self.ressources

    def place_ressources(self):
        for w, g, fo in zip(self.ressources["w"].values(), self.ressources["g"].values(),
                            self.ressources["fo"].values()):
            self.place_element(w)
            self.place_element(g)
            self.place_element(fo)

    def fill_world(self):
        village1, village2 = self.villages
        # iterating on 2 dict at the same time
        for pop1, pop2 in zip(village1.population().values(), village2.population().values()):
            for v1, v2 in zip(pop1.values(), pop2.values()):
                self.place_element(v1)
                self.place_element(v2)

    def show_world(self):
        for x in range(self.width + 1):
            for y in range(self.height + 1):
                print(self.tiles_dico[(x, y)], end=" ")
            print("", end="\n")

    def place_element(self, element):
        place = (element.position.getX(), element.position.getY())
        if (place not in self.filled_tiles.values()):
            print("adding element")
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

    # def intkey(key): #turns a float key into an int key for dict indexation
    #     return (int(key[0]),int(key[1]))


if __name__ == "__main__":
    monde = World(100, 100)
    village1 = Model("fabulous", monde)
    village2 = Model("hiraculous", monde)
    village1.initialize_villages(1, 2, 3, gold=200, wood=100, food=300)
    village2.initialize_villages(4, 5, 6, gold=2, wood=1, food=3)
    v = Villager(village1)
    village1.add_unit(v)
    v.ressources_dict["w"] = 3
    v.ressources_dict["g"] = 2
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
    print(monde.get_ressources())
    # print(monde.filled_tiles, len(monde.filled_tiles))
    # monde.show_world()

