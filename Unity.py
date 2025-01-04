from Position import Position

class Unity:
    
    def __init__(self, ident, name, cost, trainningTime, health, damage, speed, ranges, team):
        self.id = ident
        self.name = name
        self.cost = cost
        self.trainningTime = trainningTime
        self.health = health
        self.damage = damage
        self.speed = speed
        self.position = Position()
        self.range = ranges
        self.team = team
    
    def move(self,lastPosition):
        pass
    
    def attack(self,attackedObjet):
        pass
    
    def getCost(self): return self.cost
    
    def __repr__(self): return f"{self.name[0]}"
    
    def __eq__(self, other): return self.__class__ == other.__class__

    def move_easy(self,dest): #moves straight to the destination, doesn't care about collisions
        from mmonde import dist
        from math import sqrt
        speed = self.speed
        #if speed is more than the distance, we can just go to the target
        if(speed > dist(self.position,dest)):
            self.position = dest
            return
        #else, it's Thales theorem time
        x = self.position.getX()
        dx = dest.getX() - x
        y = self.position.getY()
        dy = dest.getY() - y
        diago = sqrt(dx**2+dy**2)
        ratio = diago/speed
        dx = dx/ratio
        dy = dy/ratio
        self.position.setX(x+dx)
        self.position.serY(y+dy)