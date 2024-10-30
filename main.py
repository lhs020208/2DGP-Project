from pico2d import *

from grass import Grass
from kamijo import Kamijo
from kfm import KFM
from sky_grass import Sky_Grass

global Player_x
global Player_y
Player_x = 400
Player_y = 120


def reset_frame():
    global player

    player.frame_step = 0
    player.framex = 0
    player.framey = 0

def handle_events():
    global running, Player_x, Player_y
    global player
    global enemy
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        if event.type == SDL_KEYDOWN and event.key == SDLK_LEFT: #왼쪽키
            if player.state == 'standing':
                reset_frame()
                Player_x = Player_x - 10
                player.state = 'walk'
                player.direct = -1
        if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT: #오른쪽키
            if player.state == 'standing':
                reset_frame()
                Player_x = Player_x + 10
                player.state = 'walk'
                player.direct = 1
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
            if player.state == 'walk':
                player.state = 'run'
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
            player.state = 'heat'
            reset_frame()
        if event.type == SDL_KEYDOWN and event.key == SDLK_s:  #날라감 // 테스트용
            player.state = 'thrown'
            reset_frame()

        #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        if event.type == SDL_KEYUP and event.key == SDLK_LEFT:  # 왼쪽키
            if player.state == 'walk' or player.state == 'run':
                reset_frame()
                player.state = 'standing'
        if event.type == SDL_KEYUP and event.key == SDLK_RIGHT:  # 오른쪽키
            if player.state == 'walk' or player.state == 'run':
                reset_frame()
                player.state = 'standing'
        if event.type == SDL_KEYUP and event.key == SDLK_z:  #방어
            if player.state == 'block':
                reset_frame()
                player.state = 'standing'
        if event.type == SDL_KEYUP and event.key == SDLK_LSHIFT:  # 달리기
            if player.state == 'run':
                reset_frame()
                player.state = 'walk'

def reset_world():
    global running
    global grass
    global sky_grass
    global player
    global enemy
    global world

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

def render_world():
    clear_canvas()
    for o in world:
        if isinstance(o, (Grass, Sky_Grass, KFM)):
            o.draw(Player_x, Player_y)
        else:
            o.draw()

    #히트박스 좌표 확인
    global player
    kamijo_heatbox = load_image('kamijo_heatbox.png')
    kamijo_heatbox.draw(player.x, player.y - 15)

    global enemy
    kfm_heatbox = [load_image('kfm_heatbox.png') for _ in range(2)]
    for i in range (2):
        offset_x = Player_x - 400
        offset_y = Player_y - 120
        kfm_heatbox[i].draw(enemy[i].x - offset_x, enemy[i].y - 15 - offset_y)

    heatbox_point = [load_image('heatbox_point.png') for _ in range(12)]

    kamijo_box = 140
    kamijo_w = 48
    kamijo_h = 111
    player_left = player.x - kamijo_w/2
    player_right = player.x + kamijo_w / 2
    player_top = player.y - kamijo_box/2 + kamijo_h
    player_bottom = player.y - kamijo_box/2

    kfm_box = 140
    kfm_w = 47
    kfm_h = 106
    enemy_left = [0, 0]
    enemy_right = [0, 0]
    enemy_top = [0, 0]
    enemy_bottom = [0, 0]
    offset_x = Player_x - 400
    offset_y = Player_y - 120
    for i in range(2):
        enemy_x = enemy[i].x - offset_x
        enemy_y = enemy[i].y - offset_y
        enemy_left[i] = enemy_x - kfm_w / 2
        enemy_right[i] = enemy_x + kfm_w / 2
        enemy_top[i] = enemy_y - kfm_box / 2 + kfm_h
        enemy_bottom[i] = enemy_y - kfm_box / 2

    for i in range(2):
        heatbox_point[i].draw(enemy_left[i], enemy_bottom[i])
        heatbox_point[i].draw(enemy_left[i], enemy_top[i])
        heatbox_point[i].draw(enemy_right[i], enemy_bottom[i])
        heatbox_point[i].draw(enemy_right[i], enemy_top[i])

    heatbox_point[8].draw(player_left,player_bottom)
    heatbox_point[9].draw(player_left, player_top)
    heatbox_point[10].draw(player_right, player_bottom)
    heatbox_point[11].draw(player_right, player_top)

    update_canvas()

open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()
