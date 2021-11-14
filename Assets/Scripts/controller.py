import pygame

from .         import __author__
from .settings import CAPTION, SCENE
from .manager  import logo_icon
from .scenes   import Main, Menu, Load, Game, Record


class Controller():
    # Initialize pygame and mixer
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()

    def __init__(self):
        # Load logo icon
        pygame.display.set_icon(pygame.image.load(logo_icon))

        # Tuple of all scenes
        self.scene_tuple = (Main(), Menu(), Load(), Game(), Record())

    def launch_manager(self):
        i = SCENE
        play = False

        # Main loop
        while True:
            # Manage each scene
            self.scene_caption(i)
            self.scene_tuple[i].music(i)
            browser, play = self.scene_tuple[i].main_loop(play)

            # Cycle through each scene until reset to 0
            i = (i + browser) % len(self.scene_tuple)

    def scene_caption(self, index):
        pygame.display.set_caption(CAPTION[0] + CAPTION[1][index])

    def __del__(self):
        print(__author__)
