from Horseman import Horseman
from Archer import Archer
from Villager import Villager
from mressources import Food
from Swordsman import Swordsman

if __name__ == "__main__":
    horseman = Horseman("h1",1);
    archer = Archer("a1",1);

    food = Food()

    horseman1 = Horseman("h2",2)
    archer1 = Archer("a2",2)
    villager1 = Villager(id = "v1", buildingSpeed=20, carry=0, team=1)
    print(horseman, archer)
    print(horseman == Archer)
    print("Ressources avant")
    print(villager1.resourcesDict)
    villager1.collect(food, 2)
    print("Ressources Apres")
    print(villager1.resourcesDict)

    tupleE = (2, 1)
    print(tupleE[1])