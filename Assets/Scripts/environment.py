import pygame, random

from .manager import planet_def
from .tools   import Sprite_sheet


class Foreground():

    def __init__(self, screen, SCREEN_W, SCREEN_H, *args):
        self.screen = screen
        self.SCREEN_W = SCREEN_W
        self.SCREEN_H = SCREEN_H

        self.pos_list = []
        for star in range(*args):
            pos_x = random.randint(0, self.SCREEN_W)
            pos_y = random.randint(0, self.SCREEN_H)
            self.pos_list.append([pos_x, pos_y])

        self.delta_x = 0
        self.delta_y = 0
        self.speed = 0.5

    def update(self, player):
        # Follow the movement with the Player
        self.delta_x = -(player.delta.x * (self.speed/2))
        if player.turbo: self.delta_y = self.speed * (2 + player.turbo_up)
        else: self.delta_y = self.speed

    def draw(self):
        # Draw randomly placed stars on the screen
        for pos in self.pos_list:
            color = random.randint(0, 255)
            radius = random.randint(0, 4)
            pygame.draw.circle(self.screen, (color, color, color), pos, radius)
            pos[0] += self.delta_x
            pos[1] += self.delta_y
            # Random reset from top when loop ends down
            if pos[1] > self.SCREEN_H:
                pos[0] = random.randint(0, self.SCREEN_W)
                pos[1] = 0


class Background():

    def __init__(self, screen, SCREEN_W, SCREEN_H, *args):
        self.screen = screen
        self.SCREEN_W = SCREEN_W
        self.SCREEN_H = SCREEN_H

        self.image   = pygame.image.load(*args).convert_alpha()
        self.rect    = self.image.get_rect()
        self.delta_y = 0
        self.speed   = 0.5

    def update(self, player):
        self.player_x = player.rect.x

        # Move the delta y and increase the speed if the player turbo
        if player.turbo: self.delta_y += self.speed * (2 + player.turbo_up)
        else: self.delta_y += self.speed

        # Relative y that uses the rest of the image height for looping display
        self.relative_y = self.delta_y % self.rect.height

    def draw(self):
        # Repeat the image in a loop following the movement with the player
        for scroll_x in range(2):
            self.screen.blit(self.image, (scroll_x * self.rect.width - self.player_x * self.speed/2, self.relative_y - self.rect.height))
            # Recover the image if it finishes before
            if self.relative_y < self.SCREEN_H:
                self.screen.blit(self.image, (scroll_x * self.rect.width - self.player_x * self.speed/2, self.relative_y))


class Farground():

    def __init__(self, screen, SCREEN_W, SCREEN_H, *args):
        self.screen = screen
        self.SCREEN_W = SCREEN_W
        self.SCREEN_H = SCREEN_H

        self.pos_list = []
        for star in range(*args):
            pos_x = random.randint(0, self.SCREEN_W)
            pos_y = random.randint(0, self.SCREEN_H)
            self.pos_list.append([pos_x, pos_y])

        self.delta_x = 0
        self.delta_y = 0
        self.speed = 0.5

    def update(self, player):
        # Follow the movement with the Player
        self.delta_x = -(player.delta.x * (self.speed/2)) if player.alive else 0
        if player.turbo: self.delta_y = self.speed * (2 + player.turbo_up)
        else: self.delta_y = self.speed

    def draw(self):
        # Draw randomly placed stars on the screen
        for pos in self.pos_list:
            color = random.randint(0, 255)
            radius = random.randint(0, 4)
            pygame.draw.circle(self.screen, (color, color, color), pos, radius)
            pos[0] += self.delta_x
            pos[1] += self.delta_y
            # Random reset from top when loop ends down
            if pos[1] > self.SCREEN_H:
                pos[0] = random.randint(0, self.SCREEN_W)
                pos[1] = 0


class Planet(Sprite_sheet):

    def __init__(self, screen, planet, init_planet, SCREEN_W, SCREEN_H, **kwargs):
        planet_img, planet_dict = planet_def()
        super().__init__(planet_img)
        self.create_animation(800, 800, planet_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect  = self.image.get_rect(**kwargs)

        self.screen = screen
        self.planet = planet
        self.total_planet   = len(planet_dict) - 1
        self.origin_planet  = init_planet
        self.destiny_planet = random.randint(1, self.total_planet)
        self.SCREEN_W = SCREEN_W
        self.SCREEN_H = SCREEN_H

        self.move_x = 0
        self.speed = 1

    def update(self, player):
        # Follow the image movement with the Player from the center of the screen
        self.relative_x = self.move_x + (self.SCREEN_W // 2 - self.image.get_rect().width // 2)
        self.update_animation()

        if self.origin_planet == self.destiny_planet:
            self.destiny_planet = random.randint(1, self.total_planet)

        if self.planet == 'origin':
            self.update_action(f'planet_{self.origin_planet}')
            self.flip_x = self.flip_y = False
            if self.rect.top < self.SCREEN_H:
                # Follow the movement with the Player
                self.move_x += 0
                if player.turbo: self.rect.y += self.speed * (2 + player.turbo_up)
                else: self.rect.y += self.speed
            else: self.kill()

        if self.planet == 'destiny':
            self.update_action(f'planet_{self.destiny_planet}')
            self.flip_x = self.flip_y = True
            if player.win and self.rect.top < 0:
                # Follow the movement with the Player
                self.move_x += 0
                if player.turbo: self.rect.y += self.speed * (2 + player.turbo_up)
                else: self.rect.y += self.speed

    def draw(self):
        image = pygame.transform.flip(self.image, self.flip_x, self.flip_y)
        image.set_colorkey(False)
        self.screen.blit(image, (self.relative_x, self.rect.y))
