import pygame


# Initialize pygame
pygame.init()

# Screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# Background color
BG = (8, 8, 8)

# Create window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Quest")


# Main loop
run = True
while run:

    # Update background
    screen.fill(BG)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update display
    pygame.display.update()

# Quit pygame
pygame.quit()
