import pygame

from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, LOGO, COLOR, LIVES, SURGE_NUM, enemy_select
from .manager import msg_dict, btn_text_list, keyboard_list, statue_img, bg_img, lives_img, game_over_img, load_music, load_sound
from .tools import Timer, Button, Keyboard, Canvas, Icon, HealthBar, Screen_fade
from .environment import Foreground, Background, Farground, Planet, Portal
from .obstacles import Meteor
from .players import Player
from .enemies import Enemy
from .database import Database


class Scene():

    def __init__(self, screen):
        self.screen = screen # Parameterize the screen for all scenes
        self.clock  = pygame.time.Clock() # Manage screen refresh rate

        self.db = Database()

    def load_username(self):
        read_data_list = self.db.read_data()

        username_list  = ["New User"]
        for user in read_data_list:
            username_list.append(user[0])

        return username_list

    def load_data(self, username, select, model, level, score, highscore):
        try:
            highscore = self.db.read_data(username)[0][-1]
        except: highscore = 0

        if score > highscore:
            highscore = score
            new_highscore = True
        else: new_highscore = False

        self.db.update_data(username, highscore)

        return new_highscore

    def scene_music(self, index, volume):
        pygame.mixer.music.load(load_music(index))
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1, 0.0, 1000)

    def sound(self, sfx, volume=0.5):
        fx = pygame.mixer.Sound(load_sound(sfx))
        fx.set_volume(volume)
        return fx

    def volume(self, vol=0):
        return round(pygame.mixer.music.get_volume() + vol, 1)


class Main(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.message = Canvas(size=20, center=True, color=COLOR('YELLOW'), letter_f=3)

        # Sounds fx
        self.select_loop_fx = self.sound('select_loop')
        self.select_fx      = self.sound('select')
        self.confirm_fx     = self.sound('confirm')
        self.start_fx       = self.sound('start')

        # Create menu timer
        self.menu_timer = Timer(FPS)

    def command_buttons(self):
        self.command_list = []
        pos_y = 0.0
        for btn in range(len(btn_text_list)):
            self.command_list.append(Button(btn_text_list[0][btn], center=(SCREEN_WIDTH//2, SCREEN_HEIGHT*(0.5+pos_y))))
            pos_y += 0.12

    def keyboard_buttons(self):
        self.keyboard_list = []
        margin_x = SCREEN_WIDTH//10.75
        margin_y = SCREEN_HEIGHT//7.75

        for row in range(len(keyboard_list)):
            temp_list = []
            for column in range(len(keyboard_list[row])):
                temp_list.append(Keyboard(keyboard_list[row][column], center=(column * SCREEN_WIDTH//11 + margin_x, row * SCREEN_HEIGHT//15 + margin_y)))
            self.keyboard_list.append(temp_list)

    def main_loop(self, username, select, model, level, score):
        self.command_buttons()
        self.command_list[0].select_effect(True)

        self.keyboard_buttons()
        self.keyboard_list[0][0].select_effect(True)

        vol = self.volume()
        cursor = column_key = row_key = select = 0
        login = create = confirm = False

        user = -1
        msg = 0
        turnback = False

        username_list = self.load_username()
        btn_text_list[1][0] = username_list

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
                        if not create:
                            if login: # Account select
                                if user > 0:
                                    user -= 1
                                else: user = len(username_list) - 1
                        else:
                            if column_key > 0:
                                column_key -= 1
                            else: column_key = len(self.keyboard_list[row_key]) - 1
                            self.keyboard_list[row_key][column_key].select_effect(True)

                        self.select_fx.play()

                    if event.key == pygame.K_RIGHT: # Next select
                        if not create:
                            if login: # Account select
                                if user < len(username_list) - 1:
                                    user += 1
                                else: user = 0
                        else:
                            if column_key < len(self.keyboard_list[row_key]) - 1:
                                column_key += 1
                            else: column_key = 0
                            self.keyboard_list[row_key][column_key].select_effect(True)

                        self.select_fx.play()

                    if event.key == pygame.K_UP: # Up select
                        if not create:
                            if cursor > 0:
                                cursor -= 1
                            else: cursor = len(self.command_list) - 1
                            self.command_list[cursor].select_effect(True)
                        else:
                            if row_key > 0:
                                row_key -= 1
                            else: row_key = len(self.keyboard_list) - 1
                            self.keyboard_list[row_key][column_key].select_effect(True)

                        self.select_fx.play()

                    if event.key == pygame.K_DOWN: # Down select
                        if not create:
                            if cursor < len(self.command_list) - 1:
                                cursor += 1
                            else: cursor = 0
                            self.command_list[cursor].select_effect(True)
                        else:
                            if row_key < len(self.keyboard_list) - 1:
                                row_key += 1
                            else: row_key = 0
                            self.keyboard_list[row_key][column_key].select_effect(True)

                        self.select_fx.play()

                    if event.key == pygame.K_SPACE: # Turnback select
                        if create:
                            if username == '':
                                self.command_list[0].pos_x = self.command_list[0].init_pos
                            if len(username) < 10:
                                username += self.keyboard_list[row_key][column_key].text
                                btn_text_list[2][0] = username
                            else: msg = 2

                            self.keyboard_list[row_key][column_key].trigger = True
                            self.keyboard_list[row_key][column_key].active_effect(True)
                        else:
                            turnback = True
                            run = False

                        self.confirm_fx.play()

                    if event.key == pygame.K_RETURN: # Confirm
                        self.command_list[cursor].trigger = True
                        self.command_list[cursor].active_effect(True)

                        self.confirm_fx.play()

                    if event.key == pygame.K_BACKSPACE: # Delete
                        if create:
                            if len(username) > 0:
                                username = username[:-1]

                    if event.key == pygame.K_ESCAPE: # Quit game
                        exit()

                # keyboard release
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE: # Turnback select
                        if create: self.keyboard_list[row_key][column_key].active_effect(False)

                    if event.key == pygame.K_RETURN: # Confirm
                        if self.command_list[0].trigger:
                            if not confirm:
                                if login:
                                    if username_list[user] == username_list[0]:
                                        if create:
                                            if username == '' or username in username_list[1:]:
                                                msg = 1
                                            else:
                                                self.db.create_data(username)
                                                username_list.append(username)
                                                user = -1
                                                create = False
                                                msg = 3
                                        else:
                                            username = ''
                                            create = True
                                    else: confirm = True
                                else: login = True
                            else:
                                username = username_list[user]
                                run = False

                        elif self.command_list[3].trigger:
                            if  confirm: confirm = False
                            elif create:  create = False
                            elif  login:   login = False
                            else:
                                turnback = True
                                run = False

                        self.command_list[cursor].active_effect(False)

            # Clear screen and set background color
            self.screen.fill(COLOR('ARCADE'))

            ''' --- AREA TO UPDATE AND DRAW --- '''

            self.message.text = msg_dict[msg]
            self.message.update()
            self.message.draw(self.screen)

            if  confirm: select = 3
            elif create: select = 2
            elif  login: select = 1
            else:        select = 0

            for self.command, index in zip(self.command_list, range(len(self.command_list))):
                if index % 2 == 0: self.command_list[index].flip_x = True

                if self.command != self.command_list[cursor]:
                    self.command.select_effect(False)
                    self.command.trigger = False

                if not self.command_list[index] == self.command_list[0]:
                    self.command_list[index].text = btn_text_list[select][index]
                else:
                    if  confirm: self.command_list[0].text = "Play"
                    elif create: self.command_list[0].text = username
                    elif  login: self.command_list[0].text = btn_text_list[select][index][user]

                self.command.update()
                self.command.draw(self.screen)

            if create:
                for row in range(len(self.keyboard_list)):
                    for self.keyboard, index in zip(self.keyboard_list[row], range(len(self.keyboard_list[row]))):
                        if self.keyboard != self.keyboard_list[row_key][column_key]:
                            self.keyboard.select_effect(False)
                            self.keyboard.trigger = False

                        self.keyboard.update()
                        self.keyboard.draw(self.screen)

            # Limit delay without event activity
            if self.menu_timer.countdown(1, True):
                turnback = True
                run = False

            # Update screen
            pygame.display.update()

        return username, select, model, level, score, turnback


class Menu(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.symbol    = Icon(self.screen, 'symbol', 1.5, center=(SCREEN_WIDTH//1.8, SCREEN_HEIGHT//1.39))
        self.spaceship = Icon(self.screen, 'spaceships', 4, center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2.5))
        self.portal = Portal(self.screen, center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2.5))
        self.statue = pygame.image.load(statue_img).convert_alpha()

        # Sounds fx
        self.portal_loop_fx = self.sound('portal_loop')
        self.select_loop_fx = self.sound('select_loop')
        self.select_fx      = self.sound('select')
        self.confirm_fx     = self.sound('confirm')
        self.start_fx       = self.sound('start')

        # Create menu timer
        self.menu_timer = Timer(FPS)

    def main_loop(self, username, select, model, level, score):
        vol = self.volume()
        confirm = False
        select = 0
        model = 0
        turnback = False

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
                        if not confirm:
                            self.symbol.trigger_effect(True)
                            self.portal_loop_fx.play()
                        else:
                            self.spaceship.trigger_effect(True)
                            self.select_loop_fx.play()

                    if event.key == pygame.K_RIGHT: # Next select
                        if not confirm:
                            self.symbol.trigger_effect(True)
                            self.portal_loop_fx.play()
                        else:
                            self.spaceship.trigger_effect(True)
                            self.select_loop_fx.play()

                    if event.key == pygame.K_SPACE: # Turnback select
                        if not confirm:
                            turnback = True
                            run = False
                        else:
                            confirm = False
                            model = 0
                            self.select_fx.play()
                    if event.key == pygame.K_RETURN: # Play game
                        if not confirm:
                            confirm = True
                            self.start_fx.play()
                        else:
                            run = False
                            self.start_fx.play()

                    if event.key == pygame.K_UP:
                        if self.volume() < 1.0: # Turn up the volume
                            vol = self.volume(+ 0.1)
                            pygame.mixer.music.set_volume(vol)
                            self.select_fx.play()

                    if event.key == pygame.K_DOWN:
                        if self.volume() > 0.0: # Turn down the volume
                            vol = self.volume(- 0.1)
                            pygame.mixer.music.set_volume(vol)
                            self.select_fx.play()

                    if event.key == pygame.K_ESCAPE: # Quit game
                        turnback = True
                        run = False

                # keyboard release
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT: # Back select
                        if not confirm:
                            if select > 0:
                                select -= 1
                            else: select = 2
                            self.symbol.trigger_effect(False)
                            self.select_fx.play()
                        else:
                            if model > 0:
                                model -= 1
                            else: model = 5
                            self.spaceship.trigger_effect(False)
                            self.confirm_fx.play()

                    if event.key == pygame.K_RIGHT: # Next select
                        if not confirm:
                            if select < 2:
                                select += 1
                            else: select = 0
                            self.symbol.trigger_effect(False)
                            self.select_fx.play()
                        else:
                            if model < 5:
                                model += 1
                            else: model = 0
                            self.spaceship.trigger_effect(False)
                            self.confirm_fx.play()

            # Clear screen and set background color
            self.screen.fill(COLOR('ARCADE'))

            ''' --- AREA TO UPDATE AND DRAW --- '''

            self.portal.update()
            self.portal.draw()
            self.screen.blit(self.statue, (0, SCREEN_HEIGHT//4))

            self.symbol.draw()
            if not confirm:
                self.symbol.update(select, model)
            else:
                self.spaceship.update(select, model)
                self.spaceship.draw()

            # Limit delay without event activity
            if self.menu_timer.countdown(1, True):
                turnback = True
                run = False

            # Update screen
            pygame.display.update()

        return username, select, model, level, score, turnback


class Game(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        # Create screen fades
        self.intro_fade = Screen_fade(self.screen, 'intro', COLOR('BLACK'), 4)
        self.death_fade = Screen_fade(self.screen, 'death', COLOR('BLACK'), 4)

        self.ammo_load_view = Canvas(size=15, y=50, letter_f=3)
        self.username_view  = Canvas(size=18, center=True, y=-1, color=COLOR('GREEN'), letter_f=3)
        self.level_view     = Canvas(size=18, center=True, y=SCREEN_HEIGHT*0.03, color=COLOR('GREEN'), letter_f=3)
        self.timer_view     = Canvas(size=20, center=True, y=SCREEN_HEIGHT*0.06, letter_f=1)
        self.highscore_view = Canvas(size=18, right_text=True, color=COLOR('RED'), letter_f=3)
        self.score_view     = Canvas(size=22, y=40, right=True, letter_f=3)

        self.paused         = Canvas(size=80, center=True, y=SCREEN_HEIGHT//3, color=COLOR('RED'))
        self.vol_browse     = Canvas(center=True, y=SCREEN_HEIGHT//2, color=COLOR('YELLOW'))

        self.bullet_group    = pygame.sprite.Group()
        self.missile_group   = pygame.sprite.Group()
        self.enemy_group     = pygame.sprite.Group()
        self.meteor_group    = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()

        self.ui_bar          = pygame.sprite.Group()
        self.settings        = pygame.sprite.Group()

        self.meteor_list_copy = []
        self.group_list = [self.bullet_group, self.missile_group, self.enemy_group, self.meteor_group, self.explosion_group]

        self.ui_bar.add(self.ammo_load_view, self.username_view, self.level_view, self.timer_view, self.highscore_view, self.score_view)
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

    def environment_create(self, init_planet):
        bg = Background(SCREEN_WIDTH, SCREEN_HEIGHT, bg_img)
        fg  = Farground(SCREEN_WIDTH, SCREEN_HEIGHT, 50)
        origin_planet  = Planet('origin' , init_planet, SCREEN_WIDTH, SCREEN_HEIGHT, midbottom=(SCREEN_WIDTH//2, SCREEN_HEIGHT))
        destiny_planet = Planet('destiny', init_planet, SCREEN_WIDTH, SCREEN_HEIGHT, midbottom=(SCREEN_WIDTH//2, 0))

        self.environment_list = [bg, fg, origin_planet, destiny_planet]

    def enemy_create(self, level):
        self.enemy_list = []
        temp_list = []
        for i in range(level):
            temp_list.append(Enemy(self.screen, enemy_select, i+2, self.player, self.empty_ammo_fx, self.bullet_fx, self.group_list))
        self.enemy_list.append(temp_list)
        self.enemy_group.add(self.enemy_list[0])

    def meteor_surge(self, level, surge_num):
        self.meteor_list = []
        for number in range(surge_num):
            temp_list = []
            # Increase the number of meteors per surge
            for _ in range((number + level) * 100 // 4):
                temp_list.append(Meteor(self.screen, self.player, SCREEN_WIDTH, SCREEN_HEIGHT))

            self.meteor_list.append(temp_list)

    def process_data(self, lives, select, model, level, score, init_planet):
        # Create sprites
        self.player = Player(self.screen, lives, select, model, score, 2, level*100, level, self.group_list)
        self.environment_create(init_planet)
        self.lives_view = pygame.image.load(lives_img).convert_alpha()
        self.health_bar = HealthBar(self.screen, self.player.health, self.player.max_health)
        self.enemy_create(level)
        self.meteor_surge(level, SURGE_NUM)
        self.meteor_list_copy = self.meteor_list.copy()

        # Create game timer
        self.game_timer = Timer(FPS)

    def main_loop(self, username, select, model, level, score):
        self.reset_level()
        username_data = self.db.read_data(username)
        highscore = username_data[0][-1]

        lives = LIVES
        init_planet = 1
        self.process_data(lives, select, model, level, score, init_planet)

        vol = self.volume()
        pause = False
        restart = False
        death = False

        surge_start = False
        surge_end = False
        surge_index = 0

        shoot = False
        shoot_bullets = False
        throw = False
        throw_missiles = False

        turnback = False

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
                        if not self.player.win:
                            self.player.moving_left = True # Moving left
                            self.move_fx.play()

                    if event.key == pygame.K_RIGHT:
                        if not self.player.win:
                            self.player.moving_right = True # Moving right
                            self.move_fx.play()

                    if event.key == pygame.K_UP:
                        if pause and self.volume() < 1.0: # Turn up the volume
                            vol = self.volume(+ 0.1)
                            pygame.mixer.music.set_volume(vol)
                            self.select_fx.play()
                        elif not self.player.win:
                            self.player.moving_up = True # Moving up
                            self.move_fx.play()

                    if event.key == pygame.K_DOWN:
                        if pause and self.volume() > 0.0: # Turn down the volume
                            vol = self.volume(- 0.1)
                            pygame.mixer.music.set_volume(vol)
                            self.select_fx.play()
                        elif not self.player.win:
                            self.player.moving_down = True # Moving down
                            self.move_fx.play()

                    if event.key == pygame.K_SPACE: # Turbo
                        if not self.player.spawn and self.player.alive and not self.player.win:
                            self.player.turbo = True
                            self.turbo_fx.play()
                        else: restart = True
                    if event.key == pygame.K_r: # Shoot bullets
                        if not self.player.win: shoot = True
                    if event.key == pygame.K_e: # Throw missiles
                        if not self.player.win: throw = True

                    if event.key == pygame.K_RETURN: # Pause and Settings
                        if pause:
                            pause = False
                        else: pause = True
                        self.pause_fx.play()

                    if event.key == pygame.K_ESCAPE: # Exit game
                        turnback = True
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

                elif surge_start and not surge_end:
                    # Add the next surge when the previous surge ends
                    if len(self.meteor_group) == 0:
                        if surge_index < len(self.meteor_list):
                            self.meteor_group.add(self.meteor_list[surge_index])
                            surge_index += 1
                            surge_start = False
                            self.scene_music(4, 0.5)
                        else:
                            surge_end = True
                            self.scene_music(2, 0.5)

                for self.environment in self.environment_list:
                    self.environment.update(self.player.delta_x, self.player.turbo, self.player.win)
                    self.environment.draw(self.screen)

                # self.player.check_collision()
                self.player.update()
                self.player.draw()

                for meteor in self.meteor_group:
                    meteor.check_collision(self.explosion_fx)
                    meteor.update(self.player.turbo)
                    meteor.draw()

                for enemy in self.enemy_group:
                    enemy.update()
                    enemy.check_collision(self.explosion_fx)
                    enemy.draw()

                self.bullet_group.update()
                self.missile_group.update()
                self.explosion_group.update()

                self.bullet_group.draw(self.screen)
                self.missile_group.draw(self.screen)
                self.explosion_group.draw(self.screen)

                if self.player.alive:
                    if self.player.spawn and self.intro_fade.fade():
                        self.intro_fade.fade_counter = 0
                        self.player.spawn = False

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

                    # Level countdown
                    if not self.player.win and self.game_timer.countdown(level, self.player.turbo, True):
                        self.game_timer.text_time = 0
                        self.player.win = True
                        self.win_fx.play()

                    # Check if player has completed the level
                    elif self.player.win and self.player.auto_movement():
                        level += 1
                        self.reset_level()
                        init_planet = self.environment.destiny_planet
                        self.process_data(lives, select, model, level, score, init_planet)
                else:
                    if not death:
                        death = True
                        self.game_over_fx.play()

                    # Restart the level if the player has lost
                    elif death and self.death_fade.fade():
                        if restart:
                            self.death_fade.fade_counter = 0
                            self.player.score = 0
                            if lives > 0:
                                lives -= 1
                                self.reset_level()
                                init_planet = self.environment.origin_planet
                                self.process_data(lives, select, model, level, score, init_planet)
                                self.player.alive = True
                                death = False
                                restart = False
                            else: run = False

                # Zone for user interface bar
                pygame.draw.rect(self.screen, COLOR('ARCADE'), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT//10))
                pygame.draw.line(self.screen, COLOR('SILVER'), (0, SCREEN_HEIGHT//10), (SCREEN_WIDTH, SCREEN_HEIGHT//10), 4)

                # Show player lives
                for x in range(self.player.lives):
                    self.screen.blit(self.lives_view, (0 + (x * SCREEN_WIDTH*0.05), 0))
                # Show player health
                self.health_bar.draw(self.player.health)

                self.ammo_load_view.text = f"ammo: {self.player.ammo} | load: {self.player.load}"
                self.username_view.text  = f"- {username} -"
                self.level_view.text     = f"Level - {level} -"
                self.timer_view.text     = f"Time: {self.game_timer.text_time}"
                self.score_view.text     = f"Score: {self.player.score}"
                if self.player.score > highscore:
                    self.highscore_view.x = SCREEN_WIDTH-200
                    self.highscore_view.text = "New  Highscore"
                else: self.highscore_view.text = f"Highscore: {highscore}"

                self.ui_bar.update()
                self.ui_bar.draw(self.screen)

            # Update screen
            pygame.display.update()

        return username, select, model, level, self.player.score, turnback


class Record(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.game_over_logo = pygame.image.load(game_over_img).convert_alpha()
        self.logo_x = (SCREEN_WIDTH - LOGO) // 2
        self.logo_y = SCREEN_HEIGHT

        self.text_score    = Canvas(size=24, center=True, y=SCREEN_HEIGHT//3, letter_f=3)
        self.text_continue = Canvas(size=44, center=True, y=SCREEN_HEIGHT//1.7, letter_f=2, color=COLOR('GREEN'))
        self.text_replay   = Canvas(size=40, center=True, y=SCREEN_HEIGHT//1.5, letter_f=2, color=COLOR('YELLOW'))
        self.text_exit     = Canvas(size=34, center=True, y=SCREEN_HEIGHT//1.22, letter_f=2, color=COLOR('RED'))

        self.text_continue.text = "Press <SPC> to Continue"
        self.text_replay.text   = "Press <ENTER> to Menu"
        self.text_exit.text     = "Press <ESC> to Exit"

        self.text_group = pygame.sprite.Group()
        self.text_group.add(self.text_score, self.text_replay, self.text_continue, self.text_exit)

        # Create record timer
        self.record_timer = Timer(FPS)

    def reset_ranking(self):
        top_ranking = self.db.read_data()
        self.ranking_list = []
        pos_y = 0.0
        for user in range(len(top_ranking)):
            temp_var = Canvas(size=20, x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT*(0.1+pos_y), letter_f=1, color=COLOR('BLACK'))
            temp_var.text = f"Ranking {user+1}: {top_ranking[user][0]} -> {top_ranking[user][-1]}"
            pos_y += 0.1
            self.ranking_list.append(temp_var)

    def main_loop(self, username, select, model, level, score):
        new_highscore = self.load_data(username, select, model, level, score, score)
        self.reset_ranking()
        color_up = 0
        color_down = 255
        turnback = False

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
                        turnback = True
                        run = False
                    if event.key == pygame.K_RETURN: # Show menu
                        run = False
                    if event.key == pygame.K_ESCAPE: # Quit game
                        exit()

            # Clear screen and set background color
            self.screen.fill(COLOR('BLACK'))

            ''' --- AREA TO UPDATE AND DRAW --- '''

            if new_highscore:
                self.text_score.text   = "NEW  HIGH  SCORE"
            else: self.text_score.text = "TOP  HIGH  SCORE"

            if self.logo_y > 0:
                self.logo_y -= 2
            else:
                for ranking in self.ranking_list:
                    if self.ranking_list[0].y < SCREEN_HEIGHT * 0.8:
                        ranking.y += 0.5
                    if ranking.y > SCREEN_HEIGHT * 0.25 and ranking.y < SCREEN_HEIGHT * 1.05:
                        if color_up < 255: color_up += 1
                        ranking.color = ([color_up]*3)
                    else:
                        if color_down > 0: color_down -= 1
                        ranking.color = ([color_down]*3)

                    ranking.update()
                    ranking.draw(self.screen)

            self.screen.blit(self.game_over_logo, (self.logo_x, self.logo_y))

            self.text_group.update()
            self.text_group.draw(self.screen)

            # Limit delay without event activity
            if self.record_timer.countdown(1, True):
                run = False

            # Update screen
            pygame.display.update()

        self.logo_y = SCREEN_HEIGHT

        return username, select, model, level, score, turnback
