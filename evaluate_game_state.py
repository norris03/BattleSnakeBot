from constants import *
from floodfill import create_grid, flood_fill
from math import floor as floor
from astar import a_star
import numpy as np
def evaluate_game_state(game_state):
    if game_state == {}:
        return death_score
    else: 
        x = game_state["you"]["body"][0]["x"]
        y = game_state["you"]["body"][0]["y"]
        length = game_state["you"]["length"]
        grid = create_grid(game_state)
        grid = np.ndarray.tolist(grid)
        width = game_state["board"]["width"]
        height = width + game_state["board"]["height"]
        
        max_distance_to_food = height + width
        min_distance_to_food = max_distance_to_food
        distance_to_food = max_distance_to_food
        head = (x, y)
        for apple in game_state["board"]["food"]:
            distance_to_food = a_star(grid=grid, start = head, goal = (apple["x"], apple["y"]))
            if distance_to_food < min_distance_to_food:
                min_distance_to_food = distance_to_food
        distance_to_food_score = min_distance_to_food/max_distance_to_food
        
        distance_from_center = floor(abs(x-width/2))+floor(abs(y-height/2))
        distance_from_center_score = distance_from_center/(width+height)
        
        flood_fill_score = flood_fill(game_state)/(width*height)

        return -distance_to_food_score+length+20*flood_fill_score