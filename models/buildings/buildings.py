import time

class Building:
    def __init__(self, name, cost, time_building, health, length, population=0, spawn='Unity', dropPoint=False):
        self.name = name
        self.cost = cost
        self.time_building = time_building
        self.health = health
        self.length = length
        self.is_built = False
        self.spawn = spawn
        self.dropPoint = dropPoint
        self.population = population
        self.team = None

        #self.position = Position()
        self.grid_x = None  # To be set when placed in the world
        self.grid_y = None
        self.tiles_occupied = []

    def __repr__(self):
        return f"{self.name[0]}" #first letter of the name

    def update_tiles_occupied(self):
        """Update the list of tiles occupied by this building based on grid_x and grid_y."""
        if self.grid_x is not None and self.grid_y is not None:
            self.tiles_occupied = [
                (self.grid_x + dx, self.grid_y + dy)
                for dx in range(self.length)
                for dy in range(self.length)
            ] #very nice comprehension expression btw

    def get_cost(self):
        return self.cost
    
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
