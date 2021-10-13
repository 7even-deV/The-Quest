import pygame, random

from .manager import planet_img, planet_dict
from .tools import Sprite_sheet


class Foreground():

    def __init__(self, screen, screen_width, screen_height, *args):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.pos_list = []
        for star in range(*args):
            pos_x = random.randint(0, self.screen_width)
            pos_y = random.randint(0, self.screen_height)
            self.pos_list.append([pos_x, pos_y])

    def update(self, delta_x, delta_y):
        # Follow the self.bg_img with the Player
        self.fg_x = -(delta_x / 5)
        self.fg_y = 0.5 + delta_y

    def draw(self):
        # Draw randomly placed stars on the screen
        for pos in self.pos_list:
            color = random.randint(0, 255)
            radius = random.randint(0, 4)
            pygame.draw.circle(self.screen, (color, color, color), pos, radius)
            pos[0] += self.fg_x
            pos[1] += self.fg_y
            # Random reset from top when loop ends down
            if pos[1] > self.screen_height:
                pos[0] = random.randint(0, self.screen_width)
                pos[1] = 0


class Background():

    def __init__(self, screen, screen_width, screen_height, *args):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_img = pygame.image.load(*args).convert_alpha()
        self.bg_x = 0
        self.bg_y = 0

    def update(self, delta_x, delta_y):
        # Follow the self.bg_img movement with the Player from the center of the screen
        self.relative_x = self.bg_x + (self.screen_width // 2 - self.bg_img.get_rect().width // 2)
        # Move the self.bg_y of the self.bg_img and increase the speed with self.player.turbo
        self.relative_y = self.bg_y % self.bg_img.get_rect().height

        # Follow the self.bg_img with the Player
        self.bg_x += -(delta_x / 5)
        self.bg_y += 0.5 + delta_y

    def draw(self):
        # Repeat self.bg_img in loop
        self.screen.blit(self.bg_img, (self.relative_x, self.relative_y - self.bg_img.get_rect().height))
        # Recover what was lost from the self.bg_img
        if self.relative_y < self.screen_height:
            self.screen.blit(self.bg_img, (self.relative_x, self.relative_y))


class Farground():

    def __init__(self, screen, screen_width, screen_height, *args):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fg_x = 0
        self.fg_y = 0

        self.pos_list = []
        for star in range(*args):
            pos_x = random.randint(0, self.screen_width)
            pos_y = random.randint(0, self.screen_height)
            self.pos_list.append([pos_x, pos_y])

    def update(self, delta_x, delta_y):
        # Follow the self.bg_img with the Player
        self.fg_x = -(delta_x / 5)
        self.fg_y = 0.5 + delta_y

    def draw(self):
        # Draw randomly placed stars on the screen
        for pos in self.pos_list:
            color = random.randint(0, 255)
            radius = random.randint(0, 4)
            pygame.draw.circle(self.screen, (color, color, color), pos, radius)
            pos[0] += self.fg_x
            pos[1] += self.fg_y
            # Random reset from top when loop ends down
            if pos[1] > self.screen_height:
                pos[0] = random.randint(0, self.screen_width)
                pos[1] = 0


class Planet(Sprite_sheet):

    def __init__(self, screen, **kwargs):
        super().__init__(planet_img)
        self.screen = screen

        self.create_animation(700, 400, planet_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect  = self.image.get_rect(**kwargs)

        self.flip_y = True

    def update(self):
        self.update_action('planet_1')
        self.update_animation()
        self.draw()
