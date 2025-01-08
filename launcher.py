from models.World import World
from models.model import Model
from models.Position import Position
from controllers.gameManager import GameManager
from views.world import World_GUI
from views.Cli import CLIView
from models.save import Save

import curses

def main(stdscr):
    world = World(50, 50)
    save = Save()
    
    village1 = Model("fabulous", world)
    village2 = Model("hiraculous", world)
    village1.initialize_villages(1,2,3, 1, gold=200, wood=400, food=300, town_center=1, keeps=2, houses=5, camps=3)
    village2.initialize_villages(4,5,6, 2, 1, gold=2, wood=1, food=3, barracks=1, archery_ranger=3, stables=3, farms=2)
    
    world.fill_world()
    # world.show_world()
    
    print("After saving and loading")
    
    backup = save.save(world)
    data = save.load()
    world_prime = data[0]
    # world_prime.show_world()
    
    #testing the html file
    game_manager = GameManager(1, world)
    # game_manager.html_generator()
    
    game_manager.addUnitToMoveDict(village1.community["v"]["0"], Position(5,5))
    # print(game_manager.unitToMove)
    # return
    #testing the terminal game
    terminal = CLIView(world, stdscr, game_manager)
    terminal.main_loop() 


if __name__ == "__main__":
    # curses.wrapper(main)
    world = World(30, 60)
    game_manager = GameManager(1, world)
    village1 = Model("fabulous", world)
    village2 = Model("hiraculous", world)
    village1.initialize_villages(1,2,3, gold=200, wood=400, food=300, town_center=1, keeps=2, houses=5, camps=3)
    village2.initialize_villages(4,5,6, 2, 1, gold=2, wood=1, food=3, barracks=1, archery_ranger=3, stables=3, farms=2)
    
    
    # print(world_gui.tiles)
    
    
    # print(world.villages[0].population())
    