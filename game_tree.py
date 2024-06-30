from constants import *
from update_game_state import update_game_state
import itertools
import copy

def is_bad_move(game_state, move, snake_body):
    """
    Bestimmt, ob ein Zug für die Schlange, die mit dem gegebenen Schlangen-Körper korrespondiert, schlecht ist

    Args:
        game_state (dict): Der gegebene Spielzustand
        move (str): Der zu überprüfende Zug
        snake_body (list of dict): Die Liste der Körpersegmente der Schlange

    Returns:
        bool: True, wenn der Zug schlecht ist, False sonst
    """
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
    """
    Ein Knoten im Spielbaum, der einen bestimmten Spielzustand, den Zug, der zu diesem Spielzustand geführt hat und die Bewertung (Punktzahl) des Spielzustand repräsentiert

    Attribute:
        move (str): Der Zug, der zu diesem Spielzustand geführt hat
        game_state (dict): Der aktualisierte Spielzustand
        score (float): Die Bewertung (Punktzahl) des Spielzustands
        children (list of Node): Kindknoten (folgende Spielzustände)
    """
    move = ""
    game_state = {}
    score = death_score
    children = []

    def __init__(self, game_state, move, is_our_turn):
        """
        Initialisierung des Knoten

        Args:
            game_state (dict): Der gegebene Spielzustand
            move (str): Der Zug (die Züge), der ausgeführt (die aussgeführt) werden soll(en)
            is_our_turn (bool): True, wenn unsere Schlange am Zug ist, False sonst
        """
        self.move = move
        self.game_state = update_game_state(game_state, move, is_our_turn)
        self.score = death_score
        self.children = []

    def add_child(self,node):
        """
        Fügt dem aktuellen Knoten einen Kindknoten hinzu

        Args:
            node (Node): Der hinzuzufügende Kindknoten
        """
        self.children.append(node)

    def score_game_state(self, calculated_score):
        """
        Weist dem Knoten die gegebene Punktkzahl zu

        Args:
            calculated_score (float): Die Punktzahl die dem Knoten zugewiesen werden soll
        """
        self.score = calculated_score

    def create_tree(self, depth, is_our_turn):
        """
        Erstellt einen Spielbaum

        Args:
            depth (float): Die Tiefe des zu erstellenden Baums
            is_our_turn (bool): True, wenn unsere Schlange am Zug ist, False sonst
        """
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
