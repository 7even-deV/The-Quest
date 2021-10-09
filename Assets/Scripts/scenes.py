import pygame

from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, FONTS, FPS, LOGO, COLOR
from .manager import statue_img, bg_img, game_over_img, load_sound
from .tools import Timer, Canvas, Icon
from .environment import Foreground, Background, Farground
from .obstacles import Meteor
from .players import Player
from .enemies import Enemy


class Scene():

    def __init__(self, screen):
        self.screen = screen # Parameterize the screen for all scenes
        self.clock  = pygame.time.Clock() # Manage screen refresh rate

        self.highscore = 0

    def sound(self, sfx, volume=0.5):
        fx = pygame.mixer.Sound(load_sound(sfx))
        fx.set_volume(volume)
        return fx

    def volume(self, vol=0):
        return round(pygame.mixer.music.get_volume() + vol, 1)


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

        # Create menu timer
        self.menu_timer = Timer(FPS)

    def main_loop(self, select, level, score):
        run = True
        while run:
            # Limit frames per second
            self.clock.tick(FPS)

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

            # Clear screen and set background color
            self.screen.fill(COLOR('ARCADE'))

            ''' --- AREA TO UPDATE AND DRAW --- '''

            self.screen.blit(self.statue, (0, SCREEN_HEIGHT//4))

            self.symbol.update(select)
            self.spaceship.update(select)

            self.symbol.draw()
            self.spaceship.draw()

            # Limit delay without event activity
            if self.menu_timer.countdown(1, True):
                run = False

            # Update screen
            pygame.display.update()

        return select, level, score


class Game(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.bg = Background(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, bg_img)
        self.fg  = Farground(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, 50)

        self.lives_view     = Canvas(size=20, color=COLOR('YELLOW'), letter_f=FONTS[3])
        self.health_view    = Canvas(size=15, y=35, letter_f=FONTS[3])
        self.ammo_load_view = Canvas(size=15, y=50, letter_f=FONTS[3])
        self.level_view     = Canvas(size=20, center=True, color=COLOR('GREEN'), letter_f=FONTS[3])
        self.timer_view     = Canvas(size=22, center=True, y=SCREEN_HEIGHT*0.06, letter_f=FONTS[1])
        self.highscore_view = Canvas(size=15, right_text=True, color=COLOR('RED'), letter_f=FONTS[3])
        self.score_view     = Canvas(size=22, y=40, right=True, letter_f=FONTS[3])

        self.paused         = Canvas(size=80, center=True, y=SCREEN_HEIGHT//3, color=COLOR('RED'))
        self.vol_browse     = Canvas(center=True, y=SCREEN_HEIGHT//2, color=COLOR('YELLOW'))

        self.bullet_group    = pygame.sprite.Group()
        self.missile_group   = pygame.sprite.Group()
        self.enemy_group     = pygame.sprite.Group()
        self.meteor_group    = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()

        self.ui_bar          = pygame.sprite.Group()
        self.settings        = pygame.sprite.Group()

        self.group_list = [self.bullet_group, self.missile_group, self.enemy_group, self.meteor_group, self.explosion_group]

        self.ui_bar.add(self.lives_view, self.health_view, self.ammo_load_view, self.level_view, self.timer_view, self.highscore_view, self.score_view)
        self.settings.add(self.paused, self.vol_browse)

        # Sounds fx
        self.move_fx        = self.sound('move')
        self.backmove_fx    = self.sound('backmove')
        self.turbo_fx       = self.sound('turbo')
        self.explosion_fx   = self.sound('explosion')

        self.bullet_fx      = self.sound('bullet')
        self.empty_ammo_fx  = self.sound('empty_ammo')
        self.missile_fx     = self.sound('missile')
        self.missile_cd_fx  = self.sound('missile_countdown')
        self.missile_exp_fx = self.sound('missile_explosion')
        self.empty_load_fx  = self.sound('empty_load')

        self.pause_fx       = self.sound('pause')
        self.select_fx      = self.sound('select')
        self.win_fx         = self.sound('win')
        self.game_over_fx   = self.sound('game_over')

    # Function to reset level
    def reset_level(self):
        self.bullet_group.empty()
        self.missile_group.empty()
        self.explosion_group.empty()
        self.enemy_group.empty()
        self.meteor_group.empty()
        self.meteor_list = self.meteor_list_copy

    def meteor_surge(self, level, surge_num):
        self.meteor_list = []
        for number in range(surge_num):
            temp_list = []
            # Increase the number of meteors per surge
            for _ in range((number + level) * 100 // 4):
                temp_list.append(Meteor(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT))

            self.meteor_list.append(temp_list)

    def process_data(self, select, level, score):
        # Create sprites
        self.meteor_surge(level, 1)
        self.meteor_list_copy = self.meteor_list.copy()
        self.player = Player(self.screen, select, score, 2, level*100, level, self.group_list)
        self.enemy  = Enemy(self.screen, 2, center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//5))
        self.enemy_group.add(self.enemy)

        # Create game timer
        self.game_timer = Timer(FPS)

    def main_loop(self, select, level, score):
        self.process_data(select, level, score)
        vol = self.volume()
        pause = False
        restart = False

        surge_start = False
        surge_index = 0

        shoot = False
        shoot_bullets = False
        throw = False
        throw_missiles = False

        run = True
        while run:
            # Limit frames per second
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
                        if self.player.alive:
                            self.player.turbo = True
                            self.turbo_fx.play()
                        else: restart = True
                    if event.key == pygame.K_r: # Shoot bullets
                        shoot = True
                    if event.key == pygame.K_e: # Throw missiles
                        throw = True

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

                    if event.key == pygame.K_r:
                        shoot = False
                        shoot_bullets = False
                    if event.key == pygame.K_e:
                        throw = False
                        throw_missiles = False

                    if event.key == pygame.K_SPACE: # Turbo
                        self.player.turbo = False
                        self.backmove_fx.play()

            # Clear screen and set background color
            self.screen.fill(COLOR('ARCADE'))

            ''' --- AREA TO UPDATE AND DRAW --- '''

            if pause:
                # Pause and volume control
                self.paused.text = "P A U S E"

                if vol == 0.0 or vol == 1.0:
                    self.vol_browse.color = COLOR('ORANGE')
                else: self.vol_browse.color = COLOR('YELLOW')
                self.vol_browse.text = f"Press <UP or DOWN> to vol:  {vol}"

                self.settings.update()
                self.settings.draw(self.screen)

            else:
                # Update the time of the next surge of meteors
                if not surge_start and self.game_timer.delay(level * 60 // 4 * (surge_index + 1), True):
                    surge_start = True

                elif surge_start:
                    # Add the next surge when the previous surge ends
                    if surge_index < len(self.meteor_list):
                        if len(self.meteor_group) == 0:
                            self.meteor_group.add(self.meteor_list[surge_index])
                            surge_index += 1
                            surge_start = False

                if self.player.spawn and self.game_timer.counter(2, True):
                    self.player.spawn = False

                if self.player.alive:
                    if self.player.collide and self.game_timer.counter(1, True):
                        self.player.collide = False

                    # Shoot bullets
                    if shoot and not shoot_bullets:
                        self.player.shoot(self.empty_ammo_fx, self.bullet_fx)
                        shoot_bullets = True

                    # Throw missiles
                    elif throw and not throw_missiles:
                        self.player.throw(self.empty_load_fx, self.missile_fx, self.missile_cd_fx, self.missile_exp_fx)
                        throw_missiles = True

                else: # Restart the level if the player has lost
                    if restart:
                        self.reset_level()
                        self.process_data(select, level, score)
                        restart = False

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

                self.bullet_group.update()
                self.missile_group.update()
                self.explosion_group.update()

                self.bullet_group.draw(self.screen)
                self.missile_group.draw(self.screen)
                self.explosion_group.draw(self.screen)

                # Zone for user interface bar
                pygame.draw.rect(self.screen, COLOR('ARCADE'), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT//10))
                pygame.draw.line(self.screen, COLOR('SILVER'), (0, SCREEN_HEIGHT//10), (SCREEN_WIDTH, SCREEN_HEIGHT//10), 4)

                # Level countdown
                if self.game_timer.countdown(level, self.player.turbo, True):
                    run = False
                    level += 1
                    self.win_fx.play()

                elif self.player.health <= 0:
                    run = False
                    self.player.lives -= 1
                    self.player.score = 0
                    self.game_over_fx.play()

                self.lives_view.text     = f"Lives: {self.player.lives}"
                self.health_view.text    = f"Health: {self.player.health}"
                self.ammo_load_view.text = f"ammo: {self.player.ammo} | load: {self.player.load}"
                self.level_view.text     = f"Level - {level} - "
                self.timer_view.text     = f"Time: {self.game_timer.text_time}"
                self.highscore_view.text = f"Highscore: {self.highscore}"
                self.score_view.text     = f"Score: {self.player.score}"
                self.ui_bar.update()
                self.ui_bar.draw(self.screen)

            # Update screen
            pygame.display.update()

        return select, level, self.player.score


class Record(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.game_over_logo = pygame.image.load(game_over_img).convert_alpha()
        self.logo_x = (SCREEN_WIDTH - LOGO) // 2
        self.logo_y = SCREEN_HEIGHT

        # Create record timer
        self.record_timer = Timer(FPS)

    def main_loop(self, select, level, score):
        run = True
        while run:
            # Limit frames per second
            self.clock.tick(FPS)

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

            # Clear screen and set background color
            self.screen.fill(COLOR('BLACK'))

            ''' --- AREA TO UPDATE AND DRAW --- '''

            if self.logo_y > self.logo_x:
                self.logo_y -= 2
            self.screen.blit(self.game_over_logo, (self.logo_x, self.logo_y))

            # Limit delay without event activity
            if self.record_timer.countdown(1, True):
                run = False

            # Update screen
            pygame.display.update()

        self.logo_y = SCREEN_HEIGHT

        return select, level, score
