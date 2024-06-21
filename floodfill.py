import numpy as np
from collections import deque
from constants import *
def create_grid(game_state):
    if game_state == {}:
        return 
    grid = np.rot90(np.zeros((game_state["board"]["height"],game_state["board"]["width"])))
    for c in game_state["you"]["body"][1:-1]:
        grid[c["x"]][c["y"]] = 1
    for snake in game_state["board"]["snakes"]:
        for c in snake["body"]:
            grid[c["x"]][c["y"]] = 2
    return grid

def fill(game_state, x, y):
    score = 0
    max_x=game_state["board"]["width"]-1
    max_y=game_state["board"]["height"]-1
    max_space = max_x*max_y-len(game_state["you"]["body"])
    for snake in game_state["board"]["snakes"]:
        max_space = max_space - len(snake["body"])
    grid = create_grid(game_state)  
    if grid is None:
        return -1
    l = deque()
    while len(l) != 0:
        (x, y) = l.pop()
        if 0 <= x <= max_x and 0 <= y <= max_y:
            if grid[x][y] == 0:
                grid[x][y] = 4
                score += 1
                l.append(0, (x, y + 1))
                l.append(0, (x, y - 1))
                l.append(0, (x + 1, y))
                l.append(0, (x - 1, y))
        if score > min(max_flood_fill_score,max_space):
            break
    return score

def flood_fill(game_state):
    return fill(game_state, game_state["you"]["body"][0]["x"], game_state["you"]["body"][0]["y"])
