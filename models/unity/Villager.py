# This file contains the Villager class which is a subclass of Unity
from unity.Unity import Unity

class Villager(Unity):
    def __init__(self, team):
        community = team.get_community().get('v')
        uid = len(community) if community else 0 # 0 if 
        super().__init__(uid,"v", {"f" : 50}, 25, 40, 2, 0.8, 1, team=team)
        self.carry_max = 20
        # self.buildingSpeed = buildingSpeed,
        self.ressources_dict = {
            "f" : 0,
            "w" : 0,
            "g" : 0,
        }
    
    """
        droping ressources in the village drop point
        To do : a villager Can collect resources at rate of 25/minute
    """
    def collect(self, ressource):
        all_collected = sum(self.ressources_dict.values())
        # quantity_to_collect = ressource.get_quantity()
        rest = self.carry_max - all_collected
        quantity_to_collect = rest if rest < ressource.get_quantity() else ressource.get_quantity()
        
        if all_collected >= self.carry_max:
            self.drop_ressources()
        else:
            ressource.extract(quantity_to_collect)
            self.ressources_dict[ressource.get_name().lower()] += quantity_to_collect
            if all_collected + quantity_to_collect == self.carry_max: # if the villager is full
                self.drop_ressources()
            else:
                #he has to do other things
                pass
        if ressource.get_quantity() == 0:
            ressource.remove()
        else:
            #he has to come back to the ressource to finish collecting
            # self.move(ressource.get_position())
            self.collect(ressource)
    
    def drop_ressources(self):
        for key, quantity in self.ressources_dict.items():
            self.team.add_ressources(key, quantity)
            self.ressources_dict[key] = 0
    """
        droping ressources in the village drop point
    """
    
    def build(self):
        return 0
