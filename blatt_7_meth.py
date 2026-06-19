'''
This module contains utility functions for the Cat Problem. A graph
featuring costs (effort) and distraction
values (dist) is used to evaluate and compare paths between nodes.
_______test cases are to run in this file______
'''
import random
import math
import turtle
import doctest

__author__ = "8408293, Alizadeh, 8236539, Yakout"
__credit__ = "Written with assistance from ChatGPT and Gemini."


map_pos = {"A": (-200, -100), "B": (-100, -100), "C": (-200, 100),
           "D": (-100, 100), "E": (0, -100), "H": (0, 100)}
map_letters = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["D"],
    "D": ["H"],
    "E": ["H"],
}
graph = {
    "A": {"B": {"effort": 3, "dist": 2}, "C": {"effort": 1, "dist": 0}},
    "B": {"A": {"effort": 3, "dist": 2}, "D": {"effort": 4, "dist": 5},
          "E": {"effort": 2, "dist": 1}},
    "C": {"A": {"effort": 1, "dist": 0}, "D": {"effort": 2, "dist": 3}},
    "D": {"C": {"effort": 2, "dist": 3}, "B": {"effort": 4, "dist": 5},
          "H": {"effort": 3, "dist": 4}},
    "E": {"B": {"effort": 2, "dist": 1}, "H": {"effort": 5, "dist": 0}},
    "H": {"D": {"effort": 3, "dist": 4}, "E": {"effort": 5, "dist": 0}}}


def cat_next_moves(current_pos, graph):
    '''a function that helps turning next possible positions to the cat
    into a tuple with needed functions for later usage in main()

    >>> cat_next_moves("A", graph)
    {'B': (3, 2), 'C': (1, 0)}
    >>> cat_next_moves("C", graph)
    {'A': (1, 0), 'D': (2, 3)}
    >>> cat_next_moves("X", graph)
    Traceback (most recent call last):
    ...
    KeyError: 'X'
    '''
    moves = {}
    for j in graph[current_pos]:
        moves[j] = (graph[current_pos][j]["effort"], graph[current_pos][j]["dist"])
    return moves

# --- Optimization Strategies ---
# These strictly handle (name, (effort, dist)) format for consistency


def opt_greedy(w1, w2):
    """Compares two ways: Higher distraction is priotrised first, 
    then lower effort.
    >>> opt_greedy(("A", (1,2)), ("B", (6,5)), ("C",(0,5)))
    ('C', (0, 5))
    >>> opt_greedy(("A", (1,2)), ("B", (6,5)))
    ('B', (6, 5))
    >>> opt_greedy(("A", (1,2)), ("B", (4,2)))
    ('A', (1, 2))
    """
    name1, (e1, d1) = w1
    name2, (e2, d2) = w2
    if d1 > d2:
        return w1
    if d2 > d1:
        return w2
    # Tie-breaker: Lower effort
    return w1 if e1 < e2 else (w2 if e2 < e1 else random.choice([w1, w2]))


def apply_opt(opt_fn, ways):
    """Applies an optimization function to a list of any length.
    # with greedy
    >>> apply_opt(opt_greedy,[("A", (1,2)), ("B", (6,5))])
    ('A', (1, 2))
    >>> apply_opt(opt_min_effort,[("A", (1,2)), ("B", (2,4))])
    ('A', (1, 2))
    >>> apply_opt(opt_diff,[("A", (1,2)), ("B", (2,4))])
    ('B', (2, 4))
    """
    if not ways:
        return None
    best = ways[0]
    for i in range(1, len(ways)):
        best = opt_fn(best, ways[i])
    return best


def opt_min_effort(w1, w2):
    """Rule: Minimum effort.
    prioritise minimum effort, then higher distraction.

    >>> opt_min_effort(("A", (1,2)), ("B", (2,100)))
    ('A', (1, 2))
    >>> opt_min_effort(("A", (3,2)), ("B", (3,5)))
    ('B', (3, 5))
    >>> opt_min_effort(("A", (1,2,3)), ("B", (2,4)))
    error
    """
    n1, (e1, d1) = w1
    n2, (e2, d2) = w2
    if e1 < e2:
        return w1
    if e2 < e1:
        return w2
    return w1 if d1 > d2 else w2


def opt_diff(w1, w2):
    """Rule: Maximize distraction through (Distraction - Effort).

    >>> opt_diff(("A", (1,10)), ("B", (2,4)))
    ('A', (1, 10))
    >>> opt_diff(("A", (5,6)), ("B", (1,10)))
    ('B', (1, 10))
    >>> opt_diff(None, ("B", (2,4)))
    None
    """
    n1, (e1, d1) = w1
    n2, (e2, d2) = w2
    return w1 if (d1 - e1) > (d2 - e2) else w2


def recursive_search(graph, current_pos, target, used_pos, opt_fn):
    '''this function searches all possible ways without returning to same
    position twice and then applies the optimisation functions to choose
    the best path.

    # positive: min effort -> A -> C -> D -> H
    >>> recursive_search(graph, "A", "H", (), opt_min_effort)
    (6, 7, ('A', 'C', 'D', 'H'))

    # positive: diff (dist-effort) -> tie, but your compare picks the 2nd -> also A -> C -> D -> H
    >>> recursive_search(graph, "A", "H", (), opt_diff)
    (6, 7, ('A', 'C', 'D', 'H'))

    # negative: invalid start node -> KeyError
    >>> recursive_search(graph, "X", "H", (), opt_min_effort)
    X
    '''
    used_pos = used_pos + (current_pos,)
    # Base Case: Returns 3 values
    if current_pos == target:
        return (0, 0, (target,))
    moves = cat_next_moves(current_pos, graph)
    candidates = []

    for nxt, (e_edge, d_edge) in moves.items():
        if nxt in used_pos:
            continue
        result = recursive_search(graph, nxt, target, used_pos, opt_fn)
        if result:
            # result is (effort, distraction, path) -> 3 values
            e_sub, d_sub, path_sub = result
            total_e = e_edge + e_sub
            total_d = d_edge + d_sub
            full_path = (current_pos,) + path_sub
            # Candidates stored as (PathTuple, (Effort, Dist)) for opt_fn compatibility
            candidates.append((full_path, (total_e, total_d)))

    if not candidates:
        return None
    # apply_opt returns ONE candidate: (best_path, (best_e, best_d))
    best_candidate = apply_opt(opt_fn, candidates)
    best_path, (best_e, best_d) = best_candidate
    # ALWAYS return 3 values to avoid the Unpack Error
    return (best_e, best_d, best_path)


def draw_node(name, position):
    '''a function that draws the node with turtle through its position and name
    '''
    t = turtle.Turtle()
    turtle.tracer(0)
    t.hideturtle()
    # (x, y) is the CENTER of the node
    x, y = position

    # draw the circle
    t.penup()
    # go to bottom of circle
    t.goto(x, y - 20)
    t.setheading(0)
    t.pendown()
    t.width(3)
    # draw circle with given radius
    t.circle(20)
    # draw the name in the middle
    t.penup()
    t.goto(x, y - 10)
    t.write(name, align="center", font=("Arial", 18, "normal"))
    turtle.update()


def draw_undir_relations(coord_A, coord_B):
    '''the function draws a line between nodes contact only 
    on point on border of node with vektor calculations.
    '''
    t = turtle.Turtle()
    turtle.tracer(0)
    t.hideturtle()
    x1, y1 = coord_A
    x2, y2 = coord_B
    dx, dy = x2 - x1, y2 - y1
    #  gives distance(length) between two positions
    dist = math.hypot(dx, dy)
    ux, uy = dx/dist+(10**-10), dy/dist+(10**-10)
    # calculating circles border positions
    sx = x1 + ux * 20
    sy = y1 + uy * 20
    ex = x2 - ux * 20
    ey = y2 - uy * 20
    # draw line
    t.penup()
    t.goto(sx, sy)
    t.pendown()
    t.goto(ex, ey)
    t.penup()
    turtle.update()
doctest.testmod()