import time

class Building:
    def __init__(self, name, cost, time_building, health, surface, population=0, spawn=None, dropPoint=False):
        self.name = name
        self.cost = cost
        self.time_building = time_building
        self.health = health
        self.surface = surface
        self.is_built = False
        self.spawn = spawn
        self.dropPoint = dropPoint
        self.population = population

    def can_afford(self, player_resources):
        for resource, amount_needed in self.cost.items():
            if player_resources.get(resource, 0) < amount_needed:
                return False
        return True

    def deduct_resources(self, player_resources):
        for resource, amount_needed in self.cost.items():
            player_resources[resource] -= amount_needed
        print(f"Ressources déduites pour {self.name}: {self.cost}")    

    def build(self, player_resources):
        if not self.can_afford(player_resources):
            print(f"Pas assez de ressources pour construire {self.name}.")
            return False

        self.deduct_resources(player_resources)
        print(f"Construction de {self.name} commencée...")
        for second in range(self.time_building):
            print(f"Construction en cours : {second + 1}/{self.time_building} secondes")
            time.sleep(1)

        self.is_built = True
        print(f"Construction de {self.name} terminée.")
        return True


# Bâtiments spécifiques avec leurs caractéristiques
def create_town_centre():
    return Building(
        name="Town Centre",
        cost={"wood": 350},
        time_building=150,
        health=1000,
        surface=16,  # 4x4
        population=5,
        dropPoint=True,
        spawn="Villager"
    )

def create_house():
    return Building(
        name="House",
        cost={"wood": 25},
        time_building=25,
        health=200,
        surface=4,  # 2x2
        population=5
    )

def create_camp():
    return Building(
        name="Camp",
        cost={"wood": 100},
        time_building=25,
        health=200,
        surface=4,  # 2x2
        dropPoint=True
    )

def create_farm():
    return Building(
        name="Farm",
        cost={"wood": 60},
        time_building=10,
        health=100,
        surface=4,  # 2x2
        spawn="Food"
    )

def create_barracks():
    return Building(
        name="Barracks",
        cost={"wood": 175},
        time_building=50,
        health=500,
        surface=9,  # 3x3
        spawn="Swordsman"
    )

def create_stable():
    return Building(
        name="Stable",
        cost={"wood": 175},
        time_building=50,
        health=500,
        surface=9,  # 3x3
        spawn="Horseman"
    )

def create_archery_range():
    return Building(
        name="Archery Range",
        cost={"wood": 175},
        time_building=50,
        health=500,
        surface=9,  # 3x3
        spawn="Archer"
    )

def create_keep():
    return Building(
        name="Keep",
        cost={"wood": 35, "gold": 125},
        time_building=80,
        health=800,
        surface=1,  # 1x1
    )
