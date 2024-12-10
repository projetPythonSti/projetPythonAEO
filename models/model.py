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



class Model:
    
    def __init__(self, team):
        # Dictionary of human and materiel ressources of the village
        self.community = {}
        self.resources = {'gold': 0, 'wood': 0, 'food': 0}
        self.team = team
        
    def generate_id(self):
        return self.units

    def initialize_villages(self, archers = 0, horsmen = 0, swordsmen = 0, villages = 0, town_center = 0,
                            stables = 0, keeps = 0, houses = 0, farms = 0, camps = 0, barracks = 0, 
                            archery_ranger = 0, wood = 0, food = 0, gold = 0):
        for i in range(archers):
            self.community.setdefault("a", {})[str(i)] = Archer(i + 1, team=self.team)

        for i in range(horsmen):
            self.community.setdefault("hm", {})[str(i)] = Horseman(i+1, team = self.team)
   
        for i in range(villages):
            self.community.setdefault("v", {})[str(i)] = Villager(i+1, self.team)
        
        for i in range(swordsmen):
            self.community.setdefault("sm", {})[str(i)] = Swordsman(i+1, self.team)
        
        for i in range(town_center):
            self.community.setdefault("t", {})[str(i)] = TownCenter(i+1, self.team)
        
        for i in range(archery_ranger): 
            self.community.setdefault("ar", {})[str(i)] = ArcheryRange(i + 1, self.team)

        for i in range(barracks):
            self.community.setdefault("b", {})[str(i)] = Barracks(i + 1, self.team)

        for i in range(camps):
            self.community.setdefault("c", {})[str(i)] = Camp(i + 1, self.team)

        for i in range(farms):
            self.community.setdefault("f", {})[str(i)] = Farm(i + 1, self.team)

        for i in range(houses):
            self.community.setdefault("h", {})[str(i)] = House(i + 1, self.team)

        for i in range(keeps):
            self.community.setdefault("k", {})[str(i)] = Keep(i + 1, self.team)

        for i in range(stables):
            self.community.setdefault("s", {})[str(i)] = Stable(i + 1, self.team)

        self.resources["wood"] += wood
        self.resources["food"] += food 
        self.resources["gold"] += gold
        
    def add_unit(self, unit, cost_dict):
        if(self.has_enough_resources(cost_dict)):
            self.community[unit.name.lower()][str(unit.id)] = unit
            for ressource, cost in cost_dict.items():
                self.resources[ressource] -= cost
                
    def remove_unit(self, unit):
        self.community[unit.name.lower()].pop(str(unit.id))

    # def update_unit(self, unit):
    #     """ Mettre à jour une unité dans le modèle """

    def has_enough_resources(self, cost_dict):
        """ Verify wether the village has enough ressources for the action """
        for resource, cost in cost_dict.items():
            if self.resources.get(resource) <= cost:
                return False
        return True

    # def get_villages(self):
    #     """ Retourner la liste des villages """
    #     return self.villages

    # def get_units(self):
    #     """ Retourner la liste des unités """
    #     return self.units

if __name__ == "__main__":
    
    model = Model("Mine")
    model.resources["food"] = 5
    model.initialize_villages(1, 2, 0, 3)
    model.add_unit(Villager(4, "Mine"), {"food": 2})
    model.add_unit(Villager(5, "Mine"), {"food": 5})
    model.remove_unit(Villager(4, "Mine"))
    print(model.community)
    print(model.resources)
    
    