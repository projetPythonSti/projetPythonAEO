import pygame as pg

class Button:
    def __init__(self, color, position, text, width=None, height=None):
        self.can_press = True #can be deleted maybe
        self.is_pressed = False
        self.color_base = color #can be deleted maybe
        self.color = color
        self.x = position[0]
        self.y = position[1]
        self.text = text
        # self.image_origine = pg.image.load("assets/images/hud/" + text + ".png").convert_alpha() #can be deleted maybe
        # self.image = pg.image.load("assets/images/hud/" + text + ".png").convert_alpha()
        self.width = width #if width else self.image.get_width()
        self.height = height #if height else self.image.get_height()
        print("Button :", position[0], " ", position[1])

    def draw(self, screen, outline=None):
        if outline:
            pg.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        if self.color:
            pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        screen.blit(self.image, (self.x, self.y))

    def is_over(self, position):
        return self.x < position[0] < self.x + self.width and self.y < position[1] < self.y + self.height


# class ButtonPetit(Button):
#     def __init__(self, color, position, text):
#         super().__init__(color, position, text)
#         self.can_press = True
#         self.width = 125
#         self.height = 30


# class ButtonGrand(Button):
#     def __init__(self, color, x, y, text):
#         super().__init__(color, x, y, text)
#         self.can_press = True
#         self.width = 240
#         self.height = 40


# class ButtonVide(Button):
#     def __init__(self, color, x, y, text, width, height):
#         super().__init__(color, x, y, text)
#         self.can_press = True
#         self.width = width
#         self.height = height
