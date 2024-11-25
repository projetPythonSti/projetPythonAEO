import time

class Building:
    def __init__(self, name, cost, time_building, health, longueur, assigned_villagers, spawn='Unity', dropPoint=False, flag):
        self.name = name
        self.cost = cost
        self.time_building = time_building
        self.health = health
        self.longueur = longueur
        self.assigned_villagers = []
        self.is_built = False
        self.spawn = spawn
        self.dropPoint = dropPoint
        self.population = population
        self.flag = flag

    def can_afford(self, player_resources):
        for resource, amount_needed in self.cost.items():
            if player_resources.get(resource, 0) < amount_needed:
                return False
        return True

    def deduct_resources(self, player_resources):
        for resource, amount_needed in self.cost.items():
            player_resources[resource] -= amount_needed
        print(f"Ressources déduites pour {self.name}: {self.cost}")

    def set_time_building(self.time_building, villagers_list) :
        n = len(villagers_list)
        return 3*time_builing / (n+2)
    
    def build(self, player_resources, assigned_villagers):
        n = len(assigned_vilagers)
        if not self.can_afford(player_resources):
            print(f"Pas assez de ressources pour construire {self.name}.")
            return False

        self.deduct_resources(player_resources)
        print(f"Construction de {self.name} commencée...")
        for second in range(set_time_building(self.time_building)):
            print(f"Construction en cours : {second + 1}/{self.time_building} secondes")
            time.sleep(1)

        self.is_built = True
        print(f"Construction de {self.name} terminée.")
        return True
    
