from Scripts.scenes import *

class Template():
    # Initialize pygame and mixer
    pygame.init()

    def __init__(self):
        # Create window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock  = pygame.time.Clock()
        pygame.display.set_caption("Template")

        # Create Test
        self.game = Game(self.screen)
        self.item_group = pygame.sprite.Group()

    def restart(self):
        self.player = Player(self.screen, 0, 5, 0, 10, 10, 3, self.game.group_list)
        self.player.spawn = False
        # item = Item(self.screen, self.player, [self.game.item_standby_fx, self.game.item_get_fx], bottomleft=(random.randint(0, SCREEN_WIDTH-SCREEN_WIDTH//10), 0))
        # self.item_group.empty()
        # self.item_group.add(item)

        self.meteor_list = []
        for _ in range(10):
            self.meteor_list.append(Meteor(self.screen, self.player, self.item_group, [self.game.item_standby_fx, self.game.item_get_fx]))


    def main_loop(self):
        self.restart()

        loop = False
        run  = True
        while run:
            # Limit frames per second
            self.clock.tick(FPS)

            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    exit()

                # Keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: # Moving left
                        self.player.moving_left = True
                        self.game.move_fx.play()

                    if event.key == pygame.K_RIGHT: # Moving right
                        self.player.moving_right = True
                        self.game.move_fx.play()

                    if event.key == pygame.K_UP: # Moving up
                        self.player.moving_up = True
                        self.game.move_fx.play()

                    if event.key == pygame.K_DOWN: # Moving down
                        self.player.moving_down = True
                        self.game.move_fx.play()

                    if event.key == pygame.K_r:
                        self.player.shoot(self.game.empty_ammo_fx, self.game.bullet_fx)

                    if event.key == pygame.K_e:
                        self.player.throw(self.game.empty_load_fx, self.game.missile_fx, self.game.missile_cd_fx, self.game.missile_exp_fx)

                    if event.key == pygame.K_SPACE: # Turbo
                        self.player.turbo = True

                    if event.key == pygame.K_RETURN:
                        pass

                    if event.key == pygame.K_ESCAPE: # Quit game
                        loop = True
                        run  = False

                # keyboard release
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:  # Moving left
                        self.player.moving_left = False
                    if event.key == pygame.K_RIGHT: # Moving right
                        self.player.moving_right = False
                    if event.key == pygame.K_UP:    # Moving up
                        self.player.moving_up = False
                    if event.key == pygame.K_DOWN:  # Moving down
                        self.player.moving_down = False
                    if event.key == pygame.K_SPACE: # Turbo
                        self.player.turbo = False

            # Clear screen and set background color
            self.screen.fill(COLOR('ARCADE'))

            ''' --- AREA TO UPDATE AND DRAW --- '''

            self.player.update()
            self.player.draw()
            # print(self.player.delta.x, self.player.speed.y, self.player.health, self.player.ammo, self.player.load)

            # for item in self.item_group:
            #     item.update()
            #     item.draw()

            # for bullet in self.game.bullet_group:
            #     bullet.update()
            #     bullet.draw()

            # for meteor in self.meteor_list:
            #     meteor.check_collision(self.game.explosion_fx)
            #     meteor.update(self.player.turbo)
            #     meteor.draw()

            # for group in self.game.group_list:
            #     group.update()
            #     group.draw(self.screen)

            # Update screen
            pygame.display.update()

        return loop


if __name__ == '__main__':
    template = Template()
    while True:
        loop = template.main_loop()

    pygame.quit() # Quit pygame
