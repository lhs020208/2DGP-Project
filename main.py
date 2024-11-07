from pico2d import *

from background import BGP
from decide_states import decide_state, decide_direct
from grass import Grass
from hitbox_cal import calculate_player_hitbox, calculate_enemy_hitbox
from kamijo import Kamijo
from kfm import KFM
from sky_grass import Sky_Grass

from control import control

def reset_frame():
    global player

    player.frame_step = 0
    player.framex = 0
    player.framey = 0

def move_x(state, walk, shift):
    global Player_x
    global speed
    if state in ['walk', 'run']:
        step_size = 2
        if shift: step_size = 4

        if walk < 0:
            step_size = step_size * -1

        speed += step_size
        max_speed = 5
        if shift: max_speed = 10

        if walk < 0:
            if speed < -1 * max_speed:
                speed = -1 * max_speed
        elif walk > 0:
            if speed > max_speed:
                speed = max_speed

    elif state == 'standing':
        if speed < 0: speed += 1
        elif speed > 0: speed -=1
    Player_x += speed

def check_floor(pos_x, pos_y, speed):
    fell_y = pos_y - speed

    # 발 구간 정의
    current_foot_top = pos_y - 60
    current_foot_bottom = pos_y - 70
    next_foot_top = fell_y - 60
    next_foot_bottom = fell_y - 70

    # floor_T와의 충돌 조건
    if (floor_T >= current_foot_bottom and floor_T <= current_foot_top) or \
       (current_foot_bottom > floor_T and next_foot_bottom <= floor_T):
        return 1

    return 0




def fall(player, enemy):
    global speed_Y, E_speed_Y

    # 플레이어 낙하 처리
    speed_Y -= gravity

    if check_floor(player.x, player.y, speed_Y) and speed_Y < 0:
        speed_Y = 0
        if player.state in ['fall', 'jump', 'double jump' ] :
            player.state = 'standing'
            reset_frame()
    player.y += speed_Y

    # 적 낙하 처리
    for i in range(2):
        E_speed_Y[i] -= gravity
        if check_floor(enemy[i].x, enemy[i].y, E_speed_Y[i]) and E_speed_Y[i] < 0:
            E_speed_Y[i] = 0
            if enemy[i].state in ['fall', 'jump', 'double jump' ] :
                enemy[i].state = 'standing'
        enemy[i].y += E_speed_Y[i]


def handle_events():
    global running, Player_x, Player_y
    global player
    global enemy
    global shift
    global speed_Y
    global walk

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        walk, speed_Y, shift = control(enemy, event, player, walk, speed_Y, shift)


def reset_world():
    global running
    global grass
    global sky_grass
    global player
    global enemy
    global world
    global background

    global Player_x
    global Player_y
    global PNA, PSA, ENA, ESA
    global ENA_left, ENA_right, ENA_top, ENA_bottom
    global ESA_left, ESA_right, ESA_top, ESA_bottom

    global floor_L, floor_R, floor_T
    global sky_floor_L, sky_floor_R, sky_floor_T

    global normal_speed_max, run_speed_max
    global gravity
    global speed, E_speed
    global speed_Y, E_speed_Y

    Player_x = 400
    Player_y = 125
    PNA, PSA= 0,0
    ENA, ESA = [0,0],[0,0]
    ENA_left, ENA_right, ENA_top, ENA_bottom = [0,0],[0,0],[0,0],[0,0]
    ESA_left, ESA_right, ESA_top, ESA_bottom = [0,0],[0,0],[0,0],[0,0]

    floor_L, floor_R, floor_T = 0,0,0
    sky_floor_L = [0, 0, 0]
    sky_floor_R = [0, 0, 0]
    sky_floor_T = [0, 0, 0]

    normal_speed_max = 5
    run_speed_max = 10
    gravity = 2
    speed, speed_Y = 0, 0
    E_speed, E_speed_Y = [0,0], [0,0]

    global shift
    global walk
    shift = 0
    walk = 0

    running = True
    world = []

    background = BGP()
    world.append(background)

    grass = Grass()
    world.append(grass)

    sky_grass = [Sky_Grass(i) for i in range(3)]
    world += sky_grass

    enemy = [KFM() for i in range(2)]
    enemy[1].x -= 100
    world += enemy

    player = Kamijo()
    world.append(player)

def update_world():
    global player
    global enemy

    if player.state in ['standing', 'walk', 'run']:
        player.state = decide_state(player.state, walk, shift)
        player.direct = decide_direct(player.state, player.direct, walk)
    move_x(player.state, walk, shift)
    fall(player, enemy)

    global player_left, player_right, player_top, player_bottom
    global enemy_left, enemy_right, enemy_top, enemy_bottom
    offset_x = Player_x - 400
    offset_y = Player_y - 120
    player_left, player_right, player_top, player_bottom = calculate_player_hitbox(player)
    enemy_left, enemy_right, enemy_top, enemy_bottom = calculate_enemy_hitbox(enemy, offset_x, offset_y)

    global PNA, PNA_left, PNA_right, PNA_top, PNA_bottom
    global PSA, PSA_left, PSA_right, PSA_top, PSA_bottom
    if player.state == 'normal_attack':
        hitbox = player.get_normal_attack_hitbox()
        PNA, PNA_left, PNA_right, PNA_top, PNA_bottom = hitbox
    elif player.state == 'special_attack':
        hitbox = player.get_special_attack_hitbox()
        PSA, PSA_left, PSA_right, PSA_top, PSA_bottom = hitbox

    global ENA, ENA_left, ENA_right, ENA_top, ENA_bottom
    global ESA, ESA_left, ESA_right, ESA_top, ESA_bottom

    for i in range(2):
        if enemy[i].state == 'normal_attack':
            hitbox = enemy[i].get_normal_attack_hitbox(Player_x,Player_y)
            ENA[i], ENA_left[i], ENA_right[i], ENA_top[i], ENA_bottom[i] = hitbox
        elif enemy[i].state == 'special_attack':
            hitbox = enemy[i].get_special_attack_hitbox(Player_x,Player_y)
            ESA[i], ESA_left[i], ESA_right[i], ESA_top[i], ESA_bottom[i] = hitbox

    global floor_L, floor_R, floor_T
    global sky_floor_L, sky_floor_R, sky_floor_T

    hitbox = grass.get_hitbox(Player_x,Player_y)
    floor_L, floor_R, floor_T = hitbox
    for i in range(3):
        hitbox = sky_grass[i].get_hitbox(Player_x,Player_y)
        sky_floor_L[i], sky_floor_R[i], sky_floor_T[i] = hitbox

    for o in world:
        if isinstance(o, Kamijo):  # Kamijo 클래스의 player 객체인 경우
            o.update(speed_Y)  # player에 필요한 인자 전달
        elif isinstance(o, KFM):  # KFM 클래스의 enemy 객체인 경우
            if o == enemy[0]:
                o.update(E_speed_Y[0])  # enemy[0]에 필요한 인자 전달
            elif o == enemy[1]:
                o.update(E_speed_Y[1])  # enemy[1]에 필요한 인자 전달
        else:
            o.update()  # 다른 객체는 인자 없이 호출


def render_world():
    clear_canvas()

    for o in world:
        if isinstance(o, (Grass, Sky_Grass, KFM)):
            o.draw(Player_x, Player_y)
        else:
            o.draw()

    hitbox_point = [load_image('heatbox_point.png') for _ in range(8)]

    for i in range(3):
        hitbox_point[2*i + 0].draw(sky_floor_L[i], sky_floor_T[i])
        hitbox_point[2*i + 1].draw(sky_floor_R[i], sky_floor_T[i])
    hitbox_point[6].draw(floor_L, floor_T)
    hitbox_point[7].draw(floor_R, floor_T)

    update_canvas()

open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()
