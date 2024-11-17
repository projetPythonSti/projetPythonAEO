from time import sleep

from Position import Position

class Unity:
    
    def __init__(self, id, name, cost, trainningTime, health, damage, speed, range, team, target = None, ):
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
    def move(self,destination, route):
        i = 0
        while(self.position != destination):
            print(f"Still in {i}, position {self.position}")
            if route[i+1][0] != self.position[0]:
                print(route[i+1], "is the destination")
                direction = 1 if self.position[0] < route[i+1][0] else -1
                self.position  = ((self.position[0]+direction), self.position[1])
                sleep(1.25)
            elif route[i+1][1] != self.position[1]:
                print(route[i+1], "is the destination")
                direction = 1 if self.position[1] < route[i + 1][1] else -1
                self.position = (self.position[0], self.position[1]+direction)
                sleep(1.25)
            if self.position == route[i+1]:
                print("Got to the next point")
                i += 1
        print("Arrivé à destination")
    
    def attack(attackedObjet):
        pass
    
    def __repr__(self):
        return f"{self.id} {self.name}"
    
    def __eq__(self, other):
        return self.__class__ == other.__class__
    