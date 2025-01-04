from nis import match
from enum import Enum

from models.World import World
from models.buildings.archery_range import ArcheryRange
from models.buildings.barracks import Barracks
from models.buildings.camp import Camp
from models.buildings.farm import Farm
from models.buildings.house import House
from models.buildings.keep import Keep
from models.buildings.stable import Stable
from models.buildings.town_center import TownCenter
from models.model import Model

class BuildingENUM(Enum):
    T = TownCenter
    A = ArcheryRange
    B = Barracks
    C = Camp
    F  = Farm
    H = House
    K = Keep
    S = Stable

class PlayStyle:

    def __init__(self, minWorkers):
        self.playStyleMatrix = []
        self.minWorkers = minWorkers


class AIPlayer:
    playing = False
    def __init__(self, team : Model, world : World, playStyle : PlayStyle):
        self.team = team
        self.world = world
        self.playStyle = playStyle
        self.freeUnits = {
            "v" :[team.community["v"].keys()],
            "h" : [team.community["h"].keys()],
            "s" : [team.community["s"].keys()],
            "a" : [team.community["a"].keys()]
        }
        self.eventQueue = []


    def playTurn(self):
        if self.team.workingPpl < self.playStyle.minWorkers:
            self.playing = True
            print("Minworkers hit, playing now")


    def checkRessources(self):
        vRessources = self.team.get_ressources()
        return min(vRessources.values(), key=vRessources.get())

    def checkBuildings(self):
        nbAR = range(self.team.community["A"])
        nbBr = range(self.team.community["B"])
        nbC = range(self.team.community["C"])
        nbF = range(self.team.community["F"])
        nbH = range(self.team.community["H"])
        nbK = range(self.team.community["K"])
        nbSt = range(self.team.community["S"])
        nbTc = range(self.team.community["T"])
        return {
            'ArcheryRange' : nbAR,
            "Barracks" : nbBr,
            "Camps" : nbC,
            "Farms" : nbF,
            "Houses" : nbH,
            "Keeps" : nbK,
            "Stables" : nbSt,
            "Tc" : nbTc
        }
    def getOptimalBuildingCurve(self, BuildingType):
        return 3

    def getFreePeople(self, number : int ,type):
        return self.freeUnits[type][:number]

    def getBuildTarget(self, size):
        pass


    def setResourceAction(self, concernedRes):
        pass


    def setBuildingAction(self, buildings):
        minBuildingKey = min(buildings.values(), key= buildings.get())
        if buildings[minBuildingKey] == 0:
            type  = "v"
            idList = self.getFreePeople(self.getOptimalBuildingCurve(1),type )
            if len(idList) == 0:
                return -1 # an error will be thrown later
            for i in range(idList):
                self.freeUnits[type].pop(idList[i])
            buildingEvent = {
                "action" : "Build",
                "people"  : idList,
                "infos": {
                    "type" : minBuildingKey,
                    "target" : self.getBuildTarget(BuildingENUM[minBuildingKey].value.get_surface())
                }
            }
            self.eventQueue.append()