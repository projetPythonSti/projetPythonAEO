from models.maps.Tile import Tile
# from models.model import Model #delete it after finish testing the class World
# from models.unity.Villager import Villager #delete it after finish testing the class World
from models.buildings.buildings import Building
# from models.buildings.town_center import TownCenter #delete it after finish testing the class World
from models.ressources.ressources import Gold, Wood
from collections import defaultdict
import random as rd
import numpy as np

"""
    22/12/2024 : J'ai apporté des modifications à ce fichier @tahakhetib sur ce que @amadou_yaya_diallo a écrit
        - Réglé les erreurs d'exécution lors de l'appel à la fonction remove_element, passage de monde à self
        - changé la manière dont on traite les tiles remplies
        - Décommenté la fonction convertMapToGrid afin de la réutiliser avec GameManager
    26/12/2024@tahakhetib : J'ai apporté des modifs sur ce que @amadou_yaya_diallo
        - Changé le type de l'attribut filled_tiles vers un dictionnaire
        - Modifié les fonctions place_element() et remove_element() pour qu'elle s'adapte au changement de filled_tiles
    02/12/2024@tahakhetib : J'ai apporté des modifications sur ce que @amadou_yaya_diallo a écrit
        - Passé le type des éléments du dictionnaire de tiles_dico à Tiles
"""

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.villages = list()
        self.ressources = defaultdict(dict)
        self.tiles_dico = defaultdict(None)
        self.filled_tiles = defaultdict(tuple)
        self.initialise_world()
        # les clés du dico seront de la forme (x,y)
        # self.units  #every unit on the map, a list seems better to me

    def initialise_world(self): #emplit de Tuile le dico du monde
        for x in range(self.width):
            for y in range(self.height):
                self.tiles_dico[(x,y)] = Tile()
                
    def add_village(self, village):
        self.villages.append(village)
    
    def get_ressources(self):
        return self.ressources

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
        #iterating on 2 dicts at the same time
        for pop1, pop2 in zip(village1.population().values(), village2.population().values()):
            for v1, v2 in zip(pop1.values(), pop2.values()):
                self.place_element(v1)
                self.place_element(v2)     
    
    def show_world(self):
        for x in range(self.width):
            for y in range(self.height):
                print(self.tiles_dico[(x, y)], end="")
            print("", end="\n")
    
    def place_element(self, element):
        place = (element.position.getX(), element.position.getY())
        if place not in self.filled_tiles.values() and place[0] <= self.width and place[1] <= self.height:
            if issubclass(element.__class__, Building) and all(tile not in set(self.filled_tiles.values()) for tile in element.get_occupied_tiles()):
                #check if the building can be placed
                if element.surface[0] + place[0] <= self.width and element.surface[1] + place[1] <= self.height:
                    for x in range(element.surface[0]):
                        for y in range(element.surface[1]):
                            try:
                                self.tiles_dico[(place[0] + x, place[1] + y)].set_contains(element)
                            except KeyError:
                                pass
                            self.filled_tiles[(place[0] + x, place[1] + y)] = (place[0] + x, place[1] + y)
            elif not issubclass(element.__class__, Building):       
                self.tiles_dico[place].set_contains(element)
                self.filled_tiles[place] = place
            #update the view of the element
    
    def remove_element(self, element):
        place = (element.position.getX(), element.position.getY())
        if(issubclass(element.__class__, Building)) and all(tile in set(self.filled_tiles.values()) for tile in element.get_occupied_tiles()):
            for x in range(element.surface[0]):
                for y in range(element.surface[1]):
                    self.tiles_dico[(place[0] + x, place[1] + y)].set_contains(None)
                    self.filled_tiles.pop((place[0] + x, place[1] + y))
        elif not issubclass(element.__class__, Building):           
            self.tiles_dico[place].set_contains(None)
            self.filled_tiles.pop(place)
            # self.ressources[element.name].pop(str(element.uid))
        
        #removing element from its team also
        element.team.remove_unit(element)
        #update the view of the element
        
    def convertMapToGrid(self):
        array_shape = (self.width, self.height)
        binary_array = np.zeros(array_shape, dtype=int)
        for i, (key, value) in enumerate(self.tiles_dico.items()):
            binary_array[key[0], key[1]] = 0 if value.contains == None else 1
        return binary_array
        
if __name__ == "__main__":
    monde = World(30,50)

    village1 = Model("fabulous", monde)
    village2 = Model("hiraculous", monde)
    village1.initialize_villages(1,2,3, gold=200, wood=400, food=300, town_center=1, keeps=2, houses=5, camps=3)
    village2.initialize_villages(4,5,6, 2, 1, gold=2, wood=1, food=3, barracks=1, archery_ranger=3, stables=3, farms=2)
    # v = Villager(village1)
    # village1.add_unit(v)
    # v.ressources_dict["w"] = 3
    # v.ressources_dict["g"] = 2
    town_center = TownCenter(village1)
    village1.add_unit(town_center)
    monde.fill_world()
    # monde.fill_ressources(10)
    # print(village1.population())
    # print(monde.get_ressources())
    # print("Before : ", village1.get_ressources())
    # fo = monde.get_ressources()["fo"]["0"]
    # v.drop_ressources()
    # v.collect(fo)
    # print("After : ", village1.get_ressources())
    # print(v.ressources_dict)
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