import pygame, random

from .settings import FPS, SPEED, ENEMY_SCALE, enemy_dict
from .manager  import enemy_select_function, explosion_2_img, explosion_dict
from .tools    import Sprite_sheet, Timer
from .weapons  import Bullet, Missile
from .items    import Item


class Enemy(Sprite_sheet):

    def __init__(self, screen, style, speed, player, SCREEN_W, SCREEN_H, *args, **kwargs):
        enemy_img, enemy_action_dict = enemy_select_function(style)
        super().__init__(enemy_img)
        self.screen = screen
        self.select = style
        self.speed  = speed
        self.player = player
        self.win    = self.player.win
        self.SCREEN_W = SCREEN_W
        self.SCREEN_H = SCREEN_H

        self.bullet_group    = args[0][0][0]
        self.missile_group   = args[0][0][1]
        self.enemy_group     = args[0][0][2]
        self.meteor_group    = args[0][0][3]
        self.explosion_group = args[0][0][4]
        self.item_group      = args[0][0][5]

        self.empty_ammo_fx   = args[0][1][0]
        self.bullet_fx       = args[0][1][1]
        self.empty_load_fx   = args[0][1][2]
        self.missile_fx      = args[0][1][3]
        self.missile_cd_fx   = args[0][1][4]
        self.missile_exp_fx  = args[0][1][5]
        self.explosion_fx    = args[0][1][6]

        self.item_standby_fx = args[0][1][7]
        self.item_get_fx     = args[0][1][8]

        self.ammo = enemy_dict['ammo'][self.select]
        self.load = enemy_dict['load'][self.select]
        self.exp  = enemy_dict['exp' ][self.select]
        self.start_ammo = self.ammo
        self.start_load = self.load
        self.shoot_cooldown = 0
        self.throw_cooldown = 0
        self.weapon = 1

        self.alive  = True
        self.health = 100
        self.max_health = self.health

        # Load enemy image
        self.create_animation(100, 100, enemy_action_dict)
        self.sheet = pygame.image.load(explosion_2_img).convert_alpha()
        self.create_animation(100, 100, explosion_dict)
        self.image = self.animation_dict[self.action][self.frame_index]

        # Get enemy rect
        self.rect = self.image.get_rect(**kwargs)

        self.scale = enemy_dict['scale'][self.select]
        self.rect.width  = self.image.get_width()  // ENEMY_SCALE
        self.rect.height = self.image.get_height() // ENEMY_SCALE

        # Define enemy action variables
        self.delta_x  = 0
        self.delta_y  = 0
        self.random_x = random.randint(0, 6)
        self.random_y = random.randint(0, 6)
        self.direction_x    = 1
        self.direction_y    = 1

        # AI specific variables
        self.ai_direction_x  = 1
        self.ai_direction_y  = 1
        self.ai_spawn        = True
        self.ai_stop         = False
        self.ai_moving_left  = False
        self.ai_moving_right = False
        self.ai_moving_up    = False
        self.ai_moving_down  = False
        self.ai_shoot        = False

        self.collide         = False
        self.retired         = False
        self.idling         = False
        self.idling_timer   = 200
        self.idling_counter = 0

        self.move_counter   = 0
        self.rep_total      = 6
        self.rep_count      = 0
        self.vision = pygame.Rect(0, 0, self.rect.width//2, self.SCREEN_H)
        self.timer  = Timer(FPS)

    def update(self):
        # Update enemy events
        self.ai_select()
        self.move()
        self.check_collision()
        self.check_alive()
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
        if self.alive and not self.ai_stop:
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

        if self.retired:
            self.rotate = 0
            self.flip_y = True
            self.ai_moving_down = True
            # Check if fallen off the map
            if self.rect.top > self.SCREEN_H:
                self.kill()

        elif not self.ai_spawn:
            # Check if going off the edges of the screen
            if self.limit_left():
                if self.limit_left(+1): self.delta_x = 0.1
                else: self.delta_x = 0

            if self.limit_right():
                if self.limit_right(-1): self.delta_x = -0.1
                else: self.delta_x = 0

            if self.limit_up():
                if self.limit_up(+1): self.delta_y = 0.1
                else: self.delta_y = 0

            if self.limit_down():
                if self.limit_down(-1): self.delta_y = -0.1
                else: self.delta_y = 0

        # Update rectangle position
        if not self.player.freeze:
            self.rect.x += self.delta_x
            self.rect.y += self.delta_y

    def shoot(self, *args):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 50
            # create bullet ammo
            self.bullet = Bullet('enemy', self.screen, self.weapon, self.select, self.rect.centerx, self.rect.bottom, self.rect.width, self.direction_y,\
                            self.flip_x, self.flip_y, self.player, self.bullet_group, self.enemy_group, self.meteor_group)
            self.bullet_group.add(self.bullet)
            # Reduce ammo
            self.ammo -= 1
            args[1].play()
        # Sound if weapon is unloaded
        elif self.ammo == 0: args[0].play()

    def throw(self, *args):
        if self.throw_cooldown == 0 and self.load > 0:
            self.throw_cooldown = 400
            # Create missile load
            missile = Missile('enemy', self.screen, self.rect.centerx, self.rect.bottom, self.direction_y, self.flip_x, self.flip_y,\
                                self.player, self.enemy_group, self.meteor_group, self.explosion_group, args[1], args[2], args[3])
            self.missile_group.add(missile)
            # Reduce load
            self.load -= 1
            args[1].play()
        # Sound if weapon is unloaded
        elif self.load == 0: args[0].play()

    # Select type of artificial intelligence (ai)
    def ai_select(self):
        if self.alive and self.player.alive and not self.retired:
            if self.select == 0:
                self.patrol_ai()
            if self.select == 1:
                self.faster_ai()
            if self.select == 2:
                self.kamikaze_ai()

            # pygame.draw.rect(self.screen, (255, 0, 0), self.vision)

    def patrol_ai(self):
        if self.ai_spawn:
            if self.limit_up():
                self.flip_y = True
                self.ai_moving_down = True
            elif self.timer.counter(self.random_y, True):
                self.ai_moving_down = False
                self.ai_spawn = False
        else:
            # Check if fallen off the map
            if self.rect.bottom < 0:
                self.kill()

            # Check the x limits of the screen
            if self.limit_left() or self.limit_right():
                self.direction_x *= -1

            if not self.idling and random.randint(1, self.idling_timer) == 1:
                self.ai_moving_left = self.ai_moving_right = False
                self.idling_counter = self.idling_timer
                self.idling = True
            else:
                if not self.idling:
                    if self.direction_x == 1:
                        self.ai_moving_right = True
                    else: self.ai_moving_right = False
                    self.ai_moving_left = not self.ai_moving_right

                    self.idling_counter += 1
                    if self.idling_counter > self.rect.width:
                        self.direction_x  *= -1
                        self.idling_counter *= -1

                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

            # Check if the ai in near the player
            if self.vision.colliderect(self.player.rect):
                self.ai_stop = True
                self.shoot(self.empty_ammo_fx, self.bullet_fx) # Shoot
            else: self.ai_stop = False

            # Update ai vision as the enemy moves
            self.vision.midtop = (self.rect.centerx, self.rect.centery)

    def faster_ai(self):
        if self.ai_spawn:
            if self.limit_left():
                self.rotate = -90
                self.ai_moving_right = not self.ai_moving_left
            elif self.limit_right():
                self.rotate = 90
                self.ai_moving_left = not self.ai_moving_right
            else:
                self.ai_moving_left = self.ai_moving_right = False
                self.ai_spawn = False

        else:
            # Check if fallen off the map
            if self.rect.bottom < 0:
                self.kill()

            if not self.idling:
                if self.ai_direction_x == 1:
                    self.rotate = -90
                    self.ai_moving_right = True
                    if self.limit_right():
                        self.ai_moving_right = False
                        self.ai_direction_x = 0
                        self.rep_count += 1
                        if self.rep_count > self.rep_total:
                            self.rep_count = 0
                            self.ai_direction_y = -1
                        else:
                            self.ai_direction_y = 1

                elif self.ai_direction_y == 1:
                    self.rotate = -180
                    self.ai_moving_down = True
                    if self.limit_down(self.rep_total * 100 - self.rep_count * 100):
                        self.ai_moving_down = False
                        self.ai_direction_y = 0
                        if self.rep_count % 2 == 0:
                            self.ai_direction_x = 1
                        else:
                            self.ai_direction_x = -1

                elif self.ai_direction_x == -1:
                    self.rotate = 90
                    self.ai_moving_left = True
                    if self.limit_left():
                        self.ai_moving_left = False
                        self.ai_direction_x = 0
                        self.rep_count += 1
                        if self.rep_count > self.rep_total:
                            self.rep_count = 0
                            self.ai_direction_y = -1
                        else: self.ai_direction_y = 1

                elif self.ai_direction_y == -1:
                    self.rotate = 0
                    self.ai_moving_up = True
                    self.ai_spawn = True

            # Check if the ai in near the player
            if self.vision.colliderect(self.player.rect):
                if self.ammo > 0:
                    self.rotate = -180
                    if not self.ai_shoot:
                        self.shoot(self.empty_ammo_fx, self.bullet_fx) # Shoot
                        self.ai_shoot = True
            else: self.ai_shoot = False

            # Update ai vision as the enemy moves
            self.vision.midtop = (self.rect.centerx, self.rect.centery)

    def kamikaze_ai(self):
        if self.ai_spawn:
            if self.limit_up():
                self.flip_y = True
                self.ai_moving_down = True
            else:
                self.ai_moving_down = False
                self.ai_spawn = False
        else:
            # Check if fallen off the map
            if self.rect.bottom < 0:
                self.kill()

            # Check if the ai in near the player
            if self.vision.colliderect(self.player.rect):
                if self.load > 0:
                    self.ai_stop = True
                    self.throw(self.empty_load_fx, self.missile_fx, self.missile_cd_fx, self.missile_exp_fx) # Throw
                elif self.throw_cooldown == 0:
                    self.ai_moving_left = self.ai_moving_right = False
                    self.ai_moving_down = True
            else:
                self.ai_stop = False
                self.ai_moving_down = False

                # Check the x limits of the screen
                if self.limit_left() or self.limit_right():
                    self.direction_x *= -1

                if not self.idling and random.randint(1, self.idling_timer) == 1:
                    self.ai_moving_left = self.ai_moving_right = False
                    self.idling_counter = self.idling_timer
                    self.idling = True
                else:
                    if not self.idling:
                        if self.direction_x == 1:
                            self.ai_moving_right = True
                        else: self.ai_moving_right = False
                        self.ai_moving_left = not self.ai_moving_right

                        self.idling_counter += 1
                        if self.idling_counter > self.rect.width:
                            self.direction_x  *= -1
                            self.idling_counter *= -1

                    else:
                        self.idling_counter -= 1
                        if self.idling_counter <= 0:
                            self.idling = False

            # Update ai vision as the enemy moves
            self.vision.midtop = (self.rect.centerx, self.rect.centery)

    # Create item
    def item_chance(self, spawn):
        chance = random.randint(0, 100)
        if chance <= spawn:
            item = Item('random', self.screen, self.player, self.SCREEN_W, self.SCREEN_H, [self.item_standby_fx, self.item_get_fx], center=(self.rect.centerx, self.rect.centery))
            self.item_group.add(item)

    # Check if the collision with the player
    def check_collision(self):
        if self.alive and self.player.alive and not self.collide and not self.player.win:
            if abs(self.rect.centerx - self.player.rect.centerx) < self.rect.width  * self.scale and\
               abs(self.rect.centery - self.player.rect.centery) < self.rect.height * self.scale:
                self.collide = True
                self.player.collide = True
                self.player.rect.x += (self.delta_x - self.player.delta.x) * 2
                self.player.rect.y += (self.delta_y - self.player.delta.y) * 2
                if self.player.shield: self.player.shield = False
                else:
                    self.player.health -= 50
                    self.player.max_speed = SPEED
                    self.player.less_time = False
                    self.player.freeze    = False
                    self.player.turbo_up  = 0
                    self.player.weapon_up = 0

                self.health = 0

    def check_alive(self):
        if self.health <= 0:
            if self.alive:
                self.alive  = False
                self.health = 0
                self.speed  = 0
                self.player.dead_enemy += 1
                self.item_chance(self.rect.w//2)
                self.explosion_fx.play()

            if self.player.score < self.player.score + self.exp:
                self.player.score += 1
                if self.exp > 0: self.exp -= 1

            self.animation_cooldown = self.animation_cooldown // 2
            self.update_action('destroy')

        else: self.update_action('idle')

    def limit_left(self, value=0):
        return self.rect.left + self.delta_x < self.rect.width//10 + value

    def limit_right(self, value=0):
        return self.rect.right + self.delta_x > self.SCREEN_W - (self.rect.height//10 + value)

    def limit_up(self, value=0):
        return self.rect.top + self.delta_y < self.rect.height + value

    def limit_down(self, value=0):
        return self.rect.bottom + self.delta_y > self.SCREEN_H - (self.rect.height//10 + value)
