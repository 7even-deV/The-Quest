import pygame

from .         import __author__
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION, SCENE, LEVEL
from .manager  import logo_icon
from .scenes   import Main, Menu, Game, Record


class Controller():
    # Initialize pygame and mixer
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()

    def __init__(self):
        # Create window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_icon(pygame.image.load(logo_icon))

        # Tuple of all scenes
        self.scene_tuple = (Main(self.screen), Menu(self.screen), Game(self.screen), Record(self.screen))

    def launch_manager(self):
        i = SCENE
        level = LEVEL
        username = ''

        # Main loop
        while True:
            # Manage each scene
            self.scene_caption(i)
            self.scene_tuple[i].music(i)
            username, scene_browser = self.scene_tuple[i].main_loop(username)

            # Cycle through each scene until reset to 0
            i = (i + scene_browser) % len(self.scene_tuple)

    def scene_caption(self, index):
        pygame.display.set_caption(CAPTION[0] + CAPTION[1][index])

    def __del__(self):
        print(__author__)
