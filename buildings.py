import time
import pygame as pg
from Position import *
from RessourcesManager import RessourcesManager

class Building:
    def __init__(self, name, cost, time_building, health, lenght, spawn, dropPoint: bool(), flag, position):
        self.name = name
        self.cost = cost
        self.time_building = time_building
        self.health = health
        self.lenght = lenght
        self.is_built = False
        self.spawn = spawn
        self.dropPoint = False
        self.dropPoint = dropPoint
        self.flag = flag
        self.position = position

    def can_afford(self, resource_manager : RessourcesManager):
        for resource, amount_needed in self.cost.items():
            if resource_manager.resources.get(resource, 0) < amount_needed:
                return False
        return True

    def deduct_resources(self, resource_manager : RessourcesManager):
        for resource, amount_needed in self.cost.items():
            resource_manager.resources[resource] -= amount_needed
        print(f"Ressources déduites pour {self.name}: {self.cost}")

    def set_time_building(self, resource_manager : RessourcesManager) :
        n = resource_manager.resources.get("villagers", 0)
        return 3*self.time_builing / (n+2)
    
    def build(self, resource_manager : RessourcesManager):
        if not self.can_afford(resource_manager):
            print(f"Pas assez de ressources pour construire {self.name}.")
            return False
        self.deduct_resources(resource_manager)
        print(f"Construction de {self.name} commencée...")
        build_time = int(self.set_time_building(resource_manager))
        for second in range(build_time):
            print(f"Construction en cours : {second + 1}/{self.time_building} secondes")
            time.sleep(1)

        self.is_built = True
        print(f"Construction de {self.name} terminée.")
        return True

    def set_position(self, x, y):
        # Définit la position du bâtiment
        self.position.setX(x)
        self.position.serY(y)
        print(f"Position de {self.name} définie à ({x}, {y}).")
