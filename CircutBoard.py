# Ari Chadda
# CS76 PA4 10/18/20

class CircutBoard:

    def __init__(self, boardfile): # constructor for board class
        self.shapes = []
        self.lines = []
        self.map = {} # map to visualize

        self.map_dict = {} # dictionary of domains
        self.prediction_dict = {} # to store the results
        self.options = []

        # based on file loading from PA2
        f = open(boardfile) # load file
        for line in f:
            line = line.strip()
            if len(line) == 0:
                pass
            elif line[0] == "\\":
                chars = line[1:].split("*") # asterix is used to denote newline
                width = len(chars[0])
                height = len(chars)
                self.shapes.append([line[1], width, height])
            else:
                self.lines.append(line)
        f.close()

        self.width = len(self.lines[0]) # width of the board
        self.height = len(self.lines) # height of the board
        self.viz = list("".join(self.lines)) # visualization . board


    def create_graph(self):
        for shape in self.shapes:
            collection = []

            for x in range(self.width):
                for y in range(self.height):
                    if (x + shape[1]) <= self.width and (y + shape[2]) <= self.height:
                        intermediary = []

                        for width in range(x, x + shape[1]):
                            for height in range(y, y + shape[2]):
                                intermediary.append([width, height]) # if it fits in the board add it

                        collection.append(intermediary)
                    self.options.append([x, y]) # all the points

            self.map_dict[shape[0]] = collection # only storing placements within the board
            self.prediction_dict[shape[0]] = [] # creating the prediction dict with empty assignments

        return self.map_dict, self.prediction_dict, self.options # return to pass to CSPSolver

    def minimum_value_heuristic(self, map_dict, prediction_dict):
        keys_list = []
        score_dict = {} # to store the scores
        score = 0
        keys = list(map_dict.keys())

        for key in keys:
            filled = prediction_dict.get(key) # the filled points
            options = map_dict.get(key)

            for option in options:
                for point in filled:
                    for num in option: # if the filled points take up a solution increase the score
                        if point == num:
                            score += 1
            score_dict[key] = score # store the score
            score = 0

        for k in sorted(score_dict, key=lambda k: score_dict[k], reverse=True): # sort lowest to highest and return
            keys_list.append(k)
        return keys_list

    def degree_heuristic(self, map_dict):
        keys_list = []
        # sort highest to lowest number of possible moves which constrain placement
        for k in sorted(map_dict, key=lambda k: len(map_dict[k]), reverse=True):
            keys_list.append(k)
        return keys_list

    def least_constraining_value_heuristic(self, map_dict):
        keys_list = []
        # sort lowest to highest number of possible moves which constrain placement
        for k in sorted(map_dict, key=lambda k: len(map_dict[k])):
            keys_list.append(k)
        return keys_list

    # mostly from PA2 below
    def index(self, x, y):
        # index for visualizing
        return (self.height - y - 1) * self.width + x

    # board to visulaize
    def __str__(self):
        renderlist = list(self.viz)

        for key in self.map.keys():
            points = self.map.get(key)
            for point in points:
                renderlist[self.index(point[0], point[1])] = key # swap out board pieces for empty space

        s = ""
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                s += renderlist[self.index(x, y)] # concatentate into a string with new lines
            s += "\n"

        return s # return to print


if __name__ == "__main__":
    test_board1 = CircutBoard('board1.txt')
    map_dict, prediction_dict, options = test_board1.create_graph()
    print(test_board1.shapes)
    print(map_dict)
    print(prediction_dict)
    print(options)



