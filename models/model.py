from unity.Archer import Archer
from unity.Horseman import Horseman
from unity.Swordsman import Swordsman
from unity.Villager import Villager
from buildings.town_center import TownCenter
from buildings.archery_range import ArcheryRange
from buildings.barracks import Barracks
from buildings.camp import Camp
from buildings.farm import Farm
from buildings.house import House
from buildings.keep import Keep
from buildings.stable import Stable
# from ressources.mressources import *

#faut-il l'importer et le faire hériter pour pouvoir utiliser fire_change ?
# from controllers import Game_controller
# from unity import Unity
from collections import defaultdict



class Model():
    
    def __init__(self, name):
        # Dictionary of human and materiel ressources of the village
        self.community = defaultdict(dict)
        self.resources = defaultdict(int)
        self.name = name
        
    def initialize_villages(self, archers = 0, horsmen = 0, swordsmen = 0, villages = 0, town_center = 0,
                            stables = 0, keeps = 0, houses = 0, farms = 0, camps = 0, barracks = 0, 
                            archery_ranger = 0, wood = 0, food = 0, gold = 0):
        for i in range(archers):
            self.community["a"][str(i)] = Archer(team=self)

        for i in range(horsmen):
            self.community["hm"][str(i)] = Horseman(team = self)
   
        for i in range(villages):
            self.community["v"][str(i)] = Villager(team=self)
        
        for i in range(swordsmen):
            self.community["sm"][str(i)] = Swordsman(team=self)
        
        for i in range(town_center):
            self.community["t"][str(i)] = TownCenter(team=self)
        
        for i in range(archery_ranger): 
            self.community["ar"][str(i)] = ArcheryRange(team=self)

        for i in range(barracks):
            self.community["b"][str(i)] = Barracks(team=self)

        for i in range(camps):
            self.community["c"][str(i)] = Camp(team=self)

        for i in range(farms):
            self.community["f"][str(i)] = Farm(team=self)

        for i in range(houses):
            self.community["h"][str(i)] = House(team=self)

        for i in range(keeps):
            self.community["k"][str(i)] = Keep(team=self)

        for i in range(stables):
            self.community["s"][str(i)] = Stable(team=self)

        self.resources["wood"] += wood
        self.resources["food"] += food 
        self.resources["gold"] += gold
        
        
        
    """
        unit: Unity
        cost_dict : dict
    """
    def add_unit(self, unit):
        if(self.has_enough_resources(unit.get_cost())):
            self.community[unit.name.lower()][str(unit.id)] = unit
            for ressource, cost in unit.get_cost().items():
                self.resources[ressource] -= cost
                
    """
        takes ressources to add, and update the village ressources
    """
    def add_ressources(self, ressources:dict):
        for key, value in ressources.items():
            self.resources[key] += value
        
    def remove_unit(self, unit):
        self.community[unit.name.lower()].pop(str(unit.id))


    def has_enough_resources(self, cost_dict):
        """ Verify wether the village has enough ressources for the action """
        for resource, cost in cost_dict.items():
            if self.resources.get(resource) <= cost:
                return False
        return True
    
    def get_community(self):
        return self.community


if __name__ == "__main__":
    model = Model("Mine")
    model.resources |= dict([("food",60), ("gold",30)])
    model.initialize_villages(0, 0, 0, 3)
    model.add_unit(Swordsman(team=model))
    model.add_unit(Villager(team=model))
    model.add_unit(Swordsman(team=model))
    model.add_ressources({"food":50, "wood":300, "gold": 150})
    print(model.community)
    print(model.resources)