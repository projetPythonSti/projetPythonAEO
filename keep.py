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
        self.attack_damage = 5
        self.attack_range = 8

   def calculate_distance(self, target):
        dx = self.position.getX() - target.position.getX()
        dy = self.position.getY() - target.position.getY()
        return math.sqrt(dx**2 + dy**2)

    def attack(self, target):
        if self.health != self.max_health:
            print(f"{self.name} ne peut pas attaquer car il n'est pas en pleine santé.")
            return False

        distance = self.calculate_distance(target)
        if distance <= self.attack_range:
            print(f"{self.name} attaque la cible {target.name} et inflige {self.attack_damage} points de dégâts.")
            target.take_damage(self.attack_damage)
            return True
        else:
            print(f"{self.name} ne peut pas attaquer {target.name} car hors attaque_range")
            return False
