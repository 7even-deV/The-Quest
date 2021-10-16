import pygame

from .manager import icon_type_function, button_img, button_dict, font_function, keyboard_tuple
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR


class Timer():

    def __init__(self, FPS):
        self.count = 0
        self.start_time = pygame.time.get_ticks()
        self.frame_num = 0
        self.frame_rate = FPS

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
    def countdown(self, timer, turbo=False, *events):
        self.level_time = timer * 60
        # Calculate time left
        self.time_left = self.level_time - (self.frame_num // self.frame_rate)
        # Divide by 60 to get total minutes
        minutes = self.time_left // 60
        # Use the modulo operator to get the seconds
        seconds = self.time_left % 60
        # Use string format for leading zeros
        self.text_time = "{0:02}:{1:02}".format(minutes, seconds)

        if turbo: # Reduce time if turbo is used
            self.frame_num += 2
        else: self.frame_num += 1

        if self.time_left < 0:
            self.time_left = 0
            self.frame_num = 0
            return events


class Sprite_sheet(pygame.sprite.Sprite):

    def __init__(self, *args):
        super().__init__()
        self.sheet = pygame.image.load(*args).convert_alpha()
        self.animation_dict = {}
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.animation_cooldown = 100

        self.scale = 1
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
            if self.action == 'destroy':
                self.kill() # Kill the animation
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        image = pygame.transform.scale(self.image, (self.rect.width * self.scale, self.rect.height * self.scale))
        image = pygame.transform.flip(image, self.flip_x, self.flip_y)
        image = pygame.transform.rotate(image, self.rotate)
        image.set_colorkey(False)
        self.screen.blit(image, self.rect)


class Button(Sprite_sheet):
    def __init__(self, text, letter=2, size=24, color=COLOR('BLACK'), **kwargs):
        super().__init__(button_img)
        self.create_animation(250, 75, button_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect  = self.image.get_rect(**kwargs)

        self.text   = text
        self.letter = letter
        self.size   = size
        self.color  = color

        self.font = pygame.font.Font(font_function(self.letter), self.size)
        self.font_render = self.font.render(self.text, True, self.color)
        self.text_rect   = self.font_render.get_rect(**kwargs)
        self.pos_x = self.text_rect.centerx - self.text_rect.width  // 2
        self.pos_y = self.text_rect.centery - self.text_rect.height // 2

        self.trigger = False

    def update(self):
        self.update_animation()
        self.font = pygame.font.Font(font_function(self.letter), self.size)
        self.font_render = self.font.render(self.text, True, self.color)

    def select_effect(self, select):
        # Make selection effect
        if select:
            self.update_action('on')
            self.color = COLOR('WHITE')
        else:
            self.update_action('off')
            self.color = COLOR('BLACK')

    def active_effect(self, active):
        # Make activation effect
        if active:
            self.rect.x += 2
            self.rect.y += 2
            self.rect.w -= 4
            self.rect.h -= 4

            self.color = COLOR('YELLOW')
            self.pos_x += 3
            self.pos_y += 1
            self.size -= 1
        else:
            self.rect.x -= 2
            self.rect.y -= 2
            self.rect.w += 4
            self.rect.h += 4

            self.color = COLOR('WHITE')
            self.pos_x -= 3
            self.pos_y -= 1
            self.size += 1

    def draw(self, screen):
        image = pygame.transform.scale(self.image, (self.rect.w * self.scale, self.rect.h * self.scale))
        image.set_colorkey(False)
        screen.blit(image, self.rect)
        screen.blit(self.font_render, (self.pos_x, self.pos_y))


class Canvas(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__()
        self._text = ""
        self.kwargs = kwargs

        self.x = self._keys('x') or self.is_right() or 20
        self.y = self._keys('y') or 10
        self.letter_f = self._keys('letter_f') or 0
        self.size = self._keys('size') or 28
        self.color = self._keys('color') or COLOR('WHITE')

        self.font = pygame.font.Font(font_function(self.letter_f), self.size)
        self.image = self.font.render(self._text, True, self.color)
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def update(self):
        self.image = self.font.render(self._text, True, self.color)
        self.rect = self.image.get_rect(x=self.x, y=self.y)
        self.is_left()
        self.is_center()
        self.is_right()
        self.is_right_text()

    def _keys(self, key):
        return key in self.kwargs.keys() and self.kwargs[key]

    def is_left(self):
        if self._keys('left'):
            self.x = SCREEN_WIDTH // 4

    def is_center(self):
        if self._keys('center'):
            self.x = SCREEN_WIDTH // 2 - self.rect.w // 2

    def is_right(self):
        if self._keys('right'):
            self.x = SCREEN_WIDTH - (20 + len(self.text) * 10)

    def is_right_text(self):
        if self._keys('right_text'):
            self.x = SCREEN_WIDTH - (20 + len(self.text) * 9)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)

    def draw(self, screen):
        screen.blit(self.image, (self.x*0.5, self.y*0.5))


class Keyboard(pygame.sprite.Sprite):

    def __init__(self, screen, letter_font=1, size=50, color=COLOR('WHITE')):
        super().__init__()
        self.screen = screen
        self.letter_font = letter_font
        self.color = color
        self.size = size

        self.font = pygame.font.Font(font_function(self.letter_font), self.size)
        self.keyboard_tuple = keyboard_tuple

        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT

    def update(self, index):
        self.text = self.font.render(self.keyboard_tuple[index], True, self.color)
        return self.keyboard_tuple[index]

    def trigger_effect(self, active):
        # Make activation effect
        if active:
            self.x += 2
            self.y += 2
            self.size -= 4
        else:
            self.x -= 2
            self.y -= 2
            self.size += 4

    def draw(self):
        self.screen.blit(self.text, (self.x*0.5, self.y*0.5))


class Icon(Sprite_sheet):

    def __init__(self, screen, icon_type, scale=4, **kwargs):
        icon_img, icon_type_dict = icon_type_function(icon_type)
        super().__init__(icon_img)
        self.screen = screen

        # Load icon image
        self.create_animation(100, 100, icon_type_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        # Get icon rect
        self.rect = self.image.get_rect(**kwargs)
        self.rect.width  = self.rect.width  // 4 * scale
        self.rect.height = self.rect.height // 4 * scale

    def update(self, select, model):
        # Update player events
        self.icon_select(select, model)
        self.update_animation()

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
            self.rect.x -= 2
            self.rect.y -= 2
            self.rect.width += 4
            self.rect.height += 4
        else:
            self.rect.x += 2
            self.rect.y += 2
            self.rect.width -= 4
            self.rect.height -= 4


class HealthBar():
    def __init__(self, screen, health, max_health):
        self.screen = screen
        self.health = health
        self.max_health = max_health

        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT

    def draw(self, health):
        # Update with new health
        self.health = health
        # Calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(self.screen, COLOR('BLACK'), (self.x*0.04 - 2, self.y*0.04 - 2, self.x*0.25, self.y*0.02))
        pygame.draw.rect(self.screen, COLOR('RED'),   (self.x*0.04, self.y*0.04, self.x*0.2, self.y*0.02))
        pygame.draw.rect(self.screen, COLOR('GREEN'), (self.x*0.04, self.y*0.04, self.x*0.2 * ratio, self.y*0.02))
