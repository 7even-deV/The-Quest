import pygame

from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SPEED
from .manager  import player_select_function, explosion_3_img, explosion_dict
from .tools    import Sprite_sheet, Timer, Particles
from .weapons  import Bullet, Missile


class Player(Sprite_sheet):

    def __init__(self, screen, style, model, score, ammo, load, lives, *args, **kwargs):
        player_img, player_action_dict = player_select_function(style, model)
        super().__init__(player_img)
        self.screen = screen
        self.select = style
        self.score  = score
        self.ammo   = ammo
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
        self.sheet = pygame.image.load(explosion_3_img).convert_alpha()
        self.create_animation(100, 100, explosion_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        # Get player rect
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT+SCREEN_HEIGHT//10))

        self.vector = pygame.math.Vector2
        self.max_speed = SPEED
        self.speed     = self.vector(0, 0)
        self.delta     = self.vector(0, 0)

        self.direction_x = 1
        self.direction_y = -1
        self.auto_init = False

        self.alive  = True
        self.health = 100
        self.max_health = self.health
        self.lives = lives
        self.win   = False

        # Define player action variables
        self.spawn   = True
        self.turbo   = False
        self.collide = False

        self.moving_left  = False
        self.moving_right = False
        self.moving_up    = False
        self.moving_down  = False
        self.timer = Timer(FPS)
        self.particles = Particles(self.screen, 10, self.image)

    def update(self):
        # Update player events
        self.move()
        self.check_alive()
        self.update_animation(self.animation_cooldown)
        self.particles.add_circle(self.rect.centerx-self.rect.width//4, self.rect.bottom-self.rect.height//10, self.direction_x, self.direction_y)
        self.particles.add_circle(self.rect.centerx+self.rect.width//4, self.rect.bottom-self.rect.height//10, self.direction_x, self.direction_y)
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1

    def move(self):
        self.speed = self.vector(0, 0)

        # Assign bools if moving left or right or up or down
        if self.alive and not self.spawn and not self.turbo and not self.collide:

            if not self.moving_left and not self.moving_right:
                # Recover the axis of delta x and rotate to 0
                if   self.delta.x > 0.1: self.delta.x -= 0.1
                elif self.delta.x < 0.0: self.delta.x += 0.1
                if    self.rotate > 0.0: self.rotate  -= 0.1
                elif  self.rotate < 0.0: self.rotate  += 0.1
            else:
                if self.moving_left:
                    self.speed.x = -0.1
                    if self.rotate < 5: self.rotate += 0.5
                    self.update_action('left')

                if self.moving_right:
                    self.speed.x = 0.1
                    if self.rotate > -5: self.rotate -= 0.5
                    self.update_action('right')

            if not self.moving_up and not self.moving_down:
                # Recover the axis of delta y to 0
                if   self.delta.y > 0.1: self.delta.y -= 0.1
                elif self.delta.y < 0.0: self.delta.y += 0.1
            else:
                if self.moving_up:
                    self.speed.y = -0.1

                if self.moving_down:
                    self.speed.y = 0.1

        # Check if going off the edges of the screen
        if self.limit_left():
            if self.limit_left(1): self.speed.x = 1.0
            else: self.speed.x = 0.0

        if self.limit_right():
            if self.limit_right(-1): self.speed.x = -1.0
            else: self.speed.x = 0.0

        if self.limit_up():
            if self.limit_up(1): self.speed.y = 1.0
            else: self.speed.y = 0.0

        if self.limit_down():
            if self.limit_down(-1): self.speed.y = -1.0
            else: self.speed.y = 0.0

        # Update the movement of the rectangle
        if self.delta.x > -self.max_speed and self.delta.x < self.max_speed:
            self.delta.x += self.speed.x
        if self.delta.y > -self.max_speed and self.delta.y < self.max_speed:
            self.delta.y += self.speed.y

        self.rect.x += self.delta.x + self.max_speed * self.speed.x
        self.rect.y += self.delta.y + self.max_speed * self.speed.y

        # print(self.rect.center, self.delta, self.speed, self.max_speed)

    def auto_movement(self):
        if self.win:
            if not self.auto_init:
                if self.rect.centerx < SCREEN_WIDTH//2:
                    self.moving_right = True
                else: self.moving_right = False
                if self.rect.centerx > SCREEN_WIDTH//2:
                    self.moving_left = True
                else: self.moving_left = False
                if not self.limit_down():
                    self.moving_down = True
                else:
                    self.moving_down = False
                    self.auto_init = True

            else:
                if self.direction_x == 1:
                    self.moving_right = True
                    if self.rotate > -15:
                        self.rotate -= 0.2
                    if self.limit_right(+SCREEN_WIDTH//10):
                        self.moving_right = False
                        self.direction_x  = 0
                        self.direction_y  = -1

                if self.direction_y == -1:
                    self.moving_up = True
                    if self.limit_up(+SCREEN_HEIGHT//2):
                        if self.rotate < 15:
                            self.rotate += 0.2
                        if self.limit_up(+SCREEN_HEIGHT//11):
                            self.moving_up = False
                            self.direction_y = 0
                            self.direction_x = -1

                if self.direction_x == -1:
                    self.moving_left = True
                    if self.rotate < 90:
                        self.rotate += 0.2
                        if self.limit_left(+SCREEN_WIDTH//3):
                            self.moving_left  = False
                            if self.rect.width != 0 and self.rect.height != 0:
                                self.rect.width  -= 0.1
                                self.rect.height -= 0.1
                            else:
                                self.direction_x  = 0

                                return self.win

    # def check_collision(self, *args):
    #     # Check for collision
    #     for sprite in args:
    #         # Check for collision in the x direction
    #         if sprite.colliderect(self.rect.x + self.delta.x, self.rect.y, self.rect.w, self.rect.h):
    #             self.delta.x = 0

    #         # Check for collision in the y direction
    #         if sprite.colliderect(self.rect.x, self.rect.y + self.delta.y, self.rect.w, self.rect.h):
    #             self.delta.y = 0

    #     # Check if the collision with the enemy
    #     if pygame.sprite.spritecollide(self, args, False):
    #         self.health -= 10

    def shoot(self, *args):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 10
            # create bullet ammo
            bullet = Bullet('player', self.screen, self.select, self.rect.centerx, self.rect.top, self.rect.width, self.direction_y,\
                            self.flip_x, self.flip_y, self, self.bullet_group, self.enemy_group, self.meteor_group)
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
            missile = Missile('player', self.screen, self.rect.centerx, self.rect.top, self.direction_y, self.flip_x, self.flip_y,\
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
            self.speed = self.vector(0, 0)
            self.alive = False
            self.animation_cooldown = self.animation_cooldown // 4
            self.update_action('death')
        else: self.update_action('idle')

    def limit_left(self, value=0):
        return self.rect.left + self.delta.x < self.rect.width//10 + value

    def limit_right(self, value=0):
        return self.rect.right + self.delta.x > SCREEN_WIDTH - (self.rect.height//10 + value)

    def limit_up(self, value=0):
        return self.rect.top + self.delta.y < self.rect.height + value

    def limit_down(self, value=0):
        return self.rect.bottom + self.delta.y > SCREEN_HEIGHT - (self.rect.height//10 + value)
