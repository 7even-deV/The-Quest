import pygame

from .settings import player_dict
from .manager  import player_select_def, explosion_type_def
from .tools    import Sprite_sheet, Timer, Particles
from .weapons  import Bullet, Missile


class Player(Sprite_sheet):

    def __init__(self, screen, style, model, lives, *args, **kwargs):
        player_img, player_action_dict = player_select_def(style, model)
        super().__init__(player_img)
        self.screen = screen
        self.select = style
        self.lives  = lives

        self.weapon          = args[0][0][0]
        self.level           = args[0][0][1]
        self.score           = args[0][0][2]
        self.dead_enemy      = args[0][0][3]
        self.dead_meteor     = args[0][0][4]
        self.SCREEN_W        = args[0][0][5]
        self.SCREEN_H        = args[0][0][6]

        self.bullet_group    = args[0][1][0]
        self.missile_group   = args[0][1][1]
        self.enemy_group     = args[0][1][2]
        self.meteor_group    = args[0][1][3]
        self.explosion_group = args[0][1][4]

        # Load player image and rect
        self.create_animation(200, 200, player_action_dict, scale=0.5)
        explosion_img, explosion_dict = explosion_type_def(2)
        self.sheet = pygame.image.load(explosion_img).convert_alpha()
        self.create_animation(100, 100, explosion_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect  = self.image.get_rect(center=(self.SCREEN_W//2, self.SCREEN_H+self.SCREEN_H//10))

        self.ammo = (self.level*100 + player_dict['ammo'][self.select]) // 2
        self.start_ammo = self.ammo
        self.shoot_cooldown = 0
        self.load = self.level
        self.start_load = self.load
        self.throw_cooldown = 0

        self.vector = pygame.math.Vector2
        self.delta      = self.vector(0, 0)
        self.speed      = self.vector(0, 0)
        self.max_speed  = player_dict['speed'][self.select]
        self.init_speed = self.max_speed

        self.direction_x = 1
        self.direction_y = -1
        self.auto_init = False
        self.auto_land = False

        self.alive  = True
        self.health = player_dict['health'][self.select]
        self.max_health = self.health
        self.shield = False
        self.win    = False

        # Define player action variables
        self.spawn   = True
        self.turbo   = False
        self.collide = False

        self.moving_left  = False
        self.moving_right = False
        self.moving_up    = False
        self.moving_down  = False

        # Define item variables
        self.less_time = False
        self.freeze    = False
        self.atomic    = False
        self.turbo_up  = 0
        self.vision = pygame.Rect(self.SCREEN_W//20, self.SCREEN_H//7, self.SCREEN_W-self.SCREEN_W//10, self.SCREEN_H-self.SCREEN_H//5.5)
        self.particles = Particles('fire', self.screen, self.image, self.select)
        self.timer_list = []
        for _ in range(2):
            self.timer_list.append(Timer())

    def update(self):
        # Update player events
        if self.alive: self.move()
        self.check_collision()
        self.update_animation(self.animation_cooldown)
        if self.alive and not self.spawn and not self.auto_init:
            self.particles.add_circle(self.rect.centerx-self.rect.width//4, self.rect.bottom-self.rect.height//10, self.direction_x, self.direction_y)
            self.particles.add_circle(self.rect.centerx+self.rect.width//4, self.rect.bottom-self.rect.height//10, self.direction_x, self.direction_y)
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1

    def move(self):
        self.speed = self.vector(0, 0)

        if self.moving_left and self.moving_right or not self.moving_left and not self.moving_right:
            # Recover the axis of delta x and rotate to 0
            if    self.delta.x > 0.1: self.delta.x -= 0.1
            elif  self.delta.x < 0.0: self.delta.x += 0.1
            else: self.delta.x = 0

            if    self.rotate > 0.0: self.rotate -= 0.1
            elif  self.rotate < 0.0: self.rotate += 0.1
        else:
            if self.moving_left:
                self.speed.x = -0.1
                if self.rotate < 5: self.rotate += 0.5
                self.direction_x = -1
                self.update_action('left')

            if self.moving_right:
                self.speed.x = 0.1
                if self.rotate > -5: self.rotate -= 0.5
                self.direction_x = 1
                self.update_action('right')

        if self.moving_up and self.moving_down or not self.moving_up and not self.moving_down:
            # Recover the axis of delta y to 0
            if    self.delta.y > 0.1: self.delta.y -= 0.1
            elif  self.delta.y < 0.0: self.delta.y += 0.1
            else: self.delta.y = 0

        else:
            if self.moving_up:
                self.speed.y = -0.1

            if self.moving_down:
                self.speed.y = 0.1

        # Check if going off the edges of the screen
        if self.limit_left(self.rect.width//10):
            if self.limit_left(): self.speed.x = 0.1
            else: self.moving_left = False

        if self.limit_right(self.rect.width//10):
            if self.limit_right(): self.speed.x = -0.1
            else: self.moving_right = False

        if self.limit_up(self.rect.height//10):
            if self.limit_up(): self.speed.y = 0.1
            else: self.moving_up = False

        if self.limit_down(self.rect.height//10):
            if self.limit_down(): self.speed.y = -0.1
            else: self.moving_down = False

        # Limits the maximum speed
        if not self.spawn and not self.collide:
            if self.moving_left and self.delta.x > -self.max_speed:
                self.delta.x += self.speed.x
            if self.moving_right and self.delta.x < self.max_speed:
                self.delta.x += self.speed.x
            if self.moving_up and self.delta.y > -self.max_speed:
                self.delta.y += self.speed.y
            if self.moving_down and self.delta.y < self.max_speed:
                self.delta.y += self.speed.y

        # Update the movement of the rectangle
        if self.alive:
            self.rect.x += self.delta.x + self.max_speed * self.speed.x
            self.rect.y += self.delta.y + self.max_speed * self.speed.y

        # print(self.rect.center, self.delta, self.speed, self.max_speed)

    def auto_movement(self):
        if self.win:
            if not self.auto_init:
                self.turbo = False

                if self.rect.centerx < self.SCREEN_W//2:
                    self.moving_right = True
                else: self.moving_right = False

                if self.rect.centerx > self.SCREEN_W//2:
                    self.moving_left = True
                else: self.moving_left = False

                if self.rect.centery < self.SCREEN_H//2:
                    self.moving_down = True
                else: self.moving_down = False

                if self.rect.centery > self.SCREEN_H//2:
                    self.moving_up = True
                else: self.moving_up = False

                if not self.moving_left and not self.moving_right and not self.moving_up and not self.moving_down:
                    self.auto_init = True
            else:
                if not self.auto_land:
                    if not self.limit_up(): self.rect.y -= 0.1

                    if self.limit_up(self.rect.height):
                        if self.rotate < 90: self.rotate += 1
                        else: self.auto_land = True
                else:
                    if self.rect.width > 1 and self.rect.height > 1:
                        self.rect.width  -= 1
                        self.rect.height -= 1

                    if self.rotate < 180: self.rotate += 1
                    else:
                        self.auto_init = False
                        self.auto_land = False

                        return True

    def shoot(self, *args):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 10
            # create bullet ammo
            bullet = Bullet('player', self.screen, self.weapon, self.select, self.rect.centerx, self.rect.centery-self.rect.height//2, self.rect.width, self.direction_y,\
                            self.flip_x, self.flip_y, self, self.bullet_group, self.enemy_group, self.meteor_group, self.SCREEN_W, self.SCREEN_H)
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
            missile = Missile('player', self.screen, self.select, self.rect.centerx, self.rect.top, self.direction_y, self.flip_x, self.flip_y,\
                                self, self.enemy_group, self.meteor_group, self.explosion_group, args[1], args[2], args[3])
            self.missile_group.add(missile)
            # Reduce load
            self.load -= 1
            args[1].play()
        # Sound if weapon is unloaded
        elif self.load == 0: args[0].play()

    # Check if the collision with the enemy or obstacles
    def check_collision(self):
        if self.freeze:
            if self.timer_list[0].time(5, True):
                self.freeze = False

        if self.atomic:
            if self.timer_list[1].time(5, True):
                self.atomic = False
            # Check if there is any threat inside the screen
            for enemy in self.enemy_group:
                if self.vision.colliderect(enemy.rect):
                    enemy.health = 0
                    self.atomic = False

            for meteor in self.meteor_group:
                if self.vision.colliderect(meteor.rect):
                    meteor.health = 0
                    self.atomic = False

            # pygame.draw.rect(self.screen, (255, 0, 0), self.vision)

    def check_alive(self, *args):
        if self.health <= 0:
            if self.alive:
                self.alive  = False
                self.health = 0
                # self.score  = 0
                self.speed  = self.vector(0, 0)
                # args[0].play()

            self.animation_cooldown = self.animation_cooldown // 2
            self.update_action('death')
        else:
            self.update_action('idle')

    def limit_left(self, value=0):
        return self.rect.left + self.delta.x < self.rect.width//10 + value

    def limit_right(self, value=0):
        return self.rect.right + self.delta.x > self.SCREEN_W - (self.rect.height//10 + value)

    def limit_up(self, value=0):
        return self.rect.top + self.delta.y < self.rect.height + value

    def limit_down(self, value=0):
        return self.rect.bottom + self.delta.y > self.SCREEN_H - (self.rect.height//10 + value)
