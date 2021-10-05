import pygame


# Set framerate
FPS = 60

# Define colours (R, G, B)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)


class Scene():

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

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
            self.screen.fill(WHITE)
            # Update screen
            pygame.display.update()


class Game(Scene):

    def __init__(self, screen):
        super().__init__(screen)

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
                    if event.key == pygame.K_SPACE:  # Turbo
                        pass
                    if event.key == pygame.K_RETURN:  # Pause and Settings
                        pass
                    if event.key == pygame.K_ESCAPE:  # Exit game
                        run = False

            # Draw background
            self.screen.fill(GRAY)
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
