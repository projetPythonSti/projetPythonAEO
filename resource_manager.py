
import pygame as pg



class ResourceManager:


    def __init__(self):

        # resources
        self.resources = {
            "Wood": 50000,
            "Stone": 10000,
            "Gold": 10000
        }

        #costs
        self.costs = {
            "Town Centre": {"Wood": 350},
            "House": {"Wood": 25},
            "Camp": {"Wood": 100},
            "Farm": {"Wood": 60},
            "Barracks": {"Wood": 175},
            "Stable": {"Wood": 175},
            "Archery Range": {"Wood": 175},
            "Keep": {"Wood": 35, "Gold": 125},
        }

    def apply_cost_to_resource(self, building):
        """Deduct the cost of building from available resources."""
        if building in self.costs:
            for resource, cost in self.costs[building].items():
                self.resources[resource] -= cost
        else:
            print(f"Error: Building {building} does not have defined costs.")

    def is_affordable(self, building):
        affordable = True
        for resource, cost in self.costs[building].items():
            if cost > self.resources[resource]:
                affordable = False
        return True

