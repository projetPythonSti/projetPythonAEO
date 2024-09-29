from Unity import Unity

class Archer(Unity):
    
    def __init__(self, id):
        super().__init__(id, "Archer", { "wood" : 25, "gold" : 45}, 35, 30, 4, 1, 4)
    
