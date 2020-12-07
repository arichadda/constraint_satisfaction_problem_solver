# Ari Chadda
# CS76 PA4 10/18/20

from collections import deque


class CSPSolver:
    def __init__(self, map_dict, options, prediction_dict, problem_instance, use_min_val=False, use_degree=True,
                 least_constraining=False, arc_consistency=False, is_map_problem=True, is_board_problem=False):
        self.map_dict = map_dict
        self.options = options
        self.prediction_dict = prediction_dict
        self.original_pred_dict = prediction_dict
        self.problem_instance = problem_instance
        self.remove_dict = {}

        self.minimum_value_flag = use_min_val
        self.degree_heuristic_flag = use_degree
        self.least_constraining_value_flag = least_constraining
        self.arc_consistency_three_flag = arc_consistency

        self.map_problem_flag = is_map_problem
        self.board_problem_flag = is_board_problem

    def backtracing(self):

        answer = self.recursive_backtracing_search(0)
        if self.check_complete():
            return answer
        else:
            return "Failure"

    def recursive_backtracing_search(self, val):

        if self.check_complete(): # exit condition
            return self.prediction_dict
        else:

            if self.minimum_value_flag: # mvr flag
                keys_list = self.minimum_value_heuristic()
            elif self.degree_heuristic_flag: # degree heuristic flag
                keys_list = self.degree_heuristic()
            elif self.least_constraining_value_flag: # lcv flag
                keys_list = self.least_constraining_value_heuristic()
            else:
                keys_list = list(self.map_dict.keys())

            for option in self.options:
                if self.is_valid(keys_list[val], option): # if it is a valid move then go ahead
                    self.prediction_dict.update({keys_list[val]: [option]})
                    if (val + 1) < len(keys_list) and val > -1:

                        if self.arc_consistency_three_flag: # arc consistency flag
                            if self.arc_consistency_three(keys_list[val], keys_list): # domain reduction

                                if not self.prediction_dict in self.remove_dict.values():
                                    val += 1
                                    result = self.recursive_backtracing_search(val) # keep drilling down till end

                                    if not self.check_complete(): # if fails then restart
                                        for num in range(val):
                                            self.prediction_dict[keys_list[num]] = []
                                        val = 0
                                    else:
                                        return result

                        else:
                            if not self.prediction_dict in self.remove_dict.values(): # no arc checking
                                val += 1
                                result = self.recursive_backtracing_search(val) # keep drilling down till end

                                if not self.check_complete():
                                    for num in range(val):
                                        self.prediction_dict[keys_list[num]] = []  # if fails then restart
                                    val = 0
                                else:
                                    return result

        return self.prediction_dict

    # as the mvr heuristic required specific parsing each heuristic was stored in the problem file for parity
    def minimum_value_heuristic(self):
        return self.problem_instance.minimum_value_heuristic(self.map_dict, self.prediction_dict)

    # return problem file response
    def degree_heuristic(self):
        return self.problem_instance.degree_heuristic(self.map_dict)

    # return problem file response
    def least_constraining_value_heuristic(self):
        return self.problem_instance.least_constraining_value_heuristic(self.map_dict)

    # AC3 was also tweaked slightly based on problem parsing using flags
    def arc_consistency_three(self, current_node, keys_list):

        if self.map_problem_flag: # adjacents stored slightly differently in both problems
            adjacents = self.map_dict.get(current_node).copy()
        elif self.board_problem_flag:
            adjacents = keys_list.copy() # copying to not mutate original with removals

        queue = deque() # queue for first in last out
        predictions = self.prediction_dict.copy()
        for node in adjacents: # for the options
            if not self.prediction_dict.get(node):
                queue.append((current_node, node)) # add them to the queue

        while queue:
            current_options = self.options.copy()
            (current, next) = queue.pop()
            if self.to_remove(current, next, current_options, predictions): # remove illegal domains
                if len(current_options) == 0:
                    return False

                if adjacents:
                    adjacents.remove(next) # remove the tested one and try next
                    for step in adjacents:
                        queue.append((current, step))
        return True


    def to_remove(self, current, next, current_options, predictions):
        if self.map_problem_flag:
            for option_current in current_options:
                for option_next in self.options:

                    predictions.update({current: [option_current]})
                    predictions.update({next: [option_next]})
                    # test current and next assignment for legality
                    if not self.is_valid(current, option_current, predictions) \
                            and not self.is_valid(next, option_next, predictions):
                        self.remove_dict[current] = predictions # if illegal then remove

            return True

    def is_valid(self, selected, assignment, predictions=None): # make sure move is legal changes for each problem

        if self.map_problem_flag:
            adjacent = self.map_dict.get(selected)
            if adjacent is not None:

                for node in adjacent:
                    if predictions:
                        current = predictions.get(node) # get the adjacent nodes
                    else:
                        current = self.prediction_dict.get(node)
                    if current:
                        for guess in current: # make sure that the adjacent nodes are not equal to the guess
                            if guess == assignment:
                                return False # if they are then not a valid solution
            return True

        elif self.board_problem_flag:
            options = self.map_dict.get(selected) # all the possible placements for the piece within the board
            self.current_locations()

            if options is not None:
                for node in options:
                    # if it is within the board and does not overlap another piece the move is legal
                    if node[0] == assignment and not self.check_overlap(node):
                        return True
            return False

    def current_locations(self): # helper for circuit board validity checking
        for shape in self.prediction_dict.keys():
            start = self.prediction_dict.get(shape)
            options = self.map_dict.get(shape)

            for option in options:
                if start:
                    if option[0] == start[0]: # model the current locations of the boards, also used in visualization
                        self.problem_instance.map[shape] = option

    def check_overlap(self, points): # helper for circuit board validity checking
        for value in self.problem_instance.map.values():
            for point in points:
                for num in value:

                    if num == point: # if points overlap then return true, meaning invalid placement
                        return True
        return False

    def check_complete(self):
        count = 0
        if list(self.prediction_dict.keys()) == list(self.map_dict.keys()):

            for value in list(self.prediction_dict.values()):
                if len(value) == 1: # counter to make sure list values have length greater than 0
                    count += 1

            if count == len(list(self.map_dict.keys())): # if the counts are the same then the problem is solved
                return True
            else:
                return False
