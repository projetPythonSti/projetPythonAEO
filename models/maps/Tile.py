class Tile:
    def __init__(self): #id c'est le tuple (x,y)
        self.contains = None #tile with nothing inside

    def set_contains(self, contains):
        self.contains = contains
    
    def get_contains(self):
        return self.contains
    
    def __repr__(self):
        return self.contains.get_name() if self.contains != None else "_"
    
    # def affiche(self): #magic method repr wasn't doing me right, made a non-magic method    #KillAllWizards
    #     if self.unites!=[]:
    #         return self.unites[0].name[0].lower() #lowered first letter of the first unit on the tile
    #     return self.contains #ressource

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y
