# Ari Chadda
# CS76 PA4 10/18/20

from CSPSolver import CSPSolver
from Map import Map
import time

if __name__ == "__main__":

    t0 = time.process_time() # gives you the time to run
    test_map1 = Map('map1.txt')
    map_dict1, color_options1, prediction_dict1 = test_map1.create_graph() # creates map object and then graph
    # specify which flags (see CSPSolver.py) and make sure that second to last flag is True
    solver1 = CSPSolver(map_dict1, color_options1, prediction_dict1, test_map1, False, True, False, False, True, False)
    # start backtracing to solve
    answer1 = solver1.backtracing()
    t1 = time.process_time()
    print("Time elapsed: ", t1 - t0)
    print("Answer to map 1:", answer1)

    # test_map2 = Map('map2.txt')
    # map_dict2, color_options2, prediction_dict2 = test_map2.create_graph()
    # solver2 = CSPSolver(map_dict2, color_options2, prediction_dict2, test_map2)
    # answer2 = solver2.backtracing()
    # print("Answer to map 2:", answer2)


