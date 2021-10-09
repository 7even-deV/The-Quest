logo_icon = 'Assets/Images/logo_7z.ico'

statue_img = 'Assets/Images/statue.png'

icon_type_list = ['symbol', 'spaceship']


def icon_type_function(i_type):
    icon_img = f'Assets/Images/{i_type}.png'

    if i_type == 'symbol':
        icon_type_dict = {
            'dps' : (1, 1, 1, 1),  # Circle
            'tank': (1, 1, 1, 2),  # Square
            'heal': (1, 1, 1, 3),  # Triangle
        }
    if i_type == 'spaceship':
        icon_type_dict = {
            'dps' : (2, 1, 1, 1),  # Circle
            'tank': (2, 1, 2, 1),  # Square
            'heal': (2, 1, 3, 1),  # Triangle
        }

    return icon_img, icon_type_dict


def player_select_function(p_select):
    player_img = 'Assets/Images/spaceship.png'

    player_action_dict = {
        'idle' : (2, 1, p_select+1, 1),
        'left' : (1, 1, p_select+1, 1),
        'right': (1, 1, p_select+1, 2),
    }

    return player_img, player_action_dict


def weapon_select_function(w_select):
    bullet_img = f'Assets/Images/bullet_{w_select+1}.png'

    if w_select+1 == 1: # Bullet dps
        bullet_dict = {'bullet': (5, 3, 2, 1),  'destroy': (5, 4, 5, 1)}

    if w_select+1 == 2: # Bullet tank
        bullet_dict = {'bullet': (5, 11, 1, 1), 'destroy': (5, 4, 12, 1)}

    if w_select+1 == 3: # Bullet heal
        bullet_dict = {'bullet': (8, 3, 2, 1),  'destroy': (8, 4, 5, 1)}

    return bullet_img, bullet_dict

missile_img = f'Assets/Images/missile.png'
missile_dict = {'missile': (5, 11, 1, 1), 'destroy': (5, 4, 12, 1)}
missile_exp_img = f'Assets/Images/missile_exp_2.png'
missile_exp_dict = {'destroy': (5, 6)}


enemy_img = 'Assets/Images/enemy.png'
enemy_action_dict = {
    'idle' : (2, 1, 1, 1),
    'left' : (1, 1, 1, 1),
    'right': (1, 1, 1, 2),
}

bg_img = 'Assets/Images/background.jpg'

meteor_img = 'Assets/Images/meteor.png'
meteor_action_dict = {
    'turn_l': (8, 4, 1, 1),
    'turn_r': (8, 4, 5, 1),
}

explosion_0_img = 'Assets/Images/explosion_0.png'
explosion_1_img = 'Assets/Images/explosion_1.png'
explosion_2_img = 'Assets/Images/explosion_2.png'
explosion_3_img = 'Assets/Images/explosion_3.png'
explosion_dict = {'destroy': (8, 8)}


game_over_img = 'Assets/Images/game_over.png'


# Load music and sounds
scene_music_list = ['music_menu', 'music_game', 'music_record']
def load_music(scene_music):
    return f'Assets/Audio/music/{scene_music_list[scene_music]}.ogg'

sound_list = [
    'select', 'select_loop', 'portal_loop', 'confirm', 'start', 'pause',
    'bullet', 'empty_ammo', 'missile', 'missile_countdown', 'missile_explosion', 'empty_load',
    'move', 'backmove', 'turbo', 'explosion', 'win', 'death', 'game_over',
]
def load_sound(sfx):
    if sfx in sound_list:
        return f'Assets/Audio/sound/{sfx}.ogg'
