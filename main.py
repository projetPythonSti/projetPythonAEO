from Horseman import Horseman
from Archer import Archer


if __name__ == "__main__":
    horseman = Horseman("h1");
    archer = Archer("a1");
    
    horseman1 = Horseman("h2");
    archer1 = Archer("a2");
    
    print(horseman, archer)
    print(horseman == Archer)
    