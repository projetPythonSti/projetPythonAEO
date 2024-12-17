import time
from Position import Position
from Ressource import Ressource

class Building:
    def __init__(self, name, cost, time_building, health, longueur, spawn, dropPoint, flag, position):
        self.name = name
        self.cost = cost
        self.time_building = time_building
        self.health = health
        self.longueur = longueur
        self.is_built = False
        self.spawn = spawn
        self.dropPoint = False
        self.dropPoint = dropPoint
        self.flag = flag
        self.position = position

    def can_afford(self, resources: list):
        for res_name, amount_needed in self.cost.items():
            found = False
            for res in resources:
                if res.name == res_name and res.getQuantity() >= amount_needed:
                    found = True
                    break
            if not found:
                return False
        return True

    def deduct_resources(self, resources: list):
        for res_name, amount_needed in self.cost.items():
            for res in resources:
                if res.name == res_name:
                    res.setQuantity(res.getQuantity() - amount_needed)
        print(f"Ressources déduites pour {self.name}: {self.cost}")

    def set_time_building(self, villagers: int):
        return max(1, int(3 * self.time_building / (villagers + 2)))
    
    def build(self, resources: list, villagers: int):
        if not self.can_afford(resources):
            print(f"Pas assez de ressources pour construire {self.name}.")
            return False
        self.deduct_resources(resources)
        print(f"Construction de {self.name} commencée...")
        build_time = int(self.set_time_building(villagers))
        for second in range(build_time):
            print(f"Construction en cours : {second + 1}/{build_time} secondes")
            time.sleep(1)

        self.is_built = True
        print(f"Construction de {self.name} terminée.")
        return True

    def set_position(self, x, y):
        self.position.setX(x)
        self.position.setY(y)
        print(f"Position de {self.name} définie à ({x}, {y}).")


class Population:
    def __init__(self, population):
        self.population = population
