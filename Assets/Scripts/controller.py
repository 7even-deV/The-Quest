import pygame

from . import __author__
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION, LEVEL
from .manager import logo_icon
from .scenes import Main, Menu, Game, Record


class Controller():
    # Initialize pygame and mixer
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()

    def __init__(self):
        # Create window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_icon(pygame.image.load(logo_icon))

        # List of all scenes
        self.scene_list = [Main(self.screen), Menu(self.screen), Game(self.screen), Record(self.screen)]

    def launch_manager(self):
        i = 0
        username = ''
        select = 0
        model = 0
        level = LEVEL
        score = 0

        # Main loop
        while True:
            # Manage each scene
            self.scene_caption(i)
            self.scene_list[i].scene_music(i, 0.5)
            username, select, model, level, score, turnback = self.scene_list[i].main_loop(username, select, model, level, score)

            # Cycle through each scene until reset to 0
            if turnback:
                i = (i - 1) % len(self.scene_list)
            else:
                i = (i + 1) % len(self.scene_list)

    def scene_caption(self, index):
        pygame.display.set_caption(CAPTION[0] + CAPTION[1][index])

    def __del__(self):
        print(__author__)
