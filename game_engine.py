from pico2d import *
import time

from sdl2.examples.pong import Player

from background import BGP
from decide_states import decide_state, decide_direct
from effect import EFFECT
from game_end import GAME_END
from grass import Grass
from hitbox_cal import calculate_player_hitbox, calculate_enemy_hitbox
from kamijo import Kamijo
from kfm import KFM
from sky_grass import Sky_Grass

from control import control
from AI_control import ai_control, chage_ai_state
from state_bar import State_bar


def reset_frame():
    global player

    player.frame_step = 0
    player.framex = 0
    player.framey = 0

def move_x(state, walk, shift):
    global Player_x
    global speed

    PIXEL_PER_METER = (11.0 / 16.0)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


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
    elif state in ['jump', 'double jump', 'fall'] and moving:
        step_size = 1
        if walk < 0:
            step_size = step_size * -1
        elif walk == 0:
            step_size = 0

        speed += step_size
        max_speed = 10

        if walk < 0:
            if speed < -1 * max_speed:
                speed = -1 * max_speed
        elif walk > 0:
            if speed > max_speed:
                speed = max_speed
    elif state == 'thrown' and speed_Y != 0:
        pass
    else:
        if speed < 0: speed += 1
        elif speed > 0: speed -=1
    Player_x += speed * RUN_SPEED_PPS * frame_time * 5

def E_move_x(enemy, state, walk, shift, i):
    global E_speed

    PIXEL_PER_METER = (11.0 / 16.0)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    if i == 1: RUN_SPEED_PPS +=1

    if state in ['walk', 'run']:
        step_size = 2
        if shift: step_size = 4

        if walk < 0:
            step_size = step_size * -1

        E_speed[i] += step_size
        max_speed = 5
        if shift: max_speed = 10

        if walk < 0:
            if E_speed[i] < -1 * max_speed:
                E_speed[i] = -1 * max_speed
        elif walk > 0:
            if E_speed[i] > max_speed:
                E_speed[i] = max_speed
    elif state in ['jump', 'double jump', 'fall'] and moving:
        step_size = 1
        if walk < 0:
            step_size = step_size * -1
        elif walk == 0:
            step_size = 0

        E_speed[i] += step_size
        max_speed = 10

        if walk < 0:
            if E_speed[i] < -1 * max_speed:
                E_speed[i] = -1 * max_speed
        elif walk > 0:
            if E_speed[i] > max_speed:
                E_speed[i] = max_speed
    elif state in ['standing', 'hit']:
        if E_speed[i] < 0: E_speed[i] += 1
        elif E_speed[i] > 0: E_speed[i] -=1
    elif state == 'thrown' and E_speed_Y[i] == 0:
        if E_speed[i] < 0: E_speed[i] += 1
        elif E_speed[i] > 0: E_speed[i] -=1


    enemy.x += E_speed[i] * RUN_SPEED_PPS * frame_time * 5

def check_floor(pos_x, pos_y, speed):
    fell_y = pos_y - speed

    # 발 구간 정의
    current_foot_top = pos_y - 50
    current_foot_bottom = pos_y - 70
    next_foot_top = fell_y - 50
    next_foot_bottom = fell_y - 70

    # floor_T와의 충돌 조건 강화
    if floor_R > pos_x > floor_L:
        if (next_foot_bottom <= floor_T <= next_foot_top) or \
            (current_foot_bottom <= floor_T <= current_foot_top) or \
            (current_foot_bottom > floor_T >= next_foot_bottom):
            return floor_T + 70

    for i in range(3):
        if sky_floor_R[i] > pos_x > sky_floor_L[i]:
            if (next_foot_bottom <= sky_floor_T[i] <= next_foot_top) or \
                    (current_foot_bottom <= sky_floor_T[i] <= current_foot_top) or \
                    (current_foot_bottom > sky_floor_T[i] >= next_foot_bottom):
                return sky_floor_T[i] + 70

    return -1

def fall(stop_control, player, enemy):
    global speed_Y, E_speed_Y
    global Player_x, Player_y
    global E_event

    if stop_control != 1:
        # 플레이어 낙하 처리
        speed_Y -= gravity
        if speed_Y <= -20: speed_Y = -20

        # 충돌 감지
        stop_y = check_floor(Player_x, Player_y, speed_Y)
        if stop_y >= 0 > speed_Y:
            speed_Y = 0
            Player_y = stop_y
            if player.state in ['fall', 'jump', 'double jump']:
                player.state = 'standing'
                reset_frame()
        else:
            #player.y += speed_Y
            Player_y += speed_Y  # Player_y 동기화
    # 적 낙하 처리
    for i in range(2):
        E_speed_Y[i] -= gravity
        if E_speed_Y[i] <= -20: E_speed_Y[i] = -20

        # 충돌 감지
        stop_y = check_floor(enemy[i].x, enemy[i].y, E_speed_Y[i])
        if stop_y >= 0 > E_speed_Y[i]:
            # 충돌한 경우 속도를 0으로 설정하고 위치 수정
            E_speed_Y[i] = 0
            enemy[i].y = stop_y
            if enemy[i].state in ['fall', 'jump', 'double jump']:
                E_event[i] = chage_ai_state(enemy[i], E_event[i], "standing")
        else:
            # 충돌하지 않은 경우 계속 낙하
            enemy[i].y += E_speed_Y[i]



def handle_events():
    global running, Player_x, Player_y
    global player
    global enemy
    global shift
    global speed_Y
    global walk
    global moving

    global ai_on
    global stop_control
    global start

    events = get_events()
    for event in events:
        if  event.type == SDL_KEYDOWN and start == 0:
            start = 1
            ai_on = 1
            stop_control = 0

        if event.type == SDL_QUIT:
            running = False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        if stop_control == 0:
            walk, speed_Y, shift, moving = control(enemy, event, player, walk, speed_Y, shift, moving)

def reset_world():
    global ai_on
    global stop_control
    global start
    global loading

    ai_on = 0
    stop_control = 1
    start = 0
    loading = load_image('UI/start_screen.png')

    global running
    global grass
    global sky_grass
    global player
    global enemy
    global world
    global background
    global state_bar
    global ge
    global eff

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
    global moving

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
    moving = 0

    global shift
    global walk
    shift = 0
    walk = 0
    global E_event
    global E_shift
    global E_walk
    global E_moving
    E_event = ['standing', 'standing']
    E_shift = [0,0]
    E_walk = [0,0]
    E_moving = [0, 0]

    running = True
    world = []

    background = BGP()
    world.append(background)

    grass = Grass()
    world.append(grass)

    sky_grass = [Sky_Grass(i) for i in range(3)]
    world += sky_grass

    enemy = [KFM() for i in range(2)]
    enemy[0].x = -100
    enemy[0].y = 350
    enemy[1].x = 900
    enemy[1].y = 350
    world += enemy

    player = Kamijo()
    world.append(player)

    eff = [EFFECT() for i in range(3)]
    world += eff

    state_bar = State_bar()
    world.append(state_bar)

    ge = GAME_END()
    world.append(ge)


def update_world():
    global player
    global enemy
    global Player_x
    global Player_y
    global player_left, player_right, player_top, player_bottom
    global enemy_left, enemy_right, enemy_top, enemy_bottom
    global PNA, PNA_left, PNA_right, PNA_top, PNA_bottom
    global PSA, PSA_left, PSA_right, PSA_top, PSA_bottom
    global ENA, ENA_left, ENA_right, ENA_top, ENA_bottom
    global ESA, ESA_left, ESA_right, ESA_top, ESA_bottom
    global floor_L, floor_R, floor_T
    global sky_floor_L, sky_floor_R, sky_floor_T
    global speed, speed_Y
    global E_event
    global E_shift
    global E_walk
    global E_moving
    global E_speed_Y, E_speed
    global ai_on
    global stop_control

    if player.state in ['standing', 'walk', 'run']:
        player.state = decide_state(player.state, walk, shift)
        player.direct = decide_direct(player.state, player.direct, walk)
    if stop_control != 1:
        move_x(player.state, walk, shift)
    for i in range(2):
        E_move_x(enemy[i], enemy[i].state, E_walk[i], E_shift[i], i)
    fall(stop_control, player, enemy)

    offset_x = Player_x - 400
    offset_y = Player_y - 200
    player_left, player_right, player_top, player_bottom = calculate_player_hitbox(player)
    enemy_left, enemy_right, enemy_top, enemy_bottom = calculate_enemy_hitbox(enemy, offset_x, offset_y)


    if player.state == 'normal_attack':
        hitbox = player.get_normal_attack_hitbox()
        PNA, PNA_left, PNA_right, PNA_top, PNA_bottom = hitbox
    elif player.state == 'special_attack':
        hitbox = player.get_special_attack_hitbox()
        PSA, PSA_left, PSA_right, PSA_top, PSA_bottom = hitbox

    for i in range(2):
        if enemy[i].state == 'normal_attack':
            hitbox = enemy[i].get_normal_attack_hitbox(Player_x,Player_y)
            ENA[i], ENA_left[i], ENA_right[i], ENA_top[i], ENA_bottom[i] = hitbox
        elif enemy[i].state == 'special_attack':
            hitbox = enemy[i].get_special_attack_hitbox(Player_x,Player_y)
            ESA[i], ESA_left[i], ESA_right[i], ESA_top[i], ESA_bottom[i] = hitbox


    hitbox = grass.get_hitbox(player.x,player.y)
    floor_L, floor_R, floor_T = hitbox
    for i in range(3):
        hitbox = sky_grass[i].get_hitbox(player.x,player.y)
        sky_floor_L[i], sky_floor_R[i], sky_floor_T[i] = hitbox

    for i in range (2):

        if PNA == 1:
            if (enemy_left[i] < PNA_right and enemy_right[i] > PNA_left and
                    enemy_top[i] > PNA_bottom and enemy_bottom[i] < PNA_top
                    and player.stop_attack != 1):
                E_event[i] = chage_ai_state(enemy[i], E_event[i], "HIT")
                enemy[i].damage += 10
                E_speed[i] = 0.2 * player.direct * (enemy[i].damage / 20)
                E_speed_Y[i] = 8.0
                player.stop_attack = 1
                enemy[i].stand_time = 0
                eff[i].play_nh_sound()
                eff[i].set_image('nh', PNA_left, PNA_top, PNA_right, PNA_bottom)
        if PSA == 1:
            if (enemy_left[i] < PSA_right and enemy_right[i] > PSA_left and
                    enemy_top[i] > PSA_bottom and enemy_bottom[i] < PSA_top
                    and player.stop_attack != 1):
                E_event[i] = chage_ai_state(enemy[i], E_event[i], "THROWN")
                enemy[i].damage += 50
                E_speed[i] = 0.4 * player.direct * (enemy[i].damage / 20)
                E_speed_Y[i] = 20.0
                player.stop_attack = 1
                enemy[i].stand_time = 0
                eff[i].play_sh_sound()
                eff[i].set_image('sh', PSA_left, PSA_top, PSA_right, PSA_bottom)
        if ai_on:
            if enemy[i].state in ['jump', 'fall']:
                if enemy[i].y < Player_y and E_speed_Y[i] == 0:
                    E_event[i] = chage_ai_state(enemy[i], E_event[i], "D_JUMP")
                    E_speed_Y[i] = 20.0
            if enemy[i].state in ['jump', 'double jump', 'fall']:
                if enemy[i].x < Player_x:
                    enemy[i].walk = 1
                    enemy[i].direct = 1
                    enemy[i].moving = 1

                elif enemy[i].x > Player_x:
                    enemy[i].walk = -1
                    enemy[i].direct = -1
                    enemy[i].moving = 1

            if enemy[i].state in ['standing', 'walk', 'run']:
                if enemy[i].y < Player_y and Player_y - enemy[i].y > 20:
                    E_event[i] = chage_ai_state(enemy[i], E_event[i], "JUMP")
                    E_speed_Y[i] = 30.0
                elif (enemy[i].x < Player_x) and Player_x - enemy[i].x > 30:
                    if (enemy[i].state == 'run' and enemy[i].direct != 1) or (enemy[i].state in ['standing', 'walk']):
                        E_event[i] = chage_ai_state(enemy[i], E_event[i], "R_RIGHT")
                elif (enemy[i].x > Player_x) and enemy[i].x - Player_x > 30:
                    if (enemy[i].state == 'run' and enemy[i].direct != -1) or (enemy[i].state in ['standing', 'walk']):
                        E_event[i] = chage_ai_state(enemy[i], E_event[i], "R_LEFT")
                else:
                    import random
                    if random.random() < 0.5:
                        E_event[i] = chage_ai_state(enemy[i], E_event[i], "NA")
                    else:
                        E_event[i] = chage_ai_state(enemy[i], E_event[i], "SA")


        E_event[i], E_walk[i],  E_speed_Y[i], E_speed[i], E_shift[i], E_moving[i] = (
            ai_control(enemy[i], E_event[i], E_walk[i], E_speed_Y[i], E_speed[i], E_shift[i], E_moving[i]))

    for i in range(2):
            if ENA[i] == 1 and enemy[i].stop_attack == 0:
                if (player_left < ENA_right[i] and player_right > ENA_left[i] and
                        player_top > ENA_bottom[i] and player_bottom < ENA_top[i] and
                        player.state != 'block' and enemy[i].stop_attack != 1):
                    player.frame_step = 0
                    player.framex = 0
                    player.framey = 0
                    player.state = 'hit'
                    player.damage += 10
                    speed = 0.2 * enemy[i].direct * (player.damage / 20)
                    speed_Y = 8.0
                    enemy[i].stop_attack = 1
                    ENA[i] = 0
                    eff[2].play_nh_sound()
                    eff[2].set_image('nh', ENA_left[i], ENA_top[i], ENA_right[i], ENA_bottom[i])
                    break

            elif ESA[i] == 1 and enemy[i].stop_attack == 0:
                if (player_left < ESA_right[i] and player_right > ESA_left[i] and
                        player_top > ESA_bottom[i] and player_bottom < ESA_top[i] and
                        player.state != 'block' and enemy[i].stop_attack != 1):
                    player.frame_step = 0
                    player.framex = 0
                    player.framey = 0
                    player.state = 'thrown'
                    player.damage += 50
                    speed = 0.4 * enemy[i].direct * (player.damage / 20)
                    speed_Y = 20.0
                    enemy[i].stop_attack = 1
                    ESA[i] = 0
                    eff[2].play_sh_sound()
                    eff[2].set_image('sh', ESA_left[i], ESA_top[i], ESA_right[i], ESA_bottom[i])
                    break

    if (Player_x < -1000) or (Player_x > 1800) or (Player_y < -500):
        eff[2].play_dead_sound()
        eff[2].set_image('die',Player_x,Player_y,Player_x,Player_y)
        player.life = state_bar.minus_hp('P', player.life)
        player.damage = 0
        Player_x = 400
        Player_y = 125
        speed_Y = 0
        speed = 0
        pass
    for i in range(2):
        if (enemy[i].x < -1000) or (enemy[i].x > 1800) or (enemy[i].y < -500):
            eff[i].play_dead_sound()
            eff[i].set_image('die',enemy[i].x, enemy[i].y,enemy[i].x,enemy[i].y)
            enemy[i].life = state_bar.minus_hp(f'E{i}', enemy[i].life)
            enemy[i].damage = 0
            if i == 0:
                enemy[0].x = -100
                enemy[0].y = 350
            else:
                enemy[1].x = 900
                enemy[1].y = 350
            E_speed_Y[i] = 0
            E_speed[i] = 0
            pass
    if player.life <= 0:
        ai_on = 0
        stop_control = 1
        player.damage = -1
        ge.change_image(1)
        if player in world:
            world.remove(player)
    for i in range(2):
        if enemy[i].life <= 0:
            enemy[i].damage = -1
            enemy[i].x = 400
            enemy[i].y = 10000
    if  (enemy[0].life <= 0) and (enemy[1].life <= 0):
        ge.change_image(2)

    for o in world:
        if isinstance(o, Kamijo):  # Kamijo 클래스의 player 객체인 경우
            o.update(speed_Y, frame_time)  # player에 필요한 인자 전달
            PNA, PSA =player.shutdown_attack(PNA, PSA)
        elif isinstance(o, KFM):  # KFM 클래스의 enemy 객체인 경우
            if o == enemy[0]:
                o.update(E_speed_Y[0], frame_time)  # enemy[0]에 필요한 인자 전달
                ENA[0], ENA[0] = enemy[0].shutdown_attack( ENA[0], ENA[0])
            elif o == enemy[1]:
                o.update(E_speed_Y[1], frame_time)  # enemy[1]에 필요한 인자 전달
                ENA[1], ENA[1] = enemy[1].shutdown_attack(ENA[1], ENA[1])
        elif isinstance(o, EFFECT):
            o.update(frame_time)
        else:
            o.update()  # 다른 객체는 인자 없이 호출


def render_world():
    clear_canvas()

    for o in world:
        if isinstance(o, (Grass, Sky_Grass, KFM, EFFECT)):
            o.draw(Player_x, Player_y)
        elif isinstance(o, State_bar):
            o.draw(player.damage, enemy[0].damage, enemy[1].damage)
        else:
            o.draw()
    update_canvas()

frame_time = 0.0