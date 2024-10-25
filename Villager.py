from gc import collect

from Unity import Unity
import mressources
class Villager(Unity):
    carryMax = 25
    def __init__(self,id, carry, buildingSpeed):
        super().__init__(id,"V", {"food" : 50}, 25, 40, 4, 0.8, 1)
        self.carry = carry
        self.buildingSpeed = buildingSpeed,
        self.resourcesDict = {
            "food" : 0,
            "wood" : 0,
            "gold" : 0,
        }
    # Cette méthode considère qu'il existe une liste contenant les ressources portées par le self
    # Sinon, comment est-il possible de savoir les ressources qu'il faut déposer dans le TC, et si le villageois à plusieurs ressources
    def collect(self , resource):
        aR = sum(self.resourcesDict[key] for key in self.resourcesDict)
        collectedQuantity = resource.getQuantity
        print("ar = ",aR)
        if aR+collectedQuantity > self.carryMax :
            if aR > self.carryMax:
                print("Trop de ressources")
                return resource
            else :
                if resource.__class__ == mressources.Food:
                    print("FOOD resources")
                    self.resourcesDict["food"] += collectedQuantity-self.carryMax-aR

                elif resource.__class__ == mressources.Wood:
                    print("WOOD Resource")
                    self.resourcesDict["wood"] += resource.getQuantity()-self.carryMax-aR
                elif resource.__class__ == mressources.Gold:
                    print("GOLD Resource")
                    self.resourcesDict["gold"] += resource.getQuantity()-self.carryMax-aR
                resource.setQuantity(collectedQuantity - (collectedQuantity - self.carryMax - aR))
                return resource
        else:
            if resource.__class__ == mressources.Food:
                print("FOOD resources")
                self.resourcesDict["food"] += resource.getQuantity()
            elif resource.__class__ == mressources.Wood:
                print("WOOD Resource")
                self.resourcesDict["wood"] += resource.getQuantity()
            elif resource.__class__ == mressources.Gold:
                print("GOLD Resource")
                self.resourcesDict["gold"] += resource.getQuantity()
            resource.setQuantity(0)
            return resource

    def build(self):
        return 0
