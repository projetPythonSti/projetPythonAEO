import time
from enum import Enum

import pygame as pg
from models.Position import Position
import random as rd

class BuildingHealthENUM(Enum):
    T = 1000
    A = 500
    B = 500
    C = 200
    F = 100
    H = 200
    K = 800
    S = 500
class Building:
    """
                06/01/2025@tahakhetib - J'ai ajouté les modifications au dessus de ce que @amadou_yaya_diallo à écrit
                    - Passé l'attribut surface en statique afin de pouvoir y accéder sans avoir à créer un Building
                25/01/2025@tahahkhetib - J'ai ajouté des modifications au dessus de ce que @amadou_yaya_diallo à écrit
                    - Changé la définition de l'UID au niveau de toutes les classes filles de Building
                26/01/2025@tahahkhetib - J'ai ajouté des modifications au dessus de ce que @amadou_yaya_diallo à écrit
                    - Supprimé la ligne self.time_building = 3*ksjfl afin de garder le calcul du temps pour construire au niveau du GameManager
    """
    surface = (1,1)
    def __init__(self, uid, name, cost, time_building, health, spawn="", population=0, dropPoint=False, position=None, team=None):
        self.uid = uid
        self.name = name
        self.cost = cost
        self.time_building = time_building
        self.health = health
        self.hp_max = health
        self.is_built = False
        self.spawn = spawn
        self.dropPoint = dropPoint
        self.population = population
        self.builders = 1
        #self.time_building = 3 * time_building / (self.builders + 2)
        self.team = team
        self.position = position if position else Position(rd.randint(0, self.team.world.width - 1), rd.randint(0, self.team.world.height - 1))
        self.image = f"./assets/images/buildings/{self.name}.png"
        # self.images = pg.image.load(f"./assets/images/buildings/{self.name}.png").convert_alpha()


    def get_cost(self):
        return self.cost

    def get_occupied_tiles(self):
        return [(self.position.getX() + x, self.position.getY() + y) for x in range(self.surface[0]) for y in range(self.surface[1])]
    
    def get_name(self):
        return self.name
    
    # def can_afford(self, player_resources):
    #     for resource, amount_needed in self.cost.items():
    #         if player_resources.get(resource, 0) < amount_needed:
    #             return False
    #     return True

    def deduct_resources(self, player_resources):
        for resource, amount_needed in self.cost.items():
            player_resources[resource] -= amount_needed
        print(f"Ressources déduites pour {self.name}: {self.cost}")    

    # def build(self, player_resources):
    #     if not self.can_afford(player_resources):
    #         print(f"Pas assez de ressources pour construire {self.name}.")
    #         return False

    #     self.deduct_resources(player_resources)
    #     print(f"Construction de {self.name} commencée...")
    #     for second in range(self.time_building):
    #         print(f"Construction en cours : {second + 1}/{self.time_building} secondes")
    #         time.sleep(1)

    #     self.is_built = True
    #     print(f"Construction de {self.name} terminée.")
    #     return True
    
    def build(self):
        # print(f"Construction de {self.name} commencée...")
        self.time_building = 3*self.time_building/(self.builders + 2)
        for second in range(self.time_building):
            time.sleep(1)
            
        self.is_built = True
        print(f"Construction de {self.name} terminée.")
        return True
    
    
    def get_position(self):
        return self.position

    def getTPosition(self):
        return self.position.toTuple()

    def personalizedStr(self,term): return f"{term.red if self.health<BuildingHealthENUM[self.name].value else term.normal}{self.name}{term.normal}"

    def __repr__(self):
        return self.name
    

    def destroy(self):
        """
        Handles the destruction of the building.
        """
        self.is_built = False
        self.health = 0
        # Additional logic for destruction can be added here, such as removing the building from the game world
        self.team.world.remove_element(self)

        print(f"{self.name} has been destroyed.")

    def is_destroyed(self):
        return self.health <= 0