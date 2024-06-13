from constants import *
from floodfill import create_grid, flood_fill
from math import floor as floor
from math import ceil as ceil
from astar import a_star, heuristic
def evaluate_game_state(game_state):
    if game_state == {}:
        return death_score
    else: 
        game_state_score = death_score
        x = game_state["you"]["body"][0]["x"]
        y = game_state["you"]["body"][0]["y"]
        length = game_state["you"]["length"]
        grid = create_grid(game_state)
        width = game_state["board"]["width"]
        height = game_state["board"]["height"]
        board_area = width*height
        board_length = width+height
        
        max_distance_to_food = board_length - 1
        min_distance_to_food = max_distance_to_food
        distance_to_food = max_distance_to_food
        head = (x, y)
        for apple in game_state["board"]["food"]:
            goal = (apple["x"], apple["y"])
            if heuristic(head, goal) > food_in_reach_distance:
                continue
            distance_to_food = a_star(grid=grid, start = head, goal = goal)
            if distance_to_food < min_distance_to_food:
                min_distance_to_food = distance_to_food
        distance_to_food_score = min_distance_to_food/max_distance_to_food
        
        distance_from_center = floor(abs(x-width/2))+floor(abs(y-height/2))
        distance_from_center_score = distance_from_center/(board_length/2)

        flood_fill_score = flood_fill(game_state)/(board_area)

        edge_penalty = 0
        if x == 0 or y == 0 or x == width - 1 or y == height - 1:
            edge_penalty = -1

        health_score = game_state["you"]["health"]/100
        health_bonus = 0
        if health_score >= 0.99:
            health_bonus = 1

        length_score = length/board_area

        number_of_enemies = len(game_state["board"]["snakes"])

        if flood_fill_score > length_score:
            game_state_score = (
                w_distance_to_food*distance_to_food_score
                +w_health_bonus*health_bonus                
                +w_distance_from_center*distance_from_center_score             
                +w_edge_penalty*edge_penalty+w_flood_fill*flood_fill_score                
                +w_length*length_score+w_number_of_enemies*number_of_enemies
            )
        else:
            game_state_score = flood_fill_score
        
        return game_state_score
    
