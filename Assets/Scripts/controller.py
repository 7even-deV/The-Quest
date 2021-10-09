import pygame

from . import __author__
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION
from .manager import logo_icon, load_music
from .scenes import Menu, Game, Record


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
        self.scene_list = [Menu(self.screen), Game(self.screen), Record(self.screen)]

    def launch_manager(self):
        i = 0
        select = 0
        level = 1
        score = 0
        # Main loop
        while True:
            # Manage each scene
            self.scene_caption(i)
            self.scene_music(i, 0.5)
            select, level, score = self.scene_list[i].main_loop(select, level, score)

            # Cycle through each scene until reset to 0
            i = (i + 1) % len(self.scene_list)

    def scene_caption(self, index):
        pygame.display.set_caption(CAPTION[0] + CAPTION[1][index])

    def scene_music(self, index, volume):
        pygame.mixer.music.load(load_music(index))
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1, 0.0, 1000)

    def __del__(self):
        print(__author__)
