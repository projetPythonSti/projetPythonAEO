from Unity import Unity

class Horseman(Unity):
    
    def __init__(self, id):
        super().__init__(id, "Horseman", { "food" : 30, "gold" : 20}, 20, 45, 4, 1.2, 1)