import pygame

from . import __author__
from .scenes import Menu, Game, Record


# Screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# Background color
BG = (8, 8, 8)


class Controller():
    # Initialize pygame
    pygame.init()

    def __init__(self):
        # Create window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Quest")

        # List of all scenes
        self.scene_list = [Menu(self.screen), Game(self.screen), Record(self.screen)]

    def launch_manager(self):
        i = 0
        # Main loop
        while True:
            # Manage each scene
            self.scene_list[i].main_loop()

            # Cycle through each scene until reset to 0
            i = (i + 1) % len(self.scene_list)

    def __del__(self):
        print(__author__)
