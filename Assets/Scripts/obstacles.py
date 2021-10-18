import pygame, random

from .manager import meteor_img, meteor_action_dict, explosion_1_img, explosion_dict
from .tools import Sprite_sheet


class Meteor(Sprite_sheet):

    def __init__(self, screen, player, screen_width, screen_height):
        super().__init__(meteor_img)
        self.screen = screen
        self.player = player
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load meteor and explosion image
        self.create_animation(128, 128, meteor_action_dict)
        self.sheet = pygame.image.load(explosion_1_img).convert_alpha()
        self.create_animation(128, 128, {'destroy': (6, 8, 2)})
        self.image = self.animation_dict[self.action][self.frame_index]
        # Get random meteor rect
        self.rect = self.image.get_rect(center=(random.randint(0, self.screen_width), -random.randint(0, 5000)))

        self.scale = random.randint(1.0, 4.0)
        self.rect.width = self.rect.width // 4
        self.rect.height = self.rect.height // 4

        self.flip_x = random.randint(False, True)
        self.flip_y = random.randint(False, True)
        self.animation_cooldown = random.randint(10, 100)

        self.moving_x = False
        self.delta_x = 0
        self.delta_y = random.randint(1.0, 4.0)
        self.collide = False

        self.health = 100

    def update(self, speed_y):
        # Update meteor events
        self.update_animation(self.animation_cooldown, 1)

        if not self.moving_x and self.rect.bottom > 0:
            self.moving_x = True
            self.delta_x = random.randint(-1.0, 1.0)

        # Check if going off the edges of the screen
        if self.rect.right < 0 or self.rect.left > self.screen_width or self.rect.top > self.screen_height:
            self.kill() # Kill the object
        elif not self.collide:
            self.update_action('turn_l')

        # Update rectangle position
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y + speed_y

    def check_collision(self, sfx):
        if not self.collide and not self.player.win:
            margin_width = self.rect.width // 10
            margin_height = self.rect.height // 10
            if self.rect.right >= self.player.rect.left + margin_width and self.rect.left <= self.player.rect.right - margin_width and \
                self.rect.bottom >= self.player.rect.top + margin_height and self.rect.top <= self.player.rect.bottom - margin_height:
                self.collide = True
                self.player.collide = True
                self.player.rect.x += (self.delta_x - self.player.delta_x) * 2
                self.player.rect.y += (self.delta_y - self.player.delta_y) * 2
                self.player.health -= self.scale * 10
                self.player.score += self.scale * 10
                self.delta_x = self.delta_y = 0
                self.animation_cooldown = self.animation_cooldown // 4
                self.update_action('destroy')
                sfx.play()
