#Créé par Max le 27/09/2024

class Tuile:
    def __init__(self,id):
        self.id=id
        self.ressource="O"
        self.unites={} #les cles seront les ids et les valeurs seront les instances Unite

    def __repr__(self):
        if self.unites!={}:
            return self.unites
        return self.ressource

class Monde:
    def __init__(self, tuple):
        self.x=tuple[0]
        self.y=tuple[1]
        self.dico={} #à chaque clé sera associé une Tuile
        #les clés du dico seront de la forme "0,0"

    def creer_monde(self):
        for x in range(self.x):
            for y in range(self.y):
                cle=(x,y)
                self.dico[cle]=Tuile(cle)

    def afficher_console(self):
        for x in range(self.x):
            for y in range(self.y):
                print(self.dico[(x,y)],end="")
            print("",end="\n")

#monde=Monde((5,20))
#monde.creer_monde()
#monde.afficher_console()