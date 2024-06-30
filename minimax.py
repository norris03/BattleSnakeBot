from constants import *
from evaluate_game_state import evaluate_game_state

def minimax(node, depth, alpha, beta, our_turn):
    """
    Führt den Minimax-Algorithmus mit Alpha-Beta-Pruning durch, um den besten Zug zu berechnen

    Args:
        node (Node): Der gegebene Knoten im Spielbaum
        depth (float): Die Tiefe, bis zu dem der Baum durchsucht werden soll
        alpha (float): Die bisher beste Punktzahl
        beta (float): Die bisher schlechteste Punktzahl
        our_turn (bool): True, falls unsere Schlange am Zug ist, False sonst

    Returns:
        float: Die beste Punktzahl, die von dem gegebenen Knoten (Spielzustand) erreichbar ist
    """
    if depth == 0 or node.game_state == {}:
        eval = evaluate_game_state(node.game_state)
        node.score_game_state(eval)
        return eval
    if our_turn:
        max_eval = death_score
        for child in node.children:
            eval = minimax(child, depth - 0.5, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        node.score_game_state(max_eval)
        return max_eval
    else:
        min_eval = win_score
        for child in node.children:
            eval = minimax(child, depth - 0.5, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        node.score_game_state(min_eval)
        return min_eval
