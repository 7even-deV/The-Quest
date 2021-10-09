import pygame

from .manager import player_select_function
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT
from .tools import Sprite_sheet


class Player(Sprite_sheet):

    def __init__(self, screen, select, score, speed, **kwargs):
        player_img, player_action_dict = player_select_function(select)
        super().__init__(player_img)
        self.screen = screen
        self.speed = speed

        # Load player image
        self.create_animation(100, 100, player_action_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        # Get player rect
        self.rect = self.image.get_rect(midtop=(SCREEN_WIDTH//2, SCREEN_HEIGHT))

        self.alive = True
        self.lives = 3
        self.health = 100
        self.max_health = self.health
        self.score = score

        self.delta_x = 0
        self.delta_y = 0
        self.margin_x = self.rect.width // 10
        self.margin_y = self.rect.height // 10

        # Define player action variables
        self.spawn = True
        self.turbo = False
        self.collide = False

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
        if not self.spawn and not self.turbo and not self.collide:
            if self.moving_left:
                self.delta_x = -self.speed
                self.update_action('left')

            if self.moving_right:
                self.delta_x = self.speed
                self.update_action('right')

            if self.moving_up:
                self.delta_y = -self.speed

            if self.moving_down:
                self.delta_y = self.speed

        # Check if going off the edges of the screen
        if self.rect.left + self.delta_x < self.margin_x:
            if self.rect.left + self.delta_x < self.margin_x - 1:
                self.delta_x = 0.1
            else: self.delta_x = 0

        if self.rect.right + self.delta_x > SCREEN_WIDTH - self.margin_x:
            if self.rect.right + self.delta_x > SCREEN_WIDTH - self.margin_x + 1:
                self.delta_x = -0.1
            else: self.delta_x = 0

        if self.rect.top + self.delta_y < self.margin_y * 10:
            if self.rect.top + self.delta_y < self.margin_y * 10 - 1:
                self.delta_y = 0.1
            else: self.delta_y = 0

        if self.rect.bottom + self.delta_y > SCREEN_HEIGHT - self.margin_y:
            if self.rect.bottom + self.delta_y > SCREEN_HEIGHT - self.margin_y + 1:
                self.delta_y = -0.1
            else: self.delta_y = 0

        # Update rectangle position
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

    def check_collision(self, *args):
        # Check for collision
        for sprite in args:
            # Check for collision in the x direction
            if sprite.colliderect(self.rect.x + self.delta_x, self.rect.y, self.rect.w, self.rect.h):
                self.delta_x = 0

            # Check for collision in the y direction
            if sprite.colliderect(self.rect.x, self.rect.y + self.delta_y, self.rect.w, self.rect.h):
                self.delta_y = 0

        # Check if the collision with the enemy
        if pygame.sprite.spritecollide(self, args, False):
            # self.health -= 10
            pass
