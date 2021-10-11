import pygame, random

from .manager import enemy_select_function, explosion_2_img, explosion_dict
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, enemy_dict
from .tools import Sprite_sheet, Timer
from .weapons import Bullet, Missile


class Enemy(Sprite_sheet):

    def __init__(self, screen, select, speed, player, empty_ammo_fx, bullet_fx, *args, **kwargs):
        enemy_img, enemy_action_dict = enemy_select_function(select)
        super().__init__(enemy_img)
        self.screen = screen
        self.select = select
        self.speed  = speed
        self.player = player

        self.bullet_group    = args[0][0]
        self.missile_group   = args[0][1]
        self.enemy_group     = args[0][2]
        self.meteor_group    = args[0][3]
        self.explosion_group = args[0][4]

        self.empty_ammo_fx = empty_ammo_fx
        self.bullet_fx = bullet_fx

        self.scale = enemy_dict['scale'][self.select]
        self.ammo  = enemy_dict['ammo'][self.select]
        self.load  = enemy_dict['load'][self.select]
        self.exp   = enemy_dict['exp'][self.select]
        self.start_ammo = self.ammo
        self.start_load = self.load
        self.shoot_cooldown = 0
        self.throw_cooldown = 0

        self.alive = True
        self.health = 100
        self.max_health = self.health

        # Load enemy image
        self.create_animation(100, 100, enemy_action_dict)
        self.sheet = pygame.image.load(explosion_2_img).convert_alpha()
        self.create_animation(100, 100, explosion_dict)
        self.image = self.animation_dict[self.action][self.frame_index]

        # Get enemy rect
        self.rect = self.image.get_rect(center=(enemy_dict['pos_x'][self.select], enemy_dict['pos_y'][self.select]))
        self.rect.width = self.rect.width // 2
        self.rect.height = self.rect.height // 2

        self.delta_x = 0
        self.delta_y = 0
        self.random_x = random.randint(0, 6)
        self.random_y = random.randint(0, 6)

        # Define enemy action variables
        self.ai_moving_left = False
        self.ai_moving_right = False
        self.ai_moving_up = False
        self.ai_moving_down = False
        self.collide = False

        # AI specific variables
        self.vision = pygame.Rect(0, 0, 300, 600)
        self.idling = False
        self.direction_x = 1
        self.direction_y = 1
        self.move_counter = 0
        self.rep_count = 0
        self.timer = Timer(FPS)

    def update(self):
        # Update enemy events
        self.check_alive()
        self.ai()
        self.move()
        self.update_animation(self.animation_cooldown)
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

        if self.ai_moving_down:
            self.delta_y = self.speed
            self.direction_y = 1

        # Update rectangle position
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

    # Check if the collision with the player
    def check_collision(self, other, sfx):
        if not self.collide:
            margin_width = other.rect.width // 4
            margin_height = other.rect.height // 4
            if self.rect.right >= other.rect.left + margin_width and self.rect.left <= other.rect.right - margin_width and \
                self.rect.bottom >= other.rect.top + margin_height and self.rect.top <= other.rect.bottom - margin_height:
                self.collide = True
                other.collide = True
                other.rect.x += (self.delta_x - other.delta_x) * 2
                other.rect.y += (self.delta_y - other.delta_y) * 2
                other.score += 10
                other.health -= 10
                self.health -= 100
                self.delta_x = self.delta_y = 0
                self.animation_cooldown = self.animation_cooldown // 4
                sfx.play()

    def shoot(self, *args):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 8
            # create bullet ammo
            bullet = Bullet(self, self.screen, self.select, self.rect.centerx, self.rect.bottom*1.2, self.direction_y,\
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
            missile = Missile(self.screen, self.rect.centerx, self.rect.bottom, self.direction_y, self.flip_x, self.flip_y,\
                                self, self.enemy_group, self.meteor_group, self.explosion_group, args[1], args[2], args[3])
            self.missile_group.add(missile)
            # Reduce load
            self.load -= 1
            args[1].play()
        # Sound if weapon is unloaded
        elif self.load == 0: args[0].play()

    def ai(self):
        if self.alive and self.player.alive:
            if self.select == 0:
                self.patrol()
            if self.select == 1:
                self.fighter()

    def patrol(self):
        if self.limit_up:
            self.ai_moving_down = True
            self.flip_y = True
        # elif self.timer.counter(self.random_y, True):
        else:
            self.ai_moving_down = False

        if self.alive and self.player.alive:
            if not self.idling and random.randint(1, 200) == 1:
                self.idling = True
                self.idling_counter = 50
            # Check if the ai in near the player
            if self.vision.colliderect(self.player.rect):
                # Shoot
                self.shoot(self.empty_ammo_fx, self.bullet_fx)
            else:
                if not self.idling:
                    if self.direction_x == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move()
                    self.move_counter += 1
                    # Update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction_x, self.rect.centery)

                    if self.move_counter > self.rect.width:
                        self.direction_x *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

    def fighter(self):
        if not self.idling:
            if self.limit_left:
                self.ai_moving_right = True
                self.rotate = -90

            if self.limit_right:
                self.ai_moving_left = True
                self.rotate = 90

            else: self.idling = True

        else:
            # Check if fallen off the map
            if self.rect.bottom < 0:
                self.kill()

            if self.direction_x == 1:
                self.ai_moving_right = not self.ai_moving_right
                self.rotate = -90
                if self.limit_right:
                    self.ai_moving_right = False
                    self.direction_x = 0
                    self.rep_count += 1
                    if self.rep_count > 6:
                        self.rep_count = 0
                        self.direction_y = -1
                    else:
                        self.direction_y = 1

            elif self.direction_y == 1:
                self.ai_moving_down = not self.ai_moving_right
                self.rotate = -180
                if self.limit_down(10 - (self.rep_count-1) * 2):
                    self.ai_moving_down = False
                    self.direction_y = 0
                    if self.rep_count % 2 == 0:
                        self.direction_x = 1
                    else:
                        self.direction_x = -1

            elif self.direction_x == -1:
                self.ai_moving_left = not self.ai_moving_right
                self.rotate = -90
                if self.limit_left:
                    self.ai_moving_left = False
                    self.direction_x = 0
                    self.rep_count += 1
                    if self.rep_count > 6:
                        self.rep_count = 0
                        self.direction_y = -1
                    else: self.direction_y = 1

            elif self.direction_y == -1:
                self.ai_moving_up = not self.ai_moving_down
                self.rotate = 0

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.exp = 0
            self.alive = False
            self.update_action('destroy')
        else: self.update_action('idle')

    @property
    def limit_left(self):
        return self.rect.left < 0 + self.rect.width
    @property
    def limit_right(self):
        return self.rect.right > SCREEN_WIDTH - self.rect.width
    @property
    def limit_up(self):
        return self.rect.top < 0 + self.rect.height * 2

    def limit_down(self, value=0):
        return self.rect.bottom > SCREEN_HEIGHT - (self.rect.height * value)
