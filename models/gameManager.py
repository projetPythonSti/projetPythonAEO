from collections import defaultdict

from controllers.Game_controller import Game_controller
from models.Pathfinding import Pathfinding


class GameManager:
        unitToMove = defaultdict()
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
        def __init__(self, speed, controller: Game_controller ):
            self.gameSpeed = speed
            self.controller = controller


        def moveUnit(self):
            pass

        def checkUnitsToMove(self):
            for k in self.unitToMove:
                    self.controller.model
            pass

        def addUnitToMoveDict(self):
            pass





