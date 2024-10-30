def calculate_player_heatbox(player, offset_x, offset_y):
    kamijo_box = 140
    kamijo_w = 48
    kamijo_h = 111
    player_left = player.x - kamijo_w / 2
    player_right = player.x + kamijo_w / 2
    player_top = player.y - kamijo_box / 2 + kamijo_h
    player_bottom = player.y - kamijo_box / 2
    return player_left, player_right, player_top, player_bottom


def calculate_enemy_heatbox(enemy_list, offset_x, offset_y):
    kfm_box = 140
    kfm_w = 47
    kfm_h = 106
    enemy_left = [0, 0]
    enemy_right = [0, 0]
    enemy_top = [0, 0]
    enemy_bottom = [0, 0]

    for i in range(2):
        enemy_x = enemy_list[i].x - offset_x
        enemy_y = enemy_list[i].y - offset_y
        enemy_left[i] = enemy_x - kfm_w / 2
        enemy_right[i] = enemy_x + kfm_w / 2
        enemy_top[i] = enemy_y - kfm_box / 2 + kfm_h
        enemy_bottom[i] = enemy_y - kfm_box / 2

    return enemy_left, enemy_right, enemy_top, enemy_bottom
