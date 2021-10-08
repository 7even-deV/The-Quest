import pygame

from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, FONTS, FPS, LOGO, COLOURS
from .manager import statue_img, bg_img, game_over_img, load_sound
from .tools import Timer, Canvas, Icon
from .environment import Foreground, Background, Farground
from .obstacles import Meteor
from .players import Player
from .enemies import Enemy


class Scene():

    def __init__(self, screen):
        self.screen = screen
        self.clock  = pygame.time.Clock()

        self.timer = Timer() # Create self.timer

    def sound(self, sfx, volume=0.5):
        fx = pygame.mixer.Sound(load_sound(sfx))
        fx.set_volume(volume)
        return fx

    def volume(self, vol=0):
        return round(pygame.mixer.music.get_volume() + vol, 1)

    def color(self, color_key):
        return COLOURS(color_key.upper())


class Menu(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.symbol    = Icon(self.screen, 'symbol', center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//1.47))
        self.spaceship = Icon(self.screen, 'spaceship', center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2.5))
        self.statue = pygame.image.load(statue_img).convert_alpha()

        # Sounds fx
        self.portal_loop_fx = self.sound('portal_loop')
        self.select_loop_fx = self.sound('select_loop')
        self.select_fx      = self.sound('select')
        self.confirm_fx     = self.sound('confirm')
        self.start_fx       = self.sound('start')

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
                        self.portal_loop_fx.play()

                        # self.select_fx.play()
                    if event.key == pygame.K_RIGHT: # Next select

                        self.portal_loop_fx.play()
                        # self.select_fx.play()

                    if event.key == pygame.K_SPACE: # Play game
                        run = False
                        self.start_fx.play()
                    if event.key == pygame.K_RETURN: # Show record
                        pass
                    if event.key == pygame.K_ESCAPE: # Quit game
                        exit()

                # keyboard release
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT: # Back select
                        if select > 0:
                            select -= 1
                        else: select = 2
                        self.select_fx.play()

                    if event.key == pygame.K_RIGHT: # Next select
                        if select < 2:
                            select += 1
                        else: select = 0
                        self.select_fx.play()

                    if event.key == pygame.K_UP: # Moving up
                        self.player.moving_up = False
                    if event.key == pygame.K_DOWN: # Moving down
                        self.player.moving_down = False

            # Background color
            self.screen.fill(self.color('ARCADE'))

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
        self.paused     = Canvas(size=80, center=True, y=SCREEN_HEIGHT//3, color=self.color('RED'))
        self.vol_browse = Canvas(center=True, y=SCREEN_HEIGHT//2, color=self.color('YELLOW'))

        self.enemy   = Enemy(self.screen, 2, center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//10.1))
        self.bg = Background(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, bg_img)
        self.fg  = Farground(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, 50)

        self.meteor_group = pygame.sprite.Group()
        self.enemy_group  = pygame.sprite.Group()
        self.settings     = pygame.sprite.Group()
        self.settings.add(self.paused, self.vol_browse)


        # Sounds fx
        self.move_fx      = self.sound('move')
        self.backmove_fx  = self.sound('backmove')
        self.turbo_fx     = self.sound('turbo')
        self.explosion_fx = self.sound('explosion')

        self.pause_fx     = self.sound('pause')
        self.select_fx    = self.sound('select')
        self.game_over_fx = self.sound('game_over')

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
        self.player = Player(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, select, 2, midtop=(SCREEN_WIDTH//2, SCREEN_HEIGHT))
        self.meteor_surge(1, 1)
        self.enemy_group.add(self.enemy)

    def main_loop(self, select):
        self.process_data(select)
        surge_start = False
        surge_index = 0

        vol = self.volume()
        pause = False

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
                    if event.key == pygame.K_LEFT:
                            self.player.moving_left = True # Moving left
                            self.move_fx.play()

                    if event.key == pygame.K_RIGHT:
                            self.player.moving_right = True # Moving right
                            self.move_fx.play()

                    if event.key == pygame.K_UP:
                        if pause and self.volume() < 1.0: # Turn up the volume
                            vol = self.volume(+ 0.1)
                            pygame.mixer.music.set_volume(vol)
                            self.select_fx.play()
                        else:
                            self.player.moving_up = True # Moving up
                            self.move_fx.play()

                    if event.key == pygame.K_DOWN:
                        if pause and self.volume() > 0.0: # Turn down the volume
                            vol = self.volume(- 0.1)
                            pygame.mixer.music.set_volume(vol)
                            self.select_fx.play()
                        else:
                            self.player.moving_down = True # Moving down
                            self.move_fx.play()

                    if event.key == pygame.K_SPACE: # Turbo
                        self.player.turbo = True
                        self.turbo_fx.play()
                    if event.key == pygame.K_RETURN: # Pause and Settings
                        if pause:
                            pause = False
                        else: pause = True
                        self.pause_fx.play()
                    if event.key == pygame.K_ESCAPE: # Exit game
                        run = False
                        self.game_over_fx.play()

                # keyboard release
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT: # Moving left
                        self.player.moving_left = False
                    if event.key == pygame.K_RIGHT: # Moving right
                        self.player.moving_right = False
                    if event.key == pygame.K_UP: # Moving up
                        self.player.moving_up = False
                    if event.key == pygame.K_DOWN: # Moving down
                        self.player.moving_down = False

                    if event.key == pygame.K_SPACE: # Turbo
                        self.player.turbo = False
                        self.backmove_fx.play()

            # Pause and volume control
            self.paused.text = "P A U S E"

            if vol == 0.0 or vol == 1.0:
                self.vol_browse.color = self.color('ORANGE')
            else: self.vol_browse.color = self.color('YELLOW')
            self.vol_browse.text = f"Press <UP or DOWN> to vol:  {vol}"

            # Update the time of the next surge of meteors
            if not surge_start and self.timer.time(8, True):
                surge_start = True

            elif surge_start:
                # Add the next surge when the previous surge ends
                if surge_index < len(self.meteor_list):
                    if len(self.meteor_group) == 0:
                        self.meteor_group.add(self.meteor_list[surge_index])
                        surge_index += 1
                        surge_start = False

            # Background color
            self.screen.fill(self.color('ARCADE'))

            # Area - update and draw
            if self.player.spawn and self.timer.time(1, True):
                self.player.spawn = False

            if self.player.alive:
                if self.player.collide and self.timer.time(0.1, True):
                    self.player.collide = False

            if pause:
                self.settings.update()
                self.settings.draw(self.screen)
            else:
                self.bg.update(self.player.delta_x, self.player.turbo)
                self.fg.update(self.player.delta_x, self.player.turbo)
                self.bg.draw()
                self.fg.draw()

                self.player.check_collision()
                self.player.update()
                self.player.draw()

                for meteor in self.meteor_group:
                    meteor.check_collision(self.player, self.explosion_fx)
                    meteor.update(self.player.turbo)
                    meteor.draw()

                for enemy in self.enemy_group:
                    enemy.check_collision(self.player, self.explosion_fx)
                    enemy.update()
                    enemy.draw()

            # Update screen
            pygame.display.update()

        return select


class Record(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.game_over_logo = pygame.image.load(game_over_img).convert_alpha()
        self.logo_x = (SCREEN_WIDTH - LOGO) // 2
        self.logo_y = SCREEN_HEIGHT

    def main_loop(self, select):
        run = True
        while run:
            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    exit()

                # Keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: # Restart game
                        pass
                    if event.key == pygame.K_RETURN: # Show menu
                        run = False
                    if event.key == pygame.K_ESCAPE: # Quit game
                        exit()

            # Draw background
            self.screen.fill(self.color('BLACK'))

            # Area - update and draw
            if self.logo_y > self.logo_x:
                self.logo_y -= 0.2
            self.screen.blit(self.game_over_logo, (self.logo_x, self.logo_y))

            # Update screen
            pygame.display.update()

        self.logo_y = SCREEN_HEIGHT

        return select
