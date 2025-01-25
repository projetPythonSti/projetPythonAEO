from views.Cli import *
from models.model import Model
from models.buildings.projectile import Projectile
import pygame as pg  # Ensure Pygame is imported
import logging
import numpy as np
from models.buildings.buildings import Building
from models.buildings.Keep import Keep
logger = logging.getLogger(__name__)

"""
le controleur doit gerer l'interaction des utilisateur du jeu avec le jeu
"""

class Game_controller:
    def __init__(self, model:Model, view):
        self.model = model  
        self.view = view    
        # self.units = []
        self.projectiles = pg.sprite.Group()
        logger.debug("Game_controller initialized with model and view.")

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
        """ Managing attack between two units or buildings """
        if attacker not in self.units and not isinstance(attacker, Building):
            logger.warning("Attempted attack with non-existent attacker.")
            print("Attacker does not exist.")
            return
        if defender not in self.units:
            logger.warning("Attempted attack on non-existent defender.")
            print("Defender does not exist.")
            return

        logger.info(f"{attacker.name} is attacking {defender.name}")
        print(f"{attacker.name} attaque {defender.name}")
        if isinstance(attacker, Building) and isinstance(attacker, Keep):
            # Keep-specific projectile attack
            if self.is_within_range(attacker, defender):
                projectile = Projectile(
                    start_pos=attacker.position.toTuple(),
                    target_entity=defender,
                    damage=attacker.damage,
                    speed=attacker.projectile_speed,
                    team=attacker.team
                )
                projectile.activate(
                    start_pos=attacker.position.toTuple(),
                    target_entity=defender,
                    damage=attacker.damage,
                    speed=attacker.projectile_speed,
                    team=attacker.team
                )
                self.projectiles.add(projectile)
                self.view.add_projectile(projectile)
                logger.info(f"{attacker.name} launched a projectile towards {defender.name}")
                print(f"{attacker.name} has launched a projectile towards {defender.name}")
            else:
                logger.debug(f"{defender.name} is out of range for projectile attack.")
                print(f"{defender.name} est hors de portée pour l'attaque.")
        else:
            # Existing melee attack logic
            if attacker.position == defender.position:
                damage = attacker.damage
                defender.health -= damage
                logger.info(f"Melee attack: {defender.name} took {damage} damage, remaining health {defender.health}")
                print(f"{defender.name} a subi {damage} dégâts. Santé restante: {defender.health}")
                if defender.health <= 0:
                    logger.warning(f"{defender.name} has been eliminated.")
                    print(f"{defender.name} a été éliminé.")
                    self.model.remove_unit(defender)  # Retirer l'unité morte du modèle
                    self.units.remove(defender)  # Retirer de la liste des unités
                    self.view.remove_unit(defender)  # Mettre à jour la vue (enlever l'unité)
            else:
                logger.debug(f"Melee attack out of range: {defender.name} is out of melee range.")
                print(f"{defender.name} est hors de portée pour l'attaque.")

    def is_within_range(self, attacker, defender):
        distance = np.sqrt((attacker.position.x - defender.position.x) ** 2 + 
                           (attacker.position.y - defender.position.y) ** 2)
        within = distance <= attacker.attack_range
        logger.debug(f"Checking if {defender.name} is within range of {attacker.name}: {within}")
        return within

    def update_projectiles(self):
        """ Update all active projectiles """
        logger.debug("Updating all active projectiles.")
        self.projectiles.update()
        for projectile in self.projectiles:
            if not projectile.active:
                logger.info(f"Removing inactive projectile targeting {projectile.target_entity.name}")
                self.projectiles.remove(projectile)
                self.view.remove_projectile(projectile)

    def game_tick(self):
        # ...existing game tick logic...
        logger.debug("Game tick started.")
        self.update_projectiles()
        # ...other updates...
        logger.debug("Game tick ended.")

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

