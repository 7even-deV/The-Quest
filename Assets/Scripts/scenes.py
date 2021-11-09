import pygame, sys, random

from .settings    import FPS, MUSIC_VOL, SOUND_VOL, LOGO, COLOR, STARS, LIVES, SURGE_NUM, enemy_select, enemy_position
from .documents   import CREDITS, HISTORY, GUIDE
from .manager     import msg_dict, button_list, bar_list, keyboard_list, statue_img, bg_img, lives_img, load_music, load_sound, record_btn_list
from .tools       import Timer, Logo, Button, Bar, Keyboard, Board, View, Canvas, Icon, HealthBar, Screen_fade
from .environment import Foreground, Background, Farground, Planet, Portal
from .players     import Player
from .enemies     import Enemy
from .obstacles   import Meteor
from .items       import Item
from .database    import Database


class Scene():
    # Create class variable to use the same instance in each scene
    db = Database()

    def __init__(self, screen):
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.fullscreen = False

        self.screen = screen # Parameterize the screen for all scenes
        self.clock  = pygame.time.Clock() # Manage screen refresh rate

        self.db = Database()

        self.timer_list = []
        for _ in range(2): # Create timer list
            self.timer_list.append(Timer(FPS))

    def load_username(self, username):
        read_data_list = self.db.read_data()

        # Read the new table if it was deleted
        if read_data_list == []:
            read_data_list = self.db.read_data()

            # Create the default data if it was deleted
            if read_data_list == []:
                self.db.create_data(username)
                read_data_list = self.db.read_data()

        username_list  = ["New User"]
        for user in read_data_list:
            username_list.append(user[0])

        return username_list

    def load_select(self, username, style, model, level):
        self.db.update_data(username, STYLE=style)
        self.db.update_data(username, MODEL=model)
        self.db.update_data(username, LEVEL=level)

    def load_size(self, username, screen_w, screen_h):
        self.db.update_data(username, SCREEN_W=screen_w)
        self.db.update_data(username, SCREEN_H=screen_h)

    def load_volume(self, username, music, sound):
        self.db.update_data(username, MUSIC=music)
        self.db.update_data(username, SOUND=sound)

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

    def music(self, index, volume=MUSIC_VOL):
        pygame.mixer.music.load(load_music(index))
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1, 0.0, 1000)

    def sound(self, sfx, volume=SOUND_VOL):
        fx = pygame.mixer.Sound(load_sound(sfx))
        fx.set_volume(volume)
        return fx

    def volume(self, mixer, vol=0):
        return round(mixer.get_volume() + vol, 1)


class Main(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        # Sounds fx
        self.select_loop_fx = self.sound('select_loop')
        self.select_fx      = self.sound('select')
        self.confirm_fx     = self.sound('confirm')
        self.start_fx       = self.sound('start')

        self.sfx_list = [self.select_loop_fx, self.select_fx, self.confirm_fx, self.start_fx]

    def command_buttons(self, SCREEN_W, SCREEN_H):
        self.command_list = []
        margin_y = SCREEN_H//2

        for btn in range(len(button_list)):
            temp_var = Button(button_list[0][btn], center=(SCREEN_W//2, btn * SCREEN_H//8 + margin_y))
            if btn % 2 == 0:
                temp_var.flip_x = True
            self.command_list.append(temp_var)

        self.command_list[0].select_effect(True)

    def config_buttons(self, SCREEN_W, SCREEN_H):
        self.config_list = []
        margin_y = SCREEN_H//5

        for bar in range(len(bar_list)):
            self.config_list.append(Bar(bar_list[bar], center=(SCREEN_W//1.8, bar * SCREEN_H//10 + margin_y)))

        self.config_list[0].gage.active_effect(True)

    def keyboard_buttons(self, SCREEN_W, SCREEN_H):
        self.keyboard_list = []
        margin_x = SCREEN_W//10.75
        margin_y = SCREEN_H//7.75

        for row in range(len(keyboard_list)):
            temp_list = []
            for column in range(len(keyboard_list[row])):
                temp_list.append(Keyboard(keyboard_list[row][column], center=(column * SCREEN_W//11 + margin_x, row * SCREEN_H//15 + margin_y)))
            self.keyboard_list.append(temp_list)

        self.keyboard_list[0][0].select_effect(True)

    def reset(self, SCREEN_W, SCREEN_H):
        self.message = View(self.screen, center=(SCREEN_W//2, SCREEN_H//2.5), letter=2, size=20)
        self.board   = Board(midbottom=(SCREEN_W//2, 0))

        self.command_buttons(SCREEN_W, SCREEN_H)
        self.config_buttons(SCREEN_W, SCREEN_H)
        self.keyboard_buttons(SCREEN_W, SCREEN_H)

    def main_loop(self, username, play):
        username_list = self.load_username(username)
        user = -1
        username_data = self.db.read_data(username_list[user])[0]

        username = username_data[0]
        music    = username_data[7]
        sound    = username_data[8]
        SCREEN_W = username_data[9]
        SCREEN_H = username_data[10]

        vol_scan = [music, sound]
        pygame.mixer.music.set_volume(music)
        for sfx in self.sfx_list:
            sfx.set_volume(sound)

        self.reset(SCREEN_W, SCREEN_H)

        empty = False
        if 'empty' in username_list:
            username_list.remove('empty')
            empty = True
        button_list[1][0] = username_list

        cursor = bar = row_key = column_key = select = 0
        login = create = confirm = False
        str_key   = ''
        press_key = False
        msg = 0

        self.timer_list[0].frame_num = 0
        scene_browser = 1
        run = True
        while run:
            # Limit frames per second
            self.clock.tick(FPS)

            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Video resize
                if event.type == pygame.VIDEORESIZE:
                    if not self.fullscreen:
                        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                        self.load_size(username, event.w, event.h)
                        scene_browser = 0
                        run = False

                # Keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()), pygame.RESIZABLE)

                    if event.key == pygame.K_LEFT: # Back select
                        if not create:
                            if login: # Account select
                                if user > 0:
                                    user -= 1
                                else: user = len(username_list) - 1

                            elif self.command_list[1].trigger:
                                if self.config_list[bar].gage == self.config_list[0].gage:
                                    if self.volume(pygame.mixer.music) > 0.0: # Turn down the volume
                                        vol_scan[0] = self.volume(pygame.mixer.music, - 0.1)
                                        pygame.mixer.music.set_volume(vol_scan[0])

                                elif self.config_list[bar].gage == self.config_list[1].gage:
                                    if self.volume(self.sfx_list[0]) > 0.0: # Turn down the sound
                                        for sfx in self.sfx_list:
                                            vol_scan[1] = self.volume(sfx, - 0.1)
                                            sfx.set_volume(vol_scan[1])
                        else:
                            if column_key > 0:
                                column_key -= 1
                            else: column_key = len(self.keyboard_list[row_key]) - 1

                        self.select_fx.play()

                    if event.key == pygame.K_RIGHT: # Next select
                        if not create:
                            if login: # Account select
                                if user < len(username_list) - 1:
                                    user += 1
                                else: user = 0

                            elif self.command_list[1].trigger:
                                if self.config_list[bar].gage == self.config_list[0].gage:
                                    if self.volume(pygame.mixer.music) < 1.0: # Turn up the volume
                                        vol_scan[0] = self.volume(pygame.mixer.music, + 0.1)
                                        pygame.mixer.music.set_volume(vol_scan[0])

                                elif self.config_list[bar].gage == self.config_list[1].gage:
                                    if self.volume(self.sfx_list[0]) < 1.0: # Turn up the sound
                                        for sfx in self.sfx_list:
                                            vol_scan[1] = self.volume(sfx, + 0.1)
                                            sfx.set_volume(vol_scan[1])
                        else:
                            if column_key < len(self.keyboard_list[row_key]) - 1:
                                column_key += 1
                            else: column_key = 0

                        self.select_fx.play()

                    if event.key == pygame.K_UP: # Up select
                        if not create:
                            if not login and self.command_list[1].trigger:
                                if bar > 0:
                                    bar -= 1
                                else: bar = len(self.config_list) - 1
                                self.config_list[bar].gage.active_effect(True)

                            else:
                                if cursor > 0:
                                    cursor -= 1
                                else: cursor = len(self.command_list) - 1
                                self.command_list[cursor].select_effect(True)
                        else:
                            if row_key > 0:
                                row_key -= 1
                            else: row_key = len(self.keyboard_list) - 1

                        self.board.show = False
                        self.select_fx.play()

                    if event.key == pygame.K_DOWN: # Down select
                        if not create:
                            if not login and self.command_list[1].trigger:
                                if bar < len(self.config_list) - 1:
                                    bar += 1
                                else: bar = 0
                                self.config_list[bar].gage.active_effect(True)

                            else:
                                if cursor < len(self.command_list) - 1:
                                    cursor += 1
                                else: cursor = 0
                                self.command_list[cursor].select_effect(True)
                        else:
                            if row_key < len(self.keyboard_list) - 1:
                                row_key += 1
                            else: row_key = 0

                        self.board.show = False
                        self.select_fx.play()

                    # Select the effect of the key that is pressed
                    if create: self.keyboard_list[row_key][column_key].select_effect(True)

                    if event.key == pygame.K_SPACE: # Turnback select
                        if create:
                            if len(username) < 10:
                                # These 2 conditions are for not typing if the Delete key or the Shift key is pressed.
                                if  self.keyboard_list[row_key][column_key] != self.keyboard_list[-1][-1]\
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
                        pygame.quit()
                        sys.exit()

                    self.timer_list[0].frame_num = 0

                # keyboard text input
                if create and event.type == pygame.TEXTINPUT:
                    if str_key != str(event)[31]:
                        str_key = str(event)[31]
                        press_key = True

                    if str(event)[31] != ' ':
                        if len(username) < 10:
                            username += str_key
                            button_list[2][0] = username
                        else: msg = 2
                        self.confirm_fx.play()

                    else: msg = 0

                # keyboard release
                if event.type == pygame.KEYUP:
                    # Turns off the effect of the key that is release
                    if create and self.keyboard_list[row_key][column_key].trigger:
                        self.keyboard_list[row_key][column_key].trigger = False
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
                                                if empty: self.db.delete_data('empty')
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
                                        self.board.create_textline(GUIDE, midleft=(self.board.rect.width//3, self.board.rect.top))
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
            # pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.screen.get_width() - 5 - (self.screen.get_width() / 5), 50, self.screen.get_width() / 5, 50))

            ''' --- AREA TO UPDATE AND DRAW --- '''

            self.message.text = msg_dict[msg]
            self.message.update()
            self.message.draw()

            if  confirm: select = 3
            elif create: select = 2
            elif  login: select = 1
            else:        select = 0

            for self.command, index in zip(self.command_list, range(len(self.command_list))):
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
                    self.config_list[bar].gage.trigger = True
                    if self.config != self.config_list[bar] and self.config.gage.trigger:
                        self.config.gage.active_effect(False)
                        self.config.gage.trigger = False

                    self.config_list[0].displace_effect(vol_scan[0])
                    self.config_list[1].displace_effect(vol_scan[1])

                    self.config.update()
                    self.config.draw(self.screen)

            if create:
                for row in range(len(self.keyboard_list)):
                    for self.keyboard, index in zip(self.keyboard_list[row], range(len(self.keyboard_list[row]))):

                        if self.keyboard != self.keyboard_list[row_key][column_key]:
                            self.keyboard.select_effect(False)
                            if self.keyboard != self.keyboard_list[-1][-1]:
                                if  self.keyboard.trigger:
                                    self.keyboard.trigger = False
                                    self.keyboard.active_effect(False)

                        if press_key:
                            if self.keyboard_list[row][index].text == str_key\
                            or self.keyboard_list[row][index].text.upper() == str_key:
                                row_key = row
                                column_key = index
                                self.keyboard.trigger = True
                                self.keyboard.select_effect(True)
                                self.keyboard.active_effect(True)
                                press_key = False

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
            if self.timer_list[0].countdown(1, True):
                scene_browser = -1
                run = False

            # Update screen
            pygame.display.update()

        return username, play, scene_browser


class Menu(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        # Sounds fx
        self.portal_loop_fx = self.sound('portal_loop')
        self.select_loop_fx = self.sound('select_loop')
        self.select_fx      = self.sound('select')
        self.confirm_fx     = self.sound('confirm')
        self.start_fx       = self.sound('start')

        self.sfx_list = [self.portal_loop_fx, self.select_loop_fx, self.select_fx, self.confirm_fx, self.start_fx]

    def reset(self, SCREEN_W, SCREEN_H):
        self.statue    = pygame.image.load(statue_img).convert_alpha()
        self.bg_rect   = self.statue.get_rect(midbottom=(SCREEN_W//2, SCREEN_H))
        self.spaceship = Icon(self.screen, 'spaceships', 4, center=(self.bg_rect.centerx, self.bg_rect.centery//1.55))
        self.symbol    = Icon(self.screen, 'symbol', 1.5, center=(self.bg_rect.centerx*1.08, self.bg_rect.centery*1.15))
        self.portal = Portal(self.screen, center=(SCREEN_W//2, SCREEN_H//2.5))

    def main_loop(self, username, play):
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

        SCREEN_W  = username_data[9]
        SCREEN_H  = username_data[10]
        self.reset(SCREEN_W, SCREEN_H)

        confirm   = False

        self.timer_list[0].frame_num = 0
        scene_browser = 1
        run = True
        while run:
            # Limit frames per second
            self.clock.tick(FPS)

            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Video resize
                if event.type == pygame.VIDEORESIZE:
                    if not self.fullscreen:
                        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                        self.load_size(username, event.w, event.h)
                        scene_browser = 0
                        run = False

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
                        if self.volume(pygame.mixer.music) < 1.0: # Turn up the volume
                            vol = self.volume(pygame.mixer.music, + 0.1)
                            pygame.mixer.music.set_volume(vol)
                            self.select_fx.play()

                    if event.key == pygame.K_DOWN:
                        if self.volume(pygame.mixer.music) > 0.0: # Turn down the volume
                            vol = self.volume(pygame.mixer.music, - 0.1)
                            pygame.mixer.music.set_volume(vol)
                            self.select_fx.play()

                    if event.key == pygame.K_ESCAPE: # Quit game
                        scene_browser = -1
                        run = False

                    self.timer_list[0].frame_num = 0

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
            self.screen.blit(self.statue, self.bg_rect)

            self.symbol.draw()
            if not confirm:
                self.symbol.update(style, model)
            else:
                self.spaceship.update(style, model)
                self.spaceship.draw()

            # Limit delay without event activity
            if self.timer_list[0].countdown(1, True):
                scene_browser = -1
                run = False

            # Update screen
            pygame.display.update()

        self.load_select(username, style, model, level)
        return username, play, scene_browser


class Game(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.bullet_group    = pygame.sprite.Group()
        self.missile_group   = pygame.sprite.Group()
        self.enemy_group     = pygame.sprite.Group()
        self.meteor_group    = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.item_group      = pygame.sprite.Group()

        self.canvas_group    = pygame.sprite.Group()
        self.settings        = pygame.sprite.Group()

        self.meteor_list_copy = []
        self.group_list = [self.bullet_group, self.missile_group, self.enemy_group, self.meteor_group, self.explosion_group, self.item_group]

        # Sounds fx
        self.move_fx         = self.sound('move')
        self.backmove_fx     = self.sound('backmove')
        self.turbo_fx        = self.sound('turbo')
        self.explosion_fx    = self.sound('explosion')

        self.bullet_fx       = self.sound('bullet')
        self.empty_ammo_fx   = self.sound('empty_ammo')
        self.missile_fx      = self.sound('missile')
        self.missile_cd_fx   = self.sound('missile_countdown')
        self.missile_exp_fx  = self.sound('missile_explosion')
        self.empty_load_fx   = self.sound('empty_load')
        self.item_standby_fx = self.sound('item_standby')
        self.item_get_fx     = self.sound('item_get')

        self.pause_fx        = self.sound('pause')
        self.select_fx       = self.sound('select')
        self.win_fx          = self.sound('win')
        self.game_over_fx    = self.sound('game_over')

        self.enemy_sfx_list  = [self.empty_ammo_fx, self.bullet_fx, self.empty_load_fx, self.missile_fx, self.missile_cd_fx, self.missile_exp_fx, self.item_standby_fx, self.item_get_fx]
        self.sfx_list        = [self.move_fx, self.backmove_fx, self.turbo_fx, self.explosion_fx, self.pause_fx, self.select_fx, self.win_fx, self.game_over_fx]
        self.sfx_list.extend(self.enemy_sfx_list)

    def reset(self, SCREEN_W, SCREEN_H):
        self.intro_fade = Screen_fade(self.screen, 'intro', COLOR('BLACK'), 4, SCREEN_W, SCREEN_H)
        self.death_fade = Screen_fade(self.screen, 'death', COLOR('BLACK'), 4, SCREEN_W, SCREEN_H)

        self.lives_canvas   = Canvas(self.screen, 'lives',  1, 9, topleft=(SCREEN_W*0.01, SCREEN_H*0.04))
        self.load_canvas    = Canvas(self.screen, 'load',   4, 9, topleft=(SCREEN_W*0.07, SCREEN_H*0.04))
        self.ammo_canvas    = Canvas(self.screen, 'ammo',   1, 1, topleft=(SCREEN_W*0.13, SCREEN_H*0.05))
        self.weapon_canvas  = Canvas(self.screen, 'weapon', 1, 5, topleft=(SCREEN_W*0.19, SCREEN_H*0.047))
        self.turbo_canvas   = Canvas(self.screen, 'turbo',  8, 9, topleft=(SCREEN_W*0.24, SCREEN_H*0.04))
        self.speed_canvas   = Canvas(self.screen, 'speed',  4, 5, topleft=(SCREEN_W*0.30, SCREEN_H*0.045))
        self.username_view  = View(self.screen, center  =(SCREEN_W//2,  SCREEN_H*0.02),  color=COLOR('LIME'))
        self.level_view     = View(self.screen, center  =(SCREEN_W//2,  SCREEN_H*0.05),  color=COLOR('PINK'))
        self.timer_view     = View(self.screen, center  =(SCREEN_W//2,  SCREEN_H*0.08),  letter=1, size=20)
        self.highscore_view = View(self.screen, topright=(SCREEN_W-SCREEN_W//30, SCREEN_H*0.015), color=COLOR('ORANGE'))
        self.score_view     = View(self.screen, topright=(SCREEN_W-SCREEN_W//30, SCREEN_H*0.055), color=COLOR('CYAN'))

        self.paused         = View(self.screen, center  =(SCREEN_W//2, SCREEN_H//3), letter=0, size=60, color=COLOR('RED'))
        self.space          = View(self.screen, center  =(SCREEN_W//2, SCREEN_H//2), letter=0, size=20, color=COLOR('LIME'))

        self.canvas_group.empty()
        self.canvas_group.add(self.lives_canvas, self.load_canvas, self.ammo_canvas, self.weapon_canvas, self.turbo_canvas,\
        self.speed_canvas, self.username_view, self.level_view, self.timer_view, self.highscore_view, self.score_view)

        self.settings.empty()
        self.settings.add(self.paused)

    # Function to empty level
    def empty_level(self):
        self.bullet_group.empty()
        self.missile_group.empty()
        self.explosion_group.empty()
        self.item_group.empty()
        self.enemy_group.empty()
        self.meteor_group.empty()
        self.meteor_list = self.meteor_list_copy

    def environment_create(self, init_planet, SCREEN_W, SCREEN_H):
        background = Background(self.screen, SCREEN_W, SCREEN_H, bg_img)
        farground   = Farground(self.screen, SCREEN_W, SCREEN_H, STARS)
        origin_planet  = Planet(self.screen, 'origin' , init_planet, SCREEN_W, SCREEN_H, midbottom=(SCREEN_W//2, SCREEN_H))
        destiny_planet = Planet(self.screen, 'destiny', init_planet, SCREEN_W, SCREEN_H, midbottom=(SCREEN_W//2, 0))

        self.environment_list = [background, farground, origin_planet, destiny_planet]

    def item_create(self, player, SCREEN_W, SCREEN_H):
        self.item = Item(self.screen, player, [self.item_standby_fx, self.item_get_fx], bottomleft=(random.randint(0, SCREEN_W-SCREEN_W//10), 0))
        self.item_group.add(self.item)

    def enemy_create(self, level, SCREEN_W, SCREEN_H):
        self.enemy_index = 0

        self.enemy_list = []
        for group in range(level*10//2):
            select = random.randint(0, 2)
            temp_list = []
            for num in range(random.randint(1, level)):
                temp_list.append(Enemy(self.screen, select, 2+level*0.1, self.player, SCREEN_W, SCREEN_H, [self.group_list, self.enemy_sfx_list], center=(enemy_position(select, num))))

            self.enemy_list.append(temp_list)

    def meteor_surge(self, level, surge_num, SCREEN_W, SCREEN_H):
        self.surge_start = self.surge_end = False
        self.surge_index = 0

        self.meteor_list = []
        for number in range(surge_num):
            temp_list = []
            # Increase the number of meteors per surge
            for _ in range((number + level) * 100 // 4):
                temp_list.append(Meteor(self.screen, self.player, self.item_group, SCREEN_W, SCREEN_H, [self.item_standby_fx, self.item_get_fx]))

            self.meteor_list.append(temp_list)

    def process_data(self, username, level, score, lives, init_planet):
        self.empty_level()
        self.load_data(username, level, score)
        username_data = self.db.read_data(username)[0]
        style = username_data[1]
        model = username_data[2]
        level = username_data[3]

        SCREEN_W = username_data[9]
        SCREEN_H = username_data[10]
        self.reset(SCREEN_W, SCREEN_H)

        # Create sprites
        self.player = Player(self.screen, style, model, level*100, level, lives, score, SCREEN_W, SCREEN_H, self.group_list)
        # self.item_create(self.player)
        self.environment_create(init_planet, SCREEN_W, SCREEN_H)
        self.lives_view = pygame.image.load(lives_img).convert_alpha()
        self.health_bar = HealthBar(self.screen, self.player.max_health, SCREEN_W, SCREEN_H)
        self.enemy_create(level, SCREEN_W, SCREEN_H)
        self.meteor_surge(level, SURGE_NUM, SCREEN_W, SCREEN_H)
        self.meteor_list_copy = self.meteor_list.copy()
        self.timer_list[0].frame_num = 0

        return username_data

    def config_buttons(self, SCREEN_W, SCREEN_H):
        self.config_list = []
        margin_y = SCREEN_H//2

        for bar in range(len(bar_list)):
            self.config_list.append(Bar(bar_list[bar], center=(SCREEN_W//1.8, bar * SCREEN_H//10 + margin_y)))

        self.config_list[0].gage.active_effect(True)

    def main_loop(self, username, play):
        username_data = self.db.read_data(username)[0]
        username  = username_data[0]
        level     = username_data[3]
        highscore = username_data[6]
        music     = username_data[7]
        sound     = username_data[8]
        SCREEN_W  = username_data[9]
        SCREEN_H  = username_data[10]

        init_planet = random.randint(1, 9)

        self.process_data(username, level, 0, LIVES, init_planet)

        pygame.mixer.music.set_volume(music)
        for sfx in self.sfx_list:
            sfx.set_volume(sound)

        bar = 0
        vol_scan = [music, sound]
        self.config_buttons(SCREEN_W, SCREEN_H)

        pause = False
        restart = False
        death = False

        shoot = False
        shoot_bullets = False
        throw = False
        throw_missiles = False

        scene_browser = 1
        play = True
        run = True
        while run:
            # Limit frames per second
            self.clock.tick(FPS)

            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Video resize
                if event.type == pygame.VIDEORESIZE:
                    if not self.fullscreen:
                        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                        self.load_size(username, event.w, event.h)
                        scene_browser = 0
                        run = False

                # Keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if pause:
                            if self.config_list[bar].gage == self.config_list[0].gage:
                                if self.volume(pygame.mixer.music) > 0.0: # Turn down the volume
                                    vol_scan[0] = self.volume(pygame.mixer.music, - 0.1)
                                    pygame.mixer.music.set_volume(vol_scan[0])

                            elif self.config_list[bar].gage == self.config_list[1].gage:
                                if self.volume(self.sfx_list[0]) > 0.0: # Turn down the sound
                                    for sfx in self.sfx_list:
                                        vol_scan[1] = self.volume(sfx, - 0.1)
                                        sfx.set_volume(vol_scan[1])

                        elif not self.player.win:
                            self.player.moving_left = True # Moving left
                            self.move_fx.play()

                    if event.key == pygame.K_RIGHT:
                        if pause:
                            if self.config_list[bar].gage == self.config_list[0].gage:
                                if self.volume(pygame.mixer.music) < 1.0: # Turn up the volume
                                    vol_scan[0] = self.volume(pygame.mixer.music, + 0.1)
                                    pygame.mixer.music.set_volume(vol_scan[0])

                            elif self.config_list[bar].gage == self.config_list[1].gage:
                                if self.volume(self.sfx_list[0]) < 1.0: # Turn up the sound
                                    for sfx in self.sfx_list:
                                        vol_scan[1] = self.volume(sfx, + 0.1)
                                        sfx.set_volume(vol_scan[1])

                        elif not self.player.win:
                            self.player.moving_right = True # Moving right
                            self.move_fx.play()

                    if event.key == pygame.K_UP:
                        if pause:
                            if bar > 0:
                                bar -= 1
                            else: bar = len(self.config_list) - 1
                            self.config_list[bar].gage.active_effect(True)
                            self.select_fx.play()

                        elif not self.player.win:
                            self.player.moving_up = True # Moving up
                            self.move_fx.play()

                    if event.key == pygame.K_DOWN:
                        if pause:
                            if bar < len(self.config_list) - 1:
                                bar += 1
                            else: bar = 0
                            self.config_list[bar].gage.active_effect(True)
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
                        pause = not pause
                        if pause:
                            pygame.mixer.music.pause()
                            self.load_volume(username, vol_scan[0], vol_scan[1])
                        else:
                            pygame.mixer.music.unpause()

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
                    self.config_list[bar].gage.trigger = True
                    if self.config != self.config_list[bar] and self.config.gage.trigger:
                        self.config.gage.active_effect(False)
                        self.config.gage.trigger = False

                    self.config_list[0].displace_effect(vol_scan[0])
                    self.config_list[1].displace_effect(vol_scan[1])

                    self.config.update()
                    self.config.draw(self.screen)

            else:
                # Update the time of the next surge of meteors
                if not self.surge_start and self.timer_list[0].delay(level * 60 // 4 * (self.surge_index + 1), True):
                    self.surge_start = True

                elif self.surge_start and not self.surge_end:
                    # Add the next surge when the previous surge ends
                    if len(self.meteor_group) == 0:
                        if self.surge_index < len(self.meteor_list):
                            self.meteor_group.add(self.meteor_list[self.surge_index])
                            self.surge_index += 1
                            self.surge_start = False
                            self.enemy.retired = True
                            self.music(4, vol_scan[0])
                        else:
                            self.surge_end = True
                            self.enemy.retired = False
                            self.music(2, vol_scan[0])

                for self.environment in self.environment_list:
                    self.environment.update(self.player)
                    self.environment.draw()

                self.player.update()
                self.player.draw()

                for self.meteor in self.meteor_group:
                    self.meteor.check_collision(self.explosion_fx)
                    self.meteor.update(self.player.turbo)
                    self.meteor.draw()

                if not self.player.spawn and not self.player.win and len(self.meteor_group) == 0:
                    if self.timer_list[0].counter(10, True):
                        if self.enemy_index < len(self.enemy_list):
                            self.enemy_group.add(self.enemy_list[self.enemy_index])
                            self.enemy_index += 1

                for self.enemy in self.enemy_group:
                    self.enemy.check_collision(self.explosion_fx)
                    self.enemy.update()
                    self.enemy.draw()

                for bullet in self.bullet_group:
                    bullet.update()
                    bullet.draw()

                self.missile_group.update()
                self.missile_group.draw(self.screen)

                self.explosion_group.update()
                self.explosion_group.draw(self.screen)

                for item in self.item_group:
                    item.update()
                    item.draw()

                if self.player.alive:
                    if self.player.spawn and self.intro_fade.fade():
                        self.intro_fade.fade_counter = 0
                        self.player.spawn = False

                    # self.item_create(self.player)

                    if self.player.collide and self.timer_list[0].time(1, True):
                        self.player.collide = False

                    # Shoot bullets
                    # if shoot and not shoot_bullets:
                    if shoot:
                        self.player.shoot(self.empty_ammo_fx, self.bullet_fx)
                        shoot_bullets = True

                    # Throw missiles
                    if throw and not throw_missiles:
                        self.player.throw(self.empty_load_fx, self.missile_fx, self.missile_cd_fx, self.missile_exp_fx)
                        throw_missiles = True

                    # Level countdown
                    if not self.player.win and self.timer_list[0].level_timer(level, self.player, True):
                        self.timer_list[0].text_time = 0
                        self.player.win = True
                        self.win_fx.play()

                    # Check if player has completed the level
                    elif self.player.win:
                        if self.player.auto_movement() or self.player.auto_land and restart:
                            level += 1
                            init_planet = self.environment.destiny_planet
                            username_data = self.process_data(username, level, self.player.score, self.player.lives, init_planet)
                            highscore = username_data[6]
                            restart = False
                else:
                    if not death:
                        death = True
                        self.game_over_fx.play()

                    # Restart the level if the player has lost
                    elif death and self.death_fade.fade():
                        if restart:
                            self.death_fade.fade_counter = 0
                            self.player.lives -= 1
                            if self.player.lives > 0:
                                init_planet = self.environment.origin_planet
                                username_data = self.process_data(username, level, self.player.score, self.player.lives, init_planet)
                                highscore = username_data[6]
                                self.player.score = 0
                                self.player.alive = True
                                death = False
                                restart = False
                            else: run = False

                # Zone for user interface bar
                pygame.draw.rect(self.screen, COLOR('ARCADE'), (0, 0, SCREEN_W, SCREEN_H//10))
                pygame.draw.line(self.screen, COLOR('SILVER'), (0, SCREEN_H//10), (SCREEN_W, SCREEN_H//10), 4)

                # Show player health
                self.health_bar.view.text = str(username)
                self.health_bar.draw(self.player.health)
                # # Show player lives
                # for x in range(self.player.lives):
                #     self.screen.blit(self.lives_view, (x * SCREEN_W * 0.05, 0))

                self.lives_canvas.view.text  = str(self.player.lives)
                self.load_canvas.view.text   = str(self.player.load)
                self.ammo_canvas.view.text   = str(self.player.ammo)
                self.weapon_canvas.view.text = str(self.player.weapon_up)
                self.turbo_canvas.view.text  = str(self.player.turbo_up)
                self.speed_canvas.view.text  = str(self.player.max_speed)
                self.level_view.text     = f"Level - {level} -"
                self.timer_view.text     = f"Time: {self.timer_list[0].text_time}"
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
                    self.space.draw()

                for canvas in self.canvas_group:
                    canvas.update()
                    canvas.draw()

            # Update screen
            pygame.display.update()

        # *After* exiting the while loop, return data
        self.load_data(username, level, self.player.score)
        return username, play, scene_browser


class Record(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        # Sounds fx
        self.select_loop_fx = self.sound('select_loop')
        self.select_fx      = self.sound('select')
        self.confirm_fx     = self.sound('confirm')
        self.start_fx       = self.sound('start')

        self.sfx_list = [self.select_loop_fx, self.select_fx, self.confirm_fx, self.start_fx]

    def command_buttons(self, SCREEN_W, SCREEN_H):
        self.command_list = []
        margin_y = SCREEN_H//2

        for btn in range(len(record_btn_list)):
            temp_var = Button(record_btn_list[btn], center=(SCREEN_W//2, btn * SCREEN_H//8 + margin_y))
            if btn % 2 == 0:
                temp_var.flip_x = True
            self.command_list.append(temp_var)

        self.command_list[0].select_effect(True)

    def reset(self, SCREEN_W, SCREEN_H):
        self.game_over_logo = Logo(self.screen, midtop=(SCREEN_W//2, SCREEN_H*0.01))
        self.ranking_view   = View(self.screen, center=(SCREEN_W//2, SCREEN_H//8), letter=0, size=30)
        self.idle_time_view = View(self.screen, midbottom=(SCREEN_W//2, SCREEN_H-SCREEN_H*0.02), letter=2, size=20)

        self.update_ranking(SCREEN_W, SCREEN_H)
        self.command_buttons(SCREEN_W, SCREEN_H)

    def update_ranking(self, SCREEN_W, SCREEN_H):
        ranking_data = self.db.read_data('HIGHSCORE', -1)

        self.ranking_list = []
        margin_y = SCREEN_H//5

        if ranking_data[0][0] != 'empty':
            # Update the top ranking list of the users highscore
            for user in range(len(ranking_data)):
                temp_var = View(self.screen, midbottom=(SCREEN_W//2, user * -SCREEN_H//16 + margin_y), letter=3, size=30, color=COLOR('BLACK'))
                temp_var.text = f"Ranking {len(ranking_data)-user}: {ranking_data[user][0]} -> {ranking_data[user][6]}"
                self.ranking_list.append(temp_var)

    def main_loop(self, username, play):
        if not play or self.db.read_data() == []:
            username_data = self.db.read_data(self.load_username('empty')[-1])[0]
        else:
            username_data = self.db.read_data(username)[0]

        username = username_data[0]
        level    = username_data[3]
        score    = username_data[5]
        music    = username_data[7]
        sound    = username_data[8]
        SCREEN_W = username_data[9]
        SCREEN_H = username_data[10]

        pygame.mixer.music.set_volume(music)
        for sfx in self.sfx_list:
            sfx.set_volume(sound)
        vol_scan = [music, sound]

        new_highscore = self.load_data(username, level, score)
        self.reset(SCREEN_W, SCREEN_H)

        record_show = False
        cursor = 0

        self.timer_list[0].frame_num = 0
        scene_browser = 1
        run = True
        while run:
            # Limit frames per second
            self.clock.tick(FPS)

            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Video resize
                if event.type == pygame.VIDEORESIZE:
                    if not self.fullscreen:
                        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                        self.load_size(username, event.w, event.h)
                        scene_browser = 0
                        run = False

                # Keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: # Up select
                        if cursor > 0:
                            cursor -= 1
                        else: cursor = len(self.command_list) - 1
                        self.command_list[cursor].select_effect(True)

                        self.select_fx.play()

                    if event.key == pygame.K_DOWN: # Down select
                        if cursor < len(self.command_list) - 1:
                            cursor += 1
                        else: cursor = 0
                        self.command_list[cursor].select_effect(True)

                        self.select_fx.play()

                    if event.key == pygame.K_SPACE: # Restart game
                        run = False
                        self.confirm_fx.play()

                    if event.key == pygame.K_RETURN: # Confirm
                        self.command_list[cursor].trigger = True
                        self.command_list[cursor].active_effect(True)

                        self.confirm_fx.play()

                    if event.key == pygame.K_ESCAPE: # Quit game
                        pygame.quit()
                        sys.exit()

                    self.timer_list[0].frame_num = 0

                # keyboard release
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN: # Confirm
                        if self.command_list[0].trigger:
                            if play:
                                scene_browser = -1
                            run = False

                        if self.command_list[1].trigger:
                            scene_browser = 1
                            run = False

                        if self.command_list[2].trigger:
                            record_show = not record_show

                        if self.command_list[3].trigger:
                            pygame.quit()
                            sys.exit()

                        self.command_list[cursor].active_effect(False)

            # Clear screen and set background color
            self.screen.fill(COLOR('BLACK'))

            ''' --- AREA TO UPDATE AND DRAW --- '''

            if record_show or not play:

                for ranking in self.ranking_list:
                    if self.ranking_list[-1].rect.y < SCREEN_H//5.5:
                        ranking.delta_y += 0.2
                    if ranking.rect.y > SCREEN_H//6 and ranking.rect.y < SCREEN_H//3:
                        if ranking.fade < 255: ranking.fade += 1
                    elif ranking.fade > 0: ranking.fade -= 1

                    ranking.color = ([ranking.fade]*3)
                    ranking.update()
                    ranking.draw()

                if new_highscore:
                    self.ranking_view.text   = "NEW  HIGH  SCORE"
                else: self.ranking_view.text = "TOP  HIGH  SCORE"

                self.ranking_view.update()
                self.ranking_view.draw()

            else:
                self.game_over_logo.update()
                self.game_over_logo.draw()

            for self.command in self.command_list:
                if self.command != self.command_list[cursor]:
                    self.command.select_effect(False)
                    self.command.trigger = False

                self.command.update()
                self.command.draw(self.screen)

            # Limit delay without event activity
            if self.timer_list[0].countdown(1, True):
                pygame.quit()
                sys.exit()
            # Show the last 10 seconds before closing the game
            if self.timer_list[0].frame_num > 3000:
                self.idle_time_view.text = f"The game will close in {self.timer_list[0].text_time[-2:]} seconds"
                self.idle_time_view.update()
                self.idle_time_view.draw()

            # Update screen
            pygame.display.update()

        return username, play, scene_browser
