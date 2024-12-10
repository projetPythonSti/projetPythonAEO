import pygame as pg
from game import Game
from menu import StartMenu, GameMenu


def main():

    running = True

    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((720, 720))
    clock = pg.time.Clock()

    # implement menus
    start_menu = StartMenu(screen, clock)
    game_menu = GameMenu(screen, clock)

    # implement game
    game = Game(screen, clock)

    while running:
        # start menu
        playing = start_menu.run()

        while playing:
            # game loop
            game.run()
            # pause loop
            playing = game_menu.run()

if __name__ == "__main__":
    main()

