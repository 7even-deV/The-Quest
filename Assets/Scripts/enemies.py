import pygame, random

from .manager import enemy_img, enemy_action_dict, explosion_img
from .tools import Sprite_sheet


class Enemy(Sprite_sheet):

    def __init__(self, screen, speed, **kwargs):
        super().__init__(enemy_img)
        self.screen = screen
        self.speed = speed

        # Load enemy image
        self.create_animation(100, 100, enemy_action_dict)
        self.sheet = pygame.image.load(explosion_img).convert_alpha()
        self.create_animation(128, 128, {'destroy': (6, 8, 2)})
        self.image = self.animation_dict[self.action][self.frame_index]
        # Get enemy rect
        self.rect = self.image.get_rect(**kwargs)

        self.health = 100

        self.delta_x = 0
        self.delta_y = 0
        self.animation_cooldown = 100

        # Define enemy action variables
        self.ai_moving_left = False
        self.ai_moving_right = False
        self.ai_moving_up = False
        self.ai_moving_down = False
        self.collide = False

        # AI specific variables
        self.vision = pygame.Rect(0, 0, 300, 400)
        self.idling = False
        self.direction_x = 1
        self.direction_y = 1
        self.move_counter = 0

    def update(self):
        # Update enemy events
        self.update_animation(self.animation_cooldown)
        self.ai()
        self.move()

    def move(self):
        # Reset movement variables
        self.delta_x = 0
        self.delta_y = 0

        # Assign bools if moving left or right or up or down
        if not self.collide:
            if self.ai_moving_left:
                self.delta_x = -self.speed
                self.direction_x = -1
                self.update_action('left')

            if self.ai_moving_right:
                self.delta_x = self.speed
                self.direction_x = 1
                self.update_action('right')

            if self.ai_moving_up:
                self.delta_y = -self.speed
                self.direction_y = -1

            if self.ai_moving_down:
                self.delta_y = self.speed
                self.direction_y = 1

            self.update_action('idle')

        # Update rectangle position
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

    # def check_collision(self, *player):
    #     # Check if the collision with the player
    #     if pygame.sprite.spritecollide(self, player, False):
    #         self.update_action('destroy')

    def check_collision(self, other, sfx):
        if not self.collide:
            margin_width = other.rect.width // 4
            margin_height = other.rect.height // 4
            if self.rect.right >= other.rect.left + margin_width and self.rect.left <= other.rect.right - margin_width and \
                self.rect.bottom >= other.rect.top + margin_height and self.rect.top <= other.rect.bottom - margin_height:
                self.collide = True
                other.collide = True
                other.rect.x += (self.delta_x - other.delta_x) * 2
                other.rect.y += (self.delta_y - other.delta_y) * 2
                other.health -= 10
                self.delta_x = self.delta_y = 0
                self.animation_cooldown = self.animation_cooldown // 2
                self.update_action('destroy')
                sfx.play()

    def ai(self):
        pass
