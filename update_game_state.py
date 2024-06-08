#from test import *

def clean_game_state(game_state):
    del game_state["game"]
    game_state["board"]["snakes"] = [snake for snake in game_state["board"]["snakes"] if snake["id"] != game_state["you"]["id"]]
    for snake in game_state["board"]["snakes"]:
        del snake["head"]
        del snake["shout"]
        del snake["squad"]
        del snake["customizations"]
    del game_state["you"]["head"]
    del game_state["you"]["shout"]
    del game_state["you"]["squad"]
    del game_state["you"]["customizations"]
    return game_state   


def update_game_state(game_state, move, is_our_turn):
    if move == "":
        return game_state
    if game_state == {}:
        return {}
    if is_our_turn == True:
        game_state["turn"] += 0.5
        head = game_state["you"]["body"][0]
        if move == "up":
            game_state["you"]["body"].insert(0,{"x":head["x"],"y":head["y"]+1})
        elif move == "down":
            game_state["you"]["body"].insert(0,{"x":head["x"],"y":head["y"]-1})
        elif move == "right":
            game_state["you"]["body"].insert(0,{"x":head["x"]+1,"y":head["y"]})
        else:
            game_state["you"]["body"].insert(0,{"x":head["x"]-1,"y":head["y"]})
        head = game_state["you"]["body"][0]
        if head in game_state["board"]["food"]:
            game_state["you"]["heath"] = 100
            game_state["you"]["length"] += 1 
        else:
            game_state["you"]["health"] -= 1
            if game_state["you"]["health"] == 0:
                return {}
            game_state["you"]["body"].pop()
        return game_state
    
    else:
        game_state["turn"] += 0.5
        dead_snakes_id = set()
        eaten_apples = []
        
        for i in range(0, len(move)):
            enemy = game_state["board"]["snakes"][i]
            head = enemy["body"][0]
            if move[i] == "up":
                enemy["body"].insert(0,{"x":head["x"],"y":head["y"]+1})
            elif move[i] == "down":
                enemy["body"].insert(0,{"x":head["x"],"y":head["y"]-1})
            elif move[i] == "right":
                enemy["body"].insert(0,{"x":head["x"]+1,"y":head["y"]})
            elif move[i] == "left":
                enemy["body"].insert(0,{"x":head["x"]-1,"y":head["y"]})
            else:
                dead_snakes_id.add(enemy["id"])
            head = enemy["body"][0]
            if head in game_state["board"]["food"]:
                enemy["health"] = 100
                enemy["length"] += 1
            else:
                enemy["health"] -= 1
                if enemy["health"] == 0:
                    dead_snakes_id.add(enemy["id"])
                enemy["body"].pop()
        
        all_snakes = game_state["board"]["snakes"].copy()
        all_snakes.insert(0, game_state["you"])

        for snake in all_snakes:
            if snake["body"][0] in game_state["board"]["food"]:
                eaten_apples.append(snake["body"][0])

        game_state["board"]["food"] = [apple for apple in game_state["board"]["food"] if apple not in eaten_apples]

        for i in range(0, len(all_snakes)):
            head = all_snakes[i]["body"][0]
            for j in range(i+1, len(all_snakes)):
                if head == all_snakes[j]["body"][0]:
                    if all_snakes[i]["length"] < all_snakes[j]["length"]:
                        if i == 0:
                            return {}
                        dead_snakes_id.add(all_snakes[i]["id"])
                    elif all_snakes[i]["length"] == all_snakes[j]["length"]:
                        if i == 0:
                            return {}
                        dead_snakes_id.add(all_snakes[i]["id"])
                        dead_snakes_id.add(all_snakes[j]["id"])
                    else:
                        dead_snakes_id.add(all_snakes[j]["id"])

        game_state["board"]["snakes"] = [snake for snake in game_state["board"]["snakes"] if snake["id"] not in dead_snakes_id]            
        return game_state