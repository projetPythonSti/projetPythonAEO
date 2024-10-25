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


    # Function which collect a resource and add it to the resourcesDictionnary of the villager, at the end if carryMax is
    # is reached, move
    def collect(self , resource, neareastDP):
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
        if aR+(collectedQuantity - resource.getQuantity()) > self.carryMax:
            self.move(neareastDP)
    def build(self):
        return 0
