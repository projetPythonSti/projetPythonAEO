
from models.unity.Archer import  Archer
from models.unity.Horseman import Horseman
from models.unity.Swordsman import Swordsman
from models.unity.Villager import Villager
from models.buildings.town_center import TownCenter
from models.buildings.archery_range import ArcheryRange
from models.buildings.barracks import Barracks
from models.buildings.camp import Camp
from models.buildings.farm import Farm
from models.buildings.house import House
from models.buildings.keep import Keep
from models.buildings.stable import Stable
from models.ressources.ressources import Ressource, Gold, Wood, Food
# from ressources.mressources import *

#faut-il l'importer et le faire hériter pour pouvoir utiliser fire_change ?
# from controllers import Game_controller
# from unity import Unity
from collections import defaultdict



class Model:
    """
            22/12/2024@tahakhetib - J'ai apporté des modifications à ce fichier sur ce que @amadou_yaya_diallo a écrit
            - Ajouté une fonction get_name afin d'obtenir le nom d'équipe (utilisé dans Villager.py).
            - Changé la manière dont les unités sont ajoutées dans initialize_villages() pour faire en sorte que les nouveaux ID soient utilisés
            - Ajouté un compteur de population pour directement avoir accès au nombre de personnes faisant partie du village (avec le getter associé)
            04/12/2024@tahakhetib - J'ai ajouté des modifications au-dessus de ce que @amadou_yaya_diallo a écrit
                - Ajouté un compteur workingPpl qui va permettre aux IA de suivre le nombre de personnes qui doivent travailler.
            05/12/2024@tahakhetib - J'ai ajouté les modifications au-dessus de ce que @amadou_yaya_diallo a écrit
                - Retiré les compteurs workingPpl et peopleCount pour une fonction get_pplCount()

    """
    def __init__(self, name, world = None):

        # Dictionary of human, materiel and ressources of the village
        self.community = defaultdict(dict)
        self.ressources = defaultdict(int)
        self.peopleCount = 0
        self.workingPpl = 0
        self.name = name
        self.world = world
        self.world.add_village(self)

    def initialize_villages(self, archers = 0, horsmen = 0, swordsmen = 0, villages = 0, town_center = 0,
                            stables = 0, keeps = 0, houses = 0, farms = 0, camps = 0, barracks = 0, 
                            archery_ranger = 0, wood = 0, food = 0, gold = 0):
        for i in range(archers):
            self.peopleCount += 1
            a = Archer(team=self)
            self.community["a"][a.uid] = a

        for i in range(horsmen):
            self.peopleCount += 1
            h = Horseman(team=self)
            self.community["h"][h.uid] = h
   
        for i in range(villages):
            self.peopleCount += 1
            v = Villager(team=self)
            self.community["v"][v.uid] = v
        
        for i in range(swordsmen):
            self.peopleCount += 1
            s = Swordsman(team=self)
            self.community["s"][s.uid] = s
        
        for i in range(town_center):
            self.community["T"][str(i)] = TownCenter(team=self)
        
        for i in range(archery_ranger):
            self.community["A"][str(i)] = ArcheryRange(team=self)

        for i in range(barracks):
            self.community["B"][str(i)] = Barracks(team=self)

        for i in range(camps):
            self.community["C"][str(i)] = Camp(team=self)

        for i in range(farms):
            self.community["F"][str(i)] = Farm(team=self)

        for i in range(houses):
            self.community["H"][str(i)] = House(team=self)

        for i in range(keeps):
            self.community["K"][str(i)] = Keep(team=self)

        for i in range(stables):
            self.community["S"][str(i)] = Stable(team=self)
        
        self.ressources["w"] += wood
        self.ressources["g"] += gold
        self.ressources["f"] += food

    # def initialize_unit(self, unit):
    #     self.community[unit.name][str(unit.uid)] = unit
      
    #return a tuple that contains à dict of all village content and the length of it
    def population(self):
        return self.community
    """
        unit: Unity
        cost_dict : dict
    """
    def add_unit(self, unit):    
        if(self.has_enough_resources(unit.get_cost())):
            # if issubclass(unit.__class__, Building):
            #     unit.build()

            self.community[unit.name][str(unit.uid)] = unit
            for ressource, cost in unit.get_cost().items():
                self.ressources[ressource] -= cost

    """
        takes ressources to add, and update the village ressources
    """
    def add_ressources(self, ressource, quantity = 0):
        # self.add_unit(ressource)
        if(issubclass(ressource.__class__, Ressource)):
            self.ressources[ressource.get_name()] += ressource.get_quantity()
        else:
            self.ressources[ressource] += quantity

    def remove_unit(self, unit):
        self.community[unit.name].pop(str(unit.uid))
        if(issubclass(unit.__class__, Ressource)):
            self.ressources[unit.name] -= 1

    def update_unit(self, unit):
        pass

    def has_enough_resources(self, cost_dict):
        """ Verify wether the village has enough ressources for the action """
        for resource, cost in cost_dict.items():
            if not self.ressources.get(resource) or  self.ressources.get(resource) <= cost:
                return False
        return True
    
    def get_community(self):
        return self.community

    def get_ressources(self):
        return self.ressources

    def get_name(self):
        return self.name

    def get_pplCount(self):
        return self.peopleCount



if __name__ == "__main__":
    model = Model("Mine")
    # model.ressources |= dict([("fo",60), ("g",30)])
    model.initialise_villages(0, 0, 0, 3)
    # model.add_unit(Swordsman(team=model))
    # model.add_unit(Villager(team=model))
    # model.add_unit(Swordsman(team=model))
    # # model.add_unit(Food(team=model))
    # model.remove_unit(model.community["v"]["0"])
    # w = Wood(team=model)
    # model.add_ressources(w)
    # w.remove()
    
    # model.remove_unit(model.community["w"]["0"])
    print(model.community)
    print(model.ressources)