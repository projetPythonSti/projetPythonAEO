from Position import Position


class Ressource:
    def __init__(self, uid, name, quantity, team):
        self.name=name
        self.quantity=quantity
        self._position = Position()
        self.team = team

    def get_quantity(self):
        return self.quantity
    
    def get_position(self):
        return self._position
    
    def set_quantity(self, quantity):
        self.quantity = quantity

    def __repr__(self): return self.name
    
    def __eq__(self, other): return self.__class__ == other.__class__ #it gonna be useful maybe

class Wood(Ressource):
    
    def __init__(self, team):
        community = team.get_community().get('v')
        uid = len(community) if community else 0 # 0 if 
        super().__init__(uid,"W",100, team)

class Gold(Ressource):
    def __init__(self, team):
        community = team.get_community().get('v')
        uid = len(community) if community else 0 # 0 if 
        super().__init__(uid,"G",800, team)

class Food(Ressource):
    def __init__(self,team):
        community = team.get_community().get('v')
        uid = len(community) if community else 0 # 0 if 
        super().__init__(uid,"F",300, team)
