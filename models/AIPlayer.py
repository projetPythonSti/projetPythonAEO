from enum import Enum

from models.Position import Position
from models.World import World
from models.buildings.archery_range import ArcheryRange
from models.buildings.barracks import Barracks
from models.buildings.camp import Camp
from models.buildings.farm import Farm
from models.buildings.house import House
from models.buildings.keep import Keep
from models.buildings.stable import Stable
from models.buildings.town_center import TownCenter
from controllers.gameManager import GameManager
from models.model import Model
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

class PlayStyle:




    """
        Matrice de style de jeu
        [
          A B C
          D E F
          G H I
        ]

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


class AIPlayer:
    playing = False
    def __init__(self, team : Model, world : World, playStyle : PlayStyle):
        self.team = team
        self.world = world
        self.playStyle = playStyle
        self.freeUnits = {
            "v" : list(team.community["v"].keys()),
            "h" : list(team.community["h"].keys()),
            "s" : list(team.community["s"].keys()),
            "a" : list(team.community["a"].keys())
        }
        print("voici les unités libres ..",self.freeUnits)
        self.eventQueue = []


    def playTurn(self):
            self.playing = True
            workingPpl  = self.team.get_pplCount() - self.getFreePplCount()

            if workingPpl < playStyle.minWorkers:
                print("Minworkers hit, playing now")
                self.setBuildingAction(self.checkBuildings())
            else:
                print("RAS")


    def checkRessources(self):
        vRessources = self.team.get_ressources()
        return min(vRessources.values(), key=vRessources.get())

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


    def getOptimalBuildingCurve(self, BuildingType):
        return 3

    def getFreePplCount(self):
        return len(self.freeUnits["v"])+len(self.freeUnits["s"])+len(self.freeUnits["h"])+len(self.freeUnits["a"])


    def getFreePeople(self, number : int ,type):
        return self.freeUnits[type][:number]

    def getBuildTarget(self, size):
        print("Building Size", size)
        pass

    def getBuildingActionDict(self, buildingType):
        type = "v"
        idList = self.getFreePeople(self.getOptimalBuildingCurve(1), type)
        if len(idList) == 0:
            print("LISTE D'UNITES LIBRE VIDE !!!!")
            return -1  # an error will be thrown later
        for i in idList:
            print(i)
            self.freeUnits[type].remove(i)
        return {
            "action": "Build",
            "people": idList,
            "status" : "pending",
            "infos": {
                "type": buildingType,
                "target": self.getBuildTarget(BuildingENUM[buildingType].value.surface)
            }
        }

    def setResourceAction(self, concernedRes):

        pass


    def setBuildingAction(self, buildings):
        if buildings["T"] == 0:
            buildingEvent = self.getBuildingActionDict(buildingType="T")
            self.eventQueue.append(buildingEvent)
        if True:
            buildingPriority = self.getBuildingsPriority()
            builtBuildings = (
                (buildings["A"] + buildings["K"] + buildings["S"] + buildings["B"]), (buildings["H"] + buildings["T"]),
                (buildings["F"] + buildings["C"]))

            # permet d'obtenir la distance à laquelle nous nous trouvons des objectifs de batiments à construire
            buildingObjectiveDistance = {"Military":builtBuildings[0]-buildingPriority[0], "Village": builtBuildings[1]-buildingPriority[1], "Farming" : builtBuildings[2]-buildingPriority[2]}
            leastDeveloppedBuildingType  = min(buildingObjectiveDistance, key=buildingObjectiveDistance.get)
            buildingEvent = self.getBuildingActionDict(leastDeveloppedBuildingType)

            if buildingEvent == -1:
                print("No free units")
            self.eventQueue.append(buildingEvent)










if __name__ == "__main__":
    monde = World(100, 100)
    village1 = Model("1", monde)
    village2 = Model("2", monde)
    village1.initialize_villages(1, 2, 3, gold=200, wood=100, food=300)
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
    print("Added unit to move dict")
    gm.addUnitToMoveDict(community["v"]["eq1p6"], Position(10,20))
    print("Added 2nd unit to move dict")
    print(monde.filled_tiles)
    #print(gm.checkUnitsToMove())
    #Boucle pour tester le game manager
    n = 0
    playStyle = PlayStyle(minWorkers=2)
    playStyleMatrix= [
        [0,3,0],
        [0,4,0],
        [0,3,0]
    ]
    playStyle.setPlayStyleMatrix(playStyleMatrix)
    player = AIPlayer(village1,monde,playStyle)
    player.playTurn()
