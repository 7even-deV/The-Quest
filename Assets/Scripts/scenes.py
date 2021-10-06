import pygame

from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SILVER, ARCADE, BLACK
from .manager import statue_img, bg_img
from .tools import Timer, Icon
from .environment import Foreground, Background, Farground
from .obstacles import Meteor
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
        self.symbol = Icon(self.screen, 'symbol', center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//1.47))
        self.spaceship = Icon(self.screen, 'spaceship', center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2.5))
        self.statue = pygame.image.load(statue_img).convert_alpha()


    def main_loop(self, select):
        run = True
        while run:
            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    exit()

                # Keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: # Back select
                        if select > 0:
                            select -= 1
                        else: select = 2
                    if event.key == pygame.K_RIGHT: # Next select
                        if select < 2:
                            select += 1
                        else: select = 0

                    if event.key == pygame.K_SPACE:  # Play game
                        run = False
                    if event.key == pygame.K_RETURN:  # Show record
                        pass
                    if event.key == pygame.K_ESCAPE:  # Quit game
                        exit()

            # Background color
            self.screen.fill(ARCADE)

            self.screen.blit(self.statue, (0, SCREEN_HEIGHT//4))

            # Area - update and draw
            self.symbol.update(select)
            self.spaceship.update(select)

            self.symbol.draw()
            self.spaceship.draw()

            # Update screen
            pygame.display.update()

        return select


class Game(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        # Create player
        self.enemy = Enemy(self.screen, 2, center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//10.1))
        self.bg = Background(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, bg_img)
        self.fg = Farground(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, 50)

    def meteor_surge(self, level, surge_num):
        self.meteor_list = []
        for number in range(surge_num):
            temp_list = []
            # Increase the number of meteors per surge
            for _ in range((number + level) * 100 // 4):
                temp_list.append(Meteor(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT))

            self.meteor_list.append(temp_list)

    def process_data(self, select):
        # Create player
        self.player = Player(self.screen, select, 2, center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//1.1))
        self.meteor_surge(1, 3)

    def main_loop(self, select):
        self.process_data(select)
        surge_start = False
        surge_index = 0

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

            # Update the time of the next surge of meteors
            if not surge_start and self.timer.time(10, True):
                surge_start = True

            elif surge_start:
                # Add the next surge when the previous surge ends
                if surge_index < len(self.meteor_list) - 1:
                    surge_index += 1
                    surge_start = False

            # Background color
            self.screen.fill(ARCADE)

            # Area - update and draw
            self.bg.update(self.player.delta_x, self.player.delta_y)
            self.fg.update(self.player.delta_x, self.player.delta_y)
            self.bg.draw()
            self.fg.draw()

            self.player.update()
            self.player.draw()

            for meteor in self.meteor_list[surge_index]:
                meteor.update(self.player.delta_y)
                meteor.draw()

            self.enemy.update()
            self.enemy.draw()

            # Update screen
            pygame.display.update()

        return select


class Record(Scene):

    def __init__(self, screen):
        super().__init__(screen)

    def main_loop(self, select):
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

        return select
