from constants import *
from update_game_state import update_game_state
import itertools
import copy

def is_bad_move(game_state, move, snake_body):
    max_x = game_state["board"]["width"] - 1
    max_y = game_state["board"]["height"] - 1
    x = snake_body[0]["x"]
    y = snake_body[0]["y"]
    if move == "up":
        y += 1
    elif move == "right":
        x += 1
    elif move == "down":
        y -= 1
    else:
        x -= 1
    if x < 0 or x > max_x or y < 0 or y > max_y:
        return True
    elif {"x": x, "y": y} in snake_body[1:-1]:
        return True
    else:
        all_snakes = game_state["board"]["snakes"].copy()
        all_snakes.insert(0, game_state["you"])
        if snake_body == game_state["you"]["body"]:
            for snake in all_snakes:
                if snake["body"] == snake_body:
                    continue
                elif {"x": x, "y": y} in snake["body"][:-1]:
                    return True
        else:
            for snake in all_snakes:
                if snake["body"] == snake_body:
                    continue
                elif {"x": x, "y": y} in snake["body"][1:]:
                    return True
    return False

class Node:
    move = ""
    game_state = {}
    score = death_score
    children = []

    def __init__(self, game_state, move, is_our_turn):
        self.move = move
        self.game_state = update_game_state(game_state, move, is_our_turn)
        self.score = death_score
        self.children = []

    def add_child(self,node):
        self.children.append(node)

    def score_game_state(self, calculated_score):
        self.score = calculated_score

    def create_tree(self, depth, is_our_turn):
        if depth == 0 or self.game_state == {}:
            return
        legal_moves = ["up","right","down","left"]
        if is_our_turn == True:
            good_moves = [move for move in legal_moves if not is_bad_move(self.game_state, move, self.game_state["you"]["body"])]
            if good_moves == []:
                self.game_state = {}
            for move in good_moves:
                child_node = Node(copy.deepcopy(self.game_state), move, True)   
                self.add_child(child_node)   
                child_node.create_tree(depth - 0.5, False)            
        else:
            enemies_good_moves = []
            for enemy in self.game_state["board"]["snakes"]:
                good_moves = [move for move in legal_moves if not is_bad_move(self.game_state, move, enemy["body"])]
                if good_moves == []:
                    good_moves = ["X"]
                enemies_good_moves.append(good_moves)
            enemies_moves = list(itertools.product(*enemies_good_moves))
            for moves in enemies_moves:
                child_node = Node(copy.deepcopy(self.game_state), moves, False) 
                self.add_child(child_node)
                child_node.create_tree(depth - 0.5, True)
                
def preorder_traversal(node):
    if node is None:
        return
    print("\n")
    print(node.game_state)
    pretty_print(node.game_state)    
    for child in node.children:
        preorder_traversal(child)

#board = clean_game_state(state2)
#n = Node(state,"",True)
#n.create_tree(0.5,True)



#n = Node(board,"",True)
#n.create_tree(0.5,True)
#best_score = minimax(n, 0.5, death_score, -death_score, True)
#print(best_score)
#pretty_print(n.game_state)
#for child in n.children:
#    print(child.score)
#    if child.score == best_score:
#        print(child.move)
#        next_move = child.move
#        break
##preorder_traversal(n)
#def testf(node):
#    node.score_game_state(3)
#testf(n)
#print(n.score)

is_testing = 0
if is_testing:
    from test import *
    from utils import * 
    from minimax import minimax
    #board = clean_game_state(state4)
    board = state8
    n = Node(board,"",True)
    n.create_tree(1,True)
    best_score = minimax(n, 1, death_score, win_score, True)
    print("Best Score", best_score)
    preorder_traversal(n)