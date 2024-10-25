from Position import Position
import objc

class Unity:
    
    def __init__(self, id, name, cost, trainningTime, health, damage, speed, range, team, target = objc.nil, ):
        self.id = id
        self.name = name
        self.cost = cost
        self.trainningTime = trainningTime
        self.health = health
        self.damage = damage
        self.speed = speed
        self.position = Position()
        self.range = range
        self.target = target
        self.team  = team
    def move(lastPosition):
        pass
    
    def attack(attackedObjet):
        pass
    
    def __repr__(self):
        return f"{self.id} {self.name}"
    
    def __eq__(self, other):
        return self.__class__ == other.__class__
    