import pygame, random

from .manager import item_function
from .tools   import Sprite_sheet, Particles, Timer


class Item(Sprite_sheet):

    def __init__(self, item, screen, player, SCREEN_W, SCREEN_H, *args, **kwargs):
        item_img, item_type_dict, item_get_img = item_function()
        super().__init__(item_img)
        self.screen = screen
        self.player = player
        self.SCREEN_W = SCREEN_W
        self.SCREEN_H = SCREEN_H
        self.item_standby_fx = args[0][0]
        self.item_get_fx     = args[0][1]

        # Create image and rect
        self.create_animation(100, 100, item_type_dict, scale=0.5)
        self.sheet = pygame.image.load(item_get_img).convert_alpha()
        self.create_animation(100, 100, {'destroy': (8, 8, 1, 1)}, scale=0.5)
        self.image  = self.animation_dict[self.action][self.frame_index]
        self.width  = self.image.get_width()
        self.height = self.image.get_height()
        self.rect   = self.image.get_rect(**kwargs)

        self.item_list = list(item_type_dict)[:-1]
        self.chance = False

        if item == 'random':
            self.item_type = random.choice(self.item_list)
            self.validation_loop()

        elif item == 'chance':
            self.item_type = random.choice(self.item_list)
            self.validation_loop()
            self.chance = True
        else:
            self.item_type = item

        self.update_action(self.item_type)

        self.speed   = 1
        self.collide = False
        self.zoom    = True

        self.particles = Particles('glow', self.screen, 10, self.image)
        self.timer = [Timer(), Timer()]

    def validation_loop(self):
        validate = True
        while validate:
            if   self.item_type == 'health' and self.player.health >= self.player.max_health:
                self.item_type = random.choice(self.item_list)

            elif self.item_type == 'weapon' and self.player.weapon >= 4:
                self.item_type = random.choice(self.item_list)

            elif self.item_type == 'time' and self.player.less_time:
                self.item_type = random.choice(self.item_list)

            elif self.item_type == 'shield' and self.player.shield:
                self.item_type = random.choice(self.item_list)

            elif self.item_type == 'freeze' and self.player.freeze:
                self.item_type = random.choice(self.item_list)

            elif self.item_type == 'atomic' and self.player.atomic:
                self.item_type = random.choice(self.item_list)

            else: validate = False

    def update(self):
        self.update_animation(10)

        if not self.collide:
            self.check_collision()
            self.particles.add_glow(self.rect.centerx, self.rect.centery, 1, 1)

            if self.timer[0].counter(0.05, True):
                self.visual_effect(5)

            if self.timer[1].counter(1, True):
                self.item_standby_fx.play()

                if self.chance:
                    self.item_type = random.choice(self.item_list)
                    self.validation_loop()
                    self.update_action(self.item_type)

            # kill if it moves off the bottom of the screen
            if self.rect.top > self.SCREEN_H:
                self.kill()

            self.rect.y += self.speed

        else: # Delete the item
            self.update_action('destroy')

    def visual_effect(self, value):
        if self.zoom:
            if self.rect.w < self.width + value and self.rect.h < self.height + value:
                self.rect.x -= 1
                self.rect.y -= 1
                self.rect.w += 1
                self.rect.h += 1
            else: self.zoom = False

        else:
            if self.rect.w > self.width - value and self.rect.h > self.height - value:
                self.rect.x += 1
                self.rect.y += 1
                self.rect.w -= 1
                self.rect.h -= 1
            else: self.zoom = True

    def check_collision(self):
        # Check if the player has picked up the box
        if pygame.sprite.collide_rect(self, self.player):

            # Check what type of item it was
            if self.item_type == 'lives':
                self.player.lives += 1

            elif self.item_type == 'health':
                self.player.health += self.player.max_health // 2
                if self.player.health > self.player.max_health:
                    self.player.health = self.player.max_health

            elif self.item_type == 'speed':
                self.player.max_speed += 0.25

            elif self.item_type == 'turbo':
                self.player.turbo_up += 1

            elif self.item_type == 'time':
                self.player.less_time = True

            elif self.item_type == 'ammo':
                self.player.ammo += self.player.start_ammo // 4

            elif self.item_type == 'load':
                self.player.load += 1

            elif self.item_type == 'weapon':
                if self.player.weapon < 4:
                    self.player.weapon += 1

            elif self.item_type == 'shield':
                self.player.shield = True

            elif self.item_type == 'freeze':
                self.player.freeze = True

            elif self.item_type == 'atomic':
                self.player.atomic = True

            elif self.item_type == 'score':
                self.player.score += 1000

            elif self.item_type == 'super':
                self.player.health = self.player.max_health
                self.player.shield = True
                self.player.max_speed += 1.0
                self.player.turbo_up += 1
                self.player.ammo = self.player.start_ammo
                self.player.load = self.player.start_load

            self.collide = True
            self.item_get_fx.play()
