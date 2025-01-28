import http
import io
import math
import os
import socketserver
import sys
import threading
import timeit
from collections import defaultdict
from datetime import datetime
import time
import re
from http.server import HTTPServer
from typing import Tuple
import webbrowser

from models.Exceptions import PathfindingException
from models.Pathfinding import Pathfinding
from models.Position import Position
from models.World import World
from models.buildings.buildings import Building
from models.httpHandler import Serv, start_http_server
from models.ressources.ressources import Ressource
from models.unity.Unity import Unity
from enum import Enum
gmOutput = io.StringIO()


class buildingHealthENUM(Enum):
    T = 1000
    A = 500
    B = 500
    C = 200
    F = 100
    H = 200
    K = 800
    S = 500
class GameManager:


        """
            26/12/2024@tahakhetib : J'ai apporté les modifications suivantes
                - Adaptation de la fonction moveUnit() pour que celle-ci fasse bien bouger les unités sur la carte
            01/01/2025@tahakhetib : J'ai apporté les modifications suivantes
                - Corrigé le code de singe que j'ai écrit
            25/01/2025@tahakhetib : J'ai apporté les ajouts suivants sur le fichier (ce que j'ai écrit)
                - Ajouté les fonctions pour construire les batiments
                - Crée une fonction englobante pour toutes les actions du gameManager
            26/01/2025@tahakhetib :  J'ai apporté les modification suivantes sur le fichier (ce que j'ai écrit)
                - Corrigé le bug faisant qu'une unité n'avançait pas correctement dans la bonne direction
                - Corrigé l'algorithme de recherche de position près des batiments
                - Ajouté une fonction pour vérifier l'avancement de la construction d'un batiment
                - Ajouté les fonctions pour initier un combat
                - Ajouté les fonctions pour initer une collecte de ressources
            27/01/2025@tahakhetib : J'ai apporté des modifications sur ce que j'ai écrit
                - Crée des fonctions basiques de mouvements afin d'avoir une version stable

        """
        tick = timeit.default_timer()
        unitToMove = defaultdict(dict)

        '''
                    Syntaxe du dictionnaire
                    { 
                        idUnité | idGroup : {
                                    group : [idUnité1, idUnité2, idUnité3, idUnité4, idUnité5, idUnité6] // Si nous sommes dans le cadre d'un groupe d'unité à déplacer
                                    moveQueue : [(0,1),  (0,2),  (1,2)] // représente la file des positions à suivre pour atteindre la destination
                                    nextTile : (0,2) // représente la prochaine tuile dans laquelle doit se trouver le personnage (nécessaire car les personnages se déplacent à moins d'une tuile par seconde
                                    currentPos : (0,2) // Représente la position actuelle
                                   }
                    } 

                '''

        buildingsToBuild = defaultdict(dict)
        '''
            { 
                idBatiment : {
                    units : [idUnité1, idUnité2, idUnité3, idUnité4, idUnité5, idUnité6] // Toutes les unités assignées à la construction de ce batiment
                    nominalBuildTime : building.time_built
                    timeElapsed : Time // représente le temps passé à construire le batiment (ajout 
                    built : False // Représente si le batiment à été construit
                    position  : () // Position du batiment
                    team : 1 // equipe à laquelle le batiment appartient
                    nearTiles : list[Tuple[int,int]] // Tuiles situées à côté du batiment
                    type : building.name // Type du batiment
                
                /*** A noter que cette structure peut changer avec le temps ***/
                
                }
            } 
        '''
        unitAttack = defaultdict(dict)

        ressourceToCollect = defaultdict(dict)

        def __init__(self, speed , world: World,debug=False, writeToDisk=False ):
            self.gameSpeed = speed
            self.world = world
            self.debug = debug
            self.writeToDisk = writeToDisk
            self.save = False
            self.attackDict = defaultdict(list)
            self.pastAttacks = defaultdict(dict)

        def logger(self, *args, **kwargs):
            if self.debug:
                if self.writeToDisk:
                    sys.stdout = gmOutput
                    #print(*args, **kwargs)
                    sys.stdout = sys.__stdout__
                else:
                    #print(*args, **kwargs)
                    pass


        def checkModifications(self):
            self.logger("--------- Game Manager turn ---------")
            self.checkUnitsToMove()
            self.logger("--------- End Of CUTM ---------")
            self.checkBuildingsToBuild()
            self.logger("--------- End Of CBTB ---------")
            self.checkUnitToAttack()
            self.logger("--------- End Of CUTA ---------")
            self.checkResourceToCollect()
            self.logger("--------- End Of CUTA ---------")
            self.logger("--------- Game Manager End ---------")

        def getTeamNumber(self, name):
            pattern = r'\d+'
            substrings = re.findall(pattern, name)
            #print(substrings) #prints the subStrings extracted from the unitName
            return int(substrings[0])


        def moveUnit(self, uid):
            deltaTime = timeit.default_timer() - self.tick
            unit = self.unitToMove[uid]
            unit["timeElapsed"] += (deltaTime.real*self.gameSpeed)
            #self.logger("time elapsed : ", unit["timeElapsed"])
            if self.checkIfDead(uid, unit["team"]):
                self.logger("GameManager | moveUnit--- checking if dead")
                return -1
            if unit["timeElapsed"] >= (unit["timeToTile"]):
                unitObj = self.world.villages[(unit["team"]-1)].community[(unit["type"].lower())][uid]
                self.world.updateUnitPos(unit["moveQueue"][0], unit["moveQueue"][1], unitObj)
                unit["moveQueue"] = unit["moveQueue"][1::]
                self.world.villages[(unit["team"] - 1)].community[(unit["type"].lower())][uid].position = Position(unit["moveQueue"][0][0], unit["moveQueue"][0][1])
                self.logger("GameManager | moveUnit----- My position is ,",self.world.villages[(unit["team"] - 1)].community[(unit["type"].lower())][uid].position)
                #self.logger("GameManager | moveUnit----- Got to the next tile in : ", unit["timeElapsed"],"supposed to get in : ", unit["timeToTile"])
                self.logger("GameManager | moveUnit----- Infos on the nextTile to the next tile :", (unit["moveQueue"][0]), "lastTile is", (unit["goal"]))
                unit["currentTile"] = unit["moveQueue"][0]
                unit["timeElapsed"] = 0
                if (len(unit["moveQueue"]) < 2):
                    unit["moveQueue"] = []
                else:
                    unit["nextTile"] = unit["moveQueue"][1]

        def dumbMoveUnit(self, uid):
            deltaTime = timeit.default_timer() - self.tick
            unit = self.unitToMove[uid]
            unit["timeElapsed"] += (deltaTime.real * self.gameSpeed)
            if self.checkIfDead(uid, unit["team"]):
                self.logger("GameManager | moveUnit--- checking if dead")
                return -1
            if unit["timeElapsed"] >= (unit["timeToTile"]):
                unitObj = self.world.villages[(unit["team"] - 1)].community[(unit["type"].lower())][uid]
                self.world.updateUnitPos(unit["currentTile"], unit["goal"], unitObj)
                unitObj.position = Position(unit["goal"][0], unit["goal"][1])
                unit["arrived"] = True


        def buildBuilding(self, uid):
            deltaTime = timeit.default_timer() - self.tick
            building = self.buildingsToBuild[uid]
            readyToBuild = False
            buildingInstance = self.world.villages[building["team"]-1].community[building["type"]][uid]
            if self.checkIfDead(uid, building["team"]):
                building["error"] = True
                return -1
            #self.logger("GameManager | buildBuilding--- Building type :",buildingInstance.name)
            for unit in building["units"]:
                readyToBuild = self.unitNear(self.world.villages[building["team"]-1].community["v"][unit].position.toTuple(), building["nearTile"], building["type"])
                if readyToBuild:
                    self.world.villages[building["team"]-1].community[building["type"]][uid].builders += 1 if  buildingInstance.builders <= len(building["units"]) else 0
                else:
                    self.world.villages[building["team"]-1].community[building["type"]][uid].builders -= 1 if buildingInstance.builders > 0 else buildingInstance.builders
            timeToBuild = 3*building["nominalBuildTime"] / (buildingInstance.builders+2) if buildingInstance.builders>0 else -1
            #self.logger("GameManager | buildBuilding--- Temps pour construire le batiment :",timeToBuild)
            if timeToBuild > 0:
                if building["timeElapsed"] > timeToBuild:
                    self.logger("GameManager | buildBuilding--- BATIMENT CONSTRUIT")
                    building["built"] = True
                    buildingInstance.health = buildingHealthENUM[building["type"]].value
                else:
                    self.logger("GameManager | buildBuilding--- Now building the batiment")
                    building["timeElapsed"] += deltaTime*self.gameSpeed
                    buildingInstance.health += deltaTime*self.gameSpeed*buildingHealthENUM[building["type"]].value / timeToBuild
                    self.logger("Adding building time")
            else:
                pass
                self.logger("GameManager | buildBuilding--- Waiting for builders")

        def dumb_collectRessources(self, uid):

            """
            Se déclanche quand, cible unité = position ressource et position unité == position resource + ou - 1 (x,y)
            nouvel attribut a villagois -> début collect = timer début collect
            à chaque tour lancé dumb collect si condition rempli

            1er etape :
            if villageois.collect == None :
                villageois.collect = game.duration
                ressource.hp = ressource.hp -1
                villageois.pounch += 1
                if ressource.hp == 0 :
                    supprimer ressource du monde
                    villageois.collect = None
                    villageois.cible = None

            else if game.duration - villageois.collect >= 2.4 :
                if ressource.hp == 0 :
                    supprimer ressource du monde
                    villageois.collect = None
                    villageois.cible = None
                else :
                    villageois.collect += 2.4
                    ressource.hp = ressource.hp -1
                    villageois.pounch += 1
            """
            pass

        def collectResources(self, uid):
            deltaTime = timeit.default_timer() - self.tick
            resToCollect = self.ressourceToCollect[uid]
            if self.checkIfDead(uid, resToCollect["unitTeam"]):
                self.logger("GameManager | collectResources--- checking if dead")
                return -1
            # Line to check if the quantity to collect on said resource is still up to date
            realResQuantity = resToCollect["resourceQuantity"] if resToCollect["resourceQuantity"]<= self.world.ressources[resToCollect["resourceType"]][resToCollect["resourceID"]].quantity else self.world.ressources[resToCollect["resourceType"]][resToCollect["resourceID"]].quantity
            resToCollect["resourceQuantity"] = realResQuantity
            gameDTTime = (deltaTime.real*self.gameSpeed)
            unitInstance = self.world.villages[resToCollect["unitTeam"]-1].community["v"][uid]
            dpDistance = unitInstance.estimateDistance(unitInstance.position.toTuple(), resToCollect["nearDPPos"])
            if not resToCollect["routeStarted"]:
                if dpDistance< (1,1):
                    resToCollect["routeStarted"] = True
                    self.addUnitToMoveDict(unitInstance, Position(resToCollect["resourceTarget"][0],resToCollect["resourceTarget"][1]), prePath=resToCollect["pathToDP"][-1::])
                else:
                    self.logger("GameManager | collectResources--- Still not been to the nearestDP")
                    return -1
            resDistance = unitInstance.estimateDistance(unitInstance.position.toTuple(), resToCollect["resourceTarget"])
            unitSpaceLeft = unitInstance.spaceLeft()
            timeToFillPouch = int(unitSpaceLeft*60/25)
            if resDistance <= (1,1):
                self.logger("GameManager | collectResources--- Near to the ressource, begin collecting")
                if resToCollect["timeElapsed"] < timeToFillPouch and not resToCollect["full"]:
                    resToCollect["timeElapsed"] +=  gameDTTime
                elif resToCollect["timeElapsed"] > timeToFillPouch:
                    self.logger("GameManager | collectResources--- Pouch should be filled now")
                    quantityToCollect = unitSpaceLeft if unitSpaceLeft <= resToCollect["resourceQuantity"] else resToCollect["resourceQuantity"]
                    unitInstance.pouch[resToCollect["resourceType"]] += quantityToCollect
                    resToCollect["resourceQuantity"] -=  quantityToCollect
                    resToCollect["full"] = unitInstance.isFull()
                elif resToCollect["full"]:
                    self.logger("GameManager | collectResources--- Pouch is filled")
                    self.addUnitToMoveDict(unitInstance,resToCollect["nearDPPos"], prePath=resToCollect["pathToDP"])

            else:
                if resToCollect["full"]:
                    self.logger("GameManager | collectResources--- Full and going back to DP")
                    if dpDistance <= (1,1):
                        self.logger("GameManager | collectResources--- Arrived to DP")
                        unitInstance.dropResources()
                        resToCollect["full"] = False
                        resToCollect["finished"] = resToCollect["quantity"] == 0
                        if resToCollect["finished"]:
                            pass
                        else:
                            self.addUnitToMoveDict(unitInstance, resToCollect["nearDPPos"],prePath=resToCollect["pathToDP"][-1::])
                    else:
                        self.logger("GameManager | collectResources--- Waiting to arrive to DP")
                else:
                    self.logger("GameManager | collectResources--- Waiting to arrive to Resource")

        def attackUnit(self, uid):
            self.logger("GameManager | attackUnit--- Ennemi à attaquer")
            deltaTime = (timeit.default_timer() - self.tick)
            gameDeltaTime = deltaTime*self.gameSpeed
            attackingUnit = self.unitAttack[uid]
            if uid in self.world.villages[attackingUnit["team"]-1].deads:
                return -1
            attackingUnitInstance = self.world.villages[attackingUnit["team"]-1].community[attackingUnit["type"]][uid]
            targetPosition = attackingUnit["targetPosition"]
            if attackingUnit["targetID"] in self.world.villages[attackingUnit["targetTeam"]-1].deads:
                attackingUnit["success"] = True
                return -1
            targetInstance = self.world.villages[attackingUnit["targetTeam"]-1].community[attackingUnit["targetType"]][attackingUnit["targetID"]]
            self.logger("GameManager | attackUnit--- Quel type ?", targetInstance.name)
            self.logger("Game manager attackUnit--- Position unité,: ",attackingUnitInstance.position, "Position à atteindre :",targetInstance.position)
            if attackingUnit["movingTarget"]:
                self.logger("Game manager attackUnit--- Element qui bouge")
                if targetPosition != targetInstance.position.toTuple() and attackingUnitInstance.estimateDistance(targetPosition,targetInstance.position.toTuple()) < (10,10):
                    pass
                    """
                    self.unitToMove[uid]["currentTile"] = self.unitToMove[attackingUnit["targetID"]]["currentTile"] if attackingUnit["targetID"] in self.unitToMove else targetPosition
                    self.unitToMove[uid]["nextTile"] = self.unitToMove[attackingUnit["targetID"]]["nextTile"] if attackingUnit["targetID"] in self.unitToMove else targetInstance.position.toTuple()
                    self.unitToMove[uid]["moveQueue"] = self.unitToMove[attackingUnit["targetID"]]["moveQueue"] if attackingUnit["targetID"] in self.unitToMove else Pathfinding(mapGrid=self.world.convertMapToGrid(),statingPoint=attackingUnitInstance.position, goal=targetInstance.position)
                    attackingUnit["targetPosition"] = targetInstance.position.toTuple()"""
                    """self.logger("Game manager attackUnit--- Calcul à nouveau du chemin à suivre")
                    if attackingUnit["targetID"] in self.unitToMove and targetPosition != self.unitToMove[attackingUnit["targetID"]]["goal"] :
                        self.logger("Game manager attackUnit--- L'unité bougeait déjà et notre position enregistrée n'est pas la même")
                        self.addUnitToMoveDict(attackingUnitInstance, Position(self.unitToMove[attackingUnit["targetID"]]["goal"][0], self.unitToMove[attackingUnit["targetID"]]["goal"][0]))
                        attackingUnit["targetPosition"] = self.unitToMove[attackingUnit["targetID"]]["goal"]
                    elif not (attackingUnit["targetID"] in self.unitToMove):
                        self.logger("Game manager attackUnit--- L'unité ne bougeait pas et s'est mise à bouger")"""


            if attackingUnitInstance.isInRange(targetPosition):
                self.logger("GameManager | attackUnit--- Unit in Range")
                if not(attackingUnit["targetInRange"]):
                    self.logger("GameManager | attackUnit--- Adding unit to attackedUnitList")
                    self.attackDict[attackingUnit["targetTeam"]] += [(attackingUnit["targetType"], attackingUnitInstance,attackingUnitInstance.team.name)]
                attackingUnit["targetInRange"] = True
                if targetInstance.health < 0:
                    self.unitAttack[uid]["success"] = True
                    if issubclass(targetInstance.__class__, Unity):
                        #targetInstance.die()
                        self.world.villages[attackingUnit["targetTeam"]-1].markAsDead(targetInstance)
                        if targetInstance.uid in self.unitToMove:
                            self.logger("GameManager | attackUnit--- should pop targetInstance in unitToMove")
                            self.unitToMove.pop(targetInstance.uid)
                        if targetInstance.uid in self.ressourceToCollect:
                            self.logger("GameManager | attackUnit--- should pop targetInstance in resToCollect")
                            self.ressourceToCollect.pop(targetInstance.uid)
                        removeBuildAD = ""
                        for a in self.buildingsToBuild.keys():
                            unitToRemove = []
                            if self.getTeamNumber(a) == attackingUnit["targetTeam"]:
                                for k in self.buildingsToBuild[a]["units"]:
                                    if self.checkIfDead(k,attackingUnit["targetTeam"]):
                                        unitToRemove.append(k)
                                for unit in unitToRemove:
                                    self.logger("GameManager | attackUnit--- should pop targetInstance in buildingsToBuild", unit)
                                    self.buildingsToBuild[a]["units"].remove(unit)
                                try:
                                    self.buildingsToBuild[a]["units"][0]
                                except:

                                    removeBuildAD = a
                        if removeBuildAD is not "":
                            self.buildingsToBuild.pop(removeBuildAD)
                        self.pastAttacks[uid] = self.unitAttack[uid]
                    else:
                        self.logger("GameManager | attackUnit--- Seems to be a building who's been destroyed")
                else:
                    self.logger(f"GameManager | attackUnit---{attackingUnitInstance.damage*gameDeltaTime} PV enlevés  ")
                    self.world.villages[attackingUnit["targetTeam"] - 1].community[attackingUnit["targetType"]][attackingUnit["targetID"]].health -= attackingUnitInstance.damage*gameDeltaTime
            else:
                if uid in self.unitToMove:
                    self.unitToMove.pop(uid)
                self.world.updateUnitPos(attackingUnitInstance.position.toTuple(), targetInstance.position.toTuple(),
                                         attackingUnitInstance)
                attackingUnitInstance.position = targetInstance.position
                attackingUnit["targetPosition"] = targetInstance.position.toTuple()

        def dumbAttackUnit(self,uid):
            deltaTime = (timeit.default_timer() - self.tick)
            gameDeltaTime = deltaTime * self.gameSpeed
            attackingUnitDict = self.unitAttack[uid]
            attackingUnitTeam = attackingUnitDict["team"]
            attackingUnitType = attackingUnitDict["type"]
            attackingUnitInstance = self.world.villages[attackingUnitTeam-1].community[attackingUnitType][uid]
            targetUnitID = attackingUnitDict["targetID"]
            targetUnitInstance = self.world.villages[attackingUnitDict["targetTeam"] - 1].community[attackingUnitDict["targetType"]][attackingUnitDict["targetID"]]
            if attackingUnitInstance.isInRange(targetUnitInstance.position.toTuple()):
                if not(attackingUnitDict["targetInRange"]):
                    self.attackDict[int(attackingUnitDict["targetTeam"])] += [(attackingUnitDict["targetID"],attackingUnitInstance)]
                    self.logger("GameManager | collectResources--- Waiting to arrive to Resource")
                attackingUnitDict["targetInRange"] = True
                if attackingUnitDict["targetID"] in self.world.villages[attackingUnitDict["targetTeam"] - 1].deads:
                    attackingUnitDict["success"] = True
                    return -1
                if targetUnitInstance.health <= 0:
                    if issubclass(targetUnitInstance.__class__, Unity):
                        #targetInstance.die()
                        self.world.villages[attackingUnitDict["targetTeam"]-1].markAsDead(targetUnitInstance)
                        if targetUnitInstance.uid in self.unitToMove:
                            self.logger("GameManager | attackUnit--- should pop targetInstance in unitToMove")
                            self.unitToMove.pop(targetUnitInstance.uid)
                        if targetUnitInstance.uid in self.ressourceToCollect:
                            self.logger("GameManager | attackUnit--- should pop targetInstance in resToCollect")
                            self.ressourceToCollect.pop(targetUnitInstance.uid)
                        removeBuildAD = ""
                        for a in self.buildingsToBuild.keys():
                            unitToRemove = []
                            if self.getTeamNumber(a) == attackingUnitDict["targetTeam"]:
                                for k in self.buildingsToBuild[a]["units"]:
                                    if self.checkIfDead(k,attackingUnitDict["targetTeam"]):
                                        unitToRemove.append(k)
                                for unit in unitToRemove:
                                    self.logger("GameManager | attackUnit--- should pop targetInstance in buildingsToBuild", unit)
                                    self.buildingsToBuild[a]["units"].remove(unit)
                                try:
                                    self.buildingsToBuild[a]["units"][0]
                                except:

                                    removeBuildAD = a
                        if removeBuildAD is not "":
                            self.buildingsToBuild.pop(removeBuildAD)
                            self.buildingsToBuild.pop(targetUnitInstance.uid)
                        self.pastAttacks[uid] = self.unitAttack[uid]
                else:
                    self.world.villages[attackingUnitDict["targetTeam"] - 1].community[attackingUnitDict["targetType"]][attackingUnitDict["targetID"]].health -= attackingUnitInstance.damage*gameDeltaTime

            else:
                self.addUnitToAttackDict(attackingUnitInstance,targetUnitInstance.position)



        def checkIfDead(self, uid, team):
            try :
                self.world.villages[team - 1].deads[uid]
            except:
                return False
            return True

        def buiding_process(self, building):
            building.begin_building()
            self.time_elapse[building.uid] = 0
            begin_time = timeit.default_timer() - self.tick
            self.time_elapse += begin_time
            begin_time_seconds = self.time_elapse[building.uid] / timeit.default_timer().resolution

            if begin_time_seconds >= building.time_building:
                self.world.tiles_dico[(building.position.getX(), building.position.getY())].set_contains(building)

            #reshow the world here, because le buiding is finish to be built


        def checkUnitsToMove(self):
            if len(self.unitToMove) == 0:
                pass
            else:
                unitToDelete = ""
                for k in self.unitToMove:
                    if self.unitToMove[k]["arrived"]:
                        unitToDelete = k

                    else:
                        self.dumbMoveUnit(k)
                if unitToDelete != "":
                    self.unitToMove.pop(unitToDelete)

        def checkBuildingsToBuild(self):
            buildingToDelete = ""
            for k in self.buildingsToBuild:
                if self.buildingsToBuild[k]["built"]:
                    buildingToDelete = k

                else:
                    self.buildBuilding(k)
            if buildingToDelete != "":
                self.buildingsToBuild.pop(buildingToDelete)

        def checkResourceToCollect(self):
            resToDelete = ""
            for k in self.ressourceToCollect:
                if self.ressourceToCollect[k]["finished"]:
                    resToDelete= k
                else:
                   self.collectResources(k)
            if resToDelete != "":
                self.unitToMove.pop(resToDelete)

        def checkUnitToAttack(self):
            unitToDelete = ""
            self.logger("Unit attack is ---", self.unitAttack)
            for k in self.unitAttack:
                if self.unitAttack[k]["success"]:
                    unitToDelete= k
                else:
                    self.attackUnit(k)
            if unitToDelete != "":
                if self.unitAttack[unitToDelete]["targetID"] in self.unitAttack:
                    self.unitAttack.pop(self.unitAttack[unitToDelete]["targetID"])
                self.unitAttack.pop(unitToDelete)
        # idée, ajouter une représentation cassée dans le repr du building, et la faire changer lorsque celui-ci est en cours de construction


        def unitNear(self,unitPosition,nearTile : Tuple[int,int], type):
            self.logger("GameManager | unitNear--- unitPosition : ", unitPosition)
            self.logger("GameManager | unitNear--- NearTilePosition : ", nearTile)
            return unitPosition[0] == nearTile[0] and unitPosition[1] == nearTile[1]

        def getNearTiles(self, size, position):
            x_start, y_start = position
            width, height = size
            nearTiles = set()
            for x in range(x_start, x_start + width):
                nearTiles.add((x, y_start - 1))
            for x in range(x_start, x_start + width):
                nearTiles.add((x, y_start + height))
            for y in range(y_start, y_start + height):
                nearTiles.add((x_start - 1, y))

                # Ajouter les tuiles à l'est
            for y in range(y_start, y_start + height):
                nearTiles.add((x_start + width, y))

            """for x in range(size[0]):
                nearTiles.append((position[0]+x,position[1]))
                nearTiles.append((position[0]+x,position[1]+size[1]))
            for y in range(size[1]):
                nearTiles.append((position[0]+size[0], position[1]+y))
                nearTiles.append((position[0], position[1]+y))"""
            nearTiles = {tile for tile in nearTiles if (0<tile[0]<self.world.width) and (0<tile[1]<self.world.height) and (self.world.tiles_dico[tile].contains is None)}

            return list(nearTiles)

        def addBuildingToBuildDict(self, building : Building, target, unitsID: list[Unity],nearTileValue):
            teamNumber =  self.getTeamNumber(building.uid)
            building.health = 1
            building.position = Position(target[0],target[1])
            self.addBuildingToWorld(building, target)
            #self.logger("GameManager | addBuildingToBuildDict--- Near tile are : ", nearTileValue)
            self.logger({
                "units": unitsID,
                "nominalBuildTime": building.time_building,
                "timeElapsed": 0,
                "position":target,
                "built" : False,
                "team": teamNumber,
                "nearTile" :nearTileValue ,
                "type": building.name,
                "error" : False,
            })
            self.buildingsToBuild[building.uid] = {
                "units": unitsID,
                "nominalBuildTime": building.time_building,
                "timeElapsed": 0,
                "position":target,
                "built" : False,
                "team": teamNumber,
                "nearTile" :nearTileValue ,
                "type": building.name,
                "error" : False,
            }

        def dumbAddUnitToMoveDict(self, unit : Unity, destination : Position):
            start = unit.position.toTuple()
            end = destination.toTuple()
            distXY = (abs(end[0]- start[0]), abs(end[1]-start[1]))
            dist = math.sqrt(distXY[0]**2+distXY[1]**2)
            teamNumber = self.getTeamNumber(unit.uid)
            self.logger("hello")
            self.unitToMove[unit.uid] = {
                "timeToTile": (1/unit.speed)*dist,
                "timeElapsed": 0,
                "currentTile": unit.position.toTuple(),
                "goal": end,
                "arrived": False,
                "team" : teamNumber,
                "type" : unit.name
            }

        def addUnitToMoveDict(self, unit : Unity, destination : Position,prePath=[]):
            #self.logger("GameManager | addUnitToMoveDict--- Unit destination is : ", destination)
            grid = self.world.convertMapToGrid()
            teamNumber = self.getTeamNumber(unit.uid)
            destTuple = destination.toTuple()
            unitTuple = unit.position.toTuple()
            if (abs(destTuple[0]-unitTuple[0]) <= 2 and abs(destTuple[1]-unitTuple[1]) <= 2):
                self.logger("GameManager | addUnitToMoveDict--- distance is really short")
                path = [unitTuple, destTuple]
                self.unitToMove[unit.uid] = {
                    "group": [],
                    "timeToTile": 1 / (unit.speed),
                    "timeElapsed": 0,
                    "nextTile": path[1],
                    "currentTile": path[0],
                    "estimatedPos": path[0],
                    "goal": destination.toTuple(),
                    "team": teamNumber,
                    "type": unit.name,
                    "moveQueue": path,
                    "error": False,
                }
                return -1
            pathFinding  = Pathfinding(mapGrid=grid, statingPoint= unit.position.toTuple(), goal=destination.toTuple(), debug=False)
            path = []
            prePathSet = False
            try:
                prePath[0]
                prePathSet = True
            except:
                prePathSet = False
            if prePathSet:
                self.logger("GameManager | addUnitToMoveDict--- Prepath is not null")
                path = prePath
            else :
                path = pathFinding.astar()
            if path.__class__ == bool:
                raise PathfindingException(self.world.tiles_dico[destination.toTuple()])
                #  : AJOUTER UNE EXCEPTION QUAND IL NE TROUVE VRAIMENT PAS DE CHEMIN
                #self.logger("Found no short path")
            path = path + [pathFinding.startingPoint]
            path = path[::-1]
            self.logger("Unit ADDED TO MOVE DICT")
            #self.logger("GameManager | addUnitToMoveDict--- Path is  : ", path)
            self.unitToMove[unit.uid] = {
                "group"     : [],
                "timeToTile" : 1/(unit.speed),
                "timeElapsed" : 0,
                "nextTile" : path[1],
                "currentTile": path[0],
                "estimatedPos" : path[0],
                "goal": destination.toTuple(),
                "team": teamNumber,
                "type" : unit.name,
                "moveQueue": path,
                "error": False,
            }

        def addUnitToAttackDict(self, units, target):

            unitTeam = self.getTeamNumber(units[0].uid)
            targetTeam = self.getTeamNumber(target.uid)
            targetPosition = target.position.toTuple()
            if unitTeam == targetTeam:
                self.logger("GameManager | addUnitToAttackDict--- Friendly fire is not allowed")
                return 0
            movingUnit = target.uid in self.unitToMove
            if type(target) == Unity:
                if movingUnit :
                    targetPosition =  self.unitToMove[target]["goal"]
            else:
                for u in units:
                    self.unitAttack[u.uid] = {
                        "targetID": target.uid,
                        "targetType": target.name,
                        "type" : u.name,
                        "targetInRange": False,
                        "targetPosition": targetPosition,
                        "moving" : movingUnit,
                        "movingTarget": True if issubclass(target.__class__, Unity) else False,
                        "success" : False,
                        "team": unitTeam,
                        "targetTeam" : targetTeam,
                        "error": False,
                    }

        def dumbAddUnitToAttackDict(self,units,target):
            self.logger("AJOUT D'UNITÉS A ATTAQUER KFK")
            unitTeam = self.getTeamNumber(units[0].uid)
            targetTeam = self.getTeamNumber(target.uid)
            targetPosition = target.position.toTuple()
            if unitTeam == targetTeam:
                self.logger("GameManager | addUnitToAttackDict--- Friendly fire is not allowed")
                return 0
            else:
                for u in units:

                    self.unitAttack[u.uid] = {
                        "targetID": target.uid,
                        "targetType": target.name,
                        "type": u.name,
                        "targetInRange": False,
                        "targetPosition": targetPosition,
                        "movingTarget": True if issubclass(target.__class__, Unity) else False,
                        "success": False,
                        "team": unitTeam,
                        "targetTeam": targetTeam,
                        "error": False,
                    }

        def addRessourceToCollectDict(self, unit,resource : Ressource, quantity, nearDP):
            self.addUnitToMoveDict(unit, nearDP.position)
            grid = self.world.convertMapToGrid()
            pathFinding  = Pathfinding(mapGrid=grid, statingPoint= nearDP.position.toTuple(), goal=resource.position.toTuple(), debug=False)
            path = pathFinding.astar()
            if path.__class__ == bool:
                raise PathfindingException(self.world.tiles_dico[resource.position.toTuple()])
                #  : AJOUTER UNE EXCEPTION QUAND IL NE TROUVE VRAIMENT PAS DE CHEMIN
                #self.logger("Found no short path")
            path = path + [pathFinding.startingPoint]
            self.ressourceToCollect[unit.uid] = {
                "unit" : unit.uid,
                "unitTeam": self.getTeamNumber(unit.uid),
                "resourceType" : resource.name,
                "resourceTarget" : resource.position.toTuple(),
                "resourceID" : resource.uid,
                "resourceQuantity" : quantity,
                "timeElapsed" : 0,
                "finished" : False,
                "full": False,
                "nearDPPos" : nearDP.position.toTuple(),
                "routeStarted": False,
                "pathToDP": path,
                "error" : False
            }

        def addBuildingToWorld(self, building:Building, position):
            self.world.place_element(building)
            teamNumber = int(building.team.name)
            self.world.villages[teamNumber-1].community[building.name][building.uid] = building
            occupiedTiles = building.get_occupied_tiles()
            for a in occupiedTiles:
                self.world.filled_tiles[a] = a
        def pause(self):
            self.html_generator()

            # def play(self):
            #     datas = self.load_from_file()
            #     if datas:
            #         self.world = datas[0]

        def checkBuildingStatus(self,id):
            if id in self.buildingsToBuild:
                return self.buildingsToBuild[id]["built"]
            else:
                return True

        def checkAttackStatus(self,id):
            if id in self.unitAttack:
                return self.unitAttack[id]["success"]
        def returnBuildingEvent(self,id):
            if id in self.buildingsToBuild:
                return self.buildingsToBuild[id]
            else:
                return None
        def checkResourceStatus(self,id):
            if id in self.ressourceToCollect:
                return False

        def save_world(self, path=None):
            self.save.save(self.world, path)

        def load_from_file(self, path=None):
            data = self.save.load(path)
            # print("data", data)
            self.world = data[0]

        def html_generator(self):
            village1, village2 = self.world.villages
            #iterating on 2 dict at the same time

            body = f"""
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Game Stats</title>
            </head>
            <body>
                <h1>Welcome to the Game</h1>
                <p>You made a pause, so here are current information about the world</p>
                <ul>
                
            """
            for pop1, pop2 in zip(village1.population().values(), village2.population().values()):
                for v1, v2 in zip(pop1.values(), pop2.values()):
                    body += f"""
                    <li>Unit {v2.__class__} is at position ({v2.position.getX()}, {v2.position.getY()}) and his life is {v2.health}</li>
                    <li>Unit {v1.__class__} is at position ({v1.position.getX()}, {v1.position.getY()}) and his life is {v1.health}</li>
                    """
            body += """ 
                </ul> 
                </body>
                </html>
            """

            with open("./utils/html/gameStats.html", "w") as file:
                file.write(body)

        def openHtmlPage(self):
            directory_to_serve = "assets/web"  # Replace with the folder you want to serve
            port = 8000

            # Start the server in a separate thread
            server_thread = threading.Thread(target=start_http_server, args=(directory_to_serve, port), daemon=True)
            server_thread.start()
            # Define the handler and server
            webbrowser.open("http://localhost:8000",new=0, autoraise=True )
            # Start the server

        print("finisshed server")
if __name__ == "__main__":
    pass

