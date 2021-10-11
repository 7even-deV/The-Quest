# Define caption
CAPTION = ('T h e   Q u e s t   -   ',
('M e n u', 'G a m e', 'R e c o r d'))

# Define fonts
FONTS = ("CabinSketch", "Fixedsys500c", "LibreFranklin", "PoetsenOne")

# Screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

LOGO = 500

# Set framerate
FPS = 60

# Define game variables
LEVEL = 1
SURGE_NUM = 1

enemy_select = 1
enemy_dict = {
    'scale' : [2, 2],
    'ammo'  : [100, 1],
    'load'  : [0, 0],
    'exp'   : [20, 10],
    'pos_x' : [SCREEN_WIDTH//2, -100],
    'pos_y' : [-100, SCREEN_HEIGHT//4],
}

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
