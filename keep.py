from buildings import Building

class Keep(Building) :
    def __init__(self) :
        super().__init__(
            name="K",
            cost={"w": 35, "g": 125},
            time_building=80,
            health=800,
            max_health=800,
            longueur=1,
          )
        #self.attack_damage = 50

    def attack(self, target):
        if self.health != self.max_health :
            print(f"{self.name} ne peut pas attaquer.")
            return False

        print(f"{self.name} attaque la cible {target.name} et inflige {self.attack_damage} points de dégâts.")
        target.take_damage(self.attack_damage)
        return True
