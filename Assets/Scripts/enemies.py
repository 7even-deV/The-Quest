import pygame
import random


class Enemy(pygame.sprite.Sprite):

    def __init__(self, screen, speed, **kwargs):
        super().__init__()
        self.screen = screen
        self.speed = speed

        # Load player image
        self.image = pygame.image.load('Assets/Images/enemy.png').convert_alpha()
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
        self.ai()
        self.move()

    def move(self):
        # Reset movement variables
        self.delta_x = 0
        self.delta_y = 0

        # Assign bools if moving left or right or up or down
        if self.ai_moving_left:
            self.delta_x = -self.speed
            self.direction_x = -1

        if self.ai_moving_right:
            self.delta_x = self.speed
            self.direction_x = 1

        if self.ai_moving_up:
            self.delta_y = -self.speed
            self.direction_y = -1

        if self.ai_moving_down:
            self.delta_y = self.speed
            self.direction_y = 1

        # Update rectangle position
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

    def ai(self):
        pass

    def draw(self):
        # Draw player on screen
        self.screen.blit(self.image, self.rect)
