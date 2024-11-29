from time import sleep

from Position import Position
import time

class Unity:

    def __init__(self, id, name, cost, trainningTime, health, damage, speed, visibility, team, target = None, ):
        self.id = id
        self.name = name
        self.cost = cost
        self.trainningTime = trainningTime
        self.health = health
        self.damage = damage
        self.speed = speed
        self.position = Position()
        self.range = visibility
        self.target = target
        self.team  = team

    def move(self,destination, route):
        i = 0
        while(self.position != destination):
            print(f"Still in {i}, position {self.position}")
            if route[i+1][0] != self.position.getX():
                print(route[i+1], "is the destination")
                direction = 1 if self.position.getX() < route[i+1][0] else -1
                self.position.setX(self.position.getX()+direction)
                sleep(1.25)
            elif route[i+1][1] != self.position.getY():
                print(route[i+1], "is the destination")
                direction = 1 if self.position.getY() < route[i + 1][1] else -1
                self.position.setY(self.position.getY()+direction)
                sleep(1.25)
            if self.position == route[i+1]:
                print("Got to the next point")
                i += 1
        print("Arrivé à destination")
    
    def attack(attackedObjet):
        pass
    
    def getCost(self): return self.cost
    
    def __repr__(self): return f"{self.name}"
    
    def __eq__(self, other): return self.__class__ == other.__class__
    