import pygame

from .manager import player_select_function, explosion_2_img, explosion_dict
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT
from .tools import Sprite_sheet
from .weapons import Bullet, Missile


class Player(Sprite_sheet):

    def __init__(self, screen, select, score, speed, ammo, load, *args, **kwargs):
        player_img, player_action_dict = player_select_function(select)
        super().__init__(player_img)
        self.screen = screen
        self.select = select
        self.score = score
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.load = load
        self.start_load = load
        self.throw_cooldown = 0

        self.bullet_group    = args[0][0]
        self.missile_group   = args[0][1]
        self.enemy_group     = args[0][2]
        self.meteor_group    = args[0][3]
        self.explosion_group = args[0][4]

        # Load player image
        self.create_animation(100, 100, player_action_dict)
        self.sheet = pygame.image.load(explosion_2_img).convert_alpha()
        self.create_animation(100, 100, explosion_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        # Get player rect
        self.rect = self.image.get_rect(midtop=(SCREEN_WIDTH//2, SCREEN_HEIGHT))

        self.alive = True
        self.lives = 3
        self.health = 100
        self.max_health = self.health

        self.direction = -1
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
        self.check_alive()
        self.update_animation()
        self.move()
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1

    def move(self):
        # Reset movement variables
        self.delta_x = 0
        self.delta_y = 0

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
        # if pygame.sprite.spritecollide(self, args, False):
        #     self.health -= 10

    def shoot(self, *args):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 8
            # create bullet ammo
            bullet = Bullet(self, self.screen, self.select, self.rect.centerx, self.rect.top//1.1, self.direction,\
                            self.flip_x, self.flip_y, self.bullet_group, self.enemy_group, self.meteor_group)
            self.bullet_group.add(bullet)
            # Reduce ammo
            self.ammo -= 1
            args[1].play()
        # Sound if weapon is unloaded
        elif self.ammo == 0: args[0].play()

    def throw(self, *args):
        if self.throw_cooldown == 0 and self.load > 0:
            self.throw_cooldown = 400
            # Create missile load
            missile = Missile(self.screen, self.rect.centerx, self.rect.top, self.direction, self.flip_x, self.flip_y,\
                                self, self.enemy_group, self.meteor_group, self.explosion_group, args[1], args[2], args[3])
            self.missile_group.add(missile)
            # Reduce load
            self.load -= 1
            args[1].play()
        # Sound if weapon is unloaded
        elif self.load == 0: args[0].play()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action('destroy')
        else: self.update_action('idle')
