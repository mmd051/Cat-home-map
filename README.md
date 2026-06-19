# Cat-home-map
Cat Pathfinding & Optimization SimulationA graph-based pathfinding application that simulates a cat trying to find its way home ("H") from a starting position ("A") using different navigational strategies.
The project demonstrates the trade-offs between local greedy decisions and global recursive searches, complete with performance profiling and real-time visual tracking.
FeaturesGraph-Based Routing: Models paths using custom graph structures containing multi-variable weights (effort costs and distraction values).
Dual-Algorithm Approach:
Greedy Search: Fast, local decision-making that prioritizes immediate high distraction and lower effort.
Recursive Exhaustive Search: Traverses all non-looping paths to find the absolute global optimum based on a chosen strategy. 
Multiple Optimization Strategies: Toggle between maximizing distraction, minimizing physical effort, or optimizing the distraction-to-effort ratio.
Performance Profiling: Built-in execution time tracking using high-resolution timers (time.perf_counter) to analyze algorithm efficiency.
Visual Tracking: Animates the map network and node relations dynamically using Python's turtle graphics library.
Quality Assurance: Integrated automated unit testing utilizing Python’s doctest module to ensure algorithmic correctness. 
File Structure.
blatt_7_2.py: The main executable module handling user interaction, execution mode selection, and time tracking.
blatt_7_meth_2.py: The core utility library containing the graph definitions, search algorithms, optimization math, and UI drawing functions.  doctest_zeitmessung_2.py: A dedicated performance analysis script comparing execution speeds between the greedy and recursive implementations.
How It Works:When running the main module, you can choose between running a quick greedy path or a comprehensive recursive calculation:
Mode (greedy/recursive): recursive
1: Higher Distraction
2: Min Effort
3: High Dist/Effort Ratio
Select: 2

The system then calculates the best path, outputs the total effort and distraction values, and displays the precise computation time:
Path: ('A', 'C', 'D', 'H')
Effort: 6
Dist: 7
Time: 0.000124s
