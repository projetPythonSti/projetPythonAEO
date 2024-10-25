#Créé par Max le 27/09/2024

class Ressource:
    def __init__(self,name,quantity):
        self.name=name
        self.quantity=quantity

    def getQuantity(self):
        return self.quantity

    def __repr__(self): return self.name

#définition de toutes les ressources
wood=Ressource("W",100)
gold=Ressource("G",800)
food=Ressource("F",300) #à priori inutile ??