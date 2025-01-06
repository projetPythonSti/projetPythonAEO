from World import World
from model import Model
from save import Save


if __name__ == "__main__":
    world = World(30, 60)
    save = Save()
    
    village1 = Model("fabulous", world)
    village2 = Model("hiraculous", world)
    village1.initialize_villages(1,2,3, gold=200, wood=400, food=300, town_center=1, keeps=2, houses=5, camps=3)
    village2.initialize_villages(4,5,6, 2, 1, gold=2, wood=1, food=3, barracks=1, archery_ranger=3, stables=3, farms=2)
    
    world.fill_world()
    world.show_world()
    
    print("After saving and loading")
    
    backup = save.save(world)
    data = save.load()
    world_prime = data[0]
    world_prime.show_world()
    
    