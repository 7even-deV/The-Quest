import pygame, random

from .manager import meteor_img, meteor_action_dict, explosion_img, explosion_dict
from .tools import Sprite_sheet


class Meteor(Sprite_sheet):

    def __init__(self, screen, screen_width, screen_height):
        super().__init__(meteor_img)
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load meteor and explosion image
        self.create_animation(128, 128, meteor_action_dict)
        self.sheet = pygame.image.load(explosion_img).convert_alpha()
        self.create_animation(128, 128, {'destroy': (6, 8, 2)})
        self.image = self.animation_dict[self.action][self.frame_index]
        # Get random meteor rect
        self.rect = self.image.get_rect(center=(random.randint(0, self.screen_width), -random.randint(0, 5000)))

        self.scale = random.randint(1.0, 4.0)
        self.rect.width = self.rect.width // 4 * self.scale
        self.rect.height = self.rect.height // 4 * self.scale

        self.flip_x = random.randint(False, True)
        self.flip_y = random.randint(False, True)
        self.animation_cooldown = random.randint(10, 100)

        self.moving_x = False
        self.delta_x = 0
        self.delta_y = random.randint(1.0, 2.0)

    def update(self, speed_y):
        # Update meteor events
        self.update_animation(self.animation_cooldown, 1)
        self.update_action('turn_l')

        if not self.moving_x and self.rect.bottom > 0:
            self.moving_x = True
            self.delta_x = random.randint(-1.0, 1.0)

        # Update rectangle position
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y + speed_y

    def draw(self):
        image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        image = pygame.transform.flip(image, self.flip_x, self.flip_y)
        image.set_colorkey(False)
        self.screen.blit(image, self.rect)
