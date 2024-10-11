
import Unity

class Swordsman(Unity):
    def __init__(self,id ):
        super().__init__(id, "Swordsman", { "food" : 50, "gold" : 20}, 20, 40, 4, 0.2, 1)