import pygame

from .manager import bullet_select_def, missile_select_def
from .tools   import Sprite_sheet, Timer, Particles


class Bullet(Sprite_sheet):

    def __init__(self, origin, screen, weapon, select, x, y, w, direction, flip_x, flip_y, *args, **kwargs):
        bullet_img, bullet_dict, destroy_img = bullet_select_def(select)
        super().__init__(bullet_img)
        self.origin = origin
        self.weapon = weapon
        self.screen = screen
        self.select = select
        self.speed  = 15

        # Load bullet image
        self.create_animation(50, 50, bullet_dict, scale=0.5)
        self.sheet = pygame.image.load(destroy_img).convert_alpha()
        self.create_animation(50, 50, {'destroy': (5, 8, 1, 1)}, scale=0.5)
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect_list = []
        for i in range(self.weapon):
            self.rect = self.image.get_rect(center=(x - w//4 * (i-(self.weapon-1)/2), y))
            self.rect_list.append(self.rect)

        self.direction = direction
        self.flip_x  = flip_x
        self.flip_y  = flip_y
        self.collide = False

        self.player         = args[0]
        self.bullet_group   = args[1]
        self.enemy_group    = args[2]
        self.obstacle_group = args[3]

        self.SCREEN_W       = args[4]
        self.SCREEN_H       = args[5]

        self.particles = Particles('shoot', self.screen, self.image, self.select)

        self.update_action('bullet')

    def update(self):
        # Update bullet events
        self.update_animation(50)

        for self.rect in self.rect_list:
            self.particles.add_shoot(self.rect.centerx, self.rect.centery, self.direction, self.direction)

            if not self.collide:
                if self.origin == 'player':
                    self.player_shoot()
                elif self.origin == 'enemy':
                    self.enemy_shoot()

                # Check if bullet has gone off screen
                if self.rect.bottom < 0 or self.rect.top > self.SCREEN_H:
                    self.kill() # Kill the animation

            else: # If the bullet collide it stop and destroy
                self.speed = 1
                # self.update_action('destroy')
                self.kill() # Kill the animation

            # Move bullet
            self.rect.y += self.speed * self.direction

    def player_shoot(self):
        # Check for collision with enemies
        for enemy in self.enemy_group:
            if pygame.sprite.spritecollide(enemy, self.bullet_group, False):
                if enemy.alive:
                    self.collide = True
                    enemy.health -= 25 * self.weapon

        # Check for collision with meteors
        for obstacle in self.obstacle_group:
            if pygame.sprite.spritecollide(obstacle, self.bullet_group, False):
                self.collide = True
                obstacle.health -= 10 * self.weapon

    def enemy_shoot(self):
        # Check collision with player
        if pygame.sprite.spritecollide(self.player, self.bullet_group, False):
            if self.player.alive and not self.player.win:
                self.collide = True
                if self.player.shield: self.player.shield = False
                else:
                    self.player.health -= 10 * self.weapon
                    self.player.max_speed = self.player.init_speed
                    self.player.less_time = False
                    self.player.freeze    = False

    def draw(self):
        for self.rect in self.rect_list:
            self.screen.blit(self.image, self.rect)

class Missile(Sprite_sheet):

    def __init__(self, origin, screen, select, x, y, direction, flip_x, flip_y, *args):
        missile_img, missile_dict = missile_select_def(select, False)
        super().__init__(missile_img)
        self.origin = origin
        self.screen = screen
        self.select = select

        # Load missile image
        self.create_animation(100, 100, missile_dict, scale=0.5)
        self.image  = self.animation_dict[self.action][self.frame_index]
        self.rect   = self.image.get_rect()
        self.width  = self.image.get_width()
        self.height = self.image.get_height()
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
        self.timer = Timer()

    def update(self):
        # Update missile events
        self.update_animation(10)
        self.move()

        if self.countdown == 0:
            self.speed = 0.1
            self.kill() # Kill the animation
            self.explosion_fx.play()

            # Create the explosion
            explosion = Explosion(self.screen, self.select, center=(self.rect.x, self.rect.y))
            self.explosion_group.add(explosion)

            # Do damage to anyone that is nearby
            if self.origin == 'player':
                self.player_throw()
            elif self.origin == 'enemy':
                self.enemy_throw()

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

    def player_throw(self):
        for enemy in self.enemy_group:
            if abs(self.rect.centerx - enemy.rect.centerx) < self.width  * 5 and\
               abs(self.rect.centery - enemy.rect.centery) < self.height * 5:
                enemy.collide = True
                enemy.health = 0

        for obstacle in self.obstacle_group:
            if abs(self.rect.centerx - obstacle.rect.centerx) < self.width  * 5 and\
               abs(self.rect.centery - obstacle.rect.centery) < self.height * 5:
                obstacle.collide = True
                obstacle.health = 0

    def enemy_throw(self):
        if abs(self.rect.centerx - self.player.rect.centerx) < self.width  * 5 and\
           abs(self.rect.centery - self.player.rect.centery) < self.height * 5:
            self.player.collide = True
            if self.player.shield: self.player.shield = False
            else:
                self.player.health -= 50
                self.player.max_speed = self.player.init_speed
                self.player.less_time = False
                self.player.freeze    = False


class Explosion(Sprite_sheet):
    def __init__(self, screen, select, **kwargs):
        missile_exp_img, missile_exp_dict = missile_select_def(select, True)
        super().__init__(missile_exp_img)
        self.screen = screen

        # Load image and rect
        self.create_animation(500, 500, missile_exp_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect  = self.image.get_rect(**kwargs)

    def update(self):
        self.update_action('destroy')
        self.update_animation(50)
        self.draw()
