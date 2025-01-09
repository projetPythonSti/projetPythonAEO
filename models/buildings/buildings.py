import time
from models.Position import Position
import random as rd

class Building:

    """
    04/12/2024@tahakhetib - J'ai ajouté des modification au dessus de ce que @moutanahzir à écrit
                - ajouté un méthode get_surface() permettant d'obtenir efficacement la surface d'un batiment
    """

    def __init__(self, uid, name, cost, time_building, health, surface, spawn="", population=0, dropPoint=False, position=None, team=None):
        self.uid = uid
        self.name = name
        self.cost = cost
        self.health = health
        self.surface = surface
        self.is_built = False
        self.spawn = spawn
        self.dropPoint = dropPoint
        self.population = population
        self.builders = 1
        self.time_building = 3 * time_building / (self.builders + 2)
        self.team = team
        self.position = position if position else Position(rd.randint(0, self.team.world.width - 1), rd.randint(0, self.team.world.height - 1))
        self.image = f"./assets/images/graphics/{self.name}.png"

    def get_cost(self):
        return self.cost
    
    def get_occupied_tiles(self):
        return [(self.position.getX() + x, self.position.getY() + y) for x in range(self.surface[0]) for y in range(self.surface[1])]
    
    def get_name(self):
        return self.name

    def deduct_resources(self, player_resources):
        for resource, amount_needed in self.cost.items():
            player_resources[resource] -= amount_needed
        print(f"Ressources déduites pour {self.name}: {self.cost}")    

    def begin_building(self):
        self.team.world.book_place(self.surface, (self.position.getX(), self.position.getY()))

    def get_position(self):
        return self.position

    def get_surface(self):
        return self.surface
    
    def __repr__(self):
        return self.name