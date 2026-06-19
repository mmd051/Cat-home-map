'''
Main module for the Cat Problem.
Uses functions from 'blatt_7_meth.py' to find and evaluate paths in a graph.

Available methods:
- Greedy approach: Fast, local decision-making (not always optimal).
- Recursive search: Exhaustive search for the global optimum.

The module also tracks and displays the execution time for each method.
'''
import blatt_7_meth as meth
import time

__author__ = "8408293, Alizadeh, 8236539, Yakout"
__credit__ = "Written with assistance from ChatGPT and Gemini."


def main():
    '''this here is the main function, where
    all methodes would be manupilated to get the expected results'''
    while True:
        # draw nodes the maps points
        for node, pos in meth.map_pos.items():
            meth.draw_node(node, pos)

        # draw the ways in the map from source to neghibors(the lines)
        for src, neighs in meth.map_letters.items():
            for dst in neighs:
                meth.draw_undir_relations(meth.map_pos[src], meth.map_pos[dst])
        # choosing between recursive or greedy method
        path_type = input("Mode (greedy/recursive): ").lower()
        if path_type == "greedy":
            start_time = time.perf_counter()
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
                result = total_effort, total_dist, best_path
        elif path_type == "recursive":
            print("1: Higher Distraction\n2: Min Effort\n3: High Dist/Effort Ratio")
            choice = input("Select: ")
            
            # Pass the FUNCTION names, not function CALLS
            strategies = {"1": meth.opt_greedy, "2": meth.opt_min_effort, "3": meth.opt_diff}
            selected_fn = strategies.get(choice, meth.opt_greedy)
            
            start_time = time.perf_counter()
            result = meth.recursive_search(meth.graph, "A", "H", (), selected_fn)
        else:
            print("No path possible.")
        
        total_effort, total_dist, best_path = result
        perf_time = time.perf_counter() - start_time
        print(f"Path: {best_path}\nEffort: {total_effort}\nDist: {total_dist}")
        print(f"Time: {perf_time}s")

        if input("Again? (yes/no): ").lower() != "yes":
            break

if __name__ == '__main__':
    main()