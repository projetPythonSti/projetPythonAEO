wood = Wood()
gold = Gold()
food = Food()
resources1 = [wood, gold, food]
ressources2 = [wood, gold, food]

class Population :
    def __init__(self, population) :
        self.population = population

villagers1 = Population(23)
villagers2 = Population(15)

# Création de la keep
keep = Keep()

keep.build(resources, population.population)

# Afficher les ressources restantes
print("\nRessources restantes :")
for res in resources1:
    print(f"{res.name}: {res.getQuantity()}")

# Simuler des dégâts
keep.health -= 100  # Le bâtiment perd 100 points de santé à cause d'une attaque si vous voulez :)
print(f"Santé actuelle de la keep : {keep.health}/{keep.max_health}")

# Réparer la maison
keep.repair(resources, population.population)


# Vérifier la santé du bâtiment
print(f"Santé actuelle de la keep : {keep.health}/{keep.max_health}")

#test de attack et take_damage

house = House()

house.build(resources, villagers.population)

print("\nRessources restantes :")
for res in resources1:
    print(f"{res.name}: {res.getQuantity()}")

while house.health != 0 :
    keep.attack(house)
