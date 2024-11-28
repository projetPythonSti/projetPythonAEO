from views.Cli import *
from controllers.Game_controller import *
from models.unity import Villager, Archer, Horseman, Swordsman

class Game_controller:
    def __init__(self):
        self.units = []
        self.view = CLIView()

    def create_units(self, name):
        villager = Villager(name)
        self.units.append(villager)
        self.view.display_unit(villager)

