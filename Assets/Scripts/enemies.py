import pygame, random

from .manager import enemy_select_function, explosion_3_img, explosion_dict
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, enemy_dict
from .tools import Sprite_sheet, Timer
from .weapons import Bullet, Missile


class Enemy(Sprite_sheet):

    def __init__(self, screen, select, speed, player, *args, **kwargs):
        enemy_img, enemy_action_dict = enemy_select_function(select)
        super().__init__(enemy_img)
        self.screen = screen
        self.select = select
        self.speed  = speed
        self.player = player
        self.win    = self.player.win

        self.bullet_group    = args[0][0][0]
        self.missile_group   = args[0][0][1]
        self.enemy_group     = args[0][0][2]
        self.meteor_group    = args[0][0][3]
        self.explosion_group = args[0][0][4]

        self.empty_ammo_fx   = args[0][1][0]
        self.bullet_fx       = args[0][1][1]
        self.empty_load_fx   = args[0][1][2]
        self.missile_fx      = args[0][1][3]
        self.missile_cd_fx   = args[0][1][4]
        self.missile_exp_fx  = args[0][1][5]

        self.ammo = enemy_dict['ammo'][self.select]
        self.load = enemy_dict['load'][self.select]
        self.exp  = enemy_dict['exp' ][self.select]
        self.start_ammo = self.ammo
        self.start_load = self.load
        self.shoot_cooldown = 0
        self.throw_cooldown = 0

        self.alive  = True
        self.health = 100
        self.max_health = self.health

        # Load enemy image
        self.create_animation(100, 100, enemy_action_dict)
        self.sheet = pygame.image.load(explosion_3_img).convert_alpha()
        self.create_animation(100, 100, explosion_dict)
        self.image = self.animation_dict[self.action][self.frame_index]

        # Get enemy rect
        self.rect = self.image.get_rect(**kwargs)

        self.delta_x  = 0
        self.delta_y  = 0
        self.random_x = random.randint(0, 6)
        self.random_y = random.randint(0, 6)

        # Define enemy action variables
        self.ai_spawn        = True
        self.ai_stop         = False
        self.ai_moving_left  = False
        self.ai_moving_right = False
        self.ai_moving_up    = False
        self.ai_moving_down  = False
        self.ai_shoot        = False
        self.collide         = False
        self.retired         = False

        # AI specific variables
        self.idling         = False
        self.idling_timer   = 200
        self.idling_counter = 0
        self.direction_x    = 1
        self.direction_y    = 1
        self.move_counter   = 0
        self.rep_total      = 6
        self.rep_count      = 0
        self.vision = pygame.Rect(0, 0, self.rect.width//2, SCREEN_HEIGHT)
        self.timer  = Timer(FPS)

    def update(self):
        # Update enemy events
        self.ai_select()
        self.move()
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
        if not self.ai_stop:
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
            if self.rect.top > SCREEN_HEIGHT:
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
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

    def shoot(self, *args):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 50
            # create bullet ammo
            self.bullet = Bullet('enemy', self.screen, self.select, self.rect.centerx, self.rect.bottom*1.1, self.direction_y,\
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
            missile = Missile(self.screen, self.rect.centerx, self.rect.bottom, self.direction_y, self.flip_x, self.flip_y,\
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
            pygame.draw.rect(self.screen, (255, 0, 0), self.vision)

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
                if self.direction_x == 1:
                    self.rotate = -90
                    self.ai_moving_right = True
                    if self.limit_right():
                        self.ai_moving_right = False
                        self.direction_x = 0
                        self.rep_count += 1
                        if self.rep_count > self.rep_total:
                            self.rep_count = 0
                            self.direction_y = -1
                        else:
                            self.direction_y = 1

                elif self.direction_y == 1:
                    self.rotate = -180
                    self.ai_moving_down = True
                    if self.limit_down(self.rep_total * 100 - self.rep_count * 100):
                        self.ai_moving_down = False
                        self.direction_y = 0
                        if self.rep_count % 2 == 0:
                            self.direction_x = 1
                        else:
                            self.direction_x = -1

                elif self.direction_x == -1:
                    self.rotate = 90
                    self.ai_moving_left = True
                    if self.limit_left():
                        self.ai_moving_left = False
                        self.direction_x = 0
                        self.rep_count += 1
                        if self.rep_count > self.rep_total:
                            self.rep_count = 0
                            self.direction_y = -1
                        else: self.direction_y = 1

                elif self.direction_y == -1:
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
            pygame.draw.rect(self.screen, (255, 0, 0), self.vision)

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
            pygame.draw.rect(self.screen, (255, 0, 0), self.vision)

    # Check if the collision with the player
    def check_collision(self, sfx):
        if not self.collide and not self.player.win and self.player.alive:
            # margin_width  = self.player.rect.width // 10
            # margin_height = self.player.rect.height // 10
            margin_width  = 0
            margin_height = 0
            if self.rect.right  >= self.player.rect.left + margin_width and self.rect.left <= self.player.rect.right - margin_width and \
                self.rect.bottom >= self.player.rect.top + margin_height and self.rect.top <= self.player.rect.bottom - margin_height:
                self.collide = True
                self.player.collide = True
                self.player.rect.x += (self.delta_x - self.player.delta_x) * 2
                self.player.rect.y += (self.delta_y - self.player.delta_y) * 2
                self.player.score  += 10
                self.player.health -= 50
                self.health -= 100
                sfx.play()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.exp = 0
            self.speed = 0
            self.animation_cooldown = self.animation_cooldown // 4
            self.update_action('destroy')
        else: self.update_action('idle')

    def limit_left(self, value=0):
        return self.rect.left + self.delta_x < self.rect.width//10 + value

    def limit_right(self, value=0):
        return self.rect.right + self.delta_x > SCREEN_WIDTH - (self.rect.height//10 + value)

    def limit_up(self, value=0):
        return self.rect.top + self.delta_y < self.rect.height + value

    def limit_down(self, value=0):
        return self.rect.bottom + self.delta_y > SCREEN_HEIGHT - (self.rect.height//10 + value)
