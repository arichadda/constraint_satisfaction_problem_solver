# Ari Chadda
# CS76 PA4 10/18/20

from CSPSolver import CSPSolver
from CircutBoard import CircutBoard

if __name__ == "__main__":

    test_board1 = CircutBoard('board1.txt') # create board object
    map_dict1, prediction_dict1, options1 = test_board1.create_graph() # create graph
    # instantiate solver object (more flags in CSPSolver.py)
    solver1 = CSPSolver(map_dict1, options1, prediction_dict1, test_board1)
    answer1 = solver1.backtracing() # start backtracking
    print("Answer to map 1:", answer1)
    print(test_board1) # display filled ascii board
