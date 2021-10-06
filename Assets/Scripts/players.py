import pygame

from .manager import player_select_function
from .tools import Sprite_sheet


class Player(Sprite_sheet):

    def __init__(self, screen, select, speed, **kwargs):
        player_img, player_action_dict = player_select_function(select)
        super().__init__(player_img)
        self.screen = screen
        self.speed = speed

        # Load player image
        self.create_animation(100, 100, player_action_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        # Get player rect
        self.rect = self.image.get_rect(**kwargs)

        self.delta_x = 0
        self.delta_y = 0

        # Define player action variables
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        # Update player events
        self.update_animation()
        self.move()

    def move(self):
        # Reset movement variables
        self.delta_x = 0
        self.delta_y = 0
        self.update_action('idle')

        # Assign bools if moving left or right or up or down
        if self.moving_left:
            self.delta_x = -self.speed
            self.update_action('left')

        if self.moving_right:
            self.delta_x = self.speed
            self.update_action('right')

        if self.moving_up:
            self.delta_y = -self.speed
            self.update_action('idle')

        if self.moving_down:
            self.delta_y = self.speed
            self.update_action('idle')


        # Update rectangle position
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
