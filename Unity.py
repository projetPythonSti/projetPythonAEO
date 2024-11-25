from Position import Position
import time

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
        self.move(Position(10,30))
    
    def collapse(self, other):
        pass
    
    def move(self, destination:Position):
        while self.position != destination:
            xPositionDifference = self.position.getX() - destination.getX()
            yPositionDifference = self.position.getY() - destination.getY()
            if xPositionDifference != 0 and yPositionDifference != 0:
                self.position.setY(self.position.getY() + 1) if yPositionDifference > 0 else self.position.setY(self.position.getY() - 1)
                self.position.setX(self.position.getX() + 0.5) if xPositionDifference > 0 else self.position.setX(self.position.getX() - 0.5)
            else:   
                if xPositionDifference == 0:
                    self.position.setY(self.position.getY() + 1) if yPositionDifference > 0 else self.position.setY(self.position.getY() - 1)
                if yPositionDifference == 0:  
                    self.position.setX(self.position.getX() + 0.5) if xPositionDifference > 0 else self.position.setX(self.position.getX() - 0.5)

            destination.setY(destination.getY() - 1)
            destination.setX(destination.getY() - 0.5)
            time.sleep(0.5)
        

        
    def attack(self, attackedObjet):
        pass
    
    def getCost(self): return self.cost
    
    def __repr__(self): return f"{self.name}"
    
    def __eq__(self, other): return self.__class__ == other.__class__
    