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

explosion_img = 'Assets/Images/explosion.png'
explosion_dict = {
    'destroy': (8, 8),
}
