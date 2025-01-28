
from enum import Enum

from functools import partial
import io
import sys
from os import remove
from select import select

from models.Exceptions import PathfindingException, AIPeopleException

output = io.StringIO()

from models.Position import Position
from models.World import World
from models.buildings.archery_range import ArcheryRange
from models.buildings.barracks import Barracks
from models.buildings.buildings import Building
from models.buildings.camp import Camp
from models.buildings.farm import Farm
from models.buildings.house import House
from models.buildings.keep import Keep
from models.buildings.stable import Stable
from models.buildings.town_center import TownCenter
from controllers.gameManager import GameManager
from models.model import Model
from models.ressources.ressources import Ressource, Wood, Gold, Food
from models.unity.Villager import Villager

output = io.StringIO()
class PlayStyleMatrixEnum(Enum):
    Aggressive = [
        [2,5,0],
        [6,2,4],
        [3,2,8]
    ]
    Passive = [
        [6, 20, 0],
        [2, 2, 1],
        [1, 12, 2]
    ]
    """OLDPassive = [
        [6,1,0],
        [2,5,1],
        [1,3,10]
    ]"""
    Builder = [
        [9,1,0],
        [2,8,2],
        [1,4,0]
    ]



class BuildingENUM(Enum):
    T = TownCenter
    A = ArcheryRange
    B = Barracks
    C = Camp
    F  = Farm
    H = House
    K = Keep
    S = Stable

class BuildingTypeENUM(Enum):
    Military = [Barracks, Stable, ArcheryRange, Keep]
    Village = [House, TownCenter]
    Farming = [Farm, Camp]
    DropPoints = ["T", "C"]

class ResourceTypeENUM(Enum):
    w = Wood
    g = Gold
    f = Food

class DirectionsENUM(Enum):
    f = "East"

class PlayStyle:

    """
        Matrice de style de jeu
        [
          A B C
          D E F
          G H I
        ]

-
          A : Représente l'importance de la collecte de matières premières / 10 (Wood)
          D : Représente l'importance de la collecte de ressources pécuniaires / 10(Gold)
          G : Représente l'importance de la collecte de ressources alimentaires / 10 (Food)

          B : Représente le nombre de batiment militaires à avoir dans le village (Barracks, Stable, Archery Range, Keep)
          E : Représente le nombre de batiment faiseurs de villageois dans le village (House, TownCenter)
          H : Représente le nombre de batiment stockeurs à avoir dans le village

          C : Représente l'importance de la défense du village / 10 (Plus cette valeur est elevée, moins l'IA ira se battre et attaquera violemment toute autre équipe voulant l'attaquer)
          F : Représente l'importance de l'expansion du village /10 (Plus cette valeur est elevée, plus l'IA s'étendra sur la map et attaquera les équipes sur son chemin si nécessaire
          I : Représente l'importance de la castagne / 10 (Plus cette valeur est elevée, plus l'IA va chercher à taper tout ce qui bouge)

    """

    def __init__(self, minWorkers, matrix=None):
        if matrix is None:
            matrix = []
        self.playStyleMatrix = matrix
        self.minWorkers = minWorkers


    def setPlayStyleMatrix(self, matrix):
        self.playStyleMatrix = matrix

    def getPlayStyleMatrix(self):
        return self.playStyleMatrix

class PlayStyleEnum(Enum):
    a = PlayStyle(minWorkers=10, matrix=PlayStyleMatrixEnum["Aggressive"].value)
    p = PlayStyle(minWorkers=10, matrix=PlayStyleMatrixEnum["Passive"].value)
    b = PlayStyle(minWorkers=10, matrix=PlayStyleMatrixEnum["Builder"].value)

class AIPlayer:


    """
        25/01/2025@tahakhetib : J'ai apporté des modifications sur ce que j'ai  écrit
            - Pris en compte la fonction du gameManager pour construire les batiments
    """
    playing = False
    def __init__(self, team : Model, world : World, playStyle : PlayStyle, level : int, gm : GameManager, debug=False, writeToDisk=False):
        self.team = team
        self.world = world
        self.playStyle = playStyle
        self.level = level
        self.freeUnits = {
            "v" : list(team.community["v"].keys()),
            "h" : list(team.community["h"].keys()),
            "s" : list(team.community["s"].keys()),
            "a" : list(team.community["a"].keys())
        }
        self.topVillageBorder = (0, 0)
        self.bottomVillageBorder = (0, 0)
        self.newTopVillageBorder = None
        self.newBottomVillageBorder = None
        self.gm = gm
        self.eventQueue = []
        self.pastEvents = []
        self.currentEvents = []
        self.debug = debug
        self.writeToDisk = writeToDisk
        self.logs = ""
        tcs = list(team.community["T"].values())
        if len(tcs) >0:
            tcSurface = (tcs[0].position.getX() + tcs[0].surface[0] + self.playStyle.playStyleMatrix[1][2],
                     tcs[0].position.getY() + tcs[0].surface[1] + self.playStyle.playStyleMatrix[1][2])
            topBorder = (tcs[0].position.getX() - self.playStyle.playStyleMatrix[1][2], tcs[0].position.getY() - self.playStyle.playStyleMatrix[1][2])
            self.setVillageBorders(topBorder, tcSurface)
        self.logger("AIPlayer | AI Launched -> Init launched, currentEvents are :", self.currentEvents)

    def logger(self,*args, **kwargs):
        if self.debug:
            if self.writeToDisk:
                sys.stdout = output
                print(*args, **kwargs)
                sys.stdout = sys.__stdout__
            else:
                print(*args, **kwargs)

    def setVillageBorders(self, topLeftPos, bottomRightPos):
        self.topVillageBorder = topLeftPos
        self.bottomVillageBorder = bottomRightPos


    def playTurn(self):
        self.logger("------ START OF AI TURN ------")
        #self.logger("Village border atm => ", self.topVillageBorder, self.bottomVillageBorder)
        self.playing = True
        for i in self.freeUnits:
            for k in self.freeUnits[i]:
                self.logger("AIPlayer | playTurn : valeur k -> ",k)
                if self.gm.checkIfDead(k, team=self.team.name):
                    print("l'unité semble être morte ")
                    self.freeUnits[i].remove(k)

        self.logger(f"AIPlayer | playTurn eq${self.team.name}--- freeunits state",self.freeUnits)
        self.logger("Voici le nombre de personnes libres",self.getFreePplCount(), "Et le nb de personnes total : ",self.team.get_pplCount())
        workingPpl  = self.team.get_pplCount() - self.getFreePplCount()
        if workingPpl < self.playStyle.minWorkers and workingPpl != self.team.get_pplCount():
            self.logger("Minworkers hit, playing now")
            self.setBuildingAction(self.checkBuildings())
            #self.setResourceAction(self.team.ressources)
            if self.playStyle.playStyleMatrix[2][2] > 5:
                #self.logger("AIPlayer | playTurn--- Aggressive AI Detected, real playstyle is", PlayStyleMatrixEnum(self.playStyle.playStyleMatrix).name)
                self.setHumanAction()
                pass
            self.logger(len(self.eventQueue))
            numberOfActions = 0
            for k in range(len(self.eventQueue)):
                numberOfActions += 1
                self.logger(self.eventQueue[k-1]["action"])
                self.launchAction(self.eventQueue[k-1])
        else:
            self.checkActions()
            self.logger("RAS")
        self.logger("Voici le nombre de personnes libres",self.getFreePplCount(), "Et le nb de personnes total : ",self.team.get_pplCount())
        self.logger("------ END OF AI TURN ------")

        if self.writeToDisk:
            self.writeLogs()



    def checkBuildings(self):
        nbAR = len(self.team.community["A"])
        nbBr = len(self.team.community["B"])
        nbC = len(self.team.community["C"])
        nbF = len(self.team.community["F"])
        nbH = len(self.team.community["H"])
        nbK = len(self.team.community["K"])
        nbSt = len(self.team.community["S"])
        nbTc = len(self.team.community["T"])
        return {
            'A' : nbAR,
            "B" : nbBr,
            "C" : nbC,
            "F" : nbF,
            "H" : nbH,
            "K" : nbK,
            "S" : nbSt,
            "T" : nbTc
        }

    def getBuildingsPriority(self):
        return self.playStyle.playStyleMatrix[0][1],self.playStyle.playStyleMatrix[1][1],self.playStyle.playStyleMatrix[2][1]

    def getResourcesPriority(self):
        return self.playStyle.playStyleMatrix[0][0],self.playStyle.playStyleMatrix[1][0],self.playStyle.playStyleMatrix[2][0]

    def getPlayingPriority(self):
        return self.playStyle.playStyleMatrix[0][2],self.playStyle.playStyleMatrix[1][2],self.playStyle.playStyleMatrix[2][2]

    def getDirection(self, pos1, pos2):
        pass

    def estimateDistance(self, pos1 : tuple, pos2 : tuple):
        return abs(pos2[0] - pos1[0]), abs(pos2[1] - pos1[1])

    def getNearestRessource(self,topLeftPos,bottomRightPos,  resourceType):
        ressourceKeyDict = list(map(lambda  x : x, self.world.ressources[resourceType].keys()))
        resourcesPositionList = list(map(lambda x : self.estimateDistance(x.position.toTuple(), topLeftPos) , self.world.ressources[resourceType].values()))
        #self.logger("AIPlayer | getNearestRessource---- resPositionList value : ", ressourceKeyDict)
        if len(resourcesPositionList) == 0:
            return -1
        nearestResourcesIndex = resourcesPositionList.index(min(resourcesPositionList))
        return {
            ressourceKeyDict[nearestResourcesIndex] : resourcesPositionList[nearestResourcesIndex]
        }

    def getNearestDropPoint(self, resource):
        dpKeys1 = list(map(lambda  x : x, self.team.community["T"].keys()))
        dpKeys2 = list(map(lambda  x : x, self.team.community["T"].keys()))
        dropPoints1 = list(map(lambda x : self.estimateDistance(x.position.toTuple(), next(iter(resource.values()))) , self.team.community["T"].values()))
        dropPoints2 = list(map(lambda x : self.estimateDistance(x.values().position.toTuple(), next(iter(resource.values())).position.toTuple()) , self.team.community["C"].values()))
        self.logger("AIPlayer | getNearestDropPoint--- dropPoints1 = ", dpKeys2)
        nearestDP = -1

        nearestDP1Index = -1
        nearestDP2Index = -1
        try :
            test = dropPoints1[0]
            nearestDP1Index = dropPoints1.index(min(dropPoints1))
        except:
            self.logger("AIPlayer | getNearestDropPoint--- No TCS")
        try:
            test2 = dropPoints2[0]
            nearestDP2Index = dropPoints2.index(min(dropPoints2))
        except:
            if nearestDP1Index < 0:
                return {-1 : -1}
            else:
                finalDropPoint = nearestDP1Index

                return self.team.community["T"][dpKeys1[finalDropPoint]]
        finalDropPointIndex = min(dropPoints1[nearestDP1Index],dropPoints2[nearestDP2Index])
        type = ""
        finalList = []
        if dropPoints1[nearestDP1Index] <dropPoints2[nearestDP2Index]:
            finalDropPointIndex  = nearestDP1Index
            finalList = dpKeys1
            type = "T"
        else:
            finalDropPointIndex = nearestDP2Index
            finalList = dpKeys2
            type = "C"
        return self.team.community[type][finalList[finalDropPointIndex]]


    def getOptimalBuildingCurve(self, BuildingType):
        return 3

    def getFreePplCount(self):
        return len(self.freeUnits["v"])+len(self.freeUnits["s"])+len(self.freeUnits["h"])+len(self.freeUnits["a"])

    def isOutOfBound(self, position):
        return (position[0] <0 or position[0] > self.world.width) or (position[1] <0 or position[1] > self.world.height)

    def getFreePeople(self, number : int ,type):
        return self.freeUnits[type][:number]


    def checkIfTilesAreOccupied(self, size, position):
        for a in self.getOccupiedTiles(size,position):
            #self.logger("AIPlayer | checkIfTilesAreOccupied ----- a values is in filled_tiles ? ", self.world.filled_tiles.__contains__(a) ,"Tile value", a)
            if a in self.world.filled_tiles.values():
                self.logger("AIPlayer | checkIfTilesAreOccupied---- value is indeed in filledTiles ")
                return True
            else:
                pass
        return False #self.getOccupiedTiles(size,position) in list(self.world.filled_tiles.keys())

    def getOccupiedTiles(self,size, position):
        return [(position[0] + x, position[1] + y) for x in range(size[0]) for y in range(size[1])]


    def find_location_contour(self, size):
        w, h = (size[0]+1,size[1]+1)
        candidates = set()
        allBuildings = []
        for a in BuildingENUM:
            allBuildings += list(self.team.community[a.name].values())
        #self.logger("AIPlayer | find_location_contour----- Buildings are at ", allBuildings)
        for building in allBuildings:
            bx, by = building.getTPosition()
            bw, bh = (building.surface[0],building.surface[0])
            candidates.update([
                (bx - w, by), (bx + bw, by), (bx, by - h), (bx, by + bh)
            ])

        for x, y in candidates:
            if not self.checkIfTilesAreOccupied(size, (x, y)):
                #self.logger("AIPlayer | find_location_contour------ seems that this position was ok!")
                return x, y
        return None

    def getBuildTarget(self, size, tries=0):
        selectedPos = None
        """
        #tilesOccupiedFirst = False

        # POSITION AU NORD - 7
        for x in range(self.topVillageBorder[0], self.bottomVillageBorder[0], size[0]):
            if x+size[0]>self.bottomVillageBorder[0] or selectedPos is not None:
                if selectedPos is not None:
                    self.logger("AIPlayer | getBuildTarget---- Found position !")
                    return selectedPos
                    # When a suitable position has already been found
                else:
                    # If the position is outside of the borders of the village
                    self.logger("AIPlayer | getBuildTarget---- do nothing, outside of village border in the game")
            else:
                generalSize = (size[0] + 1, size[1] + 1)
                self.logger("AIPlayer | getBuildTarget---- searching positions north to the building")
                tileOccupied = self.checkIfTilesAreOccupied(generalSize, (x-size[0], self.topVillageBorder[1]))
                self.logger("AIPlayer | getBuildTarget---- Check if tiles are occupied result : ", tileOccupied )
                selectedPos = (x-size[0]+1,self.topVillageBorder[1]+1) if (not tileOccupied) else None
                self.logger("AIPlayer | getBuildTarget---- selectdPos iiiis : ", selectedPos)
                if selectedPos is not None and self.isOutOfBound(selectedPos):
                    selectedPos = None

                if selectedPos is not None and selectedPos[0] < self.topVillageBorder[0]:
                    newVillageBorder = (selectedPos[0]-self.playStyle.playStyleMatrix[1][2],self.topVillageBorder[1])
                    self.newTopVillageBorder = newVillageBorder if not self.isOutOfBound(newVillageBorder) else None
                if selectedPos is not None and selectedPos[1] < self.topVillageBorder[1]:
                    newVillageBorder = (self.topVillageBorder[0],selectedPos[1]-self.playStyle.playStyleMatrix[1][2])
                    self.newTopVillageBorder = newVillageBorder if not self.isOutOfBound(newVillageBorder) else None


        if selectedPos is not None:
            return selectedPos

        # POSITION A L'EST - 7
        if selectedPos is None:
            self.logger("AIPlayer | getBuildTarget---- searching positions east to the building")
            # Recherche de position disponible à l'est du bâtiment
            for y in range(self.topVillageBorder[1], self.bottomVillageBorder[1], size[1]):
                if y+size[0]>self.bottomVillageBorder[1] or selectedPos is not None:
                    if selectedPos is not None:
                        self.logger("AIPlayer | getBuildTarget---- Found position !")
                        return selectedPos
                    else:
                        pass
                else:
                    generalSize = (size[0]+1, size[1]+1)
                    tileOccupied = self.checkIfTilesAreOccupied(generalSize, (self.bottomVillageBorder[0] - size[0], y))
                    selectedPos = (self.bottomVillageBorder[0]-size[0]+1,y+1) if not tileOccupied else None
                    self.logger("AIPlayer | getBuildTarget---- selectdPos iiiis : ", selectedPos)
                    if selectedPos is not None and self.isOutOfBound(selectedPos):
                        selectedPos = None

                    # Checking if the village was possibly extended by a new building
                    if selectedPos is not None and selectedPos[0] > self.bottomVillageBorder[0]:
                        newVillageBorder = (selectedPos[0] + self.playStyle.playStyleMatrix[1][2], self.bottomVillageBorder[1])
                        self.newTopVillageBorder = newVillageBorder if not self.isOutOfBound(newVillageBorder) else None
                    if selectedPos is not None and selectedPos[1] > self.bottomVillageBorder[1]:
                        newVillageBorder = (self.bottomVillageBorder[0], selectedPos[1]+ self.playStyle.playStyleMatrix[1][2])
                        self.newTopVillageBorder = newVillageBorder if not self.isOutOfBound(newVillageBorder) else None

            if selectedPos is not None:
                return selectedPos



        # POSITION A L'OUEST - 7
        if selectedPos is None:
            self.logger("AIPlayer | getBuildTarget---- searching positions west to the building")
            # Recherche de position disponible à l'ouest du batiment
            for y in range(self.topVillageBorder[1], self.bottomVillageBorder[1], size[1]):
                if y+size[0]>self.bottomVillageBorder[1] or selectedPos is not None:
                    if selectedPos is not None:
                        self.logger("AIPlayer | getBuildTarget---- Found position !")
                        return selectedPos
                    else:
                        pass
                else:
                    generalSize = (size[0]+1, size[1]+1)

                    tileOccupied = self.checkIfTilesAreOccupied(generalSize, (self.topVillageBorder[0]-size[0], y))
                    selectedPos = (self.topVillageBorder[0]-size[0]+1,y+1) if not tileOccupied  else None
                    self.logger("AIPlayer | getBuildTarget---- selectdPos iiiis : ", selectedPos)
                    if selectedPos is not None and self.isOutOfBound(selectedPos):
                        selectedPos = None

                    #Checking if the village was possibly extended by a building
                    if selectedPos is not None and selectedPos[0] < self.topVillageBorder[0]:
                        newVillageBorder = (selectedPos[0] - self.playStyle.playStyleMatrix[1][2], self.topVillageBorder[1])
                        self.newTopVillageBorder = newVillageBorder if not self.isOutOfBound(newVillageBorder) else None
                    if selectedPos is not None and selectedPos[1] > self.bottomVillageBorder[1]:
                        newVillageBorder = (self.topVillageBorder[0], selectedPos[1] + self.playStyle.playStyleMatrix[1][2])
                        self.newTopVillageBorder = newVillageBorder if not self.isOutOfBound(newVillageBorder) else None
                    elif selectedPos is not None and selectedPos[1] < self.topVillageBorder[1]:
                        newVillageBorder = (self.topVillageBorder[0], selectedPos[1] - self.playStyle.playStyleMatrix[1][2])
                        self.newTopVillageBorder = newVillageBorder if not self.isOutOfBound(newVillageBorder) else None

            if selectedPos is not None:
                return selectedPos

        # POSITION AU SUD - 7
        if selectedPos is None:
            # Recherche de position au sud du batiment
            self.logger("AIPlayer | getBuildTarget---- Searching positions south to the building")
            for x in range(self.topVillageBorder[0], self.bottomVillageBorder[0], size[0]):
                if x+size[0]>self.bottomVillageBorder[0] or selectedPos is not None:
                    if selectedPos is not None:
                        self.logger("AIPlayer | getBuildTarget---- Found position !")

                        return selectedPos
                    else:
                        pass
                else:
                    generalSize = (size[0]+1, size[1]+1)
                    tileOccupied = self.checkIfTilesAreOccupied(generalSize, (x, self.bottomVillageBorder[1]))
                    selectedPos = (x+1,self.bottomVillageBorder[1]+1) if not tileOccupied else None
                    self.logger("AIPlayer | getBuildTarget---- selectdPos iiiis : ", selectedPos)
                    if selectedPos is not None and self.isOutOfBound(selectedPos):
                        selectedPos = None

                    if selectedPos is not None and selectedPos[0] < self.topVillageBorder[0]:
                        newVillageBorder = (selectedPos[0] - self.playStyle.playStyleMatrix[1][2], self.topVillageBorder[1])
                        self.bottomVillageBorder = newVillageBorder if not self.isOutOfBound(newVillageBorder) else None
                    elif selectedPos is not None and selectedPos[0] > self.bottomVillageBorder[0]:
                        newVillageBorder = (selectedPos[0] - self.playStyle.playStyleMatrix[1][2], self.topVillageBorder[1])
                        self.newTopVillageBorder = newVillageBorder if not self.isOutOfBound(newVillageBorder) else None
                    if selectedPos is not None and selectedPos[1] > self.bottomVillageBorder[1]:

                        newVillageBorder = (self.topVillageBorder[0], selectedPos[1] - self.playStyle.playStyleMatrix[1][2])

                        self.newTopVillageBorder = newVillageBorder if not self.isOutOfBound(newVillageBorder) else None
            if selectedPos is not None:
                return selectedPos"""
        selectedPos = self.find_location_contour(size)
        if selectedPos is not None:
            return selectedPos
        # If no positions are found, expand the village
        self.logger("AIPlayer | getBuildTarget---- Time to expand village border")
        if self.newTopVillageBorder is not None or self.newBottomVillageBorder is not None:
            self.logger("AIPlayer | getBuildTarget---- new borders were registered")
            self.topVillageBorder = self.newTopVillageBorder if self.newTopVillageBorder is not None else self.topVillageBorder
            self.bottomVillageBorder = self.bottomVillageBorder if self.newBottomVillageBorder is not None else self.bottomVillageBorder
            return self.getBuildTarget(size)
        else:
            # If no positions are to be found at all, we expand the
            """self.logger("AIPlayer | getBuildTarget---- No buildings built, so expanding village naturally")
            villageBorder = [self.topVillageBorder, self.bottomVillageBorder]
            ax1 = self.world.width-self.topVillageBorder[0]
            bx1 = abs(0-self.topVillageBorder[0])
            distancex1 = abs(ax1 - bx1)
            ay1 = abs(self.world.height-self.topVillageBorder[1])
            by1 = abs(0-self.topVillageBorder[1])
            distancey1 = abs(ay1-by1)
            distanceTuple1 = (distancex1, distancey1)
            ax2 = self.world.width - self.bottomVillageBorder[0]
            bx2 = abs(0 - self.bottomVillageBorder[0])
            distancex2 = abs(ax2 - bx2)
            ay2 = abs(self.world.height - self.bottomVillageBorder[1])
            by2 = abs(0 - self.bottomVillageBorder[1])
            distancey2 = abs(ay2 - by2)
            distanceTuple2 = (distancex2, distancey2)
            allDistancesTuple = (distanceTuple1,distanceTuple2)
            selectedDistanceIndex = allDistancesTuple.index(min(allDistancesTuple))
            self.topVillageBorder = (self.topVillageBorder[0]-self.playStyle.playStyleMatrix[1][2],self.topVillageBorder[1]-self.playStyle.playStyleMatrix[1][2]) if villageBorder[selectedDistanceIndex] == self.topVillageBorder else self.topVillageBorder
            self.bottomVillageBorder = (self.bottomVillageBorder[0]+self.playStyle.playStyleMatrix[1][2],self.bottomVillageBorder[1]+self.playStyle.playStyleMatrix[1][2]) if villageBorder[selectedDistanceIndex] == self.bottomVillageBorder else self.bottomVillageBorder"""

    def getBuildingActionDict(self, buildingType):
        villagerType = "v"
        idList = self.getFreePeople(self.getOptimalBuildingCurve(1), villagerType)
        if len(idList) == 0:
            self.logger("LISTE D'UNITES LIBRE VIDE !!!!")
            return -1  # an error will be thrown later
        for i in idList:
            #self.logger(i)
            self.freeUnits[villagerType].remove(i)
        buildTarget= self.getBuildTarget(BuildingENUM[buildingType].value.surface)
        if buildTarget is None:
            return -1
        return {
            "action": "Build",
            "people": idList,
            "status" : "pending",
            "infos": {
                "type": buildingType,
                "target": buildTarget,
            }
        }

    def getResourcesActionDict(self, resourceToCollect : dict, type, nearestDP):
        self.logger("AIPlayer | getResourcesActionDict--- restoCollectVariable : ", resourceToCollect)
        resKey = next(iter(resourceToCollect.keys()))
        resourceInstance = self.world.ressources[type][resKey]
        unitID = self.getFreePeople(1,"v")
        if len(unitID) == 0:
            errorDict = {
            "action" : "collectResource",
            "infos" :{
                "type" : type,
                "target" : "ERROR",
                "targetKey" : "ERRORR",
            }}
            #self.logger("PAS D'UNITE DE DISPONIBLE")
            raise AIPeopleException(action=errorDict)
        for i in unitID:
            self.freeUnits["v"].remove(i)
        return {
            "action" : "collectResource",
            "people" : unitID,
            "infos" :{
                "type" : type,
                "target" : resourceInstance.position.toTuple(),
                "targetKey" : resKey,
                "nearestDP" : nearestDP,
                "quantity" : resourceInstance.quantity,
            }
        }

    def getHumanActionDict(self, units,type,targetUnit):
        return {
            "action" : "attackAction",
            "people" : units,
            "infos":{
                "unitType" : type,
                "targetType": targetUnit.name,
                "target" : targetUnit.position.toTuple(),
                "targetID" : targetUnit.uid,
                "targetTeam" :self.gm.getTeamNumber(targetUnit.uid),
            }
        }

    def setResourceAction(self, concernedRes):
        resPriority = self.getResourcesPriority()
        resPriority = (resPriority[0]*self.level,resPriority[1]*self.level,resPriority[2]*self.level)
        resDistance = {"w": concernedRes["w"]-resPriority[0],"g" : concernedRes["g"]-resPriority[1], "f" :concernedRes["f"]-resPriority[2]}
        resourceToGet =  min(resDistance, key=resDistance.get)
        self.logger("Ressource to get is", ResourceTypeENUM[resourceToGet].value)
        resToCollect = self.getNearestRessource(self.topVillageBorder,self.bottomVillageBorder,resourceToGet)
        self.logger("AIPlayer | setResourceAction--- resToCollectValue", resToCollect)
        nearestDP  = self.getNearestDropPoint(resToCollect)
        self.logger("AIPlayer | setResourceAction--- nearestDP Is", nearestDP)
        if resToCollect == -1:
            return -1
        if nearestDP == {-1 :-1}:
            return -1
        try :
            resourceCollectEvent = self.getResourcesActionDict(resToCollect, resourceToGet,nearestDP)
            self.logger("Added the following resCollect event : \n Type : ", resourceCollectEvent["infos"]["type"],
                        "\t nbOfPpl : ",
                        len(resourceCollectEvent["people"]), "\t Position of the ressource :",
                        resourceCollectEvent["infos"]["target"])
            self.logger("AIPlayer | setResourceAction--- resourceCollectEvent", resourceCollectEvent)
            self.eventQueue.append(resourceCollectEvent)
        except AIPeopleException as exp:
            self.logger("AIPlayer | setResourceAction--- Not enough people to collectResource")



    def setBuildingAction(self, buildings):
        if buildings["T"] == 0:
            buildingEvent = self.getBuildingActionDict(buildingType="T")
            self.eventQueue.append(buildingEvent)
        else:
            buildingPriority = self.getBuildingsPriority()
            builtBuildings = (
                (buildings["A"] + buildings["K"] + buildings["S"] + buildings["B"]), (buildings["H"] + buildings["T"]),
                (buildings["F"] + buildings["C"]))
            #self.logger("AIPlayer | setBuildingAction--- buildings community : ", self.team.community)
            # permet d'obtenir la distance à laquelle nous nous trouvons des objectifs de batiments à construire
            buildingObjectiveDistance = {"Military":builtBuildings[0]-buildingPriority[0], "Village": builtBuildings[1]-buildingPriority[1], "Farming" : builtBuildings[2]-buildingPriority[2]}
            leastDeveloppedBuildingType  = min(buildingObjectiveDistance, key=buildingObjectiveDistance.get)
            if buildingObjectiveDistance[leastDeveloppedBuildingType] == 0:
                #self.logger("All buildings have been built")
                return -1
            else:
                #self.logger("least developped building type number according to stats", buildingObjectiveDistance[leastDeveloppedBuildingType])
                #self.logger("least developped building type according to stats", leastDeveloppedBuildingType)
                leastDeveloppedBuildingName ="0"
                leastDeveloppedBuildingNumber = 0
                for i in BuildingTypeENUM[leastDeveloppedBuildingType].value:
                    if buildings[BuildingENUM(i).name] < leastDeveloppedBuildingNumber or leastDeveloppedBuildingName == "0" :
                        leastDeveloppedBuildingName = BuildingENUM(i).name
                        leastDeveloppedBuildingNumber = buildings[BuildingENUM(i).name]
                #self.logger("Least developped batiment is", BuildingENUM[leastDeveloppedBuildingName].value)
                buildingEvent = self.getBuildingActionDict(leastDeveloppedBuildingName)

                if buildingEvent == -1:
                    self.logger("No free units")
                    return -1

                self.logger("Added the following building event : \n Type : ", buildingEvent["infos"]["type"], "\t nbOfPpl : ", len(buildingEvent["people"]))
                self.eventQueue.append(buildingEvent)

    def setHumanAction(self):
        nearestVillageDistance = (10000,10000)
        nearestVillage = -1
        for a in self.world.villages:
            if a.name == self.team.name:
                pass
            else:
                firstTargetTCKey = next(iter(a.community["T"]))
                firstTCKey = next(iter(self.team.community["T"]))
                firstTargetTC = a.community["T"][firstTargetTCKey]
                firstTC = self.team.community["T"][firstTCKey]
                villageDistance = self.estimateDistance(firstTC.position.toTuple(),firstTargetTC.position.toTuple())
                if villageDistance[0]<nearestVillageDistance[0] and villageDistance[0]<nearestVillageDistance[1]:
                    nearestVillageDistance = villageDistance
                    nearestVillage = a
        self.logger("AIPlayer | setHumanAction--- nearestVillage is", nearestVillage)
        unitList = self.getFreePeople(1, "v")
        if len(unitList) == 0:
            return -1
        for u in unitList:
            self.freeUnits["v"].remove(u)

        firstUnitKey = next(iter(nearestVillage.community["v"]))
        firstUnit = nearestVillage.community["v"][firstUnitKey]
        self.logger("AIPlayer | setHumanAction--- we are going to attack", firstUnit)
        actionDict = self.getHumanActionDict(unitList,"v", firstUnit)
        self.eventQueue.append(actionDict)



    def launchResourceAction(self, actionDict):
        if actionDict["infos"]["target"] is None:
            self.eventQueue.remove(actionDict)
            return -1
        #self.logger("J'ai envoyé qqun chercher des ressources attention")
        unitList = actionDict["people"]
        unitTeam = self.gm.getTeamNumber(unitList[0])
        unitInstance = self.team.community["v"][actionDict["people"][0]]
        self.logger(self.world.ressources[actionDict["infos"]["type"]][actionDict["infos"]["targetKey"]])
        self.logger(actionDict["infos"]["targetKey"])

        resourceInstance = self.world.ressources[actionDict["infos"]["type"]][actionDict["infos"]["targetKey"]]
        exceptionRaised = False
        for i in unitList:
            self.world.villages[unitTeam-1].community["v"][i].target = self.world.ressources[actionDict["infos"]["type"]][(actionDict["infos"]["targetKey"])]
            targetPosition = Position(actionDict["infos"]["target"][0],actionDict["infos"]["target"][1])
            try:
                self.logger("LE TYPE DE RESOURCE INSTANCE J'EN AI MARRE", resourceInstance)
                self.gm.addRessourceToCollectDict(unitInstance,resourceInstance ,actionDict["infos"]["quantity"],actionDict["infos"]["nearestDP"])
            except PathfindingException:
                exceptionRaised = True
        if not exceptionRaised:
            self.currentEvents.append(actionDict)
            self.eventQueue.remove(actionDict)

    def launchBuildAction(self, actionDict):
        #self.logger("J'ai lancé une construction attention")
        buildingToBuild = actionDict["infos"]["type"]
        target = actionDict["infos"]["target"]
        newBuilding = BuildingENUM[buildingToBuild].value
        newInstanciatedBuilding = newBuilding(self.team)
        nearTiles = self.gm.getNearTiles((newBuilding.surface[0], newBuilding.surface[1]),
                                         (target[0], target[1]))
        self.logger("AIPlayer | NearTiles result --- Building surface is :",newBuilding.surface)
        for u in actionDict["people"]:
            self.logger("AIPlayer | launchBuildAction--- building position is, and sendingPeopleTo :", target,nearTiles)
            unit = self.team.community["v"][u]
            self.gm.dumbAddUnitToMoveDict(unit,Position(nearTiles[0][0],nearTiles[0][1]))
        self.team.add_building()
        actionDict["infos"]["uid"] = newInstanciatedBuilding.uid
        self.logger(actionDict)
        self.gm.addBuildingToBuildDict(newInstanciatedBuilding, target, actionDict["people"], nearTiles[0])
        self.logger("AIPlayer | launchBuildAction--- freeunits state",self.freeUnits)
        self.eventQueue.remove(actionDict)
        self.currentEvents.append(actionDict)
        #self.logger("AIPlayer | launchBuildAction----- ",target)
        #newInstanciatedBuilding.position = Position(target[0], target[1])
        #self.world.place_element(newInstanciatedBuilding)
        #self.team.community[buildingToBuild][newInstanciatedBuilding.uid] = newInstanciatedBuilding
        #for i in newInstanciatedBuilding.get_occupied_tiles():
        #    self.world.filled_tiles[i] = i
        #if target not in self.world.filled_tiles:
        #    self.logger("launchBuildAction----- Le batiment ne semble pas être construit")
        #if self.world.tiles_dico[target].contains is None:
        #    self.logger("launchBuildAction----- Batiment absent de la map")
        #self.clearBuildAction(actionDict)
        pass

    def launchHumanAction(self, actionDict):
        concernedUnits = []
        for a in actionDict["people"]:
            concernedUnits.append(self.team.community[actionDict["infos"]["unitType"]][a])
        targetUnit = self.world.villages[actionDict["infos"]["targetTeam"]-1].community[actionDict["infos"]["targetType"]][actionDict["infos"]["targetID"]]
        for u in actionDict["people"]:
            unit = self.team.community["v"][u]
            self.gm.dumbAddUnitToMoveDict(unit, Position(actionDict["infos"]["target"][0],actionDict["infos"]["target"][1]))
        self.logger("ATTAQUE INITIE !")
        self.gm.dumbAddUnitToAttackDict(concernedUnits,targetUnit)
        self.logger("J'ai lancé une attaque attention")
        self.currentEvents.append(actionDict)
        self.eventQueue.remove(actionDict)





    def launchAction(self, actionDict):
        ActionEnum[actionDict["action"]].value(self,actionDict)

    def checkActions(self):
        for k in self.currentEvents:
            self.logger("AIPlayer | checkAction--- Action to check is", k["action"])
            ActionCheckEnum[k["action"]].value(self, k)

    def checkBuildingAction(self, event):
        bldID = event["infos"]["uid"]
        if self.gm.checkBuildingStatus(bldID):
            event["status"] = "finished"
            self.clearBuildAction(event)

    def checkResourceAction(self,event):
        targetRes = event["infos"]["targetKey"]
        if self.gm.checkResourceStatus(targetRes):
            pass

    def checkAttackAction(self, event):
        unitID = event["people"]
        finishedEvent = False
        for i in unitID:
            finishedEvent = self.gm.checkAttackStatus(i)
        if finishedEvent:
            event["status"] = "finished"
            self.clearAttackAction(event)




    def clearBuildAction(self, actionDict):
        for i in actionDict["people"]:
            if not self.gm.checkIfDead(i, self.team):
                self.logger("AIPlayer | clearBuildAction : L'unité n'est pas morte")
                self.freeUnits["v"].append(i)
            else:
                self.logger("AIPlayer | clearBuildAction : L'unité est morte")
        self.pastEvents.append(actionDict)
        self.currentEvents.remove(actionDict)

    def clearAttackAction(self,actionDict):
        for i in actionDict["people"]:
            if not self.gm.checkIfDead(i, self.team):
                self.logger("AIPlayer | clearBuildAction : L'unité n'est pas morte")
                self.freeUnits["v"].append(i)
            else:
                self.logger("AIPlayer | clearBuildAction : L'unité est morte")
        self.pastEvents.append(actionDict)
        self.currentEvents.remove(actionDict)

    def writeLogs(self):
        if self.debug and self.writeToDisk:
            f = open(f"AILogs{self.team.name}.txt", "a")
            logs = output.getvalue()
            output.flush()
            f.write(logs)
            self.logs = ""





class ActionEnum(Enum):
    test = House
    Build = partial(AIPlayer.launchBuildAction)
    collectResource = partial(AIPlayer.launchResourceAction)
    attackAction = partial(AIPlayer.launchHumanAction)
class ActionCheckEnum(Enum):
    Build = partial(AIPlayer.checkBuildingAction)
    collectResource = partial(AIPlayer.checkResourceAction)
    attackAction = partial(AIPlayer.checkAttackAction)
if __name__ == "__main__":
    monde = World(100, 100)
    village1 = Model("1", monde)
    village2 = Model("2", monde)
    village1.initialize_villages(1, 2, 3,villages=50, gold=200, wood=100, food=300)
    village2.initialize_villages(4, 5, 6, gold=2, wood=1, food=3)
    v = Villager(village1)
    village1.add_unit(v)
    v.ressources_dict["w"] = 3
    v.ressources_dict["g"] = 2
    monde.fill_world()
    monde.fill_ressources(10)
    print(village1.population())
    print(monde.get_ressources())
    print("Before : ", village1.get_ressources())
    print("After : ", village1.get_ressources())
    print(v.ressources_dict)
    community = village1.get_community()
    # print(village2.population())
    #print(monde.get_ressources())
    #print(v)
    print(community)
    gm = GameManager(speed=1, world=monde)
    print("Launched GameManager")
    #gm.addUnitToMoveDict(v, Position(40, 40))
    #print("Added unit to move dict")
    #gm.addUnitToMoveDict(community["v"]["eq1p3"],community["a"]["eq1p0"].position)
    #print("Added 2nd unit to move dict")
    #print(monde.filled_tiles)

    tc = TownCenter(team=village1)
    monde.place_element(tc)
    monde.villages[0].community["T"][tc.uid] = tc
    #print("TC is in", tc.get_occupied_tiles())
    #print(gm.checkUnitsToMove())
    #Boucle pour tester le game manager
    n = 0
    play_style = PlayStyleEnum.b.value
    player = AIPlayer(village1, monde, play_style, level=100,gm=gm, debug=True, writeToDisk=False)

    print("tcSurface is ", tc.position)
    print("Player is out of bound (200,-40)?", (200,-40))
    print("Player is out of bound (-200,-40)?", (player.isOutOfBound((-200,-40))))
    print("Player is out of bound (10,101)?", (player.isOutOfBound((10,101))))
    print("Player is out of bound (-20,101)?", (player.isOutOfBound((10,101))))
    print("Player is out of bound (-20,10)?", (player.isOutOfBound((10,101))))

    #player.setVillageBorders(topBorder, tcSurface)
    for i in range(20):
        player.playTurn()
    print(monde.show_world())
    print(player.eventQueue)
    print(player.currentEvents)
    print(player.pastEvents)
    print(player.playStyle)

