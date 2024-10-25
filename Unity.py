from Position import Position

class Unity:
    
    def __init__(self, ident, name, cost, trainningTime, health, damage, speed, ranges):
        self.id = ident
        self.name = name
        self.cost = cost
        self.trainningTime = trainningTime
        self.health = health
        self.damage = damage
        self.speed = speed
        self.position = Position()
        self.range = ranges
    
    def move(lastPosition):
        pass
    
    def attack(attackedObjet):
        pass
    
    def getCost(self): return self.cost
    
    def __repr__(self): return f"{self.name[0]}"
    
    def __eq__(self, other): return self.__class__ == other.__class__
    