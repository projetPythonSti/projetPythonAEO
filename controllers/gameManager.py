import timeit
from collections import defaultdict
from datetime import datetime
import time
import re
from importlib.resources import Resource

from models.Pathfinding import Pathfinding
from models.Position import Position
from models.World import World
from models.buildings.buildings import Building
from models.unity.Unity import Unity


class GameManager:


    """
        26/12/2024@tahakhetib : J'ai apporté les modifications suivantes
            - Adaptation de la fonction moveUnit() pour que celle-ci fasse bien bouger les unités sur la carte
        01/01/2025@tahakhetib : J'ai apporté les modifications suivantes
            - Corrigé le code de singe que j'ai écrit

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
    def __init__(self, speed, world: World ):
        self.gameSpeed = speed
        self.world = world

    def getTeamNumber(self, name):
        pattern = r'\d+'
        substrings = re.findall(pattern, name)
        print(substrings)
        return int(substrings[0])

    def moveUnit(self, id):
        deltaTime = timeit.default_timer() - self.tick
        unit = self.unitToMove[id]
        unit["timeElapsed"] += deltaTime.real
        #print("time elapsed : ", unit["timeElapsed"])
        if unit["timeElapsed"] >= (unit["timeToTile"]):
            unit["moveQueue"] = unit["moveQueue"][1::]
            unitObj = self.world.villages[(unit["team"]-1)].community[(unit["type"].lower())][id]
            self.world.remove_element(unitObj)
            self.world.villages[(unit["team"] - 1)].community[(unit["type"].lower())][id].position = Position(unit["moveQueue"][0][0],unit["moveQueue"][0][0])
            self.world.place_element(unitObj)
            unit["currentTile"] = unit["moveQueue"][0]
            print("Got to the next tile in", (unit["timeElapsed"]))
            unit["timeElapsed"] = 0
            if (len(unit["moveQueue"]) < 2):
                unit["moveQueue"] = []
            else:
                unit["nextTile"] = unit["moveQueue"][1]


    def checkUnitsToMove(self):
        if (len(self.unitToMove) == 0):
            print("No unit to move")
        else:
            unitToDelete = ""
            for k in self.unitToMove:
                if self.unitToMove[k]["moveQueue"] == []:
                    unitToDelete = k
                else:
                    self.moveUnit(k)
            if unitToDelete != "":
                self.unitToMove.pop(unitToDelete)


    def addUnitToMoveDict(self, unit : Unity, destination):
        if (unit.position.toTuple() not in self.world.filled_tiles.values()):
            self.world.filled_tiles[unit.position.toTuple()] = unit.position.toTuple()
        grid = self.world.convertMapToGrid()
        teamNumber = self.getTeamNumber(unit.uid)
        pathFinding  = Pathfinding(mapGrid=grid, statingPoint= (unit.position.getX(), unit.position.getY()), goal=(destination.getX(), destination.getY()))
        path = pathFinding.astar()
        if path.__class__ == bool:
            print("Found no short path")
        path = path + [pathFinding.startingPoint]
        path = path[::-1]

        self.unitToMove[unit.uid] = {
            "group"     : [],
            "timeToTile" : 1/(unit.speed),
            "timeElapsed" : 0,
            "nextTile" : path[1],
            "currentTile": path[0],
            "estimatedPos" : path[0],
            "team": teamNumber,
            "type" : unit.name,
            "moveQueue": path,
        }

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


if __name__ == "__main__":
    pass

