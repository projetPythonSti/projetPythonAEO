import pygame as pg

class Button:
    def __init__(self, position, text, width=None, height=None, color = (255, 255, 255)):
        self.color = color
        self.position = position
        self.text = text
        self.width = width
        self.height = height
        self.rect = pg.Rect(position[0], position[1], width, height)
        self.font = pg.font.Font(None, 30)

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.position[0] + 10, self.position[1] + 10))

    def is_over(self, pos):
        return self.rect.collidepoint(pos)