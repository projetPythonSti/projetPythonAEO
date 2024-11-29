import time
from RessourcesManager import RessourcesManager


class Building:
    def __init__(self, name, cost, time_building, health, longueur, spawn='Unity', dropPoint=False, flag):
        self.name = name
        self.cost = cost
        self.time_building = time_building
        self.health = health
        self.longueur = longueur
        self.is_built = False
        self.spawn = spawn
        self.dropPoint = dropPoint
        self.flag = flag

    def can_afford(self, player_resources):
        for resource, amount_needed in self.cost.items():
            if resources_manager.resources.get(resource, 0) < amount_needed:
                return False
        return True

    def deduct_resources(self, player_resources):
        for resource, amount_needed in self.cost.items():
            resources_manager.resources[resource] -= amount_needed
        print(f"Ressources déduites pour {self.name}: {self.cost}")

    def set_time_building(self) :
        n = resources_manager.resources.get("villagers", 0)
        return 3*self.time_builing / (n+2)
    
    def build(self, ressources_manager : RessourcesManager):
        n = resources_manager.resources.get("villagers", 0)
        if not self.can_afford(resources_manager):
            print(f"Pas assez de ressources pour construire {self.name}.")
            return False
        self.deduct_resources(player_resources)
        print(f"Construction de {self.name} commencée...")
        build_time = int(self.set_time_building(resources_manager))
        for second in range(build_time)):
            print(f"Construction en cours : {second + 1}/{self.time_building} secondes")
            time.sleep(1)

        self.is_built = True
        print(f"Construction de {self.name} terminée.")
        return True
