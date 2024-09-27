#Créé par Max le 27/09/2024

class Ressource:
    def __init__(self,name,quantity):
        self.name=name
        self.quantity=quantity

    def getQuantity(self):
        return self.quantity

    def getName(self):
        return self.name

    def __repr__(self): #affiche la première lettre du nom
        return self.name[0]

#définition de toutes les ressources
wood=Ressource("Wood",100)
gold=Ressource("Gold",800)
food=Ressource("Food",300) #à priori inutile ??