logo_icon = 'Assets/Images/logo_7z.ico'

statue_img = 'Assets/Images/statue.png'


def icon_type_function(i_type):
    icon_img = f'Assets/Images/{i_type}.png'

    if i_type == 'symbol':
        icon_type_dict = {
            'dps_1'  : (1, 1, 1, 1), # Circle
            'tank_1' : (1, 1, 1, 2), # Square
            'heal_1' : (1, 1, 1, 3), # Triangle
        }
    if i_type == 'spaceships':
        icon_type_dict = {
            'dps_1'  : (2, 1, 1, 1), # Dps
            'dps_2'  : (2, 1, 2, 1), # Dps
            'dps_3'  : (2, 1, 3, 1), # Dps
            'dps_4'  : (2, 1, 4, 1), # Dps
            'dps_5'  : (2, 1, 5, 1), # Dps
            'dps_6'  : (2, 1, 6, 1), # Dps

            'tank_1' : (2, 1, 1, 3), # Tank
            'tank_2' : (2, 1, 2, 3), # Tank
            'tank_3' : (2, 1, 3, 3), # Tank
            'tank_4' : (2, 1, 4, 3), # Tank
            'tank_5' : (2, 1, 5, 3), # Tank
            'tank_6' : (2, 1, 6, 3), # Tank

            'heal_1' : (2, 1, 1, 5), # Heal
            'heal_2' : (2, 1, 2, 5), # Heal
            'heal_3' : (2, 1, 3, 5), # Heal
            'heal_4' : (2, 1, 4, 5), # Heal
            'heal_5' : (2, 1, 5, 5), # Heal
            'heal_6' : (2, 1, 6, 5), # Heal
        }

    return icon_img, icon_type_dict


def player_select_function(p_select, p_model):
    player_img = 'Assets/Images/spaceships.png'

    if p_select == 1:
        p_select = 2
    elif p_select == 2:
        p_select = 4

    player_action_dict = {
        'idle' : (2, 1, p_model+1, p_select+1),
        'left' : (1, 1, p_model+1, p_select+1),
        'right': (1, 1, p_model+1, p_select+2),
    }

    return player_img, player_action_dict


def enemy_select_function(e_select):
    enemy_img = 'Assets/Images/enemies.png'

    enemy_action_dict = {
        'idle' : (2, 1, e_select+1, 1),
        'left' : (1, 1, e_select+1, 1),
        'right': (1, 1, e_select+1, 2),
    }

    return enemy_img, enemy_action_dict


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


bg_img = 'Assets/Images/background.jpg'


meteor_img = 'Assets/Images/meteor.png'
meteor_action_dict = {
    'turn_l': (8, 4, 1, 1),
    'turn_r': (8, 4, 5, 1),
}


planet_img = 'Assets/Images/planet.jpg'
planet_dict = {
    'planet_1': (1, 1, 1, 1),
}


explosion_0_img = 'Assets/Images/explosion_0.png'
explosion_1_img = 'Assets/Images/explosion_1.png'
explosion_2_img = 'Assets/Images/explosion_2.png'
explosion_3_img = 'Assets/Images/explosion_3.png'
explosion_dict = {'destroy': (8, 8)}


game_over_img = 'Assets/Images/game_over.png'


# Load music and sounds
scene_music_list = ['music_menu', 'music_game', 'music_record', 'music_combat', 'music_danger']
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
