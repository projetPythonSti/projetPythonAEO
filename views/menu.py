import pygame as pg
import sys

from views.buttons import Button
from views.Gui import FolderSelector
from views.Gui import FileSelector


class PlayPauseMenu:
    def __init__(self, game=None):
        pg.init()
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        pg.display.set_caption("Menu")
        self.clock = pg.time.Clock()
        self.running = True
        self.game = game

        screen_width, screen_height = self.screen.get_size()
        button_width, button_height = 100, 50

        self.play_button = Button((screen_width // 2 - button_width // 2, screen_height // 2 - 150), "Play", button_width, button_height)
        self.save_button = Button((screen_width // 2 - button_width // 2, screen_height // 2 - 50), "Sauvegarder", button_width, button_height)
        self.load_button = Button((screen_width // 2 - button_width // 2, screen_height // 2 + 50), "Charger", button_width, button_height)
        self.quit_button = Button((screen_width // 2 - button_width // 2, screen_height // 2 + 150), "Quitter", button_width, button_height)

    def run(self):
        if not self.running:
            self.running = True 
        while self.running:
            self.check_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.play_button.is_over(pg.mouse.get_pos()):
                    self.play()
                if self.save_button.is_over(pg.mouse.get_pos()):
                    self.save()
                if self.load_button.is_over(pg.mouse.get_pos()):
                    self.load()
                if self.quit_button.is_over(pg.mouse.get_pos()):
                    self.quit_game()

    def update(self):
        pass

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.play_button.draw(self.screen)
        self.save_button.draw(self.screen)
        self.load_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        pg.display.flip()

    def play(self):
        print("Play button pressed")
        self.running = False
        self.game.playing = True
        print("Back to the 2.5D game")

    def save(self):
        # folder_selector = FolderSelector()
        # folder_selector.master.mainloop()
        # path = folder_selector.folder_path
    
        # print("Here is the path: ", path)
        # if self.game:
        #     self.game.game_manager.save_world(path)
        self.game.game_manager.save()
        self.running = False  # Ensure the menu keeps running after saving
        self.game.playing = True

    def load(self):
        print("Im charging...")
        # file_selector = FileSelector()
        # file_selector.master.mainloop()
        # path = file_selector.file_path
        
        # if path:
        #     try:
        #         with open(path, 'rb') as file:
        #             header = file.read(4)
        #             if header.startswith(b'\x89PNG') or header.startswith(b'\xFF\xD8\xFF'):
        #                 print("Selected file is an image.")
        #             elif header.startswith(b'%PDF'):
        #                 print("Selected file is a PDF document.")
        #             elif header.startswith(b'ID3'):
        #                 print("Selected file is an MP3 audio.")
        #             else:
        #                 print("Selected file is a binary file.")
        #                 # print("Before : ", self.game.game_manager.world.villages[0].population(), self.game.game_manager.world.villages[1].population(), sep="\n")
        #                 if self.game:
        #                     self.game.game_manager.load_from_file(path)
        #                     path=""
        #                 # print("After : ", self.game.game_manager.world.villages[0].population(), self.game.game_manager.world.villages[1].population(), sep="\n")
        #                 self.game.world.draw(self.game.screen, self.game.camera)
        #     except Exception as e:
        #         print(f"Error reading file: {e}")
        self.game.game_manager.load()
        self.running = False
        self.game.playing = True
            
    
    def quit_game(self):
        print("Quit button pressed")
        self.running = False
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    game = PlayPauseMenu()
    game.run()
    pg.quit()
    sys.exit()