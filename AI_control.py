from pico2d import *

def chage_ai_state(enemy, event, after_event):
    enemy.frame_step = 0
    enemy.framex = 0
    enemy.framey = 0
    event = after_event
    return event

def ai_control(enemy, event, walk, speed_Y, shift, moving):
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

    if event == "LEFT":
        shift = 0
        walk -= 1
        enemy.direct = -1
        moving = 1

    if event == "RIGHT":
        shift = 0
        walk += 1
        enemy.direct = 1
        moving = 1

    if event == "R_LEFT":
        shift = 1
        walk -= 1
        enemy.direct = -1
        moving = 1

    if event == "R_RIGHT":
        shift = 1
        walk += 1
        enemy.direct = 1
        moving = 1

    if event == "JUMP":  # 위키
        enemy.state = 'jump'
        speed_Y += 30

    if event == "NA":  # 약 공격
        enemy.state = 'normal_attack'

    if event == "SA":  # 약 공격
        enemy.state = 'special_attack'

    if event == "HIT": #약공 받음
        enemy.state = 'hit'

    if event == "THROWN": #강공 받음
        enemy.state = 'thrown'

    return walk, speed_Y, shift, moving