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
from ressources.ressources import Ressource, Gold, Wood, Food
# from ressources.mressources import *

#faut-il l'importer et le faire hériter pour pouvoir utiliser fire_change ?
# from controllers import Game_controller
# from unity import Unity
from collections import defaultdict



class Model:
    
    def __init__(self, name, world = None):
        # Dictionary of human, materiel and ressources of the village
        self.community = defaultdict(dict)
        self.ressources = defaultdict(int)
        self.name = name
        self.world = world
        self.world.add_village(self)
        
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

        # for i in range(wood):
        #     self.community["w"][str(i)] = Wood(team=self)
        
        # for i in range(food):
        #     self.community["fo"][str(i)] = Food(team=self)
        
        # for i in range(gold):
        #     self.community["g"][str(i)] = Gold(team=self)
            
        
        self.ressources["w"] += wood
        self.ressources["g"] += gold
        self.ressources["fo"] += food
        
    def initialise_villages(self, archers = 0, horsmen = 0, swordsmen = 0, villages = 0, town_center = 0,
                            stables = 0, keeps = 0, houses = 0, farms = 0, camps = 0, barracks = 0, 
                            archery_ranger = 0, wood = 0, food = 0, gold = 0):
        for _ in range(archers):
            Archer(team=self)
        for _ in range(horsmen):
            Horseman(team = self)
        for _ in range(villages):
            Villager(team=self)
        for _ in range(swordsmen):
            Swordsman(team=self)
        for _ in range(town_center):
            TownCenter(team=self)
        for _ in range(archery_ranger): 
            ArcheryRange(team=self)
        for _ in range(barracks):
            Barracks(team=self)
        for _ in range(camps):
            Camp(team=self)
        for _ in range(farms):
            Farm(team=self)
        for _ in range(houses):
            House(team=self)
        for _ in range(keeps):
            Keep(team=self)
        for _ in range(stables):
            Stable(team=self)
        self.ressources["w"] += wood
        self.ressources["g"] += gold
        self.ressources["fo"] += food
      
    #return a tuple that contains à dict of all village content and the length of it
    def population(self):
        return self.community
    """
        unit: Unity
        cost_dict : dict
    """
    def add_unit(self, unit):    
        if(self.has_enough_resources(unit.get_cost())):
            self.community[unit.name.lower()][str(unit.uid)] = unit
            for ressource, cost in unit.get_cost().items():
                self.ressources[ressource] -= cost
                
    """
        takes ressources to add, and update the village ressources
    """
    def add_ressources(self, ressource, quantity = 0):
        # self.add_unit(ressource)
        if(issubclass(ressource.__class__, Ressource)):
            self.ressources[ressource.get_name().lower()] += ressource.get_quantity()
        else:
            self.ressources[ressource] += quantity
        
    def remove_unit(self, unit):
        self.community[unit.name.lower()].pop(str(unit.uid))
        if(issubclass(unit.__class__, Ressource)):
            self.ressources[unit.name.lower()] -= 1

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