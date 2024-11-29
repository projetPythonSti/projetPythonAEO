from models.Position import Position


class Ressource:
    def __init__(self,name,quantity):
        self.name=name
        self.quantity=quantity
        self._position = Position()

    def getQuantity(self):
        return self.quantity
    
    def getPosition(self):
        return self._position
    
    def setQuantity(self, quantity):
        self.quantity = quantity

    def __repr__(self): return self.name
    
    def __eq__(self, other): return self.__class__ == other.__class__ #it gonna be useful maybe

class Wood(Ressource):
    def __init__(self):
        super().__init__("W",100)

class Gold(Ressource):
    def __init__(self):
        super().__init__("G",800)

class Food(Ressource):
    def __init__(self):
        super().__init__("F",300)
