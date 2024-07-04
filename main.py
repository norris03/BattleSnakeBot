# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "snek14",  # TODO: Your Battlesnake Username
        "color": "#FFFF00",  # TODO: Choose color
        "head": "fang",  # TODO: Choose head
        "tail": "block-bum",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
from update_game_state import clean_game_state
from game_tree import Node
from minimax import minimax
from constants import *
import time
decision_time = 0
decision_time_debuff = 0

def move(game_state: typing.Dict) -> typing.Dict:
    global decision_time, decision_time_debuff
    start_time = time.time()
    next_move = "down"
    board = clean_game_state(game_state)
    tree_depth = 0.5
    number_of_enemies = len(game_state["board"]["snakes"])
    if number_of_enemies == 0 or game_state["turn"] <= 2:
        tree_depth = 0.5
    elif number_of_enemies == 1:
        tree_depth = 3 - decision_time_debuff
    elif number_of_enemies == 2:
        tree_depth = 2 - decision_time_debuff
    else:
        tree_depth = 1
    
    if decision_time >= 500:
        decision_time_debuff += 0.5
    elif decision_time_debuff >= 0.5:
        decision_time_debuff -= 0.5

    print(game_state["turn"])
    print(decision_time_debuff)

    n = Node(board, "", True)
    n.create_tree(tree_depth, True)
    best_score = minimax(n, tree_depth, death_score, win_score, True)
    for child in n.children:
        if child.score == best_score:
            next_move = child.move
            break
    if best_score == death_score:
        best_score = minimax(n, 1, death_score, win_score, True)
        for child in n.children:
            if child.score == best_score:
                next_move = child.move
                break
    
    end_time = time.time()
    decision_time = (end_time-start_time)*10**3
    return {"move": next_move}

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
