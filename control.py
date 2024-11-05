from pico2d import *

def control(enemy, event, player, walk, Player_y, shift):
    if event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:  # 왼쪽키
        walk -= 1
        if player.state in ['standing', 'walk', 'run']:
            player.frame_step = 0
            player.framex = 0
            player.framey = 0
            if walk == -1:
                player.direct = -1
            elif walk == 0:
                player.direct = 0

    if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:  # 오른쪽키
        walk += 1
        if player.state in ['standing', 'walk', 'run']:
            player.frame_step = 0
            player.framex = 0
            player.framey = 0
            if walk == 1:
                player.direct = 1
            elif walk == 0:
                player.direct = 0

    if event.type == SDL_KEYDOWN and event.key == SDLK_UP:  # 위키
        if player.state in ['standing', 'run', 'walk']:
            player.frame_step = 0
            player.framex = 0
            player.framey = 0
            player.state = 'jump'
            Player_y += 10

    if event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:  # 아래키
        player.frame_step = 0
        player.framex = 0
        player.framey = 0
        Player_y -= 10

    if event.type == SDL_KEYDOWN and event.key == SDLK_z:  # 방어
        if player.state in ['standing', 'run', 'walk']:
            player.state = 'block'
            player.frame_step = 0
            player.framex = 0
            player.framey = 0

    if event.type == SDL_KEYDOWN and event.key == SDLK_LSHIFT:  # 달리기
        shift = 1
        player.frame_step = 0
        player.framex = 0
        player.framey = 0

    if event.type == SDL_KEYDOWN and event.key == SDLK_x:  # 약 공격
        if player.state in ['standing', 'run', 'walk', 'block', 'normal_attack']:
            player.state = 'normal_attack'
            player.frame_step = 0
            player.framex = 0
            player.framey = 0

    if event.type == SDL_KEYDOWN and event.key == SDLK_c:  # 강 공격
        if player.state in ['standing', 'run', 'walk', 'block', 'normal_attack']:
            player.state = 'special_attack'
            player.frame_step = 0
            player.framex = 0
            player.framey = 0

    if event.type == SDL_KEYDOWN and event.key == SDLK_a:  # 공격받음 // 테스트용
        player.state = 'hit'
        for i in range(2):
            enemy[i].state = 'special_attack'
            enemy[i].frame_step = 0
        player.frame_step = 0
        player.framex = 0
        player.framey = 0

    if event.type == SDL_KEYDOWN and event.key == SDLK_s:  # 날라감 // 테스트용
        player.state = 'thrown'
        player.frame_step = 0
        player.framex = 0
        player.framey = 0

    # 키를 뗐을 때 (KEYUP 이벤트)
    if event.type == SDL_KEYUP and event.key == SDLK_LEFT:  # 왼쪽키
        walk += 1
        if player.state in ['standing', 'walk', 'run']:
            player.frame_step = 0
            player.framex = 0
            player.framey = 0
            if walk == 1:
                player.direct = 1
            elif walk == 0:
                player.direct = 0

    if event.type == SDL_KEYUP and event.key == SDLK_RIGHT:  # 오른쪽키
        walk -= 1
        if player.state in ['standing', 'walk', 'run']:
            player.frame_step = 0
            player.framex = 0
            player.framey = 0
            if walk == -1:
                player.direct = -1
            elif walk == 0:
                player.direct = 0

    if event.type == SDL_KEYUP and event.key == SDLK_z:  # 방어
        if player.state == 'block':
            player.frame_step = 0
            player.framex = 0
            player.framey = 0
            player.state = 'standing'

    if event.type == SDL_KEYUP and event.key == SDLK_LSHIFT:  # 달리기
        shift = 0
        player.frame_step = 0
        player.framex = 0
        player.framey = 0

    return walk, Player_y, shift
