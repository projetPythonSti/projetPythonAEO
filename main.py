from Horseman import Horseman
from Archer import Archer
from Villager import Villager
from Swordsman import Swordsman

if __name__ == "__main__":
    horseman = Horseman("h1");
    archer = Archer("a1");
    
    horseman1 = Horseman("h2")
    archer1 = Archer("a2")
    villager1 = Villager(id = "v1", buildingSpeed=20, resourcesList=[], carry=0)
    print(horseman, archer)
    print(horseman == Archer)
    