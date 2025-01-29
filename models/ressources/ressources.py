# This file contains the ressources classes, which are the objects that the player can collect in the game.
from models.Position import Position
import random as rd


class Ressource:
    def __init__(self, uid, name, quantity, world):
        self.name = name
        self.quantity = quantity
        self.world = world
        self.position = Position(rd.randint(0, self.world.width - 1), rd.randint(0, self.world.height - 1))
        self.uid = uid
        self.image = f"./assets/images/ressources/{self.name}.png"



    def to_dict(self):
        return {"name" : self.name, "quantity" : self.quantity, "position" : (self.position.getX(),self.position.getY()),"uid" : self.uid}

    def get_quantity(self):
        return self.quantity
    
    def get_name(self):
        return self.name
    
    def get_position(self):
        return self.position

    def getTPosition(self):
        return self.position.toTuple()

    
    def set_position(self, x, y):
        self.position.setX(x)
        self.position.setY(y)

    def set_quantity(self, quantity):
        self.quantity = quantity
    
    def extract(self, quantity = 0):
        self.quantity -= quantity
        # self.world.update_unit(self)
        
    
    def remove(self):
        if self and self.quantity == 0:
            self.world.remove_element(element=self)
            self.position = None

    def to_json(self):
        return {
            "id": self.uid,
            "name": self.name,
            "quantity": self.quantity,
            "position": self.position.to_json(),
        }

    def __repr__(self): return self.name
    def personalizedStr(self,term): return f"{self.name}"
    def __eq__(self, other): return self.__class__ == other.__class__ # it could be useful

class Wood(Ressource):
    
    def __init__(self,  world):
        community = world.get_ressources().get('w')
        uid = len(community) if community else 0 # 0 if 
        super().__init__(uid,"w",100, world=world)

class Gold(Ressource):
    def __init__(self, world):
        community = world.get_ressources().get('g')
        uid = len(community) if community else 0 # 0 if 
        super().__init__(uid,"g",800, world=world)

class Food(Ressource):
    def __init__(self, farm, world):
        community = world.get_ressources().get('f')
        uid = len(community) if community else 0 # 0 if 
        super().__init__(uid,"f", 1, world=world)
        self.farm = farm
        self.farm.add_food(self)

