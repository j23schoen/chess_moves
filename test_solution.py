
# | 0| 1| 2| 3| 4| 5| 6| 7|
# -------------------------
# | 8| 9|10|11|12|13|14|15|
# -------------------------
# |16|17|18|19|20|21|22|23|
# -------------------------
# |24|25|26|27|28|29|30|31|
# -------------------------
# |32|33|34|35|36|37|38|39|
# -------------------------
# |40|41|42|43|44|45|46|47|
# -------------------------
# |48|49|50|51|52|53|54|55|
# -------------------------
# |56|57|58|59|60|61|62|63|


top_edges = [0, 1, 2, 3, 4, 5, 6, 7]
bottom_edges = [56, 57, 58, 59, 60, 61, 62, 63]
left_edges = [0, 8, 16, 24, 32, 40, 48, 56]
right_edges = [7, 15, 23, 31, 39, 47, 55, 63]

def create_graph(numbers):
    graph = {}

    for i in numbers:
        graph[i] = []
        number_is_top_edge = i in top_edges 
        number_is_bottom = i in bottom_edges
        number_is_left_edge = i in left_edges 
        number_is_right_edge = i in right_edges 
        # traverse vertically up the board
        if not number_is_top_edge and i - 16 >= 0:
            # can traverse upwards
            working_number = i - 16
            # try to go one left
            if not number_is_left_edge:
                graph[i].append(working_number - 1)
            # try to go one right
            if not number_is_right_edge:
                graph[i].append(working_number + 1)
            pass
        # traverse down the board
        if not number_is_bottom and i + 16 <= 63:
            # can traverse down
            working_number = i + 16
            # try to go one left
            if not number_is_left_edge:
                graph[i].append(working_number - 1)
            if not number_is_right_edge:
                graph[i].append(working_number + 1)
        # traverse left 2 places
        if not number_is_left_edge and i - 1 not in left_edges:
            # go left two places
            working_number = i - 2
            # try to go up one row (-8)
            if not number_is_top_edge:
                graph[i].append(working_number - 8)
            # try to go down one row
            if not number_is_bottom:
                graph[i].append(working_number + 8)
        # traverse right 2 places
        if not number_is_right_edge and i + 1 not in right_edges:
            # can traverse right
            working_number = i + 2
            # try to go up one row  (-8)
            if not number_is_top_edge:
                graph[i].append(working_number - 8)
            # try to down two rows (16)
            if working_number + 8 not in bottom_edges:
                graph[i].append(working_number + 8)

    return graph
    
# visits all the nodes of a graph (connected coamponent) using BFS
def bfs_shortest_path(graph, start, goal):
    # keep track of explored nodes
    explored = []
    # keep track of all the paths to be checked
    queue = [[start]]
 
    # return path if start is goal
    if start == goal:
        return "That was easy! Start = goal"
    # keeps looping until all possible paths have been checked
    while queue:
        # pop the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            # go through all neighbour nodes, construct a new path and
            # push it into the queue
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                # return path if neighbour is goal
                if neighbour == goal:
                    return len(new_path) - 1
 
            # mark node as explored
            explored.append(node)
 
    # in case there's no path between the 2 nodes
    return "no connecting path."
    
def answer(start, end):
    numbers = list(range(0, 64))
    graph = create_graph(numbers)
    return bfs_shortest_path(graph, start, end)

def test_create_graph_for_top_edge():
    numbers = [0, 1, 2, 3, 4, 5, 6, 7]
    graph = {
        0: [10, 17],
        1: [11, 16, 18],
        2: [8, 12, 17, 19],
        3: [9, 13, 18, 20],
        4: [10, 14, 19, 21],
        5: [11, 15, 20, 22],
        6: [12, 21, 23],
        7: [13, 22]
    }

    result = create_graph(numbers)

    d = {key: sorted(value) for (key, value) in result.items()}

    assert d== graph

def test_corners():
    numbers = [0, 7, 56, 63]
    graph = {
        0: [10, 17],
        7: [13, 22],
        56: [41, 50],
        63: [46, 53]
    }

    result = create_graph(numbers)
    d = {key: sorted(value) for (key, value) in graph.items()}
    assert d== graph

def test_left_edge():
    numbers = [8, 40]
    graph = {
        8: [2, 18, 25],
        40: [25, 34, 50, 57]
    }

    result = create_graph(numbers)
    d = {key: sorted(value) for (key, value) in result.items()}
    assert d== graph

def test_right_edge():
    numbers = [31, 55]
    graph = {
        31: [14, 21, 37, 46],
        55: [38, 45, 61]
    }
    result = create_graph(numbers)
    d = {key: sorted(value) for (key, value) in result.items()}
    assert d== graph

def test_middle():
    numbers = [26, 44]
    graph = {
        26: [9, 11, 16, 20, 32, 36, 41, 43],
        44: [27, 29, 34, 38, 50, 54, 59, 61]
    }

    result = create_graph(numbers)
    d = {key: sorted(value) for (key, value) in result.items()}
    assert d == graph

def test_get_shortest_path():
    result = answer(19, 36)
    assert result == 1
