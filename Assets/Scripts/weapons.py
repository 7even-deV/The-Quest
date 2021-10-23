import pygame

from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from .manager  import weapon_select_function, missile_img, missile_dict, missile_exp_img, missile_exp_dict
from .tools    import Sprite_sheet, Timer


class Bullet(Sprite_sheet):

    def __init__(self, origin, screen, select, x, y, direction, flip_x, flip_y, *args, **kwargs):
        bullet_img, weapon_dict = weapon_select_function(select)
        super().__init__(bullet_img)
        self.origin = origin
        self.screen = screen
        self.select = select
        self.speed  = 15

        # Load bullet image
        self.create_animation(50, 50, weapon_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect  = self.image.get_rect(**kwargs)
        self.rect.center = (x, y)
        self.direction   = direction
        self.flip_x  = flip_x
        self.flip_y  = flip_y
        self.collide = False

        self.player         = args[0]
        self.bullet_group   = args[1]
        self.enemy_group    = args[2]
        self.obstacle_group = args[3]

        self.update_action('bullet')

    def update(self):
        # Update bullet events
        self.update_animation(10)

        if self.origin == 'player':
            self.player_shoot()
        elif self.origin == 'enemy':
            self.enemy_shoot()

        # Check if bullet has gone off screen
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill() # Kill the animation

        # Move bullet
        self.rect.y += self.speed * self.direction

    def player_shoot(self):
        if not self.collide:
            # Check for collision with enemies
            for enemy in self.enemy_group:
                if pygame.sprite.spritecollide(enemy, self.bullet_group, False):
                    if enemy.alive:
                        self.collide = True
                        enemy.health -= 25
                        self.player.score += enemy.exp

            # Check for collision with meteors
            for obstacle in self.obstacle_group:
                if pygame.sprite.spritecollide(obstacle, self.bullet_group, False):
                    self.collide = True
                    obstacle.health -= 10
                    self.player.score += obstacle.exp

        else: # If the bullet collide it stop and destroy
            self.update_action('destroy')
            self.speed = 0

    def enemy_shoot(self):
        if not self.collide:
            # Check collision with player
            if pygame.sprite.spritecollide(self.player, self.bullet_group, False):
                if self.player.alive and not self.player.win:
                    self.collide = True
                    self.player.health -= 10

        else: # If the bullet collide it stop and destroy
            self.update_action('destroy')
            self.speed = 0


class Missile(Sprite_sheet):

    def __init__(self, screen, x, y, direction, flip_x, flip_y, *args):
        super().__init__(missile_img)
        self.screen = screen

        # Load missile image
        self.create_animation(50, 50, missile_dict)
        self.image  = self.animation_dict[self.action][self.frame_index]
        self.width  = self.image.get_width()
        self.height = self.image.get_height()
        self.rect   = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction   = direction
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.image  = pygame.transform.flip(self.image, self.flip_x, self.flip_y)

        self.player          = args[0]
        self.enemy_group     = args[1]
        self.obstacle_group  = args[2]
        self.explosion_group = args[3]
        self.missile_fx      = args[4]
        self.missile_cd_fx   = args[5]
        self.explosion_fx    = args[6]

        self.speed = 1
        self.delta_x = 0
        self.delta_y = self.direction * self.speed
        self.countdown = 3
        self.timer = Timer(FPS)

    def update(self):
        # Update missile events
        self.update_animation(10)
        self.move()

        if self.countdown == 0:
            self.speed = 0.1
            self.kill() # Kill the animation
            self.explosion_fx.play()
            # Create the explosion
            explosion = Explosion(self.screen, center=(self.rect.x, self.rect.y))
            self.explosion_group.add(explosion)

            # Do damage to anyone that is nearby
            if abs(self.rect.centerx - self.player.rect.centerx) < self.width * 5 and\
            abs(self.rect.centery - self.player.rect.centery) < self.height * 5:
                self.player.collide = True
                self.player.health -= 50
                self.player.animation_cooldown = self.player.animation_cooldown // 4
                self.player.update_action('destroy')

            for enemy in self.enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < self.width * 5 and\
                abs(self.rect.centery - enemy.rect.centery) < self.height * 5:
                    enemy.collide = True
                    enemy.health -= 100
                    enemy.animation_cooldown = enemy.animation_cooldown // 4
                    enemy.update_action('destroy')

            for obstacle in self.obstacle_group:
                if abs(self.rect.centerx - obstacle.rect.centerx) < self.width * 5 and\
                abs(self.rect.centery - obstacle.rect.centery) < self.height * 5:
                    obstacle.collide = True
                    obstacle.health -= 100
                    obstacle.animation_cooldown = obstacle.animation_cooldown // 4
                    obstacle.update_action('destroy')

        else: self.update_action('missile')

    def move(self):
        self.delta_x = 0
        self.delta_y = self.direction * self.speed

        # Countdown timer
        if self.countdown > 0 and self.timer.counter(1.5, True):
            self.countdown -= 1
            if self.countdown > 0:
                self.missile_cd_fx.play()

        # Update missile position
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y


class Explosion(Sprite_sheet):
    def __init__(self, screen, **kwargs):
        super().__init__(missile_img)
        self.screen = screen
        # Load explosion image
        self.create_animation(50, 50, {'explosion': (5, 4, 12, 1)})
        self.sheet = pygame.image.load(missile_exp_img).convert_alpha()
        self.create_animation(500, 500, missile_exp_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect  = self.image.get_rect(**kwargs)

    def update(self):
        self.update_action('destroy')
        self.update_animation(50)
        self.draw()
