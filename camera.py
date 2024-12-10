import pygame as py
py.init()

class Camera:
    def __init__(self,largeur_fenetre,hauteur_fenetre):
        self.largeur  =  largeur_fenetre
        self.hauteur = hauteur_fenetre
        self.dx = 0
        self.dy = 0
        self.vitesse = 15
        self.deplacement = py.Vector2(0,0) #vecteur de position (x,y) qui pourra être incrementer ou decre..//c'est une classe dans pygame
        self.zoom = 1.0
        self.zoom_speed=0.1


    @property
    def scroll(self):
        """Returns the camera displacement for compatibility"""
        return self.deplacement

    def update(self):
        self.zoom_me()
    #recuperons la position de la souris
        position_souris = py.mouse.get_pos() #liste [x,y]
        #occupons nous du deplacement horizontal
        if position_souris[0] > self.largeur * 0.97: #extremité droit
            self.dx = -self.vitesse  #deplacer vers la gauche
        elif position_souris[0] < self.largeur * 0.03: #extremité gauche
            self.dx = self.vitesse #deplacer vers la droite
        else:
            self.dx = 0 #on ne change rien

        #maitenant le deplacement vertical
        if position_souris[1] > self.hauteur * 0.97: #extremité haut
            self.dy = -self.vitesse  #deplacer vers le bas
        elif position_souris[1] < self.hauteur * 0.03: #extremité bas
            self.dy = self.vitesse #deplacer vers le haut
        else:
            self.dy = 0 #on ne change rien

        
        self.deplacement.x +=self.dx #champ x
        self.deplacement.y +=self.dy #champ y
    
    
    def zoom_me(self):

        touch = py.key.get_pressed()
        if touch[py.K_UP]:
            self.zoom *= (1.0 + self.zoom_speed)
        if touch [py.K_DOWN]:
            self.zoom/= (1 + self.zoom_speed)
   
        self.zoom= max(0.1,min(3.0,self.zoom))

    def get_zoom(self):
        return self.zoom


