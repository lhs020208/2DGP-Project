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
