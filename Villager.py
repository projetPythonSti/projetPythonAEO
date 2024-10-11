import Unity


class Villager():
    carryMax = 25
    def __init__(self, carry, buildingSpeed, resourcesList):
        self.carry = carry
        self.buildingSpeed = buildingSpeed,
        self.resourceList = resourcesList,
        super().__init__(id, "Villager", { "food" : 50}, 25, 40, 4, 0.8, 1)

    def __repr__(self):
        return "villager"
    # Cette méthode considère qu'il existe une liste contenant les ressources portées par le self
    # Sinon, comment est-il possible de savoir les ressources qu'il faut déposer dans le TC, et si le villageois à plusieurs ressources
    def collect(self , resource):
        if (len(self.resourceList) > self.carryMax):
            print("Trop de ressources")
        else:
            self.resourceList.__add__(resource)
            # Cette ligne à été ajoutée dans le cas où on implémente une boucle qui ajoute à une liste externe la ressource collecté
            return resource
    def build(self):
        return 0