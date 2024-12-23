from collections import defaultdict
from datetime import datetime

from pygame.examples.music_drop_fade import starting_pos

from models.Pathfinding import Pathfinding
from models.World import World
from models.unity.Unity import Unity


class GameManager:
        tick = datetime.today()
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

        def moveUnit(self, id):
            unit = self.unitToMove[id]
            time = datetime.today() - self.tick
            milli_sec = (datetime.today().microsecond.real - self.tick.microsecond.real) // 1000
            print(milli_sec)
            print("time elapsed : ", unit["timeElapsed"])
            unit["timeElapsed"] += milli_sec
            if (unit["timeElapsed"] >= (unit["timeToTile"]*1000)):
                print("Got to the next tile in", unit["timeElapsed"])
                unit["timeElapsed"] = 0
                unit["moveQueue"] = unit["moveQueue"][1::]
                unit["currentTile"] = unit["moveQueue"][0]
                print(unit["moveQueue"])
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
            grid = self.world.convertMapToGrid()
            pathFinding  = Pathfinding(mapGrid=grid, statingPoint= (unit.position.getX(), unit.position.getY()), goal=(destination.getX(), destination.getY()))
            path = pathFinding.astar()
            if path.__class__ == bool:
                print("Found no short path")
            path = path + [pathFinding.startingPoint]
            path = path[::-1]
            self.unitToMove[unit.uid] = {
                "group" : [],
                "timeToTile" : 1/(unit.speed*self.gameSpeed),
                "timeElapsed" : 0,
                "nextTile" : path[1],
                "currentTile": path[0],
                "estimatedPos" : path[0],
                "moveQueue": path,
            }



if __name__ == "__main__":
    pass

