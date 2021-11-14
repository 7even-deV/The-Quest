import pygame, random

from .settings import FPS
from .manager  import button_def, key_def, bar_def, board_def, item_def, logo_type_def, font_type_def, icon_type_def


class Timer():

    def __init__(self, FPS=FPS):
        self.count = 0
        self.start_time = pygame.time.get_ticks()
        self.frame_num = 0
        self.frame_rate = FPS
        self.text_time = f"{0:02}:{1:02}"

    # Time for seconds
    def time(self, timer, *events):
        self.count += 1
        if self.count > timer * 100:
            self.count = 0
            return events

    # Counter for seconds
    def counter(self, timer, *events):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > timer * 1000:
            self.start_time = pygame.time.get_ticks()
            return events

    # Delay for seconds
    def delay(self, timer, *events):
        # Calculate time left
        self.time_left = self.frame_num // self.frame_rate
        # Divide by 60 to get total minutes
        minutes = self.time_left // 60
        # Use the modulo operator to get the seconds
        seconds = self.time_left % 60

        if self.time_left == timer:
            return events

    # Countdown for minutes
    def countdown(self, timer, *events):
        self.level_time = timer * 60
        # Calculate time left
        self.time_left = self.level_time - (self.frame_num // self.frame_rate)
        # Divide by 60 to get total minutes
        minutes = self.time_left // 60
        # Use the modulo operator to get the seconds
        seconds = self.time_left % 60
        # Use string format for leading zeros
        self.text_time = "{0:02}:{1:02}".format(minutes, seconds)

        self.frame_num += 1

        if self.time_left < 0:
            self.time_left = 0
            self.frame_num = 0
            return events

    # Level timer for minutes
    def level_timer(self, timer, player, *events):
        self.level_time = timer * 60
        # Calculate time left
        self.time_left = self.level_time - (self.frame_num // self.frame_rate)
        # Divide by 60 to get total minutes
        minutes = self.time_left // 60
        # Use the modulo operator to get the seconds
        seconds = self.time_left % 60
        # Use string format for leading zeros
        self.text_time = "{0:02}:{1:02}".format(minutes, seconds)

        # Reduce time if turbo or item time is used
        if player.turbo and player.less_time:
            self.frame_num += 4
        elif player.turbo or player.less_time:
            self.frame_num += 2
        else: self.frame_num += 1
        self.frame_num += player.turbo_up

        if self.time_left < 0:
            self.time_left = 0
            self.frame_num = 0
            return events


class View(pygame.sprite.Sprite):

    def __init__(self, screen, text='', letter=3, size=14, color=pygame.Color('White'), **kwargs):
        super().__init__()
        self.screen = screen
        self.text   = text
        self.letter = letter
        self.size   = size
        self.color  = color

        self.kwargs = kwargs

        self.font  = pygame.font.Font(font_type_def(self.letter), self.size)
        self.image = self.font.render(self.text, True, self.color)
        self.rect  = self.image.get_rect(**self.kwargs)

        self.delta_x = 0
        self.delta_y = 0
        self.fade = 0

    def update(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect  = self.image.get_rect(**self.kwargs)

        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

    def compare(self, *args):
        if args[0] > args[1]:
            self.text = args[2]
            self.color = pygame.Color('Red')
        else:
            self.text = args[3]
            self.color = pygame.Color('Orange')

    def draw(self):
        self.screen.blit(self.image, self.rect)


class Sprite_sheet(pygame.sprite.Sprite):

    def __init__(self, *args):
        super().__init__()
        self.sheet = pygame.image.load(*args).convert_alpha()
        self.animation_dict = {}
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.animation_cooldown = 100

        self.scale  = 1
        self.flip_x = False
        self.flip_y = False
        self.rotate = 0

    def get_image(self, width, height, frame_x, frame_y, scale):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame_x * width), (frame_y * height), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(False)

        return image

    def create_animation(self, width, height, *args, scale=1):
        # Autocomplete values from frame_dict
        frame_dict = args == () and {0: (1, 1, 1, 1)} or args[0]
        frame_dict[0] = (1, 1, 1, 1)
        counter_x = counter_y = 0

        for key, value in frame_dict.items():
            if type(value) is not tuple: value = [value]
            value = list(value)
            while len(value) < 4: value.append(0)

            else:
                temp_img_list = []

                # Place frame_x if indicated
                if value[2] != 0: counter_y = value[2] - 1
                for _y in range(value[1]):
                    counter_x = 0

                    # Place frame_y if indicated
                    if value[3] != 0: counter_x = value[3] - 1
                    for _x in range(value[0]):
                        temp_img_list.append(self.get_image(width, height, counter_x, counter_y, scale))
                        counter_x += 1
                    counter_y += 1

                self.animation_dict[key] = temp_img_list

        return self.animation_dict

    def update_animation(self, animation_cooldown=100, repeated_frame=0):
        # Update image depending on current frame
        self.image = self.animation_dict[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks() # Current time
            self.frame_index += 1
        # If the animation has move out the reset back to the start
        if self.frame_index >= len(self.animation_dict[self.action]) - repeated_frame:
            # Stop animation
            if self.action == 'death':
                self.frame_index = len(self.animation_dict[self.action]) - 1
            # Delete animation
            elif self.action == 'destroy':
                self.kill()
            # Loop animation
            else: self.frame_index = 0

    def update_action(self, new_action):
        # Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update(self):
        # Update the first action by default
        self.update_action(list(self.animation_dict)[0])
        self.update_animation()

    def draw(self):
        image = pygame.transform.scale(self.image, (self.rect.width * self.scale, self.rect.height * self.scale))
        image = pygame.transform.flip(image, self.flip_x, self.flip_y)
        image = pygame.transform.rotate(image, self.rotate)
        image.set_colorkey(False)
        self.screen.blit(image, self.rect)


class Logo(Sprite_sheet):
    def __init__(self, screen, logo, **kwargs):
        logo_img, logo_dict, logo_size = logo_type_def(logo)
        super().__init__(logo_img)
        self.screen = screen

        # Create image and rect
        self.create_animation(logo_size[0], logo_size[1], logo_dict)
        self.image  = self.animation_dict[self.action][self.frame_index]
        self.rect   = self.image.get_rect(**kwargs)


class Button(Sprite_sheet):
    def __init__(self, screen, text, letter=4, size=24, color=pygame.Color('Black'), **kwargs):
        button_img, button_dict = button_def()
        super().__init__(button_img)
        self.create_animation(250, 75, button_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect  = self.image.get_rect(**kwargs)

        self.screen = screen
        self.text   = text
        self.letter = letter
        self.size   = size
        self.color  = color

        self.font = pygame.font.Font(font_type_def(self.letter), self.size)
        self.font_render = self.font.render(self.text, True, self.color)
        self.text_rect   = self.font_render.get_rect(center=(self.rect.centerx, self.rect.centery))

        self.arrow_l = View(self.screen, '<- ', letter=1, size=24, midright=(self.rect.left, self.rect.centery))
        self.arrow_r = View(self.screen, ' ->', letter=1, size=24, midleft=(self.rect.right, self.rect.centery))

        self.trigger = False
        self.many    = False

    def update(self):
        self.update_animation()
        self.font = pygame.font.Font(font_type_def(self.letter), self.size)
        self.font_render = self.font.render(self.text, True, self.color)
        self.text_rect   = self.font_render.get_rect(center=(self.rect.centerx, self.rect.centery))
        if self.many:
            self.arrow_l.update()
            self.arrow_r.update()

    def select_effect(self, select):
        # Make selection effect
        if select:
            self.update_action('on')
            self.color = pygame.Color('White')
        else:
            self.update_action('off')
            self.color = pygame.Color('Black')

    def active_effect(self, active):
        # Make activation effect
        if active:
            self.rect.x += 2
            self.rect.y += 2
            self.rect.w -= 4
            self.rect.h -= 4

            self.color = pygame.Color('Yellow')
            self.text_rect.x += 3
            self.text_rect.y += 1
            self.size -= 1
        else:
            self.rect.x -= 2
            self.rect.y -= 2
            self.rect.w += 4
            self.rect.h += 4

            self.color = pygame.Color('White')
            self.text_rect.x -= 3
            self.text_rect.y -= 1
            self.size += 1

    def draw(self):
        image = pygame.transform.scale(self.image, (self.rect.w * self.scale, self.rect.h * self.scale))
        image = pygame.transform.flip(image, self.flip_x, self.flip_y)
        image.set_colorkey(False)
        self.screen.blit(image, self.rect)
        self.screen.blit(self.font_render, self.text_rect)
        if self.many:
            self.arrow_l.draw()
            self.arrow_r.draw()


class Keyboard(Sprite_sheet):
    def __init__(self, screen, text, letter=4, size=24, color=pygame.Color('Black'), **kwargs):
        key_img, key_dict = key_def()
        super().__init__(key_img)
        self.create_animation(50, 50, key_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect  = self.image.get_rect(**kwargs)

        self.screen = screen
        self.text   = text
        self.letter = letter
        self.size   = size
        self.color  = color

        self.font = pygame.font.Font(font_type_def(self.letter), self.size)
        self.font_render = self.font.render(self.text, True, self.color)
        self.text_rect   = self.font_render.get_rect(center=(self.rect.centerx, self.rect.centery))
        self.trigger = False

    def update(self):
        self.update_animation()
        self.font = pygame.font.Font(font_type_def(self.letter), self.size)
        self.font_render = self.font.render(self.text, True, self.color)
        self.text_rect   = self.font_render.get_rect(center=(self.rect.centerx, self.rect.centery))

    def select_effect(self, select):
        # Make selection effect
        if select:
            self.update_action('on')
            self.color = pygame.Color('White')
        else:
            self.update_action('off')
            self.color = pygame.Color('Black')

    def active_effect(self, active):
        # Make activation effect
        if active:
            self.rect.x += 2
            self.rect.y += 2
            self.rect.w -= 4
            self.rect.h -= 4

            self.color = pygame.Color('Yellow')
            self.text_rect.x += 3
            self.text_rect.y += 1
            self.size -= 1
        else:
            self.rect.x -= 2
            self.rect.y -= 2
            self.rect.w += 4
            self.rect.h += 4

            self.color = pygame.Color('White')
            self.text_rect.x -= 3
            self.text_rect.y -= 1
            self.size += 1

    def draw(self):
        image = pygame.transform.scale(self.image, (self.rect.w * self.scale, self.rect.h * self.scale))
        image.set_colorkey(False)
        self.screen.blit(image, self.rect)
        self.screen.blit(self.font_render, self.text_rect)


class Bar(Sprite_sheet):
    def __init__(self, screen, text, letter=4, size=20, color=pygame.Color('White'), **kwargs):
        bar_img, bar_dict = bar_def()
        super().__init__(bar_img)
        self.create_animation(300, 50, bar_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect  = self.image.get_rect(**kwargs)

        self.screen = screen
        self.text   = text
        self.letter = letter
        self.size   = size
        self.color  = color

        self.font = pygame.font.Font(font_type_def(self.letter), self.size)
        self.font_render = self.font.render(self.text, True, self.color)
        self.text_rect   = self.font_render.get_rect(midright=(self.rect.left - self.rect.width//12, self.rect.centery))

        self.gage = Keyboard(self.screen, '', letter=0, size=size, center=(self.rect.centerx, self.rect.centery))

        self.show = False

        self.update_action('displace')

    def update(self):
        self.update_animation()
        self.font = pygame.font.Font(font_type_def(self.letter), self.size)
        self.font_render = self.font.render(self.text, True, self.color)

        self.gage.update()
        self.gage.text_rect.x = self.rect.right + self.rect.width//12

    def displace_effect(self, vol_scan):
        # Make scrolling effect calculating the volume of the database user
        self.gage.rect.x = self.rect.width//1.25 * vol_scan + self.rect.x

        if self.gage.trigger:
            self.gage.select_effect(True)
            self.gage.color = pygame.Color('Yellow')
            self.color      = pygame.Color('Yellow')
        else:
            self.gage.select_effect(False)
            self.gage.color = pygame.Color('White')
            self.color      = pygame.Color('White')

        if vol_scan == 0.0:
            self.gage.text = "min"
            self.gage.color = pygame.Color('Orange')
        elif vol_scan == 1.0:
            self.gage.text = "max"
            self.gage.color = pygame.Color('Orange')
        else:
            self.gage.text = str(vol_scan)

    def draw(self):
        image = pygame.transform.scale(self.image, (self.rect.w * self.scale, self.rect.h * self.scale))
        image.set_colorkey(False)
        self.screen.blit(image, self.rect)
        self.screen.blit(self.font_render, self.text_rect)
        self.gage.draw()


class Board(Sprite_sheet):
    def __init__(self, screen, document='', letter=4, size=16, color=pygame.Color('Black'), **kwargs):
        board_img, board_dict = board_def()
        super().__init__(board_img)
        self.create_animation(600, 300, board_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect  = self.image.get_rect(**kwargs)

        self.screen = screen
        self.letter = letter
        self.size   = size
        self.color  = color
        self.create_textline(document, **kwargs)

        self.show = False

    def update(self):
        self.move(15)
        self.update_animation()

    def move(self, speed_y):
        if self.show:
            if self.rect.top < 0:
                self.rect.y += speed_y
                for rect in self.rect_list:
                    rect.y += speed_y
        else:
            if self.rect.bottom > 0:
                self.rect.y -= speed_y
                for rect in self.rect_list:
                    rect.y -= speed_y

    def create_textline(self, document, **kwargs):
        self.text_list = []
        temp_var = ''
        for char in document:
            temp_var += char

            if char in '/':
                temp_var = temp_var[1:-1]
                self.text_list.append(temp_var)
                temp_var = ''

        self.text_list.append(temp_var[:-1])

        self.font_list = []
        self.rect_list = []
        for line, index in zip(self.text_list, range(len(self.text_list))):
            font = pygame.font.Font(font_type_def(self.letter), self.size)
            self.font_list.append(font.render(line, True, self.color))
            rect = self.font_list[index].get_rect(**kwargs)
            self.rect_list.append(rect)

    def draw(self):
        self.image.set_colorkey(False)
        self.screen.blit(self.image, self.rect)

        for font, rect, index in zip(self.font_list, self.rect_list, range(len(self.rect_list))):
            self.screen.blit(font, (rect.x, rect.top + rect.height * index + self.rect.height//7.5))


class Canvas(Sprite_sheet):

    def __init__(self, screen, icon, color, x=0, y=0, **kwargs):
        item_img, item_dict, item_get_img = item_def()
        super().__init__(item_img)
        self.screen = screen

        # Create image and rect
        self.create_animation(100, 100, item_dict, scale=0.4)
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect  = self.image.get_rect(**kwargs)

        self.update_action(icon)

        color_list = [pygame.Color('Yellow'), pygame.Color('Cyan')]
        self.view  = View(self.screen, color=color_list[color], midtop=(self.rect.centerx + x, self.rect.bottom + y))

    def update(self):
        self.update_animation()
        self.view.update()

    def switch(self, get_player_item):
        if get_player_item:
            self.view.text = 'on'
            self.view.color = pygame.Color('Green')
        else:
            self.view.text = 'off'
            self.view.color = pygame.Color('Red')

    def draw(self):
        self.image.set_colorkey(False)
        self.screen.blit(self.image, self.rect)
        self.view.draw()


class Icon(Sprite_sheet):

    def __init__(self, screen, icon_type, scale, **kwargs):
        icon_img, icon_dict = icon_type_def(icon_type)
        super().__init__(icon_img)
        self.screen = screen

        # Create image and rect
        self.create_animation(200, 200, icon_dict, scale=scale)
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect  = self.image.get_rect(**kwargs)

        self.ratio = 0
        self.max_ratio = self.rect.width//1.4
        self.particles = Particles('select', self.screen, self.image)

    def update(self, select, model, confirm=None, **kwargs):
        # Update player events
        self.icon_select(select, model)
        self.update_animation()
        if not confirm:
            if self.ratio < self.max_ratio: self.ratio += 1
            pygame.draw.circle(self.screen, False, (self.rect.centerx, self.rect.centery), self.ratio)
            self.particles.add_icon(self.rect.centerx, self.rect.centery, select)
        else:
            if self.ratio > 0: self.ratio -= 1
            pygame.draw.circle(self.screen, False, (self.rect.centerx, self.rect.centery), self.ratio)

    def icon_select(self, select, model):
        # Select icon type
        if select == 0:
            self.update_action(f'dps_{model+1}')
        if select == 1:
            self.update_action(f'tank_{model+1}')
        if select == 2:
            self.update_action(f'heal_{model+1}')

    def trigger_effect(self, active):
        # Make activation effect
        if active:
            self.rect.x += 2
            self.rect.y += 2
            self.rect.width -= 4
            self.rect.height -= 4
        else:
            self.rect.x -= 2
            self.rect.y -= 2
            self.rect.width += 4
            self.rect.height += 4


class Health_bar():
    def __init__(self, screen, health, SCREEN_W, SCREEN_H):
        self.screen = screen
        self.health = health
        self.max_health = self.health
        self.w = SCREEN_W
        self.h = SCREEN_H
        self.color_list = [pygame.Color('Gray'), pygame.Color('Red'), pygame.Color('Green')]

        self.view = View(self.screen, color=pygame.Color('Black'), midleft=(self.w*0.02, self.h*0.024))

    def draw(self, health):
        # Update with new health
        self.health = health
        # Calculate health ratio
        ratio = self.health / self.max_health

        pygame.draw.rect(self.screen, self.color_list[0], (self.w*0.015-2, self.h*0.015-2, self.w*0.208,     self.h*0.025))
        pygame.draw.rect(self.screen, self.color_list[1], (self.w*0.015,   self.h*0.015,   self.w*0.2,       self.h*0.02))
        pygame.draw.rect(self.screen, self.color_list[2], (self.w*0.015,   self.h*0.015,   self.w*0.2*ratio, self.h*0.02))

        self.view.update()
        self.view.draw()


class Screen_fade():

    def __init__(self, screen, direction, colour, speed, SCREEN_W, SCREEN_H):
        self.screen    = screen
        self.direction = direction
        self.colour    = colour
        self.speed     = speed
        self.fade_counter  = 0
        self.fade_complete = False
        self.SCREEN_W = SCREEN_W
        self.SCREEN_H = SCREEN_H

    def fade(self):
        self.fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 'intro': # Whole screen fade
            pygame.draw.rect(self.screen, self.colour, (0 - self.fade_counter, 0, self.SCREEN_W // 2, self.SCREEN_H)) # Opening left
            pygame.draw.rect(self.screen, self.colour, (self.SCREEN_W // 2 + self.fade_counter, 0, self.SCREEN_W, self.SCREEN_H)) # Opening right
            # pygame.draw.rect(self.screen, self.colour, (0, 0 - self.fade_counter, self.SCREEN_W, self.SCREEN_H)) # Opening up
            # pygame.draw.rect(self.screen, self.colour, (0, self.SCREEN_H // 2 + self.fade_counter, self.SCREEN_W, self.SCREEN_H)) # Opening down
        if self.direction == 'death': # Vertical screen fade down
            pygame.draw.rect(self.screen, self.colour, (0, 0, self.SCREEN_W, 0 + self.fade_counter))

        if self.fade_counter > self.SCREEN_H:
            self.fade_complete = True

        return self.fade_complete


class Particles():

    def __init__(self, particle_type, screen, image, select=-1):
        self.particle_type = particle_type
        self.screen = screen
        self.image  = image
        self.width  = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.size   = 10

        if   self.particle_type == 'item':
            self.color_list = [pygame.Color('Gray'), pygame.Color('White')]

        elif self.particle_type == 'select':
            if   select == 0: self.color_list = [pygame.Color('Red')]
            elif select == 1: self.color_list = [pygame.Color('Blue')]
            elif select == 2: self.color_list = [pygame.Color('Green')]
            else:             self.color_list = [pygame.Color('Yellow')]

        elif self.particle_type == 'fire':
            self.color_list = [pygame.Color('Orange'), pygame.Color('Yellow'), pygame.Color('Cyan'), pygame.Color('Gray')]

        self.particle_list = []

    def add_icon(self, pos_x, pos_y, select):
        if   select == 0: self.color_list = [pygame.Color('Red')]
        elif select == 1: self.color_list = [pygame.Color('Blue')]
        elif select == 2: self.color_list = [pygame.Color('Green')]
        else:             self.color_list = [pygame.Color('Yellow')]

        colour = random.randint(0, len(self.color_list) -1)
        number = random.randint(1, 10)
        move_x = random.randint(-number, number)
        move_y = random.randint(-number, number)
        radius = random.randint(1, 5)

        self.particle_list.append([self.color_list[colour], [pos_x, pos_y], [move_x, move_y], radius])

        for particle in self.particle_list:
            particle[1][0] += particle[2][0]
            particle[1][1] += particle[2][1]
            particle[3] -= 0.05
            pygame.draw.circle(self.screen, particle[0], particle[1], int(particle[3]))
            if particle[3] <= 0:
                self.particle_list.remove(particle)

    def add_item(self, pos_x, pos_y, direction_x, direction_y):
        colour = random.randint(0, 255)
        move_x = random.randint(-3, 3)
        move_y = random.randint(-3, 3)
        radius = random.randint(1, 5)

        self.particle_list.append([(colour, colour, colour), [pos_x, pos_y], [move_x, move_y], radius])

        for particle in self.particle_list:
            particle[1][0] += particle[2][0] * direction_x * -1
            particle[1][1] += particle[2][1] * direction_y * -1
            particle[3] -= 0.05
            pygame.draw.circle(self.screen, particle[0], particle[1], int(particle[3]))
            if particle[3] <= 0:
                self.particle_list.remove(particle)

    def add_shoot(self, pos_x, pos_y, direction_x, direction_y):
        colour = random.randint(0, len(self.color_list) -1)
        move_x = 0
        move_y = random.randint(0, 1)
        radius = random.randint(2, 6)

        self.particle_list.append([self.color_list[colour], [pos_x, pos_y], [move_x, move_y], radius])

        for particle in self.particle_list:
            particle[1][0] += particle[2][0] * direction_x * -1
            particle[1][1] += particle[2][1] * direction_y * -1
            particle[2][1] += 0.1
            particle[3] -= 1
            pygame.draw.circle(self.screen, particle[0], particle[1], int(particle[3]))
            if particle[3] <= 0:
                self.particle_list.remove(particle)

    def add_circle(self, pos_x, pos_y, direction_x, direction_y):
        colour = random.randint(0, len(self.color_list) -1)
        move_x = random.randint(0, 8) / 4 -1
        # move_x = 0
        move_y = random.randint(0, 1)
        radius = random.randint(2, 6)

        self.particle_list.append([self.color_list[colour], [pos_x, pos_y], [move_x, move_y], radius])

        for particle in self.particle_list:
            particle[1][0] += particle[2][0] * direction_x * -1
            particle[1][1] += particle[2][1] * direction_y * -1
            particle[2][1] += 0.1
            particle[3] -= 0.3
            pygame.draw.circle(self.screen, particle[0], particle[1], int(particle[3]))
            if particle[3] <= 0:
                self.particle_list.remove(particle)

    def add_rect(self, pos_x, pos_y, direction_x, direction_y):
        particle_rect = pygame.Rect(int(pos_x - self.size/2), int(pos_y - self.size/2), self.size, self.size)
        colour = random.randint(0, len(self.color_list) -1)
        self.particle_list.append((particle_rect, self.color_list[colour]))

        for particle in self.particle_list:
            particle[0].y += 1
            pygame.draw.rect(self.screen,particle[1], particle[0])
            if particle[0].y <= 0:
                self.particle_list.remove(particle)

        rect = self.image.get_rect(center=(pos_x, pos_y))
        self.screen.blit(self.image, rect)

    def add_image(self, pos_x, pos_y, direction_x, direction_y):
        _x  = pos_x - self.width  / 2
        _y  = pos_y - self.height / 2
        move_x = random.randint(-2, 2)
        move_y = random.randint(1, 2)
        lifetime = random.randint(4, 10)
        particle_rect = pygame.Rect(int(_x), int(_y), self.width, self.height)
        self.particle_list.append([particle_rect, move_x, move_y, lifetime])
        if self.particle_list:
            self.del_image()
            for particle in self.particle_list:
                particle[0].x += particle[1]
                particle[0].y += particle[2]
                particle[3] -= 0.2
                self.screen.blit(self.image, particle[0])
                # if particle[3].y <= 0:
                #     self.particle_list.remove(particle)

    def del_image(self):
        particle_copy = [particle for particle in self.particle_list if particle[3] > 0]
        self.particle_list = particle_copy
