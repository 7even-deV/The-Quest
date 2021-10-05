import pygame, random

from .manager import enemy_img, enemy_action_dict
from .tools import Sprite_sheet


class Enemy(Sprite_sheet):

    def __init__(self, screen, speed, **kwargs):
        super().__init__(enemy_img)
        self.screen = screen
        self.speed = speed

        # Load player image
        self.create_animation(100, 100, enemy_action_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        # Get player rect
        self.rect = self.image.get_rect(**kwargs)

        self.delta_x = 0
        self.delta_y = 0

        self.ai_moving_left = False
        self.ai_moving_right = False
        self.ai_moving_up = False
        self.ai_moving_down = False

        # AI specific variables
        self.idling = False
        self.direction_x = 1
        self.direction_y = 1
        self.move_counter = 0

    def update(self):
        # Update player events
        self.update_animation()
        self.ai()
        self.move()

    def move(self):
        # Reset movement variables
        self.delta_x = 0
        self.delta_y = 0
        self.update_action('idle')

        # Assign bools if moving left or right or up or down
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
            self.update_action('idle')

        if self.ai_moving_down:
            self.delta_y = self.speed
            self.direction_y = 1
            self.update_action('idle')

        # Update rectangle position
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

    def ai(self):
        pass
