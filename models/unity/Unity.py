# this class is the parent class of all the unities in the game
from models.Position import Position
import random as rd
class Unity:
    population = 0
    
    def __init__(self, uid, name, cost, trainningTime, health, damage, speed, visibility, team, position=None, target = None ):
        self.uid = uid
        self.name = name
        self.cost = cost
        self.trainningTime = trainningTime
        self.health = health
        self.damage = damage
        self.speed = speed
        self.team  = team
        self.position = position if position else Position(rd.randint(0, self.team.world.width), rd.randint(0, self.team.world.height))
        self.range = visibility
        self.target = target
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
        enemy.set_health(enemy.get_health() - self.damage)
    
    def die(self):
        self.position = None
        self.team.remove_unit(self)
    
    def get_cost(self): return self.cost
    
    def __repr__(self): return f"{self.name}"
    
    def __eq__(self, other): return self.__class__ == other.__class__
    