DB_FILE = 'Assets/Data/BBDD.db'
TBL_NAME = 'GAMMER'
SQL = '''(
    USERNAME text PRIMARY KEY,
    STYLE integer,
    MODEL integer,
    WEAPON integer,
    LEVEL integer,
    HIGHLEVEL integer,
    SCORE integer,
    HIGHSCORE integer,
    ENEMY integer,
    T_ENEMY integer,
    METEOR integer,
    T_METEOR integer,
    MUSIC float,
    SOUND float,
    SCREEN_W integer,
    SCREEN_H integer,
    PLAY integer
)'''

MEMORY_LIST = [('empty', 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0.5, 0.5, 800, 800, 1)]
# MEMORY_LIST = []
# for num in range(10):
#     MEMORY_LIST.append((f"empty-{num}", 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0.5, 0.5, 800, 800, ))


msg_dict = {
    0 : "",
    1 : "User exists",
    2 : "Maximum characters",
    3 : "User created successfully",
    4 : "User removed successfully",
    5 : "The user list is empty",
    6 : "Select a user",
    7 : "Press <Space> to write and <Enter> to confirm",
}
advice_dict = {
    0 : "Watch out for missiles, they will sound before they explode",
    1 : "Dragon items will detonate anything in range",
    2 : "Play in moderation and share the experience",
    3 : "Your weapon can hit up to 4 bullets per shot",
    4 : "The faster enemy only fire 1 time in each encounter",
    5 : "Remember to use the turbo, you will reduce the travel time",
}


logo_icon  = 'Assets/Images/logo_7z.ico'

statue_img = 'Assets/Images/statue.png'
bg_img     = 'Assets/Images/background.jpg'


# Define fonts
def font_type_def(font):
    font_tuple = ("GameCuben", "FixedsysTTF", "LibreFranklinThin", "NasalizationRg", "PoetsenOne", "SpaceAge")
    return f'Assets/Fonts/{font_tuple[font]}.ttf'


def button_def():
    button_img = 'Assets/Images/button.png'
    button_dict = {
        'off' : (1, 1, 1, 1),
        'on'  : (1, 1, 2, 1),
    }
    return button_img, button_dict


def button_list_def(scene):
    if   scene == 'main':
        button_list = [
            [
            "Account",
            "Records",
            "History",
            "Exit",
            ],[
            "Login",
            "Delete",
            "Guide",
            "Back",
            ],[
            "Play",
            "Edit",
            "Configs",
            "Back",
            ]
        ]
    elif scene == 'game':
        button_list = [
            [
            "Continue",
            "Settings",
            "Help",
            "Exit",
            ],[
            "Restart",
            "Settings",
            "Help",
            "Exit",
            ]
        ]
    elif scene == 'record':
        button_list = [
            [
            "Top-ranking",
            "Main-menu",
            "Credits",
            "Exit",
            ],[
            "Continue",
            "Main-menu",
            "Credits",
            "Back",
            ]
        ]
    return button_list


def key_def():
    key_img = 'Assets/Images/key.png'
    key_dict = {
        'off' : (1, 1, 1, 1),
        'on'  : (1, 1, 2, 1),
    }
    return key_img, key_dict

keyboard_list = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm', '-', '<<', '±'],
]


def bar_def():
    bar_img = 'Assets/Images/bar.png'
    bar_dict = {
        'displace' : (1, 1, 1, 1),
    }
    return bar_img, bar_dict

bar_list = [
    "Music vol.",
    "Sound vol.",
    "Window size",
]


def board_def():
    board_img = 'Assets/Images/board.png'
    board_dict = {
        'off' : (1, 1, 1, 1),
        'on'  : (1, 1, 2, 1),
    }
    return board_img, board_dict


def logo_type_def(logo):
    logo_img = f'Assets/Images/{logo}.png'

    if   logo == 'loading':
        logo_dict = {logo: (2, 4, 1, 1)}
        logo_size = (800, 400)

    elif logo == 'game_over':
        logo_dict = {logo: (1, 3, 1, 1)}
        logo_size = (600, 350)

    return logo_img, logo_dict, logo_size


def icon_type_def(icon):
    icon_img = f'Assets/Images/{icon}.png'

    if icon == 'symbol':
        icon_type_dict = {
            'dps_1'  : (1, 1, 1, 1), # Circle
            'dps_2'  : (1, 1, 1, 1), # Circle
            'dps_3'  : (1, 1, 1, 1), # Circle

            'tank_1' : (1, 1, 1, 2), # Square
            'tank_2' : (1, 1, 1, 2), # Square
            'tank_3' : (1, 1, 1, 2), # Square

            'heal_1' : (1, 1, 1, 3), # Triangle
            'heal_2' : (1, 1, 1, 3), # Triangle
            'heal_3' : (1, 1, 1, 3), # Triangle
        }
    elif icon == 'spaceships':
        icon_type_dict = {
            'dps_1'  : (2, 1, 1, 1), # Dps
            'dps_2'  : (2, 1, 2, 1), # Dps
            'dps_3'  : (2, 1, 3, 1), # Dps

            'tank_1' : (2, 1, 1, 3), # Tank
            'tank_2' : (2, 1, 2, 3), # Tank
            'tank_3' : (2, 1, 3, 3), # Tank

            'heal_1' : (2, 1, 1, 5), # Heal
            'heal_2' : (2, 1, 2, 5), # Heal
            'heal_3' : (2, 1, 3, 5), # Heal
        }
    return icon_img, icon_type_dict


def player_select_def(select, model):
    player_img = 'Assets/Images/spaceships.png'

    if select   == 1: select = 2
    elif select == 2: select = 4

    player_action_dict = {
        'idle' : (2, 1, model+1, select+1),
        'left' : (1, 1, model+1, select+1),
        'right': (1, 1, model+1, select+2),
    }
    return player_img, player_action_dict


def enemy_select_def(select):
    enemy_img = 'Assets/Images/enemies.png'

    enemy_action_dict = {
        'idle' : (2, 1, select+1, 1),
        'left' : (1, 1, select+1, 1),
        'right': (1, 1, select+1, 2),
    }
    return enemy_img, enemy_action_dict


def meteor_def():
    meteor_img = 'Assets/Images/meteor.png'
    meteor_action_dict = {
        'turn_l' : (8, 4, 1, 1),
        'turn_r' : (8, 4, 5, 1),
    }
    return meteor_img, meteor_action_dict


def bullet_select_def(select):
    bullet_img  = 'Assets/Images/bullet.png'
    destroy_img = 'Assets/Images/bullet_destroy.png'

    if select+1 == 1: # Bullet dps
        bullet_dict = {'bullet': (6, 4, 1, 1)}

    elif select+1 == 2: # Bullet tank
        bullet_dict = {'bullet': (6, 4, 5, 7)}

    elif select+1 == 3: # Bullet heal
        bullet_dict = {'bullet': (6, 4, 5, 1)}

    else: # Bullet enemy
        bullet_dict = {'bullet': (6, 4, 1, 7)}

    return bullet_img, bullet_dict, destroy_img


def missile_select_def(select, explosion):
    if not explosion:
        missile_img  = f'Assets/Images/missile.png'
        missile_dict = {'missile': (5, 11, 1, 1), 'destroy': (5, 4, 12, 1)}
        return missile_img, missile_dict

    else:
        missile_exp_img  = f'Assets/Images/missile_exp_{select+1}.png'
        missile_exp_dict = {'destroy': (5, 6, 1, 1)}
        return missile_exp_img, missile_exp_dict


def item_def():
    item_img       = 'Assets/Images/items.png'
    item_get_img   = 'Assets/Images/item_get.png'
    item_type_dict = {
        'lives'  : (1, 1, 1, 5),
        'health' : (1, 1, 5, 1),
        'shield' : (1, 1, 1, 2),
        'speed'  : (1, 1, 4, 2),
        'turbo'  : (1, 1, 3, 1),
        'time'   : (1, 1, 8, 3),
        'freeze' : (1, 1, 1, 3),
        'ammo'   : (1, 1, 7, 4),
        'load'   : (1, 1, 3, 3),
        'weapon' : (1, 1, 5, 5),
        'atomic' : (1, 1, 6, 1),
        'score'  : (1, 1, 6, 5),
        'super'  : (1, 1, 3, 5),
    }
    return item_img, item_type_dict, item_get_img

freeze_img = 'Assets/Images/freeze.png'


def planet_def():
    planet_img = 'Assets/Images/planets.png'
    planet_dict = {
        'planet_1' : (1, 1, 1, 1),
        'planet_2' : (1, 1, 1, 2),
        'planet_3' : (1, 1, 1, 3),
        'planet_4' : (1, 1, 2, 1),
        'planet_5' : (1, 1, 2, 2),
        'planet_6' : (1, 1, 2, 3),
    }
    return planet_img, planet_dict


def explosion_type_def(num):
    explosion_img = f'Assets/Images/explosion_{num}.png'
    explosion_dict = {
        'death'   : (8, 8, 1, 1),
        'destroy' : (8, 8, 1, 1),
    }
    return explosion_img, explosion_dict


# Load music and sounds
def load_music(music):
    scene_music_list = ['main', 'menu', 'record', 'game', 'record', 'danger']
    return f'Assets/Audio/_music_{scene_music_list[music]}.ogg'


def load_sound(sfx):
    sound_list = [
        'select',
        'select_loop',
        'portal_loop',
        'confirm',
        'start',
        'pause',
        'bullet',
        'empty_ammo',
        'missile',
        'missile_countdown',
        'missile_explosion',
        'empty_load',
        'move',
        'backmove',
        'turbo',
        'explosion',
        'item_standby',
        'item_get',
        'win',
        'death',
        'game_over',
    ]
    if sfx in sound_list:
        return f'Assets/Audio/{sfx}.ogg'
    else:
        return f'Assets/Audio/game_over.ogg'
