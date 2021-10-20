import random


# Define caption
CAPTION = ('T h e   Q u e s t   -   ',
('M a i n', 'M e n u', 'G a m e', 'R e c o r d'))

# Screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800


VOL_MUSIC = 1
VOL_SOUND = 1
LOGO = 500

# Set framerate
FPS = 60

# Define game variables
SCENE = 0
LIVES = 3
LEVEL = 1
SURGE_NUM = 1

# enemy_select = random.randint(0, 2)
enemy_select = 0
enemy_dict = {
    'ammo'  : [100, 10, 0],
    'load'  : [0, 0, 1],
    'exp'   : [20, 10, 30],
}
def enemy_position(select, for_enemy):
    if select == 0:
        return (random.randint(100, SCREEN_WIDTH-100), -100)
    if select == 1:
        return (-100*for_enemy, SCREEN_HEIGHT//5)
    if select == 2:
        return (random.randint(100, SCREEN_WIDTH-100), -100)


# Define colours (R, G, B)
def COLOR(color_key):
    color_dict = {
        'BLACK'  : (0, 0, 0),
        'DARK'   : (64, 64, 64),
        'GRAY'   : (128, 128, 128),
        'SILVER' : (192, 192, 192),
        'WHITE'  : (255, 255, 255),

        'BROWN'  : (255, 192, 192),
        'MAROON' : (128, 0, 0),
        'RED'    : (255, 0, 0),
        'ORANGE' : (255, 128, 0),
        'GREEN'  : (0, 128, 0),
        'LIME'   : (0, 255, 0),
        'OLIVE'  : (128, 128, 0),
        'YELLOW' : (255, 255, 0),
        'CYAN'   : (0, 255, 255),
        'SKY'    : (0, 128, 255),
        'TEAL'   : (0, 128, 128),
        'BLUE'   : (0, 0, 255),
        'NAVY'   : (0, 0, 128),
        'PINK'   : (255, 0, 255),
        'PURPLE' : (128, 0, 128),

        'ARCADE' : (8, 8, 8),
    }
    return color_dict[color_key.upper()]
