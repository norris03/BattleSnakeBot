"""
Baidinger, Artur 220201391
Haufe, Hans-Hauke 222200976
Hellerich, Hannes 222201181
Löbnau, Norris 222200294
Rieck, Damijan Ali 218200608
Strompen, Zoe Katharina 221200152
"""
import heapq

def heuristic(a, b):
    """
    Berechnet die Manhattan-Metrik zwischen zwei Punkten

    Args:
        a (tuple): Der erste Punkt als (x, y)-Tupel
        b (tuple): Der zweite Punkt als (x, y)-Tupel

    Returns:
        int: Die Manhattan-Metrik zwischen den Punkten a und b
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, goal):
    """
    Führt den A*-Suchalgorithmus aus, um den kürzesten Weg von einem Startfeld zu einem Zielfeld zu finden

    Args:
        grid (list of list of int): Das Spielfeld als 2D-Liste, wobei Felder mit Wert 0 begehbare Felder sind
        start (tuple): Das Startfeld als (x, y)-Tupel
        goal (tuple): Das Zielfeld als (x, y)-Tupel

    Returns:
        int: Die Länge des kürzesten Weges vom Startfeld zum Zielfeld (unendlich falls kein Weg existiert)
    """
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            return g_score[current]
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] == 0:
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return float('inf') 
