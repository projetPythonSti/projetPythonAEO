from views.Cli import *
from models.model import Model

# class Game_controller:
#     def __init__(self):
#         self.units = []
#         self.view = CLIView()

#     def create_units(self, name):
#         villager = Villager(name)
#         self.units.append(villager)
#         self.view.display_unit(villager)

class GameController:
    def __init__(self, model:Model, view):
        self.model = model  
        self.view = view    
        # self.units = []

    def start_game(self):
        """ Initialiser le jeu avec des unités et des villages """
        self.model.initialize_villages()
        self.model.initialize_units()
        self.view.display_game_start()

    def create_unit(self, unit_type, team):
        """ Créer une unité et l'ajouter au modèle """
        # Par exemple, créer un archer (peut être étendu pour d'autres unités)
        if unit_type == "Archer":
            new_unit = Archer(id=self.model.generate_id(), name="A",team=team)
        elif unit_type == "Horseman":
            new_unit = Horseman(id=self.model.generate_id(), name="Horseman", team=team)
        # Ajouter l'unité à la liste et au modèle
        self.units.append(new_unit)
        self.model.add_unit(new_unit)
        self.view.display_unit_creation(new_unit)

    def move_unit(self, unit, destination, route):
        """ Déplacer une unité sur une route donnée """
        if unit not in self.units:
            print("Unité inconnue.")
            return

        print(f"Déplacement de l'unité {unit.name} vers {destination}")
        unit.move(destination, route)  # Appeler la méthode de déplacement de l'unité
        self.model.update_unit(unit)  # Mettre à jour la position dans le modèle
        self.view.update_unit_position(unit)  # Afficher la nouvelle position dans la vue

    def attack(self, attacker, defender):
        """ Gérer une attaque entre deux unités """
        if attacker not in self.units or defender not in self.units:
            print("Une des unités n'existe pas.")
            return

        print(f"{attacker.name} attaque {defender.name}")
        # Déterminer si l'attaque est réussie (en fonction des caractéristiques, ici simplifié)
        if attacker.position == defender.position:  # Si elles sont au même endroit
            damage = attacker.damage
            defender.health -= damage  # Appliquer les dégâts
            print(f"{defender.name} a subi {damage} dégâts. Santé restante: {defender.health}")
            if defender.health <= 0:
                print(f"{defender.name} a été éliminé.")
                self.model.remove_unit(defender)  # Retirer l'unité morte du modèle
                self.units.remove(defender)  # Retirer de la liste des unités
                self.view.remove_unit(defender)  # Mettre à jour la vue (enlever l'unité)
        else:
            print(f"{defender.name} est hors de portée pour l'attaque.")

    def collect_resources(self, worker, resource):
        """ Gérer la collecte de ressources """
        if worker not in self.units:
            print("L'unité de travailleur n'existe pas.")
            return
        
        if worker.can_collect(resource):  # Vérifier si l'unité peut collecter la ressource
            worker.collect(resource)  # Collecter la ressource
            self.model.update_worker(worker)  # Mettre à jour l'état du travailleur dans le modèle
            self.view.update_resources_display(resource)  # Afficher les ressources mises à jour

    def build_building(self, village, building_type):
        """ Gérer la construction d'un bâtiment dans un village """
        if village.has_enough_resources(building_type):
            building = village.build(building_type)  # Construire le bâtiment
            self.model.add_building(village, building)  # Ajouter le bâtiment au modèle
            self.view.update_building(village, building)  # Afficher le bâtiment dans la vue
        else:
            print("Pas assez de ressources pour construire ce bâtiment.")

