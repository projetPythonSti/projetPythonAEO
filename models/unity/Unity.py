# this class is the parent class of all the unities in the game
from collections import defaultdict
from enum import Enum

from models.Position import Position
import random as rd

class UnityHealthENUM(Enum):
    a = 10
    h = 45
    s = 40
    v = 25

class Unity:
    population = 0

    """
    26/01/2025@tahakhetib :  J'ai apporté les modification suivantes sur le fichier (ce que j'ai écrit)
                - Ajouté une fonction isInRange() pour vérifier si une autre position est dans la zone d'attaque de l'unité
                - Ajouté une fonction estimateDistance() pour obtenir la distance entre 2 éléments, sert dans la fonction isInRange()
                - Ajouté une fonction isFull() retournant si l'unité est pleine ou pas et un attribut pouch représentant les ressources que l'unité porte
                - Ajouté une fonction placeLeft() retournant la place restante dans la sacoche de l'unité

    """
    def __init__(self, uid, name, cost, trainningTime, health, damage, speed, visibility, team, position=None, target = None):
        self.uid = uid
        self.name = name
        self.cost = cost
        self.trainningTime = trainningTime
        self.health = health
        self.damage = damage
        self.speed = speed
        self.team  = team
        self.position = position if position else Position(rd.randint(0, self.team.world.width - 1), rd.randint(0, self.team.world.height - 1))
        self.range = visibility
        self.target = target
        self.pouch = {
            "w" : 0,
            "g" : 0,
        }
        self.task = None
        self.image = f"./assets/images/{self.name}.png"

        # self.team.add_unit(self)
        # population += 1
    
    def move_unit(self, destination:Position):
        self.position = destination
    
    def get_health(self):
        return self.health
    
    def set_health(self, health):
        self.health = health
    
    def get_damage(self):
        return self.damage
    
    def get_name(self):
        return self.name
    
    def attack(self, enemy):
        #1 attack per second for all units
        self.task = "Fighting"
        enemy.set_health(enemy.get_health() - self.damage)
    
    def die(self):
        self.position = None
        self.team.world.remove_element(self)
    
    def get_cost(self): return self.cost
    
    def get_position(self):
        return (self.position.getX(), self.position.getY())

    def getTPosition(self):
        return self.position.toTuple()


    def estimateDistance(self, pos1 : tuple, pos2 : tuple):
        return abs(pos2[0] - pos1[0]), abs(pos2[1] - pos1[1])

    def isInRange(self, position : tuple[int,int]):
        distance = self.estimateDistance(self.position.toTuple(), position)
        return distance[0] <= self.range and distance[0]<= self.range

    def isFull(self):
        return self.pouch["w"]+self.pouch["g"] >= 20

    def spaceLeft(self):
        return 20-(self.pouch["w"]+self.pouch["g"])

    def dropResources(self):
        self.team.ressources["w"] += self.pouch["w"]
        self.pouch["w"] = 0
        self.team.ressources["g"] += self.pouch["g"]
        self.pouch["g"] = 0

    def to_json(self):
        return {
            "id": self.uid,
            "name": self.name,
            "health": self.health,
            "teamID": self.team.name, #int(x) if its not an integer please
            "position": self.position.to_json(),
            "pouch": self.pouch
        }

    def __repr__(self): return f"{self.name}"
    def personalizedStr(self,term): return f"{term.red if self.health<UnityHealthENUM[self.name].value else term.normal}{self.name}{term.normal}"
    def __eq__(self, other): return self.__class__ == other.__class__
    