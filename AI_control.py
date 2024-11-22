from pico2d import *

def chage_ai_state(enemy, event, after_event):
    enemy.frame_step = 0
    enemy.framex = 0
    enemy.framey = 0
    event = after_event
    return event

def ai_control(enemy, event, walk, speed_Y, speed, shift, moving):
    #event는 문자열 저장
    #좌측이동 LEFT
    #좌측런 R_LEFT
    #우측이동 RIGHT
    #우측런 R_RIGHT
    #점프 JUMP
    #더블점프 D_JUMP
    #약공 NA
    #강공 SA
    #약공받음 HIT
    #강공받음 THROWN


    if enemy.plz_standing == 1:
        enemy.state = 'standing'
        enemy.plz_standing = 0
        event = 'standing'

    elif event == "LEFT":
        enemy.state = 'walk'
        shift = 0
        walk -= 1
        enemy.direct = -1
        moving = 1

    elif event == "RIGHT":
        enemy.state = 'walk'
        shift = 0
        walk += 1
        enemy.direct = 1
        moving = 1

    elif event == "R_LEFT":
        enemy.state = 'run'
        shift = 1
        walk = -1
        enemy.direct = -1
        moving = 1

    elif event == "R_RIGHT":
        enemy.state = 'run'
        shift = 1
        walk = 1
        enemy.direct = 1
        moving = 1

    elif event == "JUMP":  # 위키
        enemy.state = 'jump'

    elif event == "D_JUMP":  # 위키
        enemy.state = 'double jump'

    elif event == "NA":  # 약 공격
        enemy.stop_attack = 0
        enemy.state = 'normal_attack'

    elif event == "SA":  # 강 공격
        enemy.stop_attack = 0
        enemy.state = 'special_attack'

    elif event == "HIT": #약공 받음
        enemy.state = 'hit'

    elif event == "THROWN": #강공 받음
        enemy.state = 'thrown'

    else:
        enemy.state = 'standing'
        enemy.plz_standing = 0
        event = 'standing'

    return event, walk, speed_Y, speed, shift, moving