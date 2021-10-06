import pygame

from .manager import icon_type_function


class Timer():

    def __init__(self):
        self.counter = 0

    def time(self, timer, *events):
        self.counter += 1
        if self.counter > timer * 100:
            self.counter = 0
            return events


class Sprite_sheet(pygame.sprite.Sprite):

    def __init__(self, *args):
        self.sheet = pygame.image.load(*args).convert_alpha()
        self.animation_dict = {}
        self.update_time = pygame.time.get_ticks()
        self.action = 0
        self.frame_index = 0

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
        # Draw player on screen
        self.screen.blit(self.image, self.rect)


class Icon(Sprite_sheet):

    def __init__(self, screen, icon_type, **kwargs):
        icon_img, icon_type_dict = icon_type_function(icon_type)
        super().__init__(icon_img)
        self.screen = screen

        # Load icon image
        self.create_animation(100, 100, icon_type_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        # Get icon rect
        self.rect = self.image.get_rect(**kwargs)

    def update(self, select):
        # Update player events
        self.update_animation()
        self.icon_select(select)

    def icon_select(self, select):
        # Select icon type
        if select == 0:
            self.update_action('dps')
        if select == 1:
            self.update_action('tank')
        if select == 2:
            self.update_action('heal')
