
class Ressource:
    def __init__(self,name,quantity):
        self.name=name
        self.quantity=quantity

    def getQuantity(self):
        return self.quantity
    def setQuantity(self,quantity):
        self.quantity = quantity
    def __repr__(self): return self.name


class Wood(Ressource):
    def __init__(self):
        super().__init__("Wood",100)

class Gold(Ressource):
    def __init__(self):
        super().__init__("Gold",800)

class Food(Ressource):
    def __init__(self):
        super().__init__("Food",300)
