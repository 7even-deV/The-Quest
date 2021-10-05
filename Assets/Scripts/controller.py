import pygame

from . import __author__


# Initialize pygame
pygame.init()

# Screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# Background color
BG = (8, 8, 8)


class Controller():

    def __init__(self):
        # Create window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Quest")

    def launch_manager(self):
        # Main loop
        run = True
        while run:

            # Update background
            self.screen.fill(BG)

            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Update display
            pygame.display.update()

        # Quit pygame
        pygame.quit()

    def __del__(self):
        print(__author__)
