import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, screen, speed, **kwargs):
        super().__init__()
        self.screen = screen
        self.speed = speed

        # Load player image
        self.image = pygame.image.load('Assets/Images/player.png').convert_alpha()
        # Get player rect
        self.rect = self.image.get_rect(**kwargs)

        self.delta_x = 0
        self.delta_y = 0

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        # Update player events
        self.move()

    def move(self):
        # Reset movement variables
        self.delta_x = 0
        self.delta_y = 0

        # Assign bools if moving left or right or up or down
        if self.moving_left:
            self.delta_x = -self.speed

        if self.moving_right:
            self.delta_x = self.speed

        if self.moving_up:
            self.delta_y = -self.speed

        if self.moving_down:
            self.delta_y = self.speed

        # Update rectangle position
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

    def draw(self):
        # Draw player on screen
        self.screen.blit(self.image, self.rect)
