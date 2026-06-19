'''this file checks the preformance time of recursive and greedy algorithem functions'''
import blatt_7_meth as meth
import time


_author_ = "8408293, Alizadeh, 8236539, Yakout"
_credit_ = "Written with assistance from ChatGPT and Gemini."

def time_calcul(graph):
    strt_time = time.perf_counter()
    result = meth.recursive_search(graph, "A", "H", (), meth.opt_diff)
    perf_time1 = time.perf_counter() - strt_time
    strt_time = time.perf_counter()
    total_effort = 0
    total_dist = 0
    cat_pos = "A"
    best_path = ["A"]
    used_pos = ["A"]    
    while cat_pos != "H":
        # putting the created tuples created fom the function in a list
        moves = meth.cat_next_moves(cat_pos, meth.graph)
        # filtering the positions already visited out, to compare positions later.
        posts = [(dst, vals) for dst, vals in moves.items() 
                 if dst not in used_pos]
        # in case the cat got to a place where it cant move to the house anymore:
        if not posts:
            print("Cat is stuck! No more ways home.")
            break                 
        new_pos = meth.apply_opt(meth.opt_greedy, posts)
        name, (e, d) = new_pos
        used_pos.append(name)
        best_path.append(name)
        total_effort += e
        total_dist += d
        cat_pos = name
    perf_time2 = time.perf_counter() - strt_time

    return (f'''greedy performance time: {perf_time2} 
recursive preformance time for 1 chosen function: {perf_time1}''')
print(time_calcul(meth.graph))

