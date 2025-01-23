from argparse import Action
from collections import defaultdict
from distutils.command.build import build
from enum import Enum
from os import fdopen
from select import select
from tokenize import tabsize
from typing import final
from functools import partial

import numpy as np
from numpy.f2py.crackfortran import debug

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

    def __init__(self, minWorkers):
        self.playStyleMatrix = []
        self.minWorkers = minWorkers


    def setPlayStyleMatrix(self, matrix):
        self.playStyleMatrix = matrix

    def getPlayStyleMatrix(self):
        return self.playStyleMatrix


class AIPlayer:
    playing = False
    def __init__(self, team : Model, world : World, playStyle : PlayStyle, level : int, gm : GameManager, debug=False):
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
        self.gm = gm
        self.eventQueue = []
        self.pastEvents = []
        self.currentEvents = []
        self.debug = debug

    def logger(self,*args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def setVillageBorders(self, topLeftPos, bottomRightPos):
        self.topVillageBorder = topLeftPos
        self.bottomVillageBorder = bottomRightPos


    def playTurn(self):
        self.logger("------ START OF AI TURN ------")
        #self.logger("Village border atm => ", self.topVillageBorder, self.bottomVillageBorder)
        self.playing = True
        workingPpl  = self.team.get_pplCount() - self.getFreePplCount()
        if workingPpl < self.playStyle.minWorkers:
            self.logger("Minworkers hit, playing now")
            self.setBuildingAction(self.checkBuildings())
            self.setResourceAction(self.team.ressources)
            self.logger(len(self.eventQueue))
            numberOfActions = 0
            for k in range(len(self.eventQueue)):
                numberOfActions += 1
                self.logger(self.eventQueue[k-1]["action"])
                self.launchAction(self.eventQueue[k-1])
            print(numberOfActions)
        else:
            self.logger("RAS")
        self.logger("Voici le nombre de personnes libres",self.getFreePplCount(), "Et le nb de personnes total : ",self.team.get_pplCount())
        self.logger("------ END OF AI TURN ------")



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
        nearestResourcesIndex = resourcesPositionList.index(min(resourcesPositionList))
        return {
            ressourceKeyDict[nearestResourcesIndex] : resourcesPositionList[nearestResourcesIndex]
        }


    def getOptimalBuildingCurve(self, BuildingType):
        return 3

    def getFreePplCount(self):
        return len(self.freeUnits["v"])+len(self.freeUnits["s"])+len(self.freeUnits["h"])+len(self.freeUnits["a"])

    def getFreePeople(self, number : int ,type):
        return self.freeUnits[type][:number]


    def checkIfTilesAreOccupied(self, size, position):
        for a in self.getOccupiedTiles(size,position):
            self.logger("checkIfTilesAreOccupied ----- a values is in filled_tiles ? ", self.world.filled_tiles[a])
            if a in self.world.filled_tiles.values():
                self.logger("checkIfTilesAreOccupied ----- value is indeed in filledTiles ", self.world.filled_tiles[a])
                return True
            else:
                pass
        return False #self.getOccupiedTiles(size,position) in list(self.world.filled_tiles.keys())

    def getOccupiedTiles(self,size, position):
        return [(position[0] + x, position[1] + y) for x in range(size[0]) for y in range(size[1])]

    def getBuildTarget(self, size):
        selectedPos = None
        tilesOccupiedFirst = False
        btVillageBorder = self.bottomVillageBorder[0]
        for x in range(self.topVillageBorder[0], btVillageBorder, size[0]):
            if x+size[0]>self.bottomVillageBorder[0] or selectedPos is not None:
                if selectedPos is not None:
                    self.logger("Found position !")
                    return selectedPos
                    # When a suitable position has already been found
                else:
                    # If the position is outside of the borders of the village
                    self.logger("do nothing, outside of village border in the game")
            else:
                self.logger("searching positions north to the building")
                tileOccupied = self.checkIfTilesAreOccupied(size, (x, self.topVillageBorder[1]-1))
                self.logger("Check if tiles are occupied result : ", tileOccupied )
                selectedPos = (x+tilesOccupiedFirst,self.topVillageBorder[1]-tilesOccupiedFirst) if (not tileOccupied) else None
                self.logger("selectdPos iiiis : ", selectedPos)
        if selectedPos is None:
            self.logger("searching positions east to the building")
            # Recherche de position disponible à l'est du batiment
            for y in range(self.topVillageBorder[1], self.bottomVillageBorder[1], size[1]):
                if y+size[0]>self.bottomVillageBorder[1] or selectedPos is not None:
                    if selectedPos is not None:
                        return selectedPos
                    else:
                        pass
                else:
                    self.logger("Check if tiles are occupied result : ",
                          self.checkIfTilesAreOccupied(size, (x, self.topVillageBorder[1])))
                    selectedPos = self.bottomVillageBorder[0]-size[0],y if self.checkIfTilesAreOccupied(size, (self.bottomVillageBorder[0]-size[0], y)) else None
                    self.logger("selectdPos iiiis : ", selectedPos)
        if selectedPos is None:
            self.logger("searching positions west to the building")
            # Recherche de position disponible à l'ouest du batiment
            for y in range(self.topVillageBorder[1], self.bottomVillageBorder[1], size[1]):
                if y+size[0]>self.bottomVillageBorder[1] or selectedPos is not None:
                    if selectedPos is not None:
                        return selectedPos
                    else:
                        pass
                else:
                    selectedPos = self.topVillageBorder[0]-size[0],y if self.checkIfTilesAreOccupied(size, (self.topVillageBorder[0]-size[0], y)) else None
        if selectedPos is None:
            # Recherche de position au sud du batiment
            self.logger("Searching positions south to the building")
            for x in range(self.topVillageBorder[0], self.bottomVillageBorder[0], size[0]):
                if x+size[0]>self.bottomVillageBorder[0] or selectedPos is not None:
                    if selectedPos is not None:
                        return selectedPos
                    else:
                        pass
                else:
                    selectedPos = x,self.bottomVillageBorder[1] if self.checkIfTilesAreOccupied(size, (x, self.bottomVillageBorder[1])) else None


    def getBuildingActionDict(self, buildingType):
        villagerType = "v"
        idList = self.getFreePeople(self.getOptimalBuildingCurve(1), villagerType)
        if len(idList) == 0:
            self.logger("LISTE D'UNITES LIBRE VIDE !!!!")
            return -1  # an error will be thrown later
        for i in idList:
            #self.logger(i)
            self.freeUnits[villagerType].remove(i)
        return {
            "action": "Build",
            "people": idList,
            "status" : "pending",
            "infos": {
                "type": buildingType,
                "target": self.getBuildTarget(BuildingENUM[buildingType].value.surface)
            }
        }

    def getResourcesActionDict(self, resourceToCollect : dict, type):
        resourceToCollectKey = next(iter(resourceToCollect.keys()))
        unitID = self.getFreePeople(1,"v")
        if len(unitID) == 0:
            self.logger("PAS D'UNITE DE DISPONIBLE")
        for i in unitID:
            self.freeUnits["v"].remove(i)
        return {
            "action" : "collectResource",
            "people" : unitID,
            "infos" :{
                "type" : type,
                "target" : resourceToCollect[resourceToCollectKey],
                "targetKey" : resourceToCollectKey,
            }
        }


    def setResourceAction(self, concernedRes):
        resPriority = self.getResourcesPriority()
        resPriority = (resPriority[0]*self.level,resPriority[1]*self.level,resPriority[2]*self.level)
        resDistance = {"w": concernedRes["w"]-resPriority[0],"g" : concernedRes["g"]-resPriority[1], "f" :concernedRes["f"]-resPriority[2]}
        resourceToGet =  min(resDistance, key=resDistance.get)
        #self.logger("Ressource to get is", ResourceTypeENUM[resourceToGet].value)
        resToCollect = self.getNearestRessource((0,0),(0,4),resourceToGet)
        resourceCollectEvent = self.getResourcesActionDict(resToCollect, resourceToGet)
        self.logger("Added the following resCollect event : \n Type : ", resourceCollectEvent["infos"]["type"], "\t nbOfPpl : ",
              len(resourceCollectEvent["people"]))
        self.eventQueue.append(resourceCollectEvent)


    def setBuildingAction(self, buildings):
        if buildings["T"] == 0:
            buildingEvent = self.getBuildingActionDict(buildingType="T")
            self.eventQueue.append(buildingEvent)
        else:
            buildingPriority = self.getBuildingsPriority()
            builtBuildings = (
                (buildings["A"] + buildings["K"] + buildings["S"] + buildings["B"]), (buildings["H"] + buildings["T"]),
                (buildings["F"] + buildings["C"]))

            # permet d'obtenir la distance à laquelle nous nous trouvons des objectifs de batiments à construire
            buildingObjectiveDistance = {"Military":builtBuildings[0]-buildingPriority[0], "Village": builtBuildings[1]-buildingPriority[1], "Farming" : builtBuildings[2]-buildingPriority[2]}
            leastDeveloppedBuildingType  = min(buildingObjectiveDistance, key=buildingObjectiveDistance.get)

            leastDeveloppedBuildingName = "0"
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
        pass

    def launchResourceAction(self, actionDict):
        #self.logger("J'ai envoyé qqun chercher des ressources attention")
        unitList = actionDict["people"]
        unitTeam = self.gm.getTeamNumber(unitList[0])
        for i in unitList:
            self.world.villages[unitTeam-1].community["v"][i].target = self.world.ressources[actionDict["infos"]["type"]][(actionDict["infos"]["targetKey"])]
            targetPosition = Position(actionDict["infos"]["target"][0],actionDict["infos"]["target"][0])
            self.gm.addUnitToMoveDict(self.world.villages[unitTeam-1].community["v"][i],targetPosition)
        self.currentEvents.append(actionDict)
        self.eventQueue.remove(actionDict)

    def launchBuildAction(self, actionDict):
        #self.logger("J'ai lancé une construction attention")
        buildingToBuild = actionDict["infos"]["type"]
        target = actionDict["infos"]["target"]
        newBuilding = BuildingENUM[buildingToBuild].value
        newInstanciatedBuilding = newBuilding(self.team)
        newInstanciatedBuilding.position = Position(target[0], target[1])
        self.world.place_element(newInstanciatedBuilding)
        self.team.community[buildingToBuild][newInstanciatedBuilding.uid] = newInstanciatedBuilding
        for i in newInstanciatedBuilding.get_occupied_tiles():
            self.world.filled_tiles[i] = i
        if target not in self.world.filled_tiles:
            self.logger("launchBuildAction----- Le batiment ne semble pas être construit")
        if self.world.tiles_dico[target].contains is None:
            self.logger("launchBuildAction----- Batiment absent de la map")
        self.clearBuildAction(actionDict)
        pass

    def launchHumanAction(self, actionDict):
        pass
        #self.logger("J'ai lancé une attaque attention")

    def launchAction(self, actionDict):
        ActionEnum[actionDict["action"]].value(self,actionDict)

    def clearBuildAction(self, actionDict):
        for i in actionDict["people"]:
            self.freeUnits["v"].append(i)
        self.pastEvents.append(actionDict)
        self.eventQueue.remove(actionDict)






class ActionEnum(Enum):
    test = House
    Build = partial(AIPlayer.launchBuildAction)
    collectResource = partial(AIPlayer.launchResourceAction)
    attackAction = partial(AIPlayer.launchHumanAction)

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
    #print(community)
    gm = GameManager(speed=1, world=monde)
    print("Launched GameManager")
    gm.addUnitToMoveDict(v, Position(40, 40))
    #print("Added unit to move dict")
    gm.addUnitToMoveDict(community["v"]["eq1p3"],community["a"]["eq1p0"].position)
    #print("Added 2nd unit to move dict")
    #print(monde.filled_tiles)

    tc = TownCenter(team=village1)
    monde.place_element(tc)
    monde.villages[0].community["T"][tc.uid] = tc
    #print("TC is in", tc.get_occupied_tiles())
    #print(gm.checkUnitsToMove())
    #Boucle pour tester le game manager
    n = 0
    play_style = PlayStyle(minWorkers=10)
    playStyleMatrix= [
        [4,3,0],
        [2,6,2],
        [1,3,0]
    ]
    play_style.setPlayStyleMatrix(playStyleMatrix)
    player = AIPlayer(village1, monde, play_style, level=100,gm=gm, debug=True)
    tcSurface = (tc.position.getX()+tc.surface[0]+playStyleMatrix[1][2], tc.position.getY()+tc.surface[1]+playStyleMatrix[1][2])
    topBorder = (tc.position.getX()-playStyleMatrix[1][2], tc.position.getY()-playStyleMatrix[1][2])
    print("tcSurface is ", tc.position)
    player.setVillageBorders(topBorder, tcSurface)
    for i in range(20):
        player.playTurn()
    print(monde.show_world())
    print(player.eventQueue)
    print(player.currentEvents)
    print(player.pastEvents)
    print(player.playStyle)

