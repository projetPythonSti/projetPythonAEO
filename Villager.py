from Unity import Unity
import mressources
class Villager(Unity):
    carryMax = 25
    def __init__(self,id, carry, buildingSpeed):
        super().__init__(id,"Villager", { "food" : 50}, 25, 40, 4, 0.8, 1)
        self.carry = carry
        self.buildingSpeed = buildingSpeed,
        self.resourcesDict = {},
    # Cette méthode considère qu'il existe une liste contenant les ressources portées par le self
    # Sinon, comment est-il possible de savoir les ressources qu'il faut déposer dans le TC, et si le villageois à plusieurs ressources
    def collect(self , resource):
        aR = sum(self.resourcesDict[key] for key in self.resourcesDict)
        if aR > self.carryMax:
            print("Trop de ressources")
        else:
            if resource.type == Food:

            # Cette ligne à été ajoutée dans le cas où on implémente une boucle qui ajoute à une liste externe la ressource collecté
            return resource
    def build(self):
        return 0