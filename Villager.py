from gc import collect

from Unity import Unity
import mressources
from pathfinding import Pathfinding
from RessourcesManager import RessourcesManager

class Villager(Unity):
    villagerPopulation = 0
    def __init__(self,id, team):
        super().__init__(id,"V", {"food" : 50}, 25, 40, 4, 0.8, 1, team=team)
        self.carryMax = 25
        # self.buildingSpeed = buildingSpeed,
        self.resourcesDict = {
            "food" : 0,
            "wood" : 0,
            "gold" : 0,
        }

    # Function which collect a resource and add it to the resourcesDictionnary of the villager, at the end if carryMax is
    # is reached, move to the nearest drop point
    def collect(self , resource, route:Pathfinding):
        allCollected = sum(self.resourcesDict.values())
        collectedQuantity = resource.getQuantity()
        print("allCollected = ",allCollected)
        if (allCollected + collectedQuantity) > self.carryMax :
            if allCollected > self.carryMax:
                print("Trop de ressources")
                self.move(route.getGoal(), route)
                self.dropRessources()
                # return resource
            else :
                if resource.__class__ == mressources.Food:
                    print("FOOD resources")
                    self.resourcesDict["food"] += collectedQuantity-self.carryMax-allCollected
                elif resource.__class__ == mressources.Wood:
                    print("WOOD Resource")
                    self.resourcesDict["wood"] += resource.getQuantity()-self.carryMax-allCollected
                elif resource.__class__ == mressources.Gold:
                    print("GOLD Resource")
                    self.resourcesDict["gold"] += resource.getQuantity()-self.carryMax-allCollected
                resource.setQuantity(collectedQuantity - (collectedQuantity - self.carryMax - allCollected))
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
        if allCollected+(collectedQuantity - resource.getQuantity()) > self.carryMax:
            pass
            #self.move(neareastDP)
    
        """
            droping ressources in the village drop point
        """
    def dropRessources(self, ressourcesManager:RessourcesManager):
        ressourcesManager.setRessources(self.resourcesDict)
        for key in self.resourcesDict:
            self.resourcesDict[key] = 0
    
    def build(self):
        return 0
