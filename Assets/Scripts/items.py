import pygame, random

from .settings import SCREEN_WIDTH, SCREEN_HEIGHT
from .manager  import item_img, item_type_dict, item_get_img
from .tools    import Sprite_sheet, Particles, Timer


class Item(Sprite_sheet):

    def __init__(self, screen, player, *args, **kwargs):
        super().__init__(item_img)
        self.screen = screen
        self.player = player
        self.item_standby_fx = args[0][0]
        self.item_get_fx     = args[0][1]

        # Create image and rect
        self.create_animation(50, 50, item_type_dict)
        self.sheet = pygame.image.load(item_get_img).convert_alpha()
        self.create_animation(50, 50, {'destroy': (8, 8, 1, 1)})
        self.image  = self.animation_dict[self.action][self.frame_index]
        self.width  = self.image.get_width()
        self.height = self.image.get_height()
        self.rect   = self.image.get_rect(**kwargs)

        self.item_type = random.choice(list(item_type_dict)[:-1])
        print(self.item_type)
        self.update_action(self.item_type)
        self.speed   = 1
        self.collide = False
        self.zoom    = True

        self.particles = Particles('glow', self.screen, 10, self.image)
        self.timer = [Timer(), Timer()]
        self.item_standby_fx.play()

    def update(self):
        self.update_animation(10)

        if not self.collide:
            self.check_collision()
            self.particles.add_glow(self.rect.centerx, self.rect.centery, 1, 1)

            if self.timer[0].counter(0.05, True):
                self.effect(5)

            if self.timer[1].counter(1, True):
                self.item_standby_fx.play()

            # kill if it moves off the bottom of the screen
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()

            self.rect.y += self.speed

        else: # Delete the item
            self.update_action('destroy')

    def effect(self, value):
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
                self.player.health += 25
                if self.player.health > self.player.max_health:
                    self.player.health = self.player.max_health

            elif self.item_type == 'shield':
                self.player.shield = True

            elif self.item_type == 'speed':
                self.player.max_speed += 1.0

            elif self.item_type == 'turbo':
                self.player.turbo = True

            elif self.item_type == 'time':
                self.player.item_time = True

            elif self.item_type == 'ammo':
                self.player.ammo += 20

            elif self.item_type == 'load':
                self.player.load += 1

            # elif self.item_type == 'weapon':
            #     self.player.weapon += 1

            self.collide = True
            self.item_get_fx.play()