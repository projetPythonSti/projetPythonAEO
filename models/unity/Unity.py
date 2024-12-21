from Position import Position

class Unity:
    population = 0
    
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
        # population += 1
    
    def move_unit(self, destination:Position):
        self.position = destination
    
    def attack(attackedObjet):
        pass
    
    def get_cost(self): return self.cost
    
    def __repr__(self): return f"{self.name}"
    
    def __eq__(self, other): return self.__class__ == other.__class__
    