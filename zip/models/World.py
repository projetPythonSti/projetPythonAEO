import numpy as np
import math

from models.Position import Position
from models.buildings.buildings import Building
from models.buildings.town_center import TownCenter
from models.maps.Tile import  Tile
from models.model import Model  # delete it after finish testing the class World
from models.unity.Villager import Villager  # delete it after finish testing the class World
from models.ressources.ressources import Gold, Wood, Food, Ressource
from collections import defaultdict
import random as rd
from models.unity.Unity import Unity


import logging
logging.basicConfig(level=logging.DEBUG)  # Changed from INFO to DEBUG
logger = logging.getLogger(__name__)

class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # Boundary is a rectangle
        self.capacity = capacity  # Maximum entities per QuadTree node
        self.entities = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary
        self.northeast = QuadTree((x + w / 2, y, w / 2, h / 2), self.capacity)
        self.northwest = QuadTree((x, y, w / 2, h / 2), self.capacity)
        self.southeast = QuadTree((x + w / 2, y + h / 2, w / 2, h / 2), self.capacity)
        self.southwest = QuadTree((x, y + h / 2, w / 2, h / 2), self.capacity)
        self.divided = True

    def insert(self, entity):
        ex, ey = entity.position.getX(), entity.position.getY()
        x, y, w, h = self.boundary
        if not (x <= ex < x + w and y <= ey < y + h):
            return False

        if len(self.entities) < self.capacity:
            self.entities.append(entity)
            return True
        else:
            if not self.divided:
                self.subdivide()
            if self.northeast.insert(entity):
                return True
            elif self.northwest.insert(entity):
                return True
            elif self.southeast.insert(entity):
                return True
            elif self.southwest.insert(entity):
                return True
        return False

    def remove_entity(self, entity):
        try:
            self.entities.remove(entity)  # Remove entity from the list
            logger.debug(f"Entity {entity} removed from QuadTree.")
        except ValueError:
            logger.warning(f"Attempted to remove entity {entity} which does not exist in QuadTree.")

    def query_range(self, range_boundary, found):
        x, y, w, h = self.boundary
        rx, ry, rw, rh = range_boundary
        # Check if boundaries overlap
        if not (x < rx + rw and x + w > rx and y < ry + rh):
            return
        for entity in self.entities:
            ex, ey = entity.position.getX(), entity.position.getY()
            if rx <= ex < rx + rw and ry <= ey < ry + rh:
                found.append(entity)
        if self.divided:
            self.northwest.query_range(range_boundary, found)
            self.northeast.query_range(range_boundary, found)
            self.southwest.query_range(range_boundary, found)
            self.southeast.query_range(range_boundary, found)

    def nearest_neighbor(self, target_position: tuple[int, int], team: str, best=None, best_dist=float('inf')):
        # Find the closest entity not on the same team
        
        #entities = {kv for kv in v.values() for k,v in self.all.items() if  kv.team != team}
         
        for entity in self.entities:
            if entity.position and entity.team != team:
                    dist = math.hypot(entity.position.getX() - target_position[0], entity.position.getY() - target_position[1])
                    #logger.debug(f"Checking entity {entity}: distance={dist}")
                    if dist < best_dist:
                        best_dist = dist
                        best = entity
                        logger.debug(f"New best entity: {best} with distance {best_dist}")
        if self.divided:
            # Determine the order to search quadrants based on the position
            quadrants = [self.northwest, self.northeast, self.southwest, self.southeast]
            quadrants.sort(key=lambda qt: math.hypot(qt.boundary[0] - target_position[0], qt.boundary[1] - target_position[1]))
            for quadrant in quadrants:
                if quadrant:
                    if quadrant._contains_circle(target_position, best_dist):
                        #logger.debug(f"Searching quadrant {quadrant} for closer entities.")
                        best_candidate, candidate_dist = quadrant.nearest_neighbor(target_position, team, best, best_dist)
                        if candidate_dist < best_dist:
                            best, best_dist = best_candidate, candidate_dist
                            #logger.debug(f"Updated best after searching quadrant: best={best}, best_dist={best_dist}")
        logger.debug(f"Final nearest neighbor: {best} with distance {best_dist}")
        return best, best_dist  # Ensure callers handle the tuple appropriately

    def _contains_circle(self, position, radius):
        x, y, w, h = self.boundary
        closest_x = max(x, min(position[0], x + w))
        closest_y = max(y, min(position[1], y + h))
        distance = math.hypot(position[0] - closest_x, position[1] - closest_y)
        return distance <= radius

class World:


    """
        22/12/2024 : J'ai apporté des modifications à ce fichier @tahakhetib sur ce que @amadou_yaya_diallo a écrit
            - Réglé les erreurs d'exécution lors de l'appel à la fonction remove_element, passage de monde à self
            - changé la manière dont on traite les tiles remplies
            - Décommenté la fonction convertMapToGrid afin de la réutiliser avec GameManager
        26/12/2024@tahakhetib : J'ai apporté des modifs sur ce que @amadou_yaya_diallo
            - Changé le type de l'attribut filled_tiles vers un dictionnaire
            - Modifié les fonctions place_element() et remove_element() pour qu'elle s'adapte au changement de filled_tiles
        02/12/2024@tahakhetib : J'ai apporté des modifications sur ce que @amadou_yaya_diallo a écrit
            - Passé le type des éléments du dictionnaire de tiles_dico à Tiles
    """
    def __init__(self, width, height):  # dict of villages in the world
        self.width = width
        self.height = height
        self.villages = list()
        self.ressources = defaultdict(dict)
        self.tiles_dico = defaultdict(Tile)  # à chaque clé sera associé une Tuile
        self.filled_tiles = defaultdict(tuple)
        self.unitTiles = defaultdict(dict)
        self.initialise_world()
        self.entities = []  # Centralized list of entities
        self.quad_tree = QuadTree((0, 0, width, height), capacity=4)
        self.populate_quad_tree()
        self.all = None
        self.keeps= None
        # les clés du dico seront de la forme (x,y)
        # self.units  #every unit on the map, a list seems better to me

    
    def init_self_all(self):
        self.all={**self.villages[0].population(), **self.villages[1].population()}

    def init_self_keeps(self):
        self.keeps=[kv for k,v in self.all.items() for kv in v.values() if isinstance(kv, Building) and kv.name == "K"]

    def initialise_world(self): #emplit de Tuile le dico du monde
        for x in range(self.width):
            for y in range(self.height):
                self.tiles_dico[(x,y)] = Tile()

    def add_village(self, village):
        self.villages.append(village)

    def fill_ressources(self, max_ressource):
        for i in range(rd.randint(0, max_ressource)):
           self.ressources["w"][str(i)] = Wood(world=self)

        for i in range(rd.randint(0, max_ressource//2)):
           self.ressources["g"][str(i)] = Gold(world=self)

        # for i in range(rd.randint(0, max_ressource)):
        #    self.ressources["f"][str(i)] = Food(world=self)

        self.place_ressources()

    def get_ressources(self):
        return self.ressources

    def place_ressources(self):
        for w, g in zip(self.ressources["w"].values(), self.ressources["g"].values()):
            self.place_element(w)
            self.place_element(g)
            # self.place_element(fo)


    def fill_world(self):
        village1, village2 = self.villages
        # iterating on 2 dict at the same time
        for pop1, pop2 in zip(village1.population().values(), village2.population().values()):
            for v1, v2 in zip(pop1.values(), pop2.values()):
                self.place_element(v1)
                self.place_element(v2)
                self.add_entity(v1)
                self.add_entity(v2)

    def fill_world2(self):
        for village in self.villages:
            for pop in village.population().values():
                for v in pop.values():

                    self.place_element(v)




    def updateUnitPos(self,oldPos ,position, unit):
        self.unitTiles[oldPos]["elements"].remove(unit)
        try:
            self.unitTiles[oldPos]["elements"][0]
        except:
            self.unitTiles.pop(oldPos)
        if position not in self.unitTiles:
            self.unitTiles[position] = {
                "filled": True,
                "elements": [unit]
            }
        else:
            self.unitTiles[position]["filled"] = True
            self.unitTiles[position]["elements"] += [unit]
    def removeUnitPos(self, pos,unit):
        self.unitTiles[pos]["elements"].remove(unit)
        try:
            self.unitTiles[pos]["elements"][0]
        except:
            self.unitTiles.pop(pos)
    def show_world(self): #
        for y in range(self.height):
            for x in range(self.width):
                print(self.tiles_dico[(x, y)], end="")
            print("", end="\n")

    # shows a part of the world, works with two position found in the game's loop
    def show_precise_world(self,upleft:Position,downright:Position):
        print()
        if upleft.getY()>0:
            print(' '+(downright.getX()-upleft.getX())*'ʌ')
        for y in range(upleft.getY(),downright.getY(),1):
            if upleft.getX()>0:
                print('<', end='')
            for x in range(upleft.getX(),downright.getX(),1):
                print(self.tiles_dico[(x, y)], end="")
            if downright.getX()<self.width:
                print('>', end='')
            print("", end="\n")
        if downright.getY()<self.height:
            print(' '+(downright.getX()-upleft.getX())*'v')
        print("upleft.getX = ", upleft.getX(), " upleft.getY = ", upleft.getY())

    def return_world(self):
        world_representation = []
        for x in range(self.width):
            row = []
            for y in range(self.height):
                row.append(str(self.tiles_dico[(x, y)]))  # Conversion explicite en chaîne
            world_representation.append("".join(row))  # Joindre chaque ligne en une chaîne
        return "\n".join(world_representation)

    def return_precise_world(self,upleft:Position,downright:Position,term):
        world_chunk="\n\n\n"
        if upleft.getY() > 0:
            world_chunk+=(' ' + (downright.getX() - upleft.getX()) * 'ʌ' + '\n')
        for y in range(upleft.getY(), downright.getY(), 1):
            if upleft.getX() > 0:
                world_chunk+='<'
            for x in range(upleft.getX(), downright.getX(), 1):
                if (x,y) in self.unitTiles and self.unitTiles[(x,y)]["elements"] is not []:
                    world_chunk += self.unitTiles[(x, y)]["elements"][0].personalizedStr(term)
                elif(self.tiles_dico[(x, y)].contains!=None):
                        world_chunk+=self.tiles_dico[(x, y)].contains.personalizedStr(term)
                else:
                    world_chunk+=' '
            if downright.getX() < self.width:
                world_chunk+='>'
            world_chunk+='\n'
        if downright.getY() < self.height:
            world_chunk+=(' ' + (downright.getX() - upleft.getX()) * 'v')
        #print("upleft.getX = ", upleft.getX(), " upleft.getY = ", upleft.getY())
        return world_chunk


    def place_element(self, element):
        # ...existing code...
        place = (element.position.getX(), element.position.getY())
        if place not in self.filled_tiles and place[0] <= self.width and place[1] <= self.height:
            print("World : place_element ------- Element n'étant pas dans une tuile déjà prise")
            if issubclass(element.__class__, Building) and all(tile not in set(self.filled_tiles) for tile in element.get_occupied_tiles()):
                print("World : place_element ------- Elt est un batiment, voici le batiment -> " ,element.name)
                # Check if the building can be placed
                if element.surface[0] + place[0] <= self.width and element.surface[1] + place[1] <= self.height:
                    for x in range(element.surface[0]):
                        for y in range(element.surface[1]):
                            try:
                                self.tiles_dico[(place[0] + x, place[1] + y)].set_contains(element)
                            except KeyError:
                                # ...existing code...
                                pass
                            self.filled_tiles[(place[0] + x, place[1] + y)] = (place[0] +x, place[1]+y)
            elif not issubclass(element.__class__, Building):
                if issubclass(element.__class__, Unity):
                    if place not in self.unitTiles:
                        self.unitTiles[place] = {
                            "filled" : True,
                            "elements" : []
                        }
                        self.unitTiles[place]["elements"] += [element]
                    else:
                        self.unitTiles[place]["filled"] = True
                        self.unitTiles[place]["elements"] += [element]
                else:
                    self.tiles_dico[place].set_contains(element)
                    self.filled_tiles[place] = place
        if hasattr(element, 'health') and element.health > 0:
            self.add_entity(element)  # Ensure 'element' is passed here as well
           # logger.debug(f"Element {element} added to world entities.")
            # ...existing code...

    def remove_element(self, element):
        if element.position is None:
            logger.warning(f"Attempted to remove element {element} with no position.")
            return
        place = (element.position.getX(), element.position.getY())
        if issubclass(element.__class__, Building) and all(tile in set(self.filled_tiles) for tile in element.get_occupied_tiles()):
            for x in range(element.surface[0]):
                for y in range(element.surface[1]):
                    self.tiles_dico[(place[0] + x, place[1] + y)].set_contains(None)
                    self.filled_tiles.pop((place[0] + x, place[1] + y))  # Corrected pop usage
        elif not issubclass(element.__class__, Building):
            if issubclass(element.__class__, Unity):
                    self.unitTiles[place]["elements"].remove(element)
                    if not self.unitTiles[place]["elements"]:
                        self.unitTiles.pop(place)
            else:
                self.tiles_dico[place].set_contains(None)
                self.filled_tiles.pop(place, None)
        
        if hasattr(element, 'health'):
            self.quad_tree.remove_entity(element)
            # Remove from self.all handled in remove_entity
            #self.ressources[element.name].pop(str(element.uid))

        # Removing element from its team also
        element.team.remove_unit(element)
        # Update the view of the element
        logger.debug(f"Element {element} removed from world.")

    # def afficher_console(self):
    #     # self.update_unit_presence() #updates this everytime we print the map
    #     for x in range(self.x):
    #         for y in range(self.y):
    #             print(self.dico[(x, y)].affiche(),end="") #This one works
    #         print("",end="\n")

    # def afficher_route_console(self,route):
    #     self.update_unit_presence() #updates this everytime we print the map
    #     for x in range(self.x):
    #         for y in range(self.y):
    #             if (x,y) in route:
    #                 print("-", end="")
    #             else:
    #                 print(self.dico[(x, y)].affiche(),end="") #This one works

    #         print("",end="\n")

    # def update_unit_presence(self):
    #     for x in range(self.x): #resets every tile's unit list
    #         for y in range(self.y):
    #             self.dico[(x,y)].unites=[]
    #     for u in self.units: #puts every unit in their tile's unit list
    #         key= self.intkey(u.position)
    #         self.dico[key].unites.append(u)

    def convertMapToGrid(self):
        array_shape = (self.width+1, self.height+1)
        binary_array = np.zeros(array_shape, dtype=int)
        for i, (key, value) in enumerate(self.tiles_dico.items()):
            binary_array[key[0], key[1]] = 0 if value.contains == None else 1
        return binary_array

    # def intkey(key): #turns a float key into an int key for dict indexation
    #     return (int(key[0]),int(key[1]))


    def populate_quad_tree(self):
        for entity in self.get_all_entities_with_health():
            self.quad_tree.insert(entity)
            self.entities.append(entity)  # Add to centralized entities list

    def get_all_entities_with_health(self):
        entities = []
        for village in self.villages:
            for group in village.population().values():
                for entity in group.values():
                    if hasattr(entity, 'health') and entity.health > 0:
                        entities.append(entity)
        for res in self.ressources.values():
            for entity in res.values():
                if hasattr(entity, 'health') and entity.health > 0:
                    entities.append(entity)
        return entities

    def add_entity(self, entity):
        # ...existing code...
        if hasattr(entity, 'health'):
            self.quad_tree.insert(entity)
            self.entities.append(entity)  # Maintain centralized entities list

    def remove_entity(self, entity):
        # ...existing code...
        if hasattr(entity, 'health'):
            self.quad_tree.remove_entity(entity)
            if entity in self.entities:
                self.entities.remove(entity)  # Remove from centralized entities list

    def update(self, dt):
        """Update the world and its entities."""
        # self.draw(screen, camera)
        #self.update_projectiles(dt=dt)
        self.get_all_entities_with_health()
        self.update_projectiles(dt=dt)


    def update_projectiles(self,world_gui, dt: float):
        """Update all active projectiles and activate new ones towards closest targets."""
        self.init_self_all()
        keeps=[kv for k,v in self.all.items() for kv in v.values() if isinstance(kv, Building) and kv.name == "K"]

        for building in self.keeps:
            target = self.find_closest_target(building.position.toTuple(), building.team)
            if target:
                projectile = building.projectile_pool.get_projectile()
                if projectile and not projectile.active:
                    projectile.activate(
                        start_pos=building.position,
                        target_entity=target,
                        damage=building.damage,
                        speed=building.projectile_speed,
                        team=building.team,
                        image=world_gui.tile_images["projectile"]
                    )
            building.projectile_pool.update(dt)  # Update cooldown timer and projectiles
    
    def find_closest_target(self, position: tuple[int, int], team: str):
        """
        Find the closest enemy entity with health to the given position using QuadTree.

        Parameters:
            position (tuple[int, int]): The (x, y) position of the searching entity.
            team (str): The team of the searching entity.

        Returns:
            Entity or None: The closest enemy entity or None if no enemy is found.
        """
        closest_entity, closest_dist = self.world_model.quad_tree.nearest_neighbor(position, team)
        logger.debug(f"Closest entity: {closest_entity}, distance: {closest_dist}")
        return closest_entity if closest_entity and hasattr(closest_entity, 'health') else None
    
        

if __name__ == "__main__":
    monde = World(100, 100)
    village1 = Model("fabulous", monde)
    village2 = Model("hiraculous", monde)
    village1.initialize_villages(1,2,3, gold=200, wood=400, food=300, town_center=1, keeps=2, houses=5, camps=3)
    village2.initialize_villages(4,5,6, gold=2, wood=1, food=3, barracks=1, archery_ranger=3, stables=3, farms=2)
    v = Villager(village1)
    village1.add_unit(v)
    v.ressources_dict["w"] = 3
    v.ressources_dict["g"] = 2
    town_center = TownCenter(village1)
    village1.add_unit(town_center)
    monde.fill_world()
    monde.fill_ressources(10)
    print(village1.population())
    print(monde.get_ressources())
    print("Before : ", village1.get_ressources())
    #fo = monde.get_ressources()["fo"]["0"]
    #v.drop_ressources()
    #v.collect(fo)
    #print("After : ", village1.get_ressources())
    #print(v.ressources_dict)
    # print(village2.population())
    # print(monde.get_ressources())
    # print(sorted(monde.filled_tiles, key=lambda x: x[0]), len(monde.filled_tiles))
    monde.show_world()
    # village1.remove_unit(town_center)
    # print(town_center.get_occupied_tiles())
    # print(sorted(set(monde.filled_tiles) & set(town_center.get_occupied_tiles()), key=lambda x: (x[0], x[1])))
    monde.remove_element(town_center)
    print("After removing town center")
    monde.show_world()
    monde.show_world()


    # print(monde.get_ressources())
    # print(sorted(monde.filled_tiles, key=lambda x: x[0]), len(monde.filled_tiles))
    monde.show_world()
    # village1.remove_unit(town_center)
    # print(town_center.get_occupied_tiles())
    # print(sorted(set(monde.filled_tiles) & set(town_center.get_occupied_tiles()), key=lambda x: (x[0], x[1])))
    monde.remove_element(town_center)
    print("After removing town center")
    monde.show_world()


    monde.show_world()



