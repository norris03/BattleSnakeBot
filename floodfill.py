"""
Baidinger, Artur 220201391
Haufe, Hans-Hauke 222200976
Hellerich, Hannes 222201181
Löbnau, Norris 222200294
Rieck, Damijan Ali 218200608
Strompen, Zoe Katharina 221200152
"""
import numpy as np
from collections import deque
from constants import *
def create_grid(game_state):
    """
    Erstellt ein Gitter basierend auf dem gegebenen Spielzustand

    Args:
        game_state (dict): Der gegebene Spielzustand

    Returns:
        numpy.ndarray: Ein 2D-Array, das das Spielfeld repräsentiert, wobei Felder mit Wert 0 begehbare Felder sind
    """
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
    """
    Füllt das Spielfeld vom gegebenen Startfeld aus und berechnet die Anzahl der erreichbaren Felder

    Args:
        game_state (dict): Der gegebene Spielzustand
        x (int): Die x-Koordinate des Startfelds
        y (int): Die y-Koordinate des Startfelds

    Returns:
        int: Die Anzahl der vom Startfeld aus erreichbaren Felder
    """
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
    """
    Führt den Flood-Fill-Algorithmus aus, um die Anzahl der von unserer Schlange aus erreichbaren Felder zu berechnen

    Args:
        game_state (dict): Der gegebene Spielzustand

    Returns:
        int: Die Anzahl der von unserer Schlange aus erreichbaren Felder
    """
    return fill(game_state, game_state["you"]["body"][0]["x"], game_state["you"]["body"][0]["y"])
