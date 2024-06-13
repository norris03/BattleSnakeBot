death_score = -2**20
win_score = 2**20
max_flood_fill_score = 121
food_in_reach_distance = 10

""" Weights """
w_flood_fill = 0 #[0,1]
w_distance_from_center = 0 #[0,1]
w_edge_penalty = 0 #{-1, 0}
w_distance_to_food = -1 # [0,1] 
w_health_bonus = 0 #{x >= 99:1, x < 99: 0}
w_length = 0 #[0,1]
w_number_of_enemies = -1 #{0,1,2,3,4,5,6,7}
