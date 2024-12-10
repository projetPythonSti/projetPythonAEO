from views.Cli import *
from models.model import Model

class Game_controller:
    def __init__(self, model:Model, view):
        self.model = model  
        self.view = view    
        # self.units = []

    def fire_changes(self, unit):
        self.view.update(unit)
    
    def start_game(self):
        """ Initialiser le jeu avec des unités et des villages """
        self.model.initialize_villages()
        self.view.display_game_start()

    def create_unit(self, unit):
        self.model.add_unit(unit)
        self.fire_changes() #à revoir si je vais laisser le fire_change


    def attack(self, attacker, defender):
        """ Managing attack between two units """
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

