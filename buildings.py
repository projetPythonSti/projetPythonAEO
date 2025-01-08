import time
from Position import Position



class Building:
    def __init__(self, name, cost, time_building, health, max_health, longueur, spawn=False, dropPoint=False, flag=False, position=None, population=0):
        self.name = name
        self.cost = cost
        self.time_building = time_building
        self.health = health
        self.max_health = max_health
        self.longueur = longueur
        self.is_built = False
        self.spawn = spawn
        self.dropPoint = dropPoint
        self.flag = flag
        self.position = position if position else Position(0, 0)
        self.population = population

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
    
    def take_damage(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print(f"{self.name} a été détruit !")
        else:
            print(f"{self.name} a subi {damage} points de dégâts. Santé restante : {self.health}/{self.max_health}.")
    
    def repair(self, resources: list, villagers: int):
        if self.health == self.max_health:
            print(f"{self.name} est déjà en pleine santé.")
            return False
        missing_health = self.max_health - self.health
        repair_cost = {}
        for res_name, res_value in self.cost.items():
            repair_cost[res_name] = int((missing_health * res_value) / self.max_health)

        
        for res_name, amount_needed in repair_cost.items():
            found = False
            for res in resources:
                if res.name == res_name and res.getQuantity() >= amount_needed:
                    found = True
                    break
            if not found:
                print(f"Pas assez de ressources pour réparer {self.name}.")
                return False

        
        for res_name, amount_needed in repair_cost.items():
            for res in resources:
                if res.name == res_name:
                    res.setQuantity(res.getQuantity() - amount_needed)

        
        repair_time = max(1, int(3 * missing_health * self.time_building / (self.max_health * (villagers + 2))))
        print(f"Réparation de {self.name} commencée... Cela prendra {repair_time} secondes.")
        for second in range(repair_time):
            print(f"Réparation en cours : {second + 1}/{repair_time} secondes")
            time.sleep(1)

        
        self.health = self.max_health
        print(f"{self.name} a été réparé avec succès et est maintenant à pleine santé.")
        return True

    def set_position(self, x, y):
        self.position.setX(x)
        self.position.setY(y)
        print(f"Position de {self.name} définie à ({x}, {y}).")
