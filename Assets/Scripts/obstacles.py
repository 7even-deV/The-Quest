import pygame, random

from .manager import meteor_img, meteor_action_dict, explosion_1_img, explosion_dict
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, METEOR_SCALE
from .tools import Sprite_sheet


class Meteor(Sprite_sheet):

    def __init__(self, screen, player):
        super().__init__(meteor_img)
        self.screen = screen
        self.player = player

        # Load meteor and explosion image
        self.create_animation(100, 100, meteor_action_dict)
        self.sheet = pygame.image.load(explosion_1_img).convert_alpha()
        self.create_animation(100, 100, {'destroy': (6, 8, 2)})
        self.image = self.animation_dict[self.action][self.frame_index]
        # Get random meteor rect
        self.rect = self.image.get_rect(center=(random.randint(0, SCREEN_WIDTH), -random.randint(0, 5000)))

        self.scale = random.randint(1, METEOR_SCALE)
        self.rect.width  = self.rect.width  // METEOR_SCALE
        self.rect.height = self.rect.height // METEOR_SCALE

        self.flip_x = random.randint(False, True)
        self.flip_y = random.randint(False, True)
        self.animation_cooldown = random.randint(10, 100)

        self.moving_x = False
        self.delta_x = 0
        self.delta_y = random.randint(1, 4)
        self.collide = False

        self.alive  = True
        self.health = self.scale * 10
        self.max_health = self.health
        self.exp = self.scale * 10

    def update(self, speed_y):
        # Update meteor events
        self.check_alive()
        self.update_animation(self.animation_cooldown, 1)

        if not self.moving_x and self.rect.bottom > 0:
            self.moving_x = True
            self.delta_x = random.randint(-1, 1)

        # Check if going off the edges of the screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.top > SCREEN_HEIGHT:
            self.kill() # Kill the object

        # Update rectangle position
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y + speed_y

    def check_collision(self, sfx):
        if not self.collide and not self.player.win and self.player.alive:
            # margin_width  = self.rect.width // 10
            # margin_height = self.rect.height // 10
            margin_width  = 0
            margin_height = 0
            if self.rect.right  >= self.player.rect.left + margin_width and self.rect.left <= self.player.rect.right - margin_width and \
                self.rect.bottom >= self.player.rect.top + margin_height and self.rect.top <= self.player.rect.bottom - margin_height:
                self.collide = True
                self.player.collide = True
                self.player.rect.x += (self.delta_x - self.player.delta_x) * 2
                self.player.rect.y += (self.delta_y - self.player.delta_y) * 2
                self.player.score  += self.exp
                self.player.health -= self.scale * 10
                self.health = 0
                sfx.play()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.exp = 0
            self.speed = 0
            self.animation_cooldown = self.animation_cooldown // 4
            self.update_action('destroy')
        else: self.update_action('turn_l')
