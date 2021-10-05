import pygame

from . import __author__
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION
from .manager import logo_icon
from .scenes import Menu, Game, Record



class Controller():
    # Initialize pygame
    pygame.init()

    def __init__(self):
        # Create window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_icon(pygame.image.load(logo_icon))

        # List of all scenes
        self.scene_list = [Menu(self.screen), Game(self.screen), Record(self.screen)]

    def launch_manager(self):
        i = 1
        # Main loop
        while True:
            # Manage each scene
            self.scene_caption(i)
            self.scene_list[i].main_loop()

            # Cycle through each scene until reset to 0
            i = (i + 1) % len(self.scene_list)

    def scene_caption(self, index):
        pygame.display.set_caption(f"The Quest - {CAPTION[index]}")

    def __del__(self):
        print(__author__)
