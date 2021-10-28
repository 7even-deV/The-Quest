import pygame, random

from .settings    import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, MUSIC_VOL, SOUND_VOL, LOGO, COLOR, STARS, LIVES, SPEED, SURGE_NUM, enemy_select, enemy_position
from .documents   import CREDITS, HISTORY, GUIDE
from .manager     import msg_dict, button_list, bar_list, keyboard_list, statue_img, bg_img, lives_img, game_over_img, load_music, load_sound
from .tools       import Timer, Button, Bar, Keyboard, Board, Canvas, Icon, HealthBar, Screen_fade
from .environment import Foreground, Background, Farground, Planet, Portal
from .players     import Player
from .enemies     import Enemy
from .obstacles   import Meteor
from .database    import Database


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

    def load_select(self, username, style, model, level):
        self.db.update_data(username, STYLE=style)
        self.db.update_data(username, MODEL=model)
        self.db.update_data(username, LEVEL=level)

    def load_data(self, username, level, score):
        username_data = self.db.read_data(username)

        highlevel = username_data[0][3]
        if level > highlevel:
            highlevel = level

        highscore = username_data[0][6]
        if score > highscore:
            highscore = score
            new_highscore = True
        else: new_highscore = False

        self.db.update_data(username, LEVEL=level)
        self.db.update_data(username, HIGHLEVEL=highlevel)
        self.db.update_data(username, SCORE=score)
        self.db.update_data(username, HIGHSCORE=highscore)

        return new_highscore

    def load_volume(self, username, music, sound):
        self.db.update_data(username, MUSIC=music)
        self.db.update_data(username, SOUND=sound)

    def music(self, index, volume=MUSIC_VOL):
        pygame.mixer.music.load(load_music(index))
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1, 0.0, 1000)

    def sound(self, sfx, volume=SOUND_VOL):
        fx = pygame.mixer.Sound(load_sound(sfx))
        fx.set_volume(volume)
        return fx

    def music_vol(self, vol=0):
        return round(pygame.mixer.music.get_volume() + vol, 1)

    def sound_vol(self, sfx, vol=0):
        return round(sfx.get_volume() + vol, 1)


class Main(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.message = Canvas(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2.5), letter=2, size=20)
        self.board   = Board(midbottom=(SCREEN_WIDTH//2, 0))

        # Sounds fx
        self.select_loop_fx = self.sound('select_loop')
        self.select_fx      = self.sound('select')
        self.confirm_fx     = self.sound('confirm')
        self.start_fx       = self.sound('start')

        self.sfx_list = [self.select_loop_fx, self.select_fx, self.confirm_fx, self.start_fx]

        # Create menu timer
        self.menu_timer = Timer(FPS)

    def command_buttons(self):
        self.command_list = []
        margin_y = SCREEN_HEIGHT//2

        for btn in range(len(button_list[0])):
            self.command_list.append(Button(button_list[0][btn], center=(SCREEN_WIDTH//2, btn * SCREEN_HEIGHT//8 + margin_y)))

    def config_buttons(self):
        self.config_list = []
        margin_y = SCREEN_HEIGHT//5

        for bar in range(len(bar_list)):
            self.config_list.append(Bar(bar_list[bar], center=(SCREEN_WIDTH//1.8, bar * SCREEN_HEIGHT//10 + margin_y)))

    def keyboard_buttons(self):
        self.keyboard_list = []
        margin_x = SCREEN_WIDTH//10.75
        margin_y = SCREEN_HEIGHT//7.75

        for row in range(len(keyboard_list)):
            temp_list = []
            for column in range(len(keyboard_list[row])):
                temp_list.append(Keyboard(keyboard_list[row][column], center=(column * SCREEN_WIDTH//11 + margin_x, row * SCREEN_HEIGHT//15 + margin_y)))
            self.keyboard_list.append(temp_list)

    def main_loop(self, username):
        self.command_buttons()
        self.command_list[0].select_effect(True)

        self.config_buttons()
        self.config_list[0].gage.select_effect(True)

        self.keyboard_buttons()
        self.keyboard_list[0][0].select_effect(True)

        cursor = bar = row_key = column_key = select = 0
        login = create = confirm = False

        vol_scan = [0.5] * 2

        user = -1
        msg = 0

        username_list = self.load_username()
        button_list[1][0] = username_list

        scene_browser = 1
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

                            elif self.command_list[1].trigger:
                                if self.config_list[bar].gage == self.config_list[0].gage:
                                    if self.music_vol() > 0.0: # Turn down the volume
                                        vol_scan[0] = self.music_vol(- 0.1)
                                        pygame.mixer.music.set_volume(vol_scan[0])
                                        self.config_list[bar].gage.rect.x -= 22

                                elif self.config_list[bar].gage == self.config_list[1].gage:
                                    if self.sound_vol(self.sfx_list[0]) > 0.0: # Turn down the sound
                                        for sfx in self.sfx_list:
                                            vol_scan[1] = self.sound_vol(sfx, - 0.1)
                                            sfx.set_volume(vol_scan[1])
                                        self.config_list[bar].gage.rect.x -= 22

                                # self.config_list[bar].displace_effect(vol_scan[0])
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

                            elif self.command_list[1].trigger:
                                if self.config_list[bar].gage == self.config_list[0].gage:
                                    if self.music_vol() < 1.0: # Turn up the volume
                                        vol_scan[0] = self.music_vol(+ 0.1)
                                        pygame.mixer.music.set_volume(vol_scan[0])
                                        self.config_list[bar].gage.rect.x += 22

                                elif self.config_list[bar].gage == self.config_list[1].gage:
                                    if self.sound_vol(self.sfx_list[0]) < 1.0: # Turn up the sound
                                        for sfx in self.sfx_list:
                                            vol_scan[1] = self.sound_vol(sfx, + 0.1)
                                            sfx.set_volume(vol_scan[1])
                                        self.config_list[bar].gage.rect.x += 22

                                # self.config_list[bar].displace_effect(vol_scan[0])
                        else:
                            if column_key < len(self.keyboard_list[row_key]) - 1:
                                column_key += 1
                            else: column_key = 0
                            self.keyboard_list[row_key][column_key].select_effect(True)

                        self.select_fx.play()

                    if event.key == pygame.K_UP: # Up select
                        if not create:
                            if not login and self.command_list[1].trigger:
                                if bar > 0:
                                    bar -= 1
                                else: bar = len(self.config_list) - 1
                            else:
                                if cursor > 0:
                                    cursor -= 1
                                else: cursor = len(self.command_list) - 1
                                self.command_list[cursor].select_effect(True)
                        else:
                            if row_key > 0:
                                row_key -= 1
                            else: row_key = len(self.keyboard_list) - 1
                            self.keyboard_list[row_key][column_key].select_effect(True)

                        self.board.show = False
                        self.select_fx.play()

                    if event.key == pygame.K_DOWN: # Down select
                        if not create:
                            if not login and self.command_list[1].trigger:
                                if bar < len(self.config_list) - 1:
                                    bar += 1
                                else: bar = 0
                            else:
                                if cursor < len(self.command_list) - 1:
                                    cursor += 1
                                else: cursor = 0
                                self.command_list[cursor].select_effect(True)
                        else:
                            if row_key < len(self.keyboard_list) - 1:
                                row_key += 1
                            else: row_key = 0
                            self.keyboard_list[row_key][column_key].select_effect(True)

                        self.board.show = False
                        self.select_fx.play()

                    if event.key == pygame.K_SPACE: # Turnback select
                        if create:
                            if len(username) < 10:
                                # These 2 conditions are for not typing if the Delete key or the Shift key is pressed.
                                if self.keyboard_list[row_key][column_key] != self.keyboard_list[-1][-1]\
                                and self.keyboard_list[row_key][column_key] != self.keyboard_list[-1][-2]:
                                    username += self.keyboard_list[row_key][column_key].text
                                    button_list[2][0] = username
                            else: msg = 2

                            # Delete characters from username if Delete key is pressed
                            if self.keyboard_list[row_key][column_key] == self.keyboard_list[-1][-2]:
                                if len(username) > 0: username = username[:-1]

                            # Turn keyboard capitalization on or off if the Shift key is pressed
                            if self.keyboard_list[row_key][column_key] == self.keyboard_list[-1][-1]:
                                if not self.keyboard_list[-1][-1].trigger:
                                    self.keyboard_list[-1][-1].trigger = True
                                else:
                                    self.keyboard_list[-1][-1].trigger = False
                                self.keyboard_list[-1][-1].active_effect(True)
                            else:
                                self.keyboard_list[row_key][column_key].trigger = True
                                self.keyboard_list[row_key][column_key].active_effect(True)
                        else:
                            scene_browser = -1
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
                        if create:
                            self.keyboard_list[row_key][column_key].active_effect(False)

                    if event.key == pygame.K_RETURN: # Confirm
                        # Warning with this area of nested tabulated conditions as their order is very important
                        if self.command_list[0].trigger:
                            if not confirm:
                                if login:
                                    if username_list[user] == username_list[0]:
                                        if create:
                                            msg = 6
                                            if username == '': create = False
                                            elif username in username_list[1:]: msg = 1
                                            else:
                                                self.db.create_data(username)
                                                username_list.append(username)
                                                user = -1
                                                row_key = column_key = 0
                                                self.keyboard_list[0][0].select_effect(True)
                                                self.keyboard_list[-1][-1].trigger = False
                                                create = False
                                                msg = 3
                                        else:
                                            username = ''
                                            msg = 7
                                            create = True
                                    else: confirm = True
                                else: login = True
                            else:
                                username = username_list[user]
                                scene_browser = 2
                                run = False

                        if self.command_list[1].trigger:
                            if not create and not confirm:
                                if not login:
                                    if not self.config.show:
                                        self.config.show = True
                                    else:
                                        self.load_volume(username_list[user], vol_scan[0], vol_scan[1])
                                        self.config.show = False
                                        self.command_list[1].trigger = False
                                else:
                                    if not self.board.show:
                                        self.board.show = True
                                        self.board.create_textline(HISTORY, center=(self.board.rect.centerx, self.board.rect.top))
                                    else: self.board.show = False

                            else:
                                username = username_list[user]
                                scene_browser = 1
                                run = False

                        if self.command_list[2].trigger:
                            if not create and not confirm:
                                if not login:
                                    if not self.board.show:
                                        self.board.show = True
                                        self.board.create_textline(CREDITS, center=(self.board.rect.centerx, self.board.rect.top))
                                    else: self.board.show = False
                                else:
                                    if not self.board.show:
                                        self.board.show = True
                                        self.board.create_textline(GUIDE, midleft=(self.board.rect.width//5.5, self.board.rect.top))
                                    else: self.board.show = False
                            elif username_list[user] != username_list[0]:
                                self.db.delete_data(username_list.pop(user))
                                user = -1
                                msg  = 4
                                confirm = False
                            elif len(username_list) > 1: msg = 0
                            else: msg = 5

                        if self.command_list[3].trigger:
                            if  confirm: confirm = False
                            elif create:  create = False
                            elif  login:   login = False
                            else:
                                scene_browser = -1
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
                    self.command_list[index].text = button_list[select][index]
                else:
                    if  confirm: self.command_list[0].text = "Play"
                    elif create: self.command_list[0].text = username
                    elif  login: self.command_list[0].text = button_list[select][index][user]

                self.command.update()
                self.command.draw(self.screen)

            if not login and self.command_list[1].trigger:
                for self.config in self.config_list:
                    if self.config == self.config_list[bar]:
                        self.config.gage.select_effect(True)
                        self.config.color      = COLOR('YELLOW')
                        self.config.gage.color = COLOR('YELLOW')
                        self.config_list[bar].gage.active_effect(True)
                    else:
                        self.config.gage.select_effect(False)
                        self.config.color      = COLOR('WHITE')
                        self.config.gage.color = COLOR('WHITE')
                        self.config_list[bar].gage.active_effect(False)

                    if vol_scan[bar] == 0.0:
                        self.config_list[bar].gage.text = "min"
                        self.config_list[bar].gage.color = COLOR('ORANGE')
                    elif vol_scan[bar] == 1.0:
                        self.config_list[bar].gage.text = "max"
                        self.config_list[bar].gage.color = COLOR('ORANGE')
                    else:
                        self.config_list[bar].gage.text = str(vol_scan[bar])[-1]

                    self.config.update()
                    self.config.draw(self.screen)

            if create:
                for row in range(len(self.keyboard_list)):
                    for self.keyboard, index in zip(self.keyboard_list[row], range(len(self.keyboard_list[row]))):
                        if self.keyboard != self.keyboard_list[row_key][column_key]:
                            self.keyboard.select_effect(False)
                            if self.keyboard != self.keyboard_list[-1][-1]:
                                self.keyboard.trigger = False

                        if self.keyboard_list[-1][-1].trigger:
                            self.keyboard.text = self.keyboard.text.upper()
                            self.keyboard_list[-1][-3].text = "_"
                            self.keyboard_list[-1][-1].select_effect(True)
                        else:
                            self.keyboard.text = self.keyboard.text.lower()
                            self.keyboard_list[-1][-3].text = "-"

                        self.keyboard.update()
                        self.keyboard.draw(self.screen)

            self.board.update()
            self.board.draw(self.screen)

            # Limit delay without event activity
            if self.menu_timer.countdown(1, True):
                scene_browser = -1
                run = False

            # Update screen
            pygame.display.update()

        return username, scene_browser


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

        self.sfx_list = [self.portal_loop_fx, self.select_loop_fx, self.select_fx, self.confirm_fx, self.start_fx]

        # Create menu timer
        self.menu_timer = Timer(FPS)

    def main_loop(self, username):
        username_data = self.db.read_data(username)[0]
        style     = username_data[1]
        model     = username_data[2]
        level     = username_data[3]
        highlevel = username_data[4]

        music     = username_data[7]
        sound     = username_data[8]
        pygame.mixer.music.set_volume(music)
        for sfx in self.sfx_list:
            sfx.set_volume(sound)

        confirm   = False

        vol = self.music_vol()

        scene_browser = 1
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
                            scene_browser = -1
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
                        if self.music_vol() < 1.0: # Turn up the volume
                            vol = self.music_vol(+ 0.1)
                            pygame.mixer.music.set_volume(vol)
                            self.select_fx.play()

                    if event.key == pygame.K_DOWN:
                        if self.music_vol() > 0.0: # Turn down the volume
                            vol = self.music_vol(- 0.1)
                            pygame.mixer.music.set_volume(vol)
                            self.select_fx.play()

                    if event.key == pygame.K_ESCAPE: # Quit game
                        scene_browser = -1
                        run = False

                # keyboard release
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT: # Back select
                        if not confirm:
                            if style > 0:
                                style -= 1
                            else: style = 2
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
                            if style < 2:
                                style += 1
                            else: style = 0
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

            # self.portal.update()
            # self.portal.draw()
            self.screen.blit(self.statue, (0, SCREEN_HEIGHT//4))

            self.symbol.draw()
            if not confirm:
                self.symbol.update(style, model)
            else:
                self.spaceship.update(style, model)
                self.spaceship.draw()

            # Limit delay without event activity
            if self.menu_timer.countdown(1, True):
                scene_browser = -1
                run = False

            # Update screen
            pygame.display.update()

        self.load_select(username, style, model, level)
        return username, scene_browser


class Game(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        # Create screen fades
        self.intro_fade = Screen_fade(self.screen, 'intro', COLOR('BLACK'), 4)
        self.death_fade = Screen_fade(self.screen, 'death', COLOR('BLACK'), 4)

        self.ammo_load_view = Canvas(topleft =(SCREEN_WIDTH//30, SCREEN_HEIGHT*0.065), color=COLOR('YELLOW'))
        self.username_view  = Canvas(center  =(SCREEN_WIDTH//2,  SCREEN_HEIGHT*0.02), color=COLOR('LIME'))
        self.level_view     = Canvas(center  =(SCREEN_WIDTH//2,  SCREEN_HEIGHT*0.05), color=COLOR('PINK'))
        self.timer_view     = Canvas(center  =(SCREEN_WIDTH//2,  SCREEN_HEIGHT*0.08), letter=1, size=20)
        self.highscore_view = Canvas(topright=(SCREEN_WIDTH-SCREEN_WIDTH//30, SCREEN_HEIGHT*0.015), color=COLOR('ORANGE'))
        self.score_view     = Canvas(topright=(SCREEN_WIDTH-SCREEN_WIDTH//30, SCREEN_HEIGHT*0.055), color=COLOR('CYAN'))

        self.paused         = Canvas(center  =(SCREEN_WIDTH//2, SCREEN_HEIGHT//3), letter=0, size=60, color=COLOR('RED'))
        self.space          = Canvas(center  =(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), letter=0, size=20, color=COLOR('LIME'))

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
        self.settings.add(self.paused)

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

        self.enemy_sfx_list = [self.empty_ammo_fx, self.bullet_fx, self.empty_load_fx, self.missile_fx, self.missile_cd_fx, self.missile_exp_fx]
        self.sfx_list       = [self.move_fx, self.backmove_fx, self.turbo_fx, self.explosion_fx, self.pause_fx, self.select_fx, self.win_fx, self.game_over_fx]
        self.sfx_list.extend(self.enemy_sfx_list)

    # Function to reset level
    def reset_level(self):
        self.bullet_group.empty()
        self.missile_group.empty()
        self.explosion_group.empty()
        self.enemy_group.empty()
        self.meteor_group.empty()
        self.meteor_list = self.meteor_list_copy

    def environment_create(self, init_planet):
        bg = Background(bg_img)
        fg  = Farground(STARS)
        origin_planet  = Planet('origin' , init_planet, midbottom=(SCREEN_WIDTH//2, SCREEN_HEIGHT))
        destiny_planet = Planet('destiny', init_planet, midbottom=(SCREEN_WIDTH//2, 0))

        self.environment_list = [bg, fg, origin_planet, destiny_planet]

    def enemy_create(self, level):
        enemy_select = random.randint(0, 2)
        self.enemy_list = []
        temp_list = []
        for i in range(level):
            temp_list.append(Enemy(self.screen, enemy_select, level+1, self.player, [self.group_list, self.enemy_sfx_list], center=(enemy_position(enemy_select, i))))
        self.enemy_list.append(temp_list)
        self.enemy_group.add(self.enemy_list[0])

    def meteor_surge(self, level, surge_num):
        self.surge_start = self.surge_end = False
        self.surge_index = 0

        self.meteor_list = []
        for number in range(surge_num):
            temp_list = []
            # Increase the number of meteors per surge
            for _ in range((number + level) * 100 // 4):
                temp_list.append(Meteor(self.screen, self.player))

            self.meteor_list.append(temp_list)

    def process_data(self, username, level, score, lives, init_planet):
        self.load_data(username, level, score)
        username_data = self.db.read_data(username)[0]
        style = username_data[1]
        model = username_data[2]
        level = username_data[3]

        # Create sprites
        self.player = Player(self.screen, style, model, score, SPEED, level*100, level, lives, self.group_list)
        self.environment_create(init_planet)
        self.lives_view = pygame.image.load(lives_img).convert_alpha()
        self.health_bar = HealthBar(self.screen, self.player.health, self.player.max_health)
        self.enemy_create(level)
        self.meteor_surge(level, SURGE_NUM)
        self.meteor_list_copy = self.meteor_list.copy()

        # Create game timer
        self.game_timer = Timer(FPS)

        return username_data

    def config_buttons(self):
        self.config_list = []
        margin_y = SCREEN_HEIGHT//2

        for bar in range(len(bar_list)):
            self.config_list.append(Bar(bar_list[bar], center=(SCREEN_WIDTH//1.8, bar * SCREEN_HEIGHT//10 + margin_y)))

    def main_loop(self, username):
        self.reset_level()
        level = 1
        score = 0
        lives = LIVES
        init_planet = random.randint(1, 9)

        username_data = self.process_data(username, level, score, lives, init_planet)
        username  = username_data[0]
        highscore = username_data[6]

        music     = username_data[7]
        sound     = username_data[8]
        pygame.mixer.music.set_volume(music)
        for sfx in self.sfx_list:
            sfx.set_volume(sound)

        bar = 0
        vol_scan = [music, sound]
        self.config_buttons()
        self.config_list[bar].gage.select_effect(True)

        pause = False
        restart = False
        death = False

        shoot = False
        shoot_bullets = False
        throw = False
        throw_missiles = False

        scene_browser = 1
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
                        if pause and self.config_list[bar].gage == self.config_list[0].gage:
                            if self.music_vol() > 0.0: # Turn down the volume
                                vol_scan[0] = self.music_vol(- 0.1)
                                pygame.mixer.music.set_volume(vol_scan[0])
                                self.config_list[bar].gage.rect.x -= 22

                            elif self.config_list[bar].gage == self.config_list[1].gage:
                                if self.sound_vol(self.sfx_list[0]) > 0.0: # Turn down the sound
                                    for sfx in self.sfx_list:
                                        vol_scan[1] = self.sound_vol(sfx, - 0.1)
                                        sfx.set_volume(vol_scan[1])
                                    self.config_list[bar].gage.rect.x -= 22

                        elif not self.player.win:
                            self.player.moving_left = True # Moving left
                            self.move_fx.play()

                    if event.key == pygame.K_RIGHT:
                        if pause and self.config_list[bar].gage == self.config_list[0].gage:
                            if self.music_vol() < 1.0: # Turn up the volume
                                vol_scan[0] = self.music_vol(+ 0.1)
                                pygame.mixer.music.set_volume(vol_scan[0])
                                self.config_list[bar].gage.rect.x += 22

                            elif self.config_list[bar].gage == self.config_list[1].gage:
                                if self.sound_vol(self.sfx_list[0]) < 1.0: # Turn up the sound
                                    for sfx in self.sfx_list:
                                        vol_scan[1] = self.sound_vol(sfx, + 0.1)
                                        sfx.set_volume(vol_scan[1])
                                    self.config_list[bar].gage.rect.x += 22

                        elif not self.player.win:
                            self.player.moving_right = True # Moving right
                            self.move_fx.play()

                    if event.key == pygame.K_UP:
                        if pause:
                            if bar > 0:
                                bar -= 1
                            else: bar = len(self.config_list) - 1
                            self.select_fx.play()
                        elif not self.player.win:
                            self.player.moving_up = True # Moving up
                            self.move_fx.play()

                    if event.key == pygame.K_DOWN:
                        if pause:
                            if bar < len(self.config_list) - 1:
                                bar += 1
                            else: bar = 0
                            self.select_fx.play()
                        elif not self.player.win:
                            self.player.moving_down = True # Moving down
                            self.move_fx.play()

                    if event.key == pygame.K_SPACE: # Turbo
                        if self.player.alive and not self.player.spawn and not self.player.win:
                            self.player.turbo = True
                            self.turbo_fx.play()
                        else: restart = True
                    if event.key == pygame.K_r: # Shoot bullets
                        if not self.player.win: shoot = True
                    if event.key == pygame.K_e: # Throw missiles
                        if not self.player.win: throw = True

                    if event.key == pygame.K_RETURN: # Pause and Settings
                        if not pause:
                            pause = True
                        else:
                            self.load_volume(username, vol_scan[0], vol_scan[1])
                            pause = False

                        self.pause_fx.play()

                    if event.key == pygame.K_ESCAPE: # Exit game
                        scene_browser = -1
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

            if pause: # Pause and volume control
                self.paused.text = "P A U S E"

                self.settings.update()
                self.settings.draw(self.screen)

                for self.config in self.config_list:
                    if self.config == self.config_list[bar]:
                        self.config.gage.select_effect(True)
                        self.config.color      = COLOR('YELLOW')
                        self.config.gage.color = COLOR('YELLOW')
                        self.config_list[bar].gage.active_effect(True)
                    else:
                        self.config.gage.select_effect(False)
                        self.config.color      = COLOR('WHITE')
                        self.config.gage.color = COLOR('WHITE')
                        self.config_list[bar].gage.active_effect(False)

                    if vol_scan[bar] == 0.0:
                        self.config_list[bar].gage.text = "min"
                        self.config_list[bar].gage.color = COLOR('ORANGE')
                    elif vol_scan[bar] == 1.0:
                        self.config_list[bar].gage.text = "max"
                        self.config_list[bar].gage.color = COLOR('ORANGE')
                    else:
                        self.config_list[bar].gage.text = str(vol_scan[bar])[-1]

                    self.config.update()
                    self.config.draw(self.screen)

            else:
                # Update the time of the next surge of meteors
                if not self.surge_start and self.game_timer.delay(level * 60 // 4 * (self.surge_index + 1), True):
                    self.surge_start = True

                elif self.surge_start and not self.surge_end:
                    # Add the next surge when the previous surge ends
                    if len(self.meteor_group) == 0:
                        if self.surge_index < len(self.meteor_list):
                            self.meteor_group.add(self.meteor_list[self.surge_index])
                            self.surge_index += 1
                            self.surge_start = False
                            self.enemy.retired = True
                            self.music(4, 0.5)
                        else:
                            self.surge_end = True
                            self.enemy.retired = False
                            self.music(2, 0.5)

                for self.environment in self.environment_list:
                    self.environment.update(self.player.delta_x, self.player.turbo, self.player.win)
                    self.environment.draw(self.screen)

                # self.player.check_collision()
                self.player.update()
                self.player.draw()

                for self.meteor in self.meteor_group:
                    self.meteor.check_collision(self.explosion_fx)
                    self.meteor.update(self.player.turbo)
                    self.meteor.draw()

                for self.enemy in self.enemy_group:
                    if not self.player.spawn:
                        self.enemy.check_collision(self.explosion_fx)
                        self.enemy.update()
                        self.enemy.draw()

                for bullet in self.bullet_group:
                    bullet.update()
                    bullet.draw()

                # self.bullet_group.update()
                self.missile_group.update()
                self.explosion_group.update()

                # self.bullet_group.draw(self.screen)
                self.missile_group.draw(self.screen)
                self.explosion_group.draw(self.screen)

                if self.player.alive:
                    if self.player.spawn and self.intro_fade.fade():
                        self.intro_fade.fade_counter = 0
                        self.player.spawn  = False

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
                        self.player.turbo = False
                        self.player.speed = 1
                        self.win_fx.play()

                    # Check if player has completed the level
                    elif self.player.win and self.player.auto_movement():
                        level += 1
                        self.reset_level()
                        init_planet = self.environment.destiny_planet
                        username_data = self.process_data(username, level, self.player.score, lives, init_planet)
                        # highscore = username_data[6]
                else:
                    if not death:
                        death = True
                        self.game_over_fx.play()

                    # Restart the level if the player has lost
                    elif death and self.death_fade.fade():
                        if restart:
                            self.death_fade.fade_counter = 0
                            if lives > 0:
                                lives -= 1
                                self.reset_level()
                                init_planet = self.environment.origin_planet
                                username_data = self.process_data(username, level, self.player.score, lives, init_planet)
                                highscore = username_data[6]
                                self.player.score = 0
                                self.player.alive = True
                                death = False
                                restart = False
                            else: run = False

                # Zone for user interface bar
                pygame.draw.rect(self.screen, COLOR('ARCADE'), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT//10))
                pygame.draw.line(self.screen, COLOR('SILVER'), (0, SCREEN_HEIGHT//10), (SCREEN_WIDTH, SCREEN_HEIGHT//10), 4)

                # Show player health
                self.health_bar.draw(self.player.health)
                # Show player lives
                for x in range(self.player.lives):
                    self.screen.blit(self.lives_view, (x * SCREEN_WIDTH * 0.05, 0))

                self.ammo_load_view.text = f"ammo: {self.player.ammo} | load: {self.player.load}"
                self.username_view.text  = f"- {username} -"
                self.level_view.text     = f"Level - {level} -"
                self.timer_view.text     = f"Time: {self.game_timer.text_time}"
                self.score_view.text     = f"Score: {self.player.score}"
                if self.player.score > highscore:
                    self.highscore_view.text  = "New Highscore"
                    self.highscore_view.color = COLOR('RED')
                else:
                    self.highscore_view.text  = f"Highscore: {highscore}"
                    self.highscore_view.color = COLOR('ORANGE')

                if death and not restart:
                    self.space.text = "press <SPACE> to continue"
                    self.space.update()
                    self.space.draw(self.screen)

                self.ui_bar.update()
                self.ui_bar.draw(self.screen)

            # Update screen
            pygame.display.update()

        self.load_data(username, level, self.player.score)
        return username, scene_browser


class Record(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.game_over_logo = pygame.image.load(game_over_img).convert_alpha()
        self.logo_x = (SCREEN_WIDTH - LOGO) // 2
        self.logo_y = SCREEN_HEIGHT

        self.text_score    = Canvas(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3),    letter=3, size=24)
        self.text_continue = Canvas(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//1.7),  letter=2, size=44, color=COLOR('GREEN'))
        self.text_replay   = Canvas(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//1.5),  letter=2, size=40, color=COLOR('YELLOW'))
        self.text_exit     = Canvas(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//1.22), letter=2, size=34, color=COLOR('RED'))

        self.text_continue.text = "Press <SPC> to Continue"
        self.text_replay.text   = "Press <ENTER> to Menu"
        self.text_exit.text     = "Press <ESC> to Exit"

        self.text_group = pygame.sprite.Group()
        self.text_group.add(self.text_score, self.text_replay, self.text_continue, self.text_exit)

        # Create record timer
        self.record_timer = Timer(FPS)

    def reset_ranking(self):
        top_ranking = self.db.read_data('HIGHSCORE', -1)

        self.ranking_list = []
        margin_y = SCREEN_HEIGHT//3

        for user in range(len(top_ranking)):
            temp_var = Canvas(midbottom=(SCREEN_WIDTH//2, user * -SCREEN_HEIGHT//20 + margin_y), letter=1, size=20, color=COLOR('BLACK'))
            temp_var.text = f"Ranking {len(top_ranking)-user}: {top_ranking[user][0]} -> {top_ranking[user][6]}"
            self.ranking_list.append(temp_var)

    def main_loop(self, username):
        if username != '':
            username_data = self.db.read_data(username)[0]
            new_highscore = self.load_data(username, username_data[3], username_data[5])
            self.text_continue.text = "Press <SPC> to Continue"
        else:
            new_highscore = False
            self.text_continue.text = ""

        self.reset_ranking()

        scene_browser = 1
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
                        if username != '':
                            scene_browser = -1
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
                    if self.ranking_list[-1].rect.y < SCREEN_HEIGHT//2.6:
                        ranking.delta_y += 0.2
                    if ranking.rect.y > SCREEN_HEIGHT//3 and ranking.rect.y < SCREEN_HEIGHT//2:
                        if ranking.fade < 255: ranking.fade += 1
                    elif ranking.fade > 0: ranking.fade -= 1

                    ranking.color = ([ranking.fade]*3)
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

        return username, scene_browser
