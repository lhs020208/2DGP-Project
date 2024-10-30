from pico2d import *

from grass import Grass
from hitbox_cal import calculate_player_hitbox, calculate_enemy_hitbox
from kamijo import Kamijo
from kfm import KFM
from sky_grass import Sky_Grass

global Player_x
global Player_y
global player_left, player_right, player_top, player_bottom
global enemy_left, enemy_right, enemy_top, enemy_bottom

global PNA,PNA_left, PNA_right, PNA_top, PNA_bottom
global PSA,PSA_left, PSA_right, PSA_top, PSA_bottom
global ENA,ENA_left, ENA_right, ENA_toE, ENA_bottom
global ESA,ESA_left, ESA_right, ESA_toE, ESA_bottom

def reset_frame():
    global player

    player.frame_step = 0
    player.framex = 0
    player.framey = 0

def decide_state(state, walk, shift):
    state_result = state
    if state in ['standing', 'walk', 'run']:
        if walk != 0:
            state_result = 'walk'
            if shift == 1:
                state_result = 'run'
        else: state_result = 'standing'
    return state_result
def decide_direct(state,direct,walk):
    direct_result = direct
    if state in ['walk', 'run']:
        if walk > 0:
            direct_result = 1
        elif walk < 0:
            direct_result = -1
    return direct_result

def handle_events():
    global running, Player_x, Player_y
    global player
    global enemy
    global shift
    global walk

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        if event.type == SDL_KEYDOWN and event.key == SDLK_LEFT: #왼쪽키
            walk -= 1
            if player.state in ['standing', 'walk', 'run']:
                reset_frame()
                Player_x -= 10
                if walk == -1:
                    player.direct = -1
                elif walk == 0:
                    player.direct = 0
                if walk == 0:
                    player.direct = 1
        if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT: #오른쪽키
            walk += 1
            if player.state in ['standing', 'walk', 'run']:
                reset_frame()
                Player_x += 10
                if walk == 1:
                    player.direct = 1
                elif walk == 0:
                    player.direct = 0

        if event.type == SDL_KEYDOWN and event.key == SDLK_UP: #위키
            if player.state == 'standing' or player.state =='run' or player.state =='walk':
                reset_frame()
                player.state = 'jump'
                Player_y = Player_y + 10

        if event.type == SDL_KEYDOWN and event.key == SDLK_DOWN: #아래키
            reset_frame()
            Player_y = Player_y - 10
        if event.type == SDL_KEYDOWN and event.key == SDLK_z: #방어
            if player.state == 'standing' or player.state == 'run' or player.state == 'walk':
                player.state = 'block'
                reset_frame()
        if event.type == SDL_KEYDOWN and event.key == SDLK_LSHIFT:  #달리기
            shift = 1
            reset_frame()
        if event.type == SDL_KEYDOWN and event.key == SDLK_x:  #약 공격
            if (player.state == 'standing' or
                    player.state == 'run' or
                    player.state == 'walk' or
                    player.state == 'block'):
                player.state = 'normal_attack'
                reset_frame()
        if event.type == SDL_KEYDOWN and event.key == SDLK_c:  #강 공격
            if (player.state == 'standing' or
                    player.state == 'run' or
                    player.state == 'walk' or
                    player.state == 'block'):
                player.state = 'special_attack'
                reset_frame()
        if event.type == SDL_KEYDOWN and event.key == SDLK_a:  #공격받음 // 테스트용
            player.state = 'hit'
            reset_frame()
        if event.type == SDL_KEYDOWN and event.key == SDLK_s:  #날라감 // 테스트용
            player.state = 'thrown'
            reset_frame()

        #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        if event.type == SDL_KEYUP and event.key == SDLK_LEFT:  # 왼쪽키
            walk += 1
            if player.state in ['standing', 'walk', 'run']:
                reset_frame()
                if walk == 1:
                    player.direct = 1
                    Player_x += 10
                elif walk == 0:
                    player.direct = 0

        if event.type == SDL_KEYUP and event.key == SDLK_RIGHT:  # 오른쪽키
            walk -= 1
            if player.state in ['standing', 'walk', 'run']:
                reset_frame()
                if walk == -1:
                    player.direct = -1
                    Player_x -= 10
                elif walk == 0:
                    player.direct = 0
                if walk == 0:
                    player.direct = 1
        if event.type == SDL_KEYUP and event.key == SDLK_z:  #방어
            if player.state == 'block':
                reset_frame()
                player.state = 'standing'
        if event.type == SDL_KEYUP and event.key == SDLK_LSHIFT:  # 달리기
            shift = 0
            reset_frame()

        if event.type == SDL_KEYUP or event.type == SDL_KEYDOWN:
            player.state = decide_state(player.state, walk, shift)
            player.direct = decide_direct(player.state, player.direct ,walk)
            print(player.state)

def reset_world():
    global running
    global grass
    global sky_grass
    global player
    global enemy
    global world

    global Player_x
    global Player_y
    global PNA, PSA, ENA, ESA
    Player_x = 400
    Player_y = 120
    PNA, PSA, ENA, ESA = 0,0,0,0

    global shift
    global walk
    shift = 0
    walk = 0

    running = True
    world = []

    grass = Grass()
    world.append(grass)

    sky_grass = [Sky_Grass(i) for i in range(3)]
    world += sky_grass

    player = Kamijo()
    world.append(player)

    enemy = [KFM() for i in range(2)]
    enemy[1].x -= 100
    world += enemy

def update_world():
    for o in world:
        o.update()

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

def render_world():
    clear_canvas()

    for o in world:
        if isinstance(o, (Grass, Sky_Grass, KFM)):
            o.draw(Player_x, Player_y)
        else:
            o.draw()

    global PNA, PNA_left, PNA_right, PNA_top, PNA_bottom
    if PNA == 1:
        heatbox_point = [load_image('heatbox_point.png') for _ in range(4)]
        heatbox_point[0].draw(PNA_left, PNA_bottom)
        heatbox_point[1].draw(PNA_left, PNA_top)
        heatbox_point[2].draw(PNA_right, PNA_bottom)
        heatbox_point[3].draw(PNA_right, PNA_top)

    update_canvas()

open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()
