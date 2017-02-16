STATE_SEL_EX = 0
STATE_COUNTDOWN = 1
STATE_DOING = 2
STATE_DONE = 3
STATE_ADJ = 4

cur_state = 0

def set_state(newstate):
    cur_state = newstate

def get_state():
    return cur_state