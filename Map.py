# Ari Chadda
# CS76 PA4 10/18/20

class Map:

    def __init__(self, map_file): # map object constructor
        self.map_file = map_file
        self.color_options = [] # to store color options at bottom of file
        self.map_dict = {} # to store the graph in dictionary form
        self.prediction_dict = {} # to hold the answers

    # based on code from PA2
    def create_graph(self):
        f = open(self.map_file) # read from file
        for line in f:
            line = line.strip()

            if len(line) == 0:
                pass

            elif line[0] == "\\":
                line = line.replace("\\", "")  # colors were stored at bottom of file marked with backslash
                colors_list = line.split(',')
                self.color_options = colors_list
                for key in self.map_dict:
                    self.prediction_dict[key] = []  # create prediction dict with empty predictions
            else:
                line_havles = line.split(':')
                node = line_havles[0]
                self.map_dict[node] = line_havles[1].split(',')  # add adjacents
        f.close()  # close file
        return self.map_dict, self.color_options, self.prediction_dict  # return to pass to CSPSolver

    def minimum_value_heuristic(self, map_dict, prediction_dict):
        keys_list = [] # stores the keys
        score_dict = {} # scores the key scores
        score = 0
        keys = list(map_dict.keys())

        for key in keys:
            adjacent = map_dict.get(key)

            for node in adjacent: # if the adjacent nodes have colors assigned
                if prediction_dict.get(node):
                    score += 1 # score it higher
                score_dict[key] = score
                score = 0

        for k in sorted(score_dict, key=lambda k: score_dict[k], reverse=True): # sort highest to lowest
            keys_list.append(k)
        return keys_list # return new order

    def degree_heuristic(self, map_dict):
        keys_list = [] # store keys
        # sort highest to lowest number of adjacent nodes which constrain coloring
        for k in sorted(map_dict, key=lambda k: len(map_dict[k]), reverse=True):
            keys_list.append(k)
        return keys_list

    def least_constraining_value_heuristic(self, map_dict):
        keys_list = []
        # sort lowest to highest number of adjacent nodes which constrain coloring
        for k in sorted(map_dict, key=lambda k: len(map_dict[k])):
            keys_list.append(k)
        return keys_list


if __name__ == "__main__":
    test_map1 = Map('map1.txt')
    test_map1.create_graph()
