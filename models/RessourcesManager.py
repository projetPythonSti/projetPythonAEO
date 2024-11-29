class RessourcesManager:
    def __init__(self, villagers, archers, horsemen, swordsmen, townCenter, stables, keeps, gold, wood, food):
        self.resources = {
            "villagers": villagers.population,
            "archers": archers.population,
            "horsemen": horsemen.population,
            "swordsmen":swordsmen.population,
            "townCenter": townCenter.population,
            "stables": stables.population,
            "keeps": keeps.population,
            "gold": gold.population,
            "wood": wood.population,
            "food": food.population
        }
    
    def setRessources(self, ressources:dict):
        for key, value in ressources.items():
            self.resources[key] += value
    