import pygame

from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SILVER, ARCADE, BLACK
from .tools import Timer
from .players import Player
from .enemies import Enemy


class Scene():

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.timer = Timer() # Create self.timer

    def main_loop(self):
        pass


class Menu(Scene):

    def __init__(self, screen):
        super().__init__(screen)

    def main_loop(self):
        run = True
        while run:
            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    exit()

                # Keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Play game
                        run = False
                    if event.key == pygame.K_RETURN:  # Show record
                        pass
                    if event.key == pygame.K_ESCAPE:  # Quit game
                        exit()

            # Draw background
            self.screen.fill(SILVER)
            # Update screen
            pygame.display.update()


class Game(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        # Create player
        self.player = Player(self.screen, 2, center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//1.1))
        self.enemy = Enemy(self.screen, 2, center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//10.1))

    def main_loop(self):
        run = True
        while run:
            # Clock FPS
            self.clock.tick(FPS)

            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    exit()

                # Keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: # Moving left
                        self.player.moving_left = True
                    if event.key == pygame.K_RIGHT: # Moving right
                        self.player.moving_right = True
                    if event.key == pygame.K_UP: # Moving up
                        pass
                    if event.key == pygame.K_DOWN: # Moving down
                        pass

                    if event.key == pygame.K_SPACE:  # Turbo
                        pass
                    if event.key == pygame.K_RETURN:  # Pause and Settings
                        pass
                    if event.key == pygame.K_ESCAPE:  # Exit game
                        run = False

                # keyboard release
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT: # Moving left
                        self.player.moving_left = False
                    if event.key == pygame.K_RIGHT: # Moving right
                        self.player.moving_right = False
                    if event.key == pygame.K_UP: # Moving up
                        pass
                    if event.key == pygame.K_DOWN: # Moving down
                        pass

            # Background color
            self.screen.fill(ARCADE)

            # Area - update and draw
            self.player.update()
            self.player.draw()

            self.enemy.update()
            self.enemy.draw()

            # Update screen
            pygame.display.update()


class Record(Scene):

    def __init__(self, screen):
        super().__init__(screen)

    def main_loop(self):
        run = True
        while run:
            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    exit()

                # Keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Restart game
                        pass
                    if event.key == pygame.K_RETURN:  # Show menu
                        run = False
                    if event.key == pygame.K_ESCAPE:  # Quit game
                        exit()

            # Draw background
            self.screen.fill(BLACK)
            # Update screen
            pygame.display.update()
