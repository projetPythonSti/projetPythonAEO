from views.buttons import Button
from views.Gui import FolderSelector
import pygame as pg
from utils import *
import sys

class Menu_manager:
    def __init__(self, window, game):
        self.running, self.playing = True, False
        self.DISPLAY_W, self.DISPLAY_H = window.get_size()
        self.CLICK, self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, \
                                                                                                 False, False, False
        self.key = 0
        self.game = game
        self.display = pg.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = window
        # self.font_name = 'assets/Polices&Wallpaper/Trajan_Pro_.ttf'
        # self.font_name2 = 'assets/Polices&Wallpaper/Trajan_Pro_Bold.ttf'
        self.BLACK, self.WHITE, self.RED = (0, 0, 0), (255, 255, 255), (255,  70,  70)
        # self.main_menu = Menu(self)
        self.play_pause_menu = PlayPauseMenu(menu_manager=self, game=game)
        # self.options = OptionsMenu(self)
        # self.new_game = NewGame(self, game)
        # self.credits = CreditsMenu(self)
        # self.Volume = VolumeMenu(self)
        # self.Controls = CommandsMenu(self)
        self.current_menu = self.play_pause_menu

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running, self.playing = False, False
                self.current_menu.run_display = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.START_KEY = True
                elif event.key == pg.K_BACKSPACE:
                    self.BACK_KEY = True
                elif event.key == pg.K_ESCAPE:
                    # self.game.game_manager.pause() #a voir après
                    self.ESCAPE_KEY = True
                    pg.quit()
                    sys.exit()
                elif event.key == pg.K_DOWN:
                    self.DOWN_KEY = True
                elif event.key == pg.K_UP:
                    self.UP_KEY = True
                else:
                    self.key = event.key
            if event.type == pg.MOUSEBUTTONDOWN:
                self.CLICK = True
            if event.type == pg.MOUSEBUTTONUP:
                self.CLICK = False

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, False, False

    def draw_text(self, text, size, position, color=None):
        color = color if color else self.game.WHITE
        self.game.draw_text(self.display, text, size, color, position)
    

    # def draw_text2(self, text, size, x, y):
    #     font = pg.font.Font(None, size)
    #     text_surface = font.render(text, True, self.WHITE)
    #     text_rect = text_surface.get_rect()
    #     text_rect.center = (x, y)
    #     self.display.blit(text_surface, text_rect)

    # def draw_text_from_var(self, var, size, x, y):
    #     font = pg.font.Font(self.font_name2, size)
    #     text_surface = font.render(str(var), True, self.RED)
    #     text_rect = text_surface.get_rect()
    #     text_rect.center = (x, y)
    #     self.display.blit(text_surface, text_rect)

class Menu:
    def __init__(self, menu_manager):
        self.menu_manager = menu_manager
        self.mid_width, self.mid_height = self.menu_manager.DISPLAY_W / 2, self.menu_manager.DISPLAY_H / 2
        self.run_display = True
        self.offset = - 100
        # self.save = Save()
        # self.PartieChargee = 0

    def blit_screen(self):
        self.menu_manager.window.blit(self.menu_manager.display, (0, 0))
        pg.display.update()
        self.menu_manager.reset_keys()

class PlayPauseMenu(Menu):
        def __init__(self, menu_manager, game):
            super().__init__(menu_manager)
            self.game = game
            self.screen = self.menu_manager.window
            # self.clock = pg.time.Clock()
            self.clock = self.game.clock
            self.screen_size = self.screen.get_size()
            self.playing = True
            
            self.play_x, self.play_y = self.mid_width, self.mid_height
            self.backup_x, self.backup_y = self.mid_width, self.mid_height + 20
            self.exit_x, self.exit_y = self.mid_width, self.mid_height + 40
            
            self.play_button = Button((0, 255, 0), (self.play_x - 110, self.play_y), "Play", 30, 10)
            self.backup_button = Button((0, 255, 0), (self.backup_x - 110, self.backup_y), "Backup",30, 10)
            self.exit_button = Button((0, 255, 0), (self.exit_x - 110, self.exit_y), "Quitter", 30,10)
        
        def display_menu(self):
            pg.display.init()
            image = pg.image.load("assets/images/sparta.jpeg").convert_alpha()
            while self.run_display:
                self.menu_manager.check_events()
                self.check_input()
                self.menu_manager.display.fill((0, 0, 0))
                self.menu_manager.display.blit(image, (0, 0))
                
                self.menu_manager.draw_text("Play", 40, (self.play_x, self.play_y))
                self.menu_manager.draw_text("Sauvegarder", 40, (self.backup_x, self.backup_y + 15))
                self.menu_manager.draw_text("Quitter", 40, (self.exit_x, self.exit_y + 30))
                # if self.etat == "Pas de Partie":
                #     self.menu_manager.draw_text2("Pas de Sauvegarde! Veuillez créer une partie avant.", 15, self.selectx,
                #                             self.selecty)
                self.blit_screen()
        
        def check_input(self):
            mouse_position = pg.mouse.get_pos()
            if self.menu_manager.BACK_KEY or (self.menu_manager.CLICK and self.play_button.is_over(mouse_position)):
                self.game.game_manager.play()
            elif self.menu_manager.CLICK:
                print("mouse "+mouse_position)
                # print("button " + self.exit_button.x + " " +self.exit_button.y)
                if self.backup_button.is_over(mouse_position):
                    folder_selector = FolderSelector()
                    folder_selector.master.mainloop()
                    path = folder_selector.folder_path
                    folder_selector.master.destroy()
                    self.game.game_manager.save_world(path)
                    self.menu_manager.playing = True
                    self.menu_manager.running = False
                    self.menu_manager.CLICK = False
                if self.exit_button.is_over(mouse_position):
                    self.running, self.playing = False, False
                    self.current_menu.run_display = False
                    pg.quit()
                    sys.exit()
                    #detruire les fenetre tkinter et pygame
                    
            self.run_display = False
            
        # def draw(self):
        #     self.screen.fill((0, 0, 0))
        #     self.menu_manager.draw_text('PLAY', 100, self.game.WHITE, self.screen_size[0] // 2, self.screen_size[1] * 0.3)
        #     self.menu_manager.draw_text('Sauvegarder', 100, self.game.WHITE, self.screen_size[0] // 2, self.screen_size[1] * 0.3)
        #     self.menu_manager.draw_text('Quitter', 100, self.game.WHITE, self.screen_size[0] // 2, self.screen_size[1] * 0.3)
        #     pg.display.flip()

