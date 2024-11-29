from Horseman import Horseman
from Archer import Archer
from Villager import Villager
from mmonde import World
from mressources import Food
from Swordsman import Swordsman
from pathfinding import Pathfinding
from randommap import randomise

if __name__ == "__main__":
    horseman = Horseman("h1",1)
    archer = Archer("a1",1);

    monde = World(120,120)
    monde.creer_monde()
    randomise(monde, 5)

    food = Food()

    horseman1 = Horseman("h2",2)
    archer1 = Archer("a2",2)
    villager1 = Villager(id = "v1", team=1)
    print(horseman, archer)
    print(horseman == Archer)
    print("Ressources avant")
    print(villager1.resourcesDict)
    villager1.collect(food, 2)
    print("Ressources Apres")
    print(villager1.resourcesDict)

    pathfinder = Pathfinding(monde.convertMapToGrid(),(0,0), (20,40))
    route = pathfinder.astar()
    if isinstance(route, bool):
        print("Not a bool")
    route = route + [(0,0)]
    route = route[::-1]
    monde.afficher_route_console(route)
    tupleE = (2, 1)
    print(tupleE[1])