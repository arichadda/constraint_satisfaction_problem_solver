# README.md for CSP Solver

To run the CSP solver there are two options for problems. 

The first, map coloring gives you two map options which you can specify when you instantiate the `Map` object which takes a `mapfile`. 

The second, circuit board problem gives you one board which you specify when you create your `CircutBoard` class and give it a `boardfile`. 


To run the CSP, you require the following arguments and can also specify which heuristic and inference technique if any you would like to use. 

```
map_dict, 
options, 
prediction_dict, 
problem_instance, 
use_min_val=False, 
use_degree=True, 
least_constraining=False, 
arc_consistency=False, 
is_map_problem=True, 
is_board_problem=False
```

To test the two programs run either 	`color_map.py` or `set_board.py` respectively and make sure that the appropriate flag is checked to `True`. Either `is_map_problem` or `is_board_problem` must be True. 

Map Problem: The map problem was implemented using the book's diagram on page 105 `map1.txt` and the Australia problem from class `map2.txt`. The maps were created using a similar system to the maze system from pa2 and the information was passed in a prediction dictionary which was empty except for the nodes, a map dictionary which contained the adjacents as well as a list that stored the color options. The backtracing code as specified by the instructions was constant between the two models, but I did tweak the minimum remaining values heuristic and the arc consistency to better fit the specific problem. The constraints imposed involved checking if the adjacent nodes shared the same color value. 

Circuit Board Problem: The circuit board problem was the one straight from the assignment. The board was created and printed to a similar system from pa2 and the information was passed with a map dictionary which stored the possible placements for each node within the given rectangle, an options list that contained all the possible points, and a prediction dictionary to store the first value of the placement for each node. The constraints of the problem were that no two pieces can be on top of each other and then were implemented as such and technically that no piece could be beyond the domain of the board. I also did tweak the  minimum remaining values heuristic and the arc consistency to better fit the specific problem as mentioned above, but the backtracing code remained the same. 

Backtracking: The backtracing code was fairly standard steps wise as the one we went over in class. I included flags for each of the heuristics to call them and stored the majority of the information in the class variables. With the backtracing code, it seemed inefficient to pass the entire domain with each iteration, so instead I stored the place of each recursive call as the majority of the information was already in the class variables. I also included flag processing for the use of the AC3 inference. 

Degree Heuristic: The degree heuristic was a simple list reordering of the traversal order based on the number of adjacents for the map coloring problem and the number of possible arrangements within the size of the board for the for the circuit problem. A simple length count and sorting of the dictionaries allowed for the reordering. It seemed illogical to use adjacents with the circuit problem as the pieces could be placed in any order and it did not particularly related to the constraints of the problem. The code for the degree and least constraining heuristics was the same for both problems, but because I changed the MRV heuristic, I moved all three to their respective classes for parity. 

Least Constraining Value Heuristic: The least constraining value heuristic was essentially the opposite of the degree heuristic with those nodes that were adjacent to the fewest nodes or the ones with the most possible locations respectively that would have the smallest effect on the rest of the game for the map coloring problem and the circuit problem respectively. This was again done through list reordering to change the traversal order. 

Minimum Remaining Values: The minimum remaining values heuristic sought to select those with the fewest remaining options first by scoring the number of adjacent/remaining placeable open spaces for the map coloring problem respectively. The larger the number the fewer remaining opportunities that node, so it was placed first and the list was reorganized as the algorithm iterated, recalculating each time. 

Arc Consistency Three: The AC3 algorithm was implemented using the standard drill down to eliminate impossible solutions by looping through with a queue and then creating a list of opportunities to be removed to exclude them from the domain. Due to the slightly different requirements of the problem, they were implemented slightly differently using a flag structure because of the way the domain was organized. In the map coloring problem it had to be derived, while in the circuit board problem, I had already constrained the domain in the map generation step. 

