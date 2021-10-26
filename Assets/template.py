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
        self.game   = Game(self.screen)
        self.player = Player(self.screen, 0, 5, 0, SPEED, 1000, 1000, 3, self.game.group_list)
        self.player.spawn = False

        # Main loop
        self.main_loop()

    def main_loop(self):
        run = True
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

                    if event.key == pygame.K_SPACE:
                        pass

                    if event.key == pygame.K_RETURN:
                        pass

                    if event.key == pygame.K_ESCAPE: # Quit game
                        run = False

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

            # Clear screen and set background color
            self.screen.fill(COLOR('ARCADE'))

            ''' --- AREA TO UPDATE AND DRAW --- '''

            self.player.update()
            self.player.draw()

            self.game.group_list[0].update()
            self.game.group_list[0].draw(self.screen)

            # Update screen
            pygame.display.update()

        # Quit pygame
        pygame.quit()


if __name__ == '__main__':
    template = Template()
