import pygame, sys, random

from .settings    import SCREEN_SIZE, FPS, MUSIC_VOL, SOUND_VOL, LOGO, STARS, LIVES, SURGE_NUM
from .documents   import CREDITS, HISTORY, GUIDE
from .manager     import msg_dict, advice_dict, button_list_def, bar_list, keyboard_list, statue_img, bg_img, load_music, load_sound
from .tools       import Timer, Logo, Button, Keyboard, Bar, Board, View, Canvas, Icon, Health_bar, Screen_fade
from .environment import Foreground, Background, Farground, Planet
from .players     import Player
from .enemies     import Enemy
from .obstacles   import Meteor
from .items       import Item
from .database    import Database


class Scene():
    # Create class variable to use the same instance in each scene
    db = Database()

    def __init__(self):
        # Calculate the dimensions of the width and height of the screen
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

        user_data = self.load_username()
        width, height   = user_data[14], user_data[15]
        self.screen     = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.fullscreen = False

        # Manage screen refresh rate
        self.clock  = pygame.time.Clock()

        self.timer_list = []
        for _ in range(2): # Create timer list
            self.timer_list.append(Timer(FPS))

    def update_play(self, username):
        user_data_list = self.db.read_data()

        username_list = []
        for user in user_data_list:
            username_list.append(user[0])

        for play in username_list:
            self.db.update_data(play, PLAY=0)

        self.db.update_data(username, PLAY=1)

    def load_username(self):
        user_data_list = self.db.read_data()

        # Read the new table if it was deleted
        if user_data_list == []:
            user_data_list = self.db.read_data()

            # Create the default data if it was deleted
            if user_data_list == []:
                self.db.create_data('empty')
                user_data_list = self.db.read_data()

        user_data = self.db.read_data('PLAY', -1)[-1]

        return user_data

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

    def load_data(self, username, weapon, level, score, enemy=0, meteor=0):
        user_data = self.db.read_data(username)[0]

        highlevel = user_data[5]
        highscore = user_data[7]
        T_enemy   = user_data[9]
        T_meteor  = user_data[11]

        if level > highlevel:
            highlevel = level

        if score > highscore:
            highscore = score
            new_highscore = True
        else: new_highscore = False

        T_enemy  += enemy
        T_meteor += meteor

        self.db.update_data(username, WEAPON=weapon)
        self.db.update_data(username, LEVEL=level)
        self.db.update_data(username, HIGHLEVEL=highlevel)
        self.db.update_data(username, SCORE=score)
        self.db.update_data(username, HIGHSCORE=highscore)
        self.db.update_data(username, ENEMY=enemy)
        self.db.update_data(username, T_ENEMY=T_enemy)
        self.db.update_data(username, METEOR=meteor)
        self.db.update_data(username, T_METEOR=T_meteor)

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

    def __init__(self):
        super().__init__()
        # Sounds fx
        self.select_loop_fx = self.sound('select_loop')
        self.select_fx      = self.sound('select')
        self.confirm_fx     = self.sound('confirm')
        self.start_fx       = self.sound('start')

        self.sfx_list = [self.select_loop_fx, self.select_fx, self.confirm_fx, self.start_fx]

    def command_buttons(self, SCREEN_W, SCREEN_H):
        self.command_list = []
        margin_y = SCREEN_H//2

        button_list = button_list_def('main')
        for btn in range(len(button_list[0])):
            temp_var = Button(self.screen, button_list[0][btn], center=(SCREEN_W//2, btn * SCREEN_H//8 + margin_y))
            if btn % 2 == 0:
                temp_var.flip_x = True
            self.command_list.append(temp_var)

        self.command_list[0].select_effect(True)

    def keyboard_buttons(self, SCREEN_W, SCREEN_H):
        self.keyboard_list = []
        margin_x = SCREEN_W//10.75
        margin_y = SCREEN_H//7.75

        for row in range(len(keyboard_list)):
            temp_list = []
            for column in range(len(keyboard_list[row])):
                temp_list.append(Keyboard(self.screen, keyboard_list[row][column], center=(column * SCREEN_W//11 + margin_x, row * SCREEN_H//15 + margin_y)))
            self.keyboard_list.append(temp_list)

        self.keyboard_list[0][0].select_effect(True)

    def config_buttons(self, SCREEN_W, SCREEN_H):
        self.config_list = []
        margin_y = SCREEN_H//8

        for bar in range(len(bar_list)):
            self.config_list.append(Bar(self.screen, bar_list[bar], center=(SCREEN_W//2, bar * SCREEN_H//10 + margin_y)))

        self.config_list[0].gage.active_effect(True)

    def reset(self, SCREEN_W, SCREEN_H):
        self.message    = View(self.screen, center=(SCREEN_W//2, SCREEN_H//2.5), letter=2, size=20)
        self.intro_logo = View(self.screen, "T H E   Q U E S T", 5, 50, pygame.Color('White'), center=(SCREEN_W//2, SCREEN_H//4))
        self.board      = Board(self.screen, midbottom=(SCREEN_W//2, 0))

        self.command_buttons(SCREEN_W, SCREEN_H)
        self.keyboard_buttons(SCREEN_W, SCREEN_H)
        self.config_buttons(SCREEN_W, SCREEN_H)

    def main_loop(self, play):
        user_data = self.load_username()
        username_list = ["New User"]
        for user in self.db.read_data():
            username_list.append(user[0])

        username  = user_data[0]
        style     = user_data[1]
        model     = user_data[2]
        weapon    = user_data[3]
        level     = user_data[4]
        highlevel = user_data[5]
        score     = user_data[6]
        highscore = user_data[7]
        enemy     = user_data[8]
        T_enemy   = user_data[9]
        meteor    = user_data[10]
        T_meteor  = user_data[11]
        music     = user_data[12]
        sound     = user_data[13]
        SCREEN_W  = user_data[14]
        SCREEN_H  = user_data[15]

        pygame.mixer.music.set_volume(music)
        for sfx in self.sfx_list:
            sfx.set_volume(sound)

        # Get screen resize change index from screen size dictionary
        resize = 0
        size_list = list(SCREEN_SIZE.values())[:-1]
        size_list.append((self.screen.get_width(), self.screen.get_height()))
        for width, height in size_list:
            if width == SCREEN_W and height == SCREEN_H:
                resize = size_list.index((width, height))

        scan_list = [music, sound, resize * 0.125]

        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.RESIZABLE)
        self.reset(SCREEN_W, SCREEN_H)
        button_list = button_list_def('main')

        empty = False
        if 'empty' in username_list:
            username_list.remove('empty')
            empty  = True
            user   = -1
        else: user = username_list.index(username)

        cursor = bar = row_key = column_key = select = 0
        str_key   = ''
        press_key = False
        msg = 0
        shift_key  = self.keyboard_list[-1][-1]
        delete_key = self.keyboard_list[-1][-2]

        if play:
            login = confirm = True
            play  = False
            msg   = 9
            msg_dict[msg] = username
        else: login = confirm = False
        create = False

        self.timer_list[0].frame_num = 0
        browser = 1
        run  = True
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
                        browser = 0
                        run = False

                # Keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: # Back select
                        if confirm:
                            if self.command_list[2].trigger:
                                if self.config_list[0].gage.trigger:
                                    if self.volume(pygame.mixer.music) > 0.0: # Turn down the volume
                                        scan_list[0] = self.volume(pygame.mixer.music, - 0.1)
                                        pygame.mixer.music.set_volume(scan_list[0])

                                elif self.config_list[1].gage.trigger:
                                    if self.volume(self.sfx_list[0]) > 0.0: # Turn down the sound
                                        for sfx in self.sfx_list:
                                            scan_list[1] = self.volume(sfx, - 0.1)
                                            sfx.set_volume(scan_list[1])

                                elif self.config_list[2].gage.trigger:
                                    if resize > 0:
                                        resize -= 1
                                    scan_list[2] = resize * 0.125

                        elif create:
                            if column_key > 0:
                                column_key -= 1
                            else: column_key = len(self.keyboard_list[row_key]) - 1

                        elif login:
                            if user > 0:
                                user -= 1
                            else: user = len(username_list) - 1
                            username = username_list[user]
                            if user != 0: msg = 8
                            else:         msg = 0

                        self.select_fx.play()

                    if event.key == pygame.K_RIGHT: # Next select
                        if confirm:
                            if self.command_list[2].trigger:
                                if self.config_list[0].gage.trigger:
                                    if self.volume(pygame.mixer.music) < 1.0: # Turn up the volume
                                        scan_list[0] = self.volume(pygame.mixer.music, + 0.1)
                                        pygame.mixer.music.set_volume(scan_list[0])

                                elif self.config_list[1].gage.trigger:
                                    if self.volume(self.sfx_list[0]) < 1.0: # Turn up the sound
                                        for sfx in self.sfx_list:
                                            scan_list[1] = self.volume(sfx, + 0.1)
                                            sfx.set_volume(scan_list[1])

                                elif self.config_list[2].gage.trigger:
                                    if resize < len(SCREEN_SIZE) - 1:
                                        resize += 1
                                    scan_list[2] = resize * 0.125

                        elif create:
                            if column_key < len(self.keyboard_list[row_key]) - 1:
                                column_key += 1
                            else: column_key = 0

                        elif login:
                            if user < len(username_list) - 1:
                                user += 1
                            else: user = 0
                            username = username_list[user]
                            if user != 0: msg = 8
                            else:         msg = 0

                        self.select_fx.play()

                    if event.key == pygame.K_UP: # Up select
                        if confirm and self.command_list[2].trigger:
                            if bar > 0:
                                bar -= 1
                            else: bar = len(self.config_list) - 1
                            self.config_list[bar].gage.active_effect(True)

                        elif create:
                            if row_key > 0:
                                row_key -= 1
                            else: row_key = len(self.keyboard_list) - 1

                        else:
                            if cursor > 0:
                                cursor -= 1
                            else: cursor = len(self.command_list) - 1
                            self.command_list[cursor].select_effect(True)

                        self.board.show = False
                        self.select_fx.play()

                    if event.key == pygame.K_DOWN: # Down select
                        if confirm and self.command_list[2].trigger:
                            if bar < len(self.config_list) - 1:
                                bar += 1
                            else: bar = 0
                            self.config_list[bar].gage.active_effect(True)

                        elif create:
                            if row_key < len(self.keyboard_list) - 1:
                                row_key += 1
                            else: row_key = 0

                        else:
                            if cursor < len(self.command_list) - 1:
                                cursor += 1
                            else: cursor = 0
                            self.command_list[cursor].select_effect(True)

                        self.board.show = False
                        self.select_fx.play()

                    # Select the effect of the key that is pressed
                    if create: self.keyboard_list[row_key][column_key].select_effect(True)

                    if event.key == pygame.K_SPACE: # Turnback select
                        if create:
                            if len(username) < 10:
                                # These 2 conditions are for not typing if the Delete key or the Shift key is pressed.
                                if  self.keyboard_list[row_key][column_key] != shift_key\
                                and self.keyboard_list[row_key][column_key] != delete_key:
                                    username += self.keyboard_list[row_key][column_key].text
                            else: msg = 2

                            # Delete characters from username if Delete key is pressed
                            if self.keyboard_list[row_key][column_key] == delete_key:
                                if len(username) > 0: username = username[:-1]

                            # Turn keyboard capitalization on or off if the Shift key is pressed
                            if self.keyboard_list[row_key][column_key] == shift_key:
                                if shift_key.trigger:
                                    shift_key.active_effect(False)
                                else:
                                    shift_key.active_effect(True)
                                shift_key.trigger = not shift_key.trigger
                            else:
                                self.keyboard_list[row_key][column_key].trigger = True
                                self.keyboard_list[row_key][column_key].active_effect(True)

                        self.confirm_fx.play()

                    if event.key == pygame.K_RETURN: # Confirm DOWN
                        self.command_list[cursor].trigger = True
                        self.command_list[cursor].active_effect(True)
                        self.confirm_fx.play()
                        msg = 0

                    if event.key == pygame.K_BACKSPACE: # Delete
                        if create:
                            if len(username) > 0:
                                username = username[:-1]

                    if event.key == pygame.K_ESCAPE: # Quit game
                        pygame.quit()
                        sys.exit()

                    # Reset the inactivity timer by pressing any key
                    self.timer_list[0].frame_num = 0

                # keyboard text input
                if create and event.type == pygame.TEXTINPUT:
                    if str_key != str(event)[31]:
                        str_key = str(event)[31]
                        press_key = True

                    if str(event)[31] != ' ':
                        if len(username) < 10:
                            username += str_key
                        else: msg = 2
                        self.confirm_fx.play()

                    else: msg = 0

                # keyboard release
                if event.type == pygame.KEYUP:
                    # Turns off the effect of the key that is release
                    if create and self.keyboard_list[row_key][column_key] != shift_key:
                        if  self.keyboard_list[row_key][column_key].trigger:
                            self.keyboard_list[row_key][column_key].trigger = False
                            self.keyboard_list[row_key][column_key].active_effect(False)

                    if event.key == pygame.K_SPACE: # Turnback select
                        if not create:
                            msg = 0
                            if confirm: confirm = False
                            elif login:   login = False

                    if event.key == pygame.K_RETURN: # Confirm UP
                        # Button - Account & Login & Play
                        if self.command_list[0].trigger:
                            if confirm:
                                browser = 3
                                run = False

                            elif login:
                                if username_list[user] == username_list[0]:
                                    create = not create
                                    msg = 0
                                    if create:
                                        username = ''
                                        msg = 7
                                    elif username != '':
                                        if username in username_list[1:]:
                                            create = not create
                                            msg = 1
                                        else:
                                            # Create a new username in the database
                                            if empty: self.db.delete_data('empty')
                                            self.db.create_data(username)
                                            username_list.append(username)
                                            self.update_play(username)
                                            user = -1
                                            row_key = column_key = 0
                                            self.keyboard_list[0][0].select_effect(True)
                                            shift_key.trigger = False
                                            msg = 3
                                else:
                                    username = username_list[user]
                                    self.update_play(username)
                                    browser = 0
                                    play = True
                                    run  = False

                            else: login = True

                        # Button - Records & Delete & Edit
                        elif self.command_list[1].trigger:
                            if confirm:
                                browser = 1
                                run = False

                            elif login:
                                if username_list[user] != username_list[0]:
                                    self.db.delete_data(username_list.pop(user))
                                    user = -1
                                    username = username_list[user]
                                    msg  = 4
                                elif len(username_list) > 1: msg = 0
                                else: msg = 5

                            else:
                                browser = -1
                                run = False

                        # Button - History & Guide & Configs
                        elif self.command_list[2].trigger:
                            if confirm:
                                self.config.show = not self.config.show
                                if not self.config.show:
                                    self.command_list[2].trigger = False
                                    self.load_volume(username_list[user], scan_list[0], scan_list[1])

                                    # Scale the screen size to maximum or full
                                    if resize == len(SCREEN_SIZE) - 1:
                                        self.fullscreen = not self.fullscreen
                                        if self.fullscreen:
                                            self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                                        else:
                                            self.screen = pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()), pygame.RESIZABLE)
                                        self.load_size(username, self.screen.get_width(), self.screen.get_height())
                                        browser = 0
                                        play = True
                                        run  = False

                                    # Scale other screen dimensions
                                    elif not self.fullscreen:
                                        width  = SCREEN_SIZE[list(SCREEN_SIZE)[resize]][0]
                                        height = SCREEN_SIZE[list(SCREEN_SIZE)[resize]][1]
                                        if width != SCREEN_W or height != SCREEN_H:
                                            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                                            self.load_size(username, width, height)
                                            browser = 0
                                            play = True
                                            run  = False

                            elif login:
                                self.board.show = not self.board.show
                                if self.board.show:
                                    self.board.create_textline(GUIDE, midleft=(self.board.rect.width//3, self.board.rect.top))
                            else:
                                self.board.show = not self.board.show
                                if self.board.show:
                                    self.board.create_textline(HISTORY, center=(self.board.rect.centerx, self.board.rect.top))

                        # Button - Exit & Back
                        elif self.command_list[3].trigger:
                            msg = 0
                            if  confirm: confirm = False
                            elif create:  create = False
                            elif  login:   login = False
                            else:
                                pygame.quit()
                                sys.exit()

                        self.command_list[cursor].active_effect(False)

            # Clear screen and set background color
            self.screen.fill(pygame.Color('Black'))

            ''' --- AREA TO UPDATE AND DRAW --- '''

            msg_dict[8] = f'{user} / {len(username_list) - 1}'

            self.message.text = msg_dict[msg]
            self.message.update()
            self.message.draw()

            # Select which text to assign to buttons
            if  confirm: select = 2
            elif create: select = 2
            elif  login: select = 1
            else:        select = 0

            for self.command, index in zip(self.command_list, range(len(self.command_list))):
                if  self.command != self.command_list[cursor]:
                    self.command.select_effect(False)
                    self.command.trigger = False

                if  self.command_list[index] != self.command_list[0]:
                    self.command_list[index].text = button_list[select][index]
                else:
                    if  confirm: self.command_list[0].text = button_list[select][index]
                    elif create: self.command_list[0].text = username
                    elif  login: self.command_list[0].text = username_list[user]
                    else:        self.command_list[0].text = button_list[select][index]

                    if login and not create and not confirm and cursor == 0: self.command_list[0].many = True
                    else: self.command_list[0].many = False

                self.command.update()
                self.command.draw()

            if create:
                for row in range(len(self.keyboard_list)):
                    for self.keyboard, index in zip(self.keyboard_list[row], range(len(self.keyboard_list[row]))):

                        if self.keyboard != self.keyboard_list[row_key][column_key]:
                            self.keyboard.select_effect(False)
                            if self.keyboard != shift_key:
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

                        if shift_key.trigger:
                            self.keyboard.text = self.keyboard.text.upper()
                            self.keyboard_list[-1][-3].text = "_"
                            shift_key.select_effect(True)
                        else:
                            self.keyboard.text = self.keyboard.text.lower()
                            self.keyboard_list[-1][-3].text = "-"

                        self.keyboard.update()
                        self.keyboard.draw()

            elif confirm and self.command_list[2].trigger:
                for self.config in self.config_list:
                    self.config_list[bar].gage.trigger = True
                    if self.config != self.config_list[bar] and self.config.gage.trigger:
                        self.config.gage.active_effect(False)
                        self.config.gage.trigger = False

                    self.config_list[0].displace_effect(scan_list[0])
                    self.config_list[1].displace_effect(scan_list[1])
                    self.config_list[2].displace_effect(scan_list[2])
                    self.config_list[2].gage.text = str(SCREEN_SIZE[list(SCREEN_SIZE)[resize]])

                    self.config.update()
                    self.config.draw()

            if not login and not create and not confirm and not self.board.show:
                if self.intro_logo.fade    < 255: self.intro_logo.fade += 15
            elif  self.intro_logo.fade >   0: self.intro_logo.fade -= 15

            self.intro_logo.color = ([self.intro_logo.fade]*3)
            self.intro_logo.update()
            if self.intro_logo.fade != 0: self.intro_logo.draw()

            self.board.update()
            self.board.draw()

            # Limit delay without event activity
            if self.timer_list[0].countdown(1, True):
                browser = -1
                run = False

            # Update screen
            pygame.display.update()

        return browser, play


class Menu(Scene):

    def __init__(self):
        super().__init__()
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
        self.spaceship = Icon(self.screen, 'spaceships', 0.5, midbottom=(self.bg_rect.centerx, self.bg_rect.centery-126))
        self.symbol    = Icon(self.screen, 'symbol',    0.18, midbottom=(self.bg_rect.centerx+1, self.bg_rect.centery+63))

    def main_loop(self, play):
        user_data = self.load_username()

        username  = user_data[0]
        style     = user_data[1]
        model     = user_data[2]
        weapon    = user_data[3]
        level     = user_data[4]
        highlevel = user_data[5]
        score     = user_data[6]
        highscore = user_data[7]
        enemy     = user_data[8]
        T_enemy   = user_data[9]
        meteor    = user_data[10]
        T_meteor  = user_data[11]
        music     = user_data[12]
        sound     = user_data[13]
        SCREEN_W  = user_data[14]
        SCREEN_H  = user_data[15]

        pygame.mixer.music.set_volume(music)
        for sfx in self.sfx_list:
            sfx.set_volume(sound)

        self.reset(SCREEN_W, SCREEN_H)
        confirm = False

        self.timer_list[0].frame_num = 0
        browser = 1
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
                        browser = 0
                        run = False

                # Keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: # Back select
                        if not confirm:
                            self.symbol.trigger_effect(True)
                            self.portal_loop_fx.play(-1)
                        else:
                            self.spaceship.trigger_effect(True)
                            self.select_loop_fx.play(-1)

                    if event.key == pygame.K_RIGHT: # Next select
                        if not confirm:
                            self.symbol.trigger_effect(True)
                            self.portal_loop_fx.play(-1)
                        else:
                            self.spaceship.trigger_effect(True)
                            self.select_loop_fx.play(-1)

                    if event.key == pygame.K_SPACE: # Turnback select
                        if not confirm:
                            browser = -1
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
                            browser = 2
                            run = False
                            self.start_fx.play()

                    if event.key == pygame.K_UP:
                            self.select_fx.play()

                    if event.key == pygame.K_DOWN:
                            self.select_fx.play()

                    if event.key == pygame.K_ESCAPE: # Quit game
                        browser = -1
                        run = False

                    # Reset the inactivity timer by pressing any key
                    self.timer_list[0].frame_num = 0

                # keyboard release
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT: # Back select
                        if not confirm:
                            if style > 0:
                                style -= 1
                            else: style = 2
                            self.symbol.trigger_effect(False)
                            self.portal_loop_fx.stop()
                            self.select_fx.play()
                        else:
                            if model > 0:
                                model -= 1
                            else: model = 2
                            self.spaceship.trigger_effect(False)
                            self.select_loop_fx.stop()
                            self.confirm_fx.play()

                    if event.key == pygame.K_RIGHT: # Next select
                        if not confirm:
                            if style < 2:
                                style += 1
                            else: style = 0
                            self.symbol.trigger_effect(False)
                            self.portal_loop_fx.stop()
                            self.select_fx.play()
                        else:
                            if model < 2:
                                model += 1
                            else: model = 0
                            self.spaceship.trigger_effect(False)
                            self.select_loop_fx.stop()
                            self.confirm_fx.play()

            # Clear screen and set background color
            self.screen.fill(pygame.Color('Black'))

            ''' --- AREA TO UPDATE AND DRAW --- '''

            if confirm:
                self.spaceship.update(style, model)
                self.spaceship.draw()

            self.screen.blit(self.statue, self.bg_rect)

            self.symbol.update(style, model, confirm)
            self.symbol.draw()

            # Limit delay without event activity
            if self.timer_list[0].countdown(1, True):
                browser = -1
                run = False

            # Update screen
            pygame.display.update()

        self.load_select(username, style, model, level)

        return browser, play


class Load(Scene):

    def __init__(self):
        super().__init__()
        self.game_over_fx = self.sound('game_over')

    def reset(self, SCREEN_W, SCREEN_H):
        self.loading_logo   = Logo(self.screen, 'loading',   center=(SCREEN_W//2, SCREEN_H//3))
        self.game_over_logo = Logo(self.screen, 'game_over', center=(SCREEN_W//2, SCREEN_H//3))
        self.message        = View(self.screen, center=(SCREEN_W//2, SCREEN_H//1.2), letter=2, size=20)

    def main_loop(self, play):
        user_data = self.load_username()
        SCREEN_W  = user_data[14]
        SCREEN_H  = user_data[15]

        self.reset(SCREEN_W, SCREEN_H)
        index = random.randint(0, len(advice_dict) - 1)

        if play: self.game_over_fx.play()

        browser = 1
        run = True
        while run:
            # Limit frames per second
            self.clock.tick(FPS)

            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        browser = 1
                        run = False

                    if event.key == pygame.K_ESCAPE:
                        browser = -1
                        run = False

            # Clear screen and set background color
            self.screen.fill(pygame.Color('Black'))

            ''' --- AREA TO UPDATE AND DRAW --- '''

            if not play:
                self.loading_logo.update()
                self.loading_logo.draw()
            else:
                self.game_over_logo.update()
                self.game_over_logo.draw()

            self.message.text = advice_dict[index]
            self.message.update()
            self.message.draw()

            if self.timer_list[0].countdown(0.01, True):
                browser = 1
                run = False

            # Update screen
            pygame.display.update()

        return browser, play


class Game(Scene):

    def __init__(self):
        super().__init__()
        self.bullet_group    = pygame.sprite.Group()
        self.missile_group   = pygame.sprite.Group()
        self.enemy_group     = pygame.sprite.Group()
        self.meteor_group    = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.item_group      = pygame.sprite.Group()
        self.canvas_group    = pygame.sprite.Group()

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
        self.confirm_fx      = self.sound('confirm')
        self.win_fx          = self.sound('win')
        self.death_fx        = self.sound('death')

        self.enemy_sfx_list  = [self.empty_ammo_fx, self.bullet_fx, self.empty_load_fx, self.missile_fx, self.missile_cd_fx, self.missile_exp_fx, self.explosion_fx, self.item_standby_fx, self.item_get_fx]
        self.sfx_list        = [self.move_fx, self.backmove_fx, self.turbo_fx, self.explosion_fx, self.pause_fx, self.select_fx, self.confirm_fx, self.win_fx, self.death_fx]
        self.sfx_list.extend(self.enemy_sfx_list)

        self.loading = Load()

    def reset(self, SCREEN_W, SCREEN_H):
        self.intro_fade = Screen_fade(self.screen, 'intro', pygame.Color('Black'), 3, SCREEN_W, SCREEN_H)
        self.death_fade = Screen_fade(self.screen, 'death', pygame.Color('Black'), 3, SCREEN_W, SCREEN_H)

        self.lives_canvas   = Canvas(self.screen, 'lives',  0, -3, 9, midtop=(SCREEN_W*0.300, 0))
        self.ammo_canvas    = Canvas(self.screen, 'ammo',   0, -2, 1, midtop=(SCREEN_W*0.350, 8))
        self.load_canvas    = Canvas(self.screen, 'load',   0,  0, 7, midtop=(SCREEN_W*0.400, 2))
        self.weapon_canvas  = Canvas(self.screen, 'weapon', 1, -4, 3, midtop=(SCREEN_W*0.455, 6))
        self.speed_canvas   = Canvas(self.screen, 'speed',  1,  2, 5, midtop=(SCREEN_W*0.500, 4))
        self.turbo_canvas   = Canvas(self.screen, 'turbo',  1,  4, 7, midtop=(SCREEN_W*0.548, 2))
        self.shield_canvas  = Canvas(self.screen, 'shield', 0,  2, 9, midtop=(SCREEN_W*0.601, 0))
        self.freeze_canvas  = Canvas(self.screen, 'freeze', 0, -1, 9, midtop=(SCREEN_W*0.652, 0))
        self.atomic_canvas  = Canvas(self.screen, 'atomic', 0,  3, 1, midtop=(SCREEN_W*0.695, 8))

        self.timer_view     = View(self.screen, topleft =(SCREEN_W*0.01, SCREEN_H*0.05), size=25)
        self.level_view     = View(self.screen, topleft =(SCREEN_W*0.15, SCREEN_H*0.07), color=pygame.Color('Brown'))
        self.highscore_view = View(self.screen, topright=(SCREEN_W-SCREEN_W//30, SCREEN_H*0.015), size=20, color=pygame.Color('Orange'))
        self.score_view     = View(self.screen, topright=(SCREEN_W-SCREEN_W//30, SCREEN_H*0.055), size=20, color=pygame.Color('Purple'))

        self.paused = View(self.screen, '', 5, 80, pygame.Color('Black'), center=(SCREEN_W//2, SCREEN_H//3.5))
        self.board  = Board(self.screen, midbottom=(SCREEN_W//2, 0))

        self.canvas_group.empty()
        self.canvas_group.add(self.lives_canvas, self.ammo_canvas, self.load_canvas, self.weapon_canvas, self.speed_canvas, self.turbo_canvas,\
        self.shield_canvas, self.freeze_canvas, self.atomic_canvas, self.timer_view, self.level_view, self.highscore_view, self.score_view)

    def command_buttons(self, SCREEN_W, SCREEN_H):
        self.command_list = []
        margin_y = SCREEN_H//2

        button_list = button_list_def('game')
        for btn in range(len(button_list[0])):
            temp_var = Button(self.screen, button_list[0][btn], center=(SCREEN_W//2, btn * SCREEN_H//8 + margin_y))
            if btn % 2 == 0:
                temp_var.flip_x = True
            self.command_list.append(temp_var)

        self.command_list[0].select_effect(True)

    def config_buttons(self, SCREEN_W, SCREEN_H):
        self.config_list = []
        margin_y = SCREEN_H//4.5

        for bar in range(len(bar_list[:-1])):
            self.config_list.append(Bar(self.screen, bar_list[bar], center=(SCREEN_W//2, bar * SCREEN_H//10 + margin_y)))

        self.config_list[0].gage.active_effect(True)

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
        origin_planet  = Planet(self.screen, 'origin' , init_planet, SCREEN_W, SCREEN_H, midbottom=(SCREEN_W//2, SCREEN_H+SCREEN_H*0.25))
        destiny_planet = Planet(self.screen, 'destiny', init_planet, SCREEN_W, SCREEN_H, midbottom=(SCREEN_W//2, 0))

        self.environment_list = [background, farground, origin_planet, destiny_planet]

    def item_create(self, item_name, player, SCREEN_W, SCREEN_H):
        item = Item(item_name, self.screen, player, SCREEN_W, SCREEN_H, [self.item_standby_fx, self.item_get_fx], bottomleft=(random.randint(0, SCREEN_W-SCREEN_W//10), 0))
        self.item_group.add(item)

    def enemy_create(self, level, SCREEN_W, SCREEN_H):
        self.enemy_index = 0

        self.enemy_list = []
        for group in range(level*10//2):
            select = random.randint(0, 2)
            temp_list = []
            for number in range(random.randint(1, level)):
                temp_list.append(Enemy(self.screen, number, select, 2+level*0.1, self.player, SCREEN_W, SCREEN_H, [self.group_list, self.enemy_sfx_list]))

            self.enemy_list.append(temp_list)

    def meteor_surge(self, level, surge_num, SCREEN_W, SCREEN_H):
        self.surge_start = self.surge_end = False
        self.surge_index = 0

        self.meteor_list = []
        for number in range(surge_num):
            temp_list = []
            # Increase the number of meteors per surge
            for _ in range((number + level) * 100 // 4):
                temp_list.append(Meteor(self.screen, self.player, self.item_group, SCREEN_W, SCREEN_H, [self.explosion_fx, self.item_standby_fx, self.item_get_fx]))

            self.meteor_list.append(temp_list)

    def process_data(self, username, weapon, level, score, enemy, meteor, lives, init_planet, play):
        self.loading.main_loop(play)
        self.empty_level()
        self.load_data(username, weapon, level, score, enemy, meteor)
        user_data = self.db.read_data(username)[0]

        style    = user_data[1]
        model    = user_data[2]
        weapon   = user_data[3]
        level    = user_data[4]
        score    = user_data[6]
        enemy    = user_data[8]
        meteor   = user_data[10]
        SCREEN_W = user_data[14]
        SCREEN_H = user_data[15]

        self.reset(SCREEN_W, SCREEN_H)
        self.command_buttons(SCREEN_W, SCREEN_H)
        self.config_buttons(SCREEN_W, SCREEN_H)
        temp_list = [weapon, level, score, enemy, meteor, SCREEN_W, SCREEN_H]

        # Create sprites
        self.player = Player(self.screen, style, model, lives, [temp_list, self.group_list])
        self.environment_create(init_planet, SCREEN_W, SCREEN_H)
        self.health_bar = Health_bar(self.screen, self.player.max_health, SCREEN_W, SCREEN_H)
        self.enemy_create(level, SCREEN_W, SCREEN_H)
        self.meteor_surge(level, SURGE_NUM, SCREEN_W, SCREEN_H)
        self.meteor_list_copy = self.meteor_list.copy()
        self.timer_list[0].frame_num = 0

        return user_data

    def main_loop(self, play):
        user_data = self.load_username()

        username  = user_data[0]
        style     = user_data[1]
        model     = user_data[2]
        weapon    = user_data[3]
        level     = user_data[4]
        highlevel = user_data[5]
        score     = user_data[6]
        highscore = user_data[7]
        enemy     = user_data[8]
        T_enemy   = user_data[9]
        meteor    = user_data[10]
        T_meteor  = user_data[11]
        music     = user_data[12]
        sound     = user_data[13]
        SCREEN_W  = user_data[14]
        SCREEN_H  = user_data[15]

        pygame.mixer.music.set_volume(music)
        for sfx in self.sfx_list:
            sfx.set_volume(sound)

        init_planet = random.randint(1, 6)
        # TODO WARNING! This process data will stop the screen until finished
        self.process_data(username, 1, level, 0, 0, 0, LIVES, init_planet, play)

        cursor = bar = 0
        scan_list = [music, sound]

        pause     = False
        death     = False
        restart   = False
        game_over = False

        shoot = False
        shoot_bullets = False
        throw = False
        throw_missiles = False

        trick_list = [True] * 3

        browser = 1
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
                        browser = 0
                        run = False

                # Keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if pause:
                            if self.command_list[1].trigger:
                                if self.config_list[bar].gage == self.config_list[0].gage:
                                    if self.volume(pygame.mixer.music) > 0.0: # Turn down the volume
                                        scan_list[0] = self.volume(pygame.mixer.music, - 0.1)
                                        pygame.mixer.music.set_volume(scan_list[0])

                                elif self.config_list[bar].gage == self.config_list[1].gage:
                                    if self.volume(self.sfx_list[0]) > 0.0: # Turn down the sound
                                        for sfx in self.sfx_list:
                                            scan_list[1] = self.volume(sfx, - 0.1)
                                            sfx.set_volume(scan_list[1])

                            self.select_fx.play()

                        elif not self.player.win:
                            self.player.moving_left = True # Moving left
                            self.move_fx.play()

                    if event.key == pygame.K_RIGHT:
                        if pause:
                            if self.command_list[1].trigger:
                                if self.config_list[bar].gage == self.config_list[0].gage:
                                    if self.volume(pygame.mixer.music) < 1.0: # Turn up the volume
                                        scan_list[0] = self.volume(pygame.mixer.music, + 0.1)
                                        pygame.mixer.music.set_volume(scan_list[0])

                                elif self.config_list[bar].gage == self.config_list[1].gage:
                                    if self.volume(self.sfx_list[0]) < 1.0: # Turn up the sound
                                        for sfx in self.sfx_list:
                                            scan_list[1] = self.volume(sfx, + 0.1)
                                            sfx.set_volume(scan_list[1])

                            self.select_fx.play()

                        elif not self.player.win:
                            self.player.moving_right = True # Moving right
                            self.move_fx.play()

                    if event.key == pygame.K_UP: # Moving up & Up select
                        if pause:
                            if self.command_list[1].trigger:
                                if bar > 0:
                                    bar -= 1
                                else: bar = len(self.config_list) - 1
                                self.config_list[bar].gage.active_effect(True)

                            else:
                                if cursor > 0:
                                    cursor -= 1
                                else: cursor = len(self.command_list) - 1
                                self.command_list[cursor].select_effect(True)

                            self.board.show = False
                            self.select_fx.play()

                        elif not self.player.win:
                            self.player.moving_up = True
                            self.move_fx.play()

                    if event.key == pygame.K_DOWN: # Moving down & Down select
                        if pause:
                            if self.command_list[1].trigger:
                                if bar < len(self.config_list) - 1:
                                    bar += 1
                                else: bar = 0
                                self.config_list[bar].gage.active_effect(True)

                            else:
                                if cursor < len(self.command_list) - 1:
                                    cursor += 1
                                else: cursor = 0
                                self.command_list[cursor].select_effect(True)

                            self.board.show = False
                            self.select_fx.play()

                        elif not self.player.win:
                            self.player.moving_down = True
                            self.move_fx.play()

                    if event.key == pygame.K_r: # Shoot bullets
                        if not self.player.win: shoot = True

                    if event.key == pygame.K_e: # Throw missiles
                        if not self.player.win: throw = True

                    if event.key == pygame.K_SPACE: # Turbo and Return
                        if pause:
                            if self.command_list[1].trigger:
                                self.command_list[1].trigger = False
                                self.config.show = False
                                self.load_volume(username, scan_list[0], scan_list[1])

                            elif self.command_list[2].trigger:
                                self.command_list[2].trigger = False
                                self.board.show = False

                            else:
                                if game_over:
                                    game_over = False
                                    browser = 1
                                    run = False
                                elif self.death_fade.fade_complete or self.player.auto_init: restart = True
                                self.command_list[cursor].trigger = False
                                cursor = 0
                                pause  = False
                                pygame.mixer.music.unpause()
                                self.pause_fx.play()
                        else:
                            if self.player.alive and not self.player.spawn and not self.player.win:
                                self.player.turbo = True
                                self.turbo_fx.play()

                    if event.key == pygame.K_RETURN: # Pause and Confirm DOWN
                        if pause:
                            self.command_list[cursor].trigger = True
                            self.command_list[cursor].active_effect(True)
                            self.confirm_fx.play()

                    if event.key == pygame.K_ESCAPE: # Exit game
                        browser = -2
                        run = False

                    # Reset the inactivity timer by pressing any key
                    if game_over: self.timer_list[0].frame_num = 0

                # Keyboard release
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
                        if not pause and self.player.alive and not self.player.spawn and not self.player.win:
                            self.player.turbo = False
                            self.backmove_fx.play()

                    if event.key == pygame.K_RETURN: # Confirm UP
                        if pause:
                            # Button - Continue & Restart
                            if self.command_list[0].trigger:
                                if game_over:
                                    game_over = False
                                    browser = 1
                                    run = False
                                elif self.death_fade.fade_complete or self.player.auto_init:
                                    restart = True

                                cursor = 0
                                pause  = False
                                pygame.mixer.music.unpause()
                                self.pause_fx.play()

                            # Button - Settings
                            elif self.command_list[1].trigger:
                                self.config.show = not self.config.show
                                if not self.config.show:
                                    self.command_list[1].trigger = False
                                    self.load_volume(username, scan_list[0], scan_list[1])

                            # Button - Help
                            elif self.command_list[2].trigger:
                                self.board.show = not self.board.show
                                if self.board.show:
                                    self.board.create_textline(GUIDE, midleft=(self.board.rect.width//3, self.board.rect.top))

                            # Button - Exit
                            elif self.command_list[3].trigger:
                                browser = -2
                                run = False

                            self.command_list[cursor].active_effect(False)

                        elif not self.player.spawn:
                            pause = True
                            pygame.mixer.music.pause()
                            self.pause_fx.play()

            # Clear screen and set background color
            self.screen.fill(pygame.Color('Black'))

            ''' --- AREA TO UPDATE AND DRAW --- '''

            # Pause commands
            if pause:
                if game_over:
                    # Limit delay without event activity
                    if self.timer_list[1].countdown(0.5, True):
                        game_over = False
                        browser = 1
                        run = False
                else:
                    if self.command_list[cursor].trigger or self.board.show:
                        if self.paused.fade >   0: self.paused.fade -= 15
                    elif   self.paused.fade < 255: self.paused.fade += 15

                    if self.player.win:
                        self.paused.text = 'N E X T'
                        self.paused.color = (0, self.paused.fade, 0)
                    elif self.player.alive:
                        self.paused.text = 'P A U S E'
                        self.paused.color = (self.paused.fade, 0, 0)
                    else:
                        self.paused.text = 'R E S T A R T'
                        self.paused.color = (0, 0, self.paused.fade)

                    self.paused.update()
                    self.paused.draw()

                for self.command in self.command_list:
                    if self.command != self.command_list[cursor]:
                        self.command.select_effect(False)
                        self.command.trigger = False

                    self.command.update()
                    self.command.draw()

                if self.command_list[1].trigger:
                    for self.config in self.config_list:
                        self.config_list[bar].gage.trigger = True
                        if self.config != self.config_list[bar] and self.config.gage.trigger:
                            self.config.gage.active_effect(False)
                            self.config.gage.trigger = False

                        self.config_list[0].displace_effect(scan_list[0])
                        self.config_list[1].displace_effect(scan_list[1])

                        self.config.update()
                        self.config.draw()

                self.board.update()
                self.board.draw()

            else:
                self.paused.fade = 0

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
                            self.item_create('random', self.player, SCREEN_W, SCREEN_H)
                            self.music(5, scan_list[0])
                        else:
                            self.surge_end = True
                            self.enemy.retired = False
                            self.item_create('random', self.player, SCREEN_W, SCREEN_H)
                            self.music(3, scan_list[0])

                for self.environment in self.environment_list:
                    self.environment.update(self.player)
                    self.environment.draw()

                for bullet in self.bullet_group:
                    bullet.update()
                    bullet.draw()

                self.missile_group.update()
                self.missile_group.draw(self.screen)

                self.player.check_alive(self.explosion_fx)
                self.player.update()
                self.player.draw()

                for self.meteor in self.meteor_group:
                    self.meteor.update(self.player.turbo)
                    self.meteor.draw()

                if not self.player.spawn and not self.player.win and len(self.meteor_group) == 0:
                    if self.timer_list[0].counter(10, True):
                        if self.enemy_index < len(self.enemy_list):
                            self.enemy_group.add(self.enemy_list[self.enemy_index])
                            self.enemy_index += 1

                for self.enemy in self.enemy_group:
                    self.enemy.update()
                    self.enemy.draw()

                self.explosion_group.update()
                self.explosion_group.draw(self.screen)

                # Tricks to get a specific item
                if trick_list[0] and self.player.score > highscore:
                    self.item_create('super', self.player, SCREEN_W, SCREEN_H)
                    trick_list[0] = False

                elif trick_list[1] and self.player.dead_enemy > 10:
                    self.item_create('score', self.player, SCREEN_W, SCREEN_H)
                    trick_list[1] = False

                elif trick_list[2] and self.player.dead_meteor > 10:
                    self.item_create('score', self.player, SCREEN_W, SCREEN_H)
                    trick_list[2] = False

                for item in self.item_group:
                    item.update()
                    item.draw()

                if self.player.alive:
                    if self.player.spawn and self.intro_fade.fade():
                        self.intro_fade.fade_counter = 0
                        self.player.spawn = False

                    if self.player.collide and self.timer_list[0].time(0.5, True):
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
                        self.timer_list[0].text_time = 'WIN !'
                        self.enemy.retired = True
                        self.player.win = True
                        pygame.mixer.music.stop()
                        self.win_fx.play()

                    # Check if player has completed the level
                    elif self.player.win:
                        if self.player.auto_movement() or restart:
                            level += 1
                            init_planet = self.environment.destiny_planet
                            user_data = self.process_data(username, self.player.weapon, level, self.player.score, self.player.dead_enemy, self.player.dead_meteor, self.player.lives, init_planet, play)
                            highscore = user_data[7]
                            self.player.win = False
                            restart = False
                            play = False
                            self.music(3, scan_list[0])
                            pygame.mixer.music.play()
                else:
                    if not death and not self.death_fade.fade_complete:
                        pygame.mixer.music.stop()
                        self.death_fx.play()
                        death = True
                    # Restart the level if the player has lost
                    elif not game_over and self.death_fade.fade():
                        if death:
                            pause = True
                            death = False
                        elif restart:
                            death = restart = False
                            self.death_fade.fade_counter = 0
                            self.player.lives -= 1
                            if self.player.lives > 0:
                                init_planet = self.environment.origin_planet
                                user_data   = self.process_data(username, 1, level, self.player.score, 0, 0, self.player.lives, init_planet, play)
                                highscore   = user_data[7]
                                self.player.score = 0
                                self.player.alive = True
                                play = False
                                self.music(3, scan_list[0])
                                pygame.mixer.music.play()
                            else:
                                play = True
                                self.loading.main_loop(play)
                                game_over = True
                                browser = 1
                                run = False

            # Zone for user interface bar
            pygame.draw.rect(self.screen, pygame.Color('Black'), (0, 0, SCREEN_W, SCREEN_H//10))
            pygame.draw.line(self.screen, pygame.Color('Gray'), (0, SCREEN_H//10), (SCREEN_W, SCREEN_H//10), 4)

            # Show player health
            self.health_bar.view.text = str(username)
            self.health_bar.draw(self.player.health)

            # Show canvas and view
            self.lives_canvas.view.text  = str(self.player.lives)
            self.ammo_canvas.view.text   = str(self.player.ammo)
            self.load_canvas.view.text   = str(self.player.load)
            self.weapon_canvas.view.text = str(self.player.weapon)
            self.speed_canvas.view.text  = str(self.player.max_speed)
            self.turbo_canvas.view.text  = str(self.player.turbo_up)
            self.shield_canvas.switch(self.player.shield)
            self.freeze_canvas.switch(self.player.freeze)
            self.atomic_canvas.switch(self.player.atomic)
            self.timer_view.text = f"T- {self.timer_list[0].text_time}"
            self.level_view.text = f"Level: {level}"
            self.score_view.text = f"Score: {self.player.score}"
            self.highscore_view.compare(self.player.score, highscore, "New Highscore", f"Highscore: {highscore}")

            for canvas in self.canvas_group:
                canvas.update()
                canvas.draw()

            # Update screen
            pygame.display.update()

        # *After* exiting the while loop, return data
        self.load_data(username, self.player.weapon, self.player.level, self.player.score)

        return browser, play


class Record(Scene):

    def __init__(self):
        super().__init__()
        # Sounds fx
        self.select_loop_fx = self.sound('select_loop')
        self.select_fx      = self.sound('select')
        self.confirm_fx     = self.sound('confirm')
        self.start_fx       = self.sound('start')

        self.sfx_list = [self.select_loop_fx, self.select_fx, self.confirm_fx, self.start_fx]

    def command_buttons(self, play, SCREEN_W, SCREEN_H):
        self.command_list = []
        margin_y = SCREEN_H//2
        if play: select = 1
        else:    select = 0

        button_list = button_list_def('record')
        for btn in  range(len(button_list[select])):
            temp_var = Button(self.screen, button_list[select][btn], center=(SCREEN_W//2, btn * SCREEN_H//8 + margin_y))
            if btn % 2 == 0:
                temp_var.flip_x = True
            self.command_list.append(temp_var)

        self.command_list[0].select_effect(True)

    def reset(self, play, SCREEN_W, SCREEN_H):
        self.ranking_view   = View(self.screen, center=(SCREEN_W//2, SCREEN_H//8), letter=0, size=30)
        self.idle_time_view = View(self.screen, midbottom=(SCREEN_W//2, SCREEN_H-SCREEN_H*0.02), letter=2, size=20)
        self.board = Board(self.screen, midbottom=(SCREEN_W//2, 0))

        self.update_ranking(SCREEN_W, SCREEN_H)
        self.command_buttons(play, SCREEN_W, SCREEN_H)

    def update_ranking(self, SCREEN_W, SCREEN_H):
        ranking_data = self.db.read_data('HIGHSCORE', -1)

        self.ranking_list = []
        margin_y = SCREEN_H//5

        if ranking_data[0][0] != 'empty':
            # Update the top ranking list of the users highscore
            for user in range(len(ranking_data)):
                temp_var = View(self.screen, bottomleft=(SCREEN_W//3.5, user * -SCREEN_H//16 + margin_y), letter=3, size=30, color=pygame.Color('Black'))
                temp_var.text = f"Ranking {len(ranking_data)-user}:  {ranking_data[user][0]} -> {ranking_data[user][7]}"
                self.ranking_list.append(temp_var)

    def main_loop(self, play):
        user_data = self.load_username()

        username  = user_data[0]
        style     = user_data[1]
        model     = user_data[2]
        weapon    = user_data[3]
        level     = user_data[4]
        highlevel = user_data[5]
        score     = user_data[6]
        highscore = user_data[7]
        enemy     = user_data[8]
        T_enemy   = user_data[9]
        meteor    = user_data[10]
        T_meteor  = user_data[11]
        music     = user_data[12]
        sound     = user_data[13]
        SCREEN_W  = user_data[14]
        SCREEN_H  = user_data[15]

        pygame.mixer.music.set_volume(music)
        for sfx in self.sfx_list:
            sfx.set_volume(sound)
        scan_list = [music, sound]

        new_highscore = self.load_data(username, weapon, level, score)
        self.reset(play, SCREEN_W, SCREEN_H)

        game_over = True
        cursor = 0

        self.timer_list[0].frame_num = 0
        browser = 1
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
                        browser = 0
                        run = False

                # Keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: # Up select
                        if cursor > 0:
                            cursor -= 1
                        else: cursor = len(self.command_list) - 1
                        self.command_list[cursor].select_effect(True)

                        self.board.show = False
                        self.select_fx.play()

                    if event.key == pygame.K_DOWN: # Down select
                        if cursor < len(self.command_list) - 1:
                            cursor += 1
                        else: cursor = 0
                        self.command_list[cursor].select_effect(True)

                        self.board.show = False
                        self.select_fx.play()

                    if event.key == pygame.K_SPACE: # Return Main menu
                        browser = 1
                        run = False
                        self.confirm_fx.play()

                    if event.key == pygame.K_RETURN: # Confirm DOWN
                        self.command_list[cursor].trigger = True
                        self.command_list[cursor].active_effect(True)

                        self.confirm_fx.play()

                    if event.key == pygame.K_ESCAPE: # Quit game
                        pygame.quit()
                        sys.exit()

                    # Reset the inactivity timer by pressing any key
                    self.timer_list[0].frame_num = 0

                # keyboard release
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN: # Confirm UP
                        # Button - Top-ranking & Continue
                        if self.command_list[0].trigger:
                            if play:
                                browser = -1
                                run = False
                            else:
                                for ranking in self.ranking_list:
                                    if self.ranking_list[-1].rect.y < SCREEN_H//5.5:
                                        ranking.delta_y += 40
                        # Button - Main-menu
                        elif self.command_list[1].trigger:
                            browser = 1
                            run = False

                        # Button - Credits
                        elif self.command_list[2].trigger:
                            self.board.show = not self.board.show
                            if self.board.show:
                                self.board.create_textline(CREDITS, center=(self.board.rect.centerx, self.board.rect.top))

                        # Button - Exit & Back
                        elif self.command_list[3].trigger:
                            if play: play = False
                            else:
                                pygame.quit()
                                sys.exit()

                        self.command_list[cursor].active_effect(False)

            # Clear screen and set background color
            self.screen.fill(pygame.Color('Black'))

            ''' --- AREA TO UPDATE AND DRAW --- '''

            if not self.board.show:
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

            for self.command in self.command_list:
                if self.command != self.command_list[cursor]:
                    self.command.select_effect(False)
                    self.command.trigger = False

                self.command.update()
                self.command.draw()

            self.board.update()
            self.board.draw()

            # Limit delay without event activity
            if self.timer_list[0].countdown(2, True):
                pygame.quit()
                sys.exit()
            # Show the last 10 seconds before closing the game
            if self.timer_list[0].frame_num > 6000:
                self.idle_time_view.text = f"The game will close in {self.timer_list[0].text_time[-2:]} seconds"
                self.idle_time_view.update()
                self.idle_time_view.draw()

            # Update screen
            pygame.display.update()

        return browser, play