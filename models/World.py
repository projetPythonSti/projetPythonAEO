from maps.Tile import Tile
from model import Model #delete it after finish testing the class World

class World:
    def __init__(self, dimension:tuple, villages:tuple): #dict of villages in the world
        self.dimension = dimension
        self.villages = villages
        self.tiles_dico = dict() #à chaque clé sera associé une Tuile
        #les clés du dico seront de la forme (x,y)
        # self.units  #every unit on the map, a list seems better to me

    def initialise_world(self): #emplit de Tuile le dico du monde
        for x in range(self.dimension[0]):
            for y in range(self.dimension[1]):
                self.tiles_dico[(x,y)] = Tile()
                
    def fill_world(self):
        village1, village2 = self.villages
        #iterating on 2 dict at the same time
        print("vil1 : ",village1.population()[0].values())
        print("vil2 : ",village2.population()[0].values())
        # for pop1, pop2 in zip(village1.population()[0].values(), village2.population()[0].values()):
        #     print("pop1 : ",pop1)
        #     print("pop2 : ",pop2)
        #     for v1, v2 in zip(pop1.values(), pop2.values()):
        #         self.place_element(v1)
        #         self.place_element(v2)     
    
    # def update_world(self, element):
    
    
    def show_world(self):
         for element in self.tiles_dico.values():
            print(element)
    
    def place_element(self, element):
        place = (element.position.getX(), element.position.getY())
        self.tiles_dico[place].set_contains(element)
            
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

    # def convertMapToGrid(self):
    #     array_shape = (self.x, self.y)
    #     binary_array = np.zeros(array_shape, dtype=int)
    #     for i, (key, value) in enumerate(self.dico.items()):
    #         binary_array[key[0], key[1]] = 0 if value.contains == " " else 1
    #     return binary_array
    
    # def intkey(key): #turns a float key into an int key for dict indexation
    #     return (int(key[0]),int(key[1]))
    
if __name__ == "__main__":
    village1 = Model("fabulous")
    village2 = Model("hiraculous")
    village1.initialize_villages(1,2,3, gold=2, wood=1, food=3)
    village2.initialize_villages(4,5,6, gold=2, wood=1, food=3)
    
    monde = World((100,100), (village1, village2))
    monde.initialise_world()
    monde.fill_world()
    # monde.show_world()
    """
        je dois mettre les unités sur les tiles dans mes fonctions fill_world() et show_world()
        j'ai modifiée la manière dont je crée une ressource
    """
    