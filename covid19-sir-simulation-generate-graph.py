# usage: py covid19-sir-simulation-generate-graph.py points 1000000 1.5 2.8 1 0.9
import math
from collections import deque
import sys
import random

input_points = sys.argv[1]
n = int(sys.argv[2])
r = float(sys.argv[3])
a = float(sys.argv[4])
include_long_range = int(sys.argv[5])
threshold = float(sys.argv[6])

sqrt_n = int(math.sqrt(n))

# create grid according to n and the given radius r
# add an additional row and column in order to work with uneven radii
grid = [[[] for _ in range(int(sqrt_n / r) + 1)] for _ in range(int(sqrt_n / r) + 1)]

# read points from file
nodes = {}
with open(input_points, 'r') as file:
    for line in file:
        key, x, y, meta1, meta2, meta3 = line.strip().split(',')
        key = int(key)
        x = float(x)
        y = float(y)
        nodes[key] = [(x, y), meta1 if meta1 else None, meta2, meta3]

# init graph
graph = {}

for i in range(0, n):
    graph[i] = list()

print(len(graph))


def is_threshold_reached(total, current, threshold):
    return current / total >= threshold


def bfs(node, graph, visited):
    queue = deque([node])
    visited.add(node)
    count = 1

    while queue:
        current_node = queue.popleft()

        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                count += 1

    return count  # return the count instead of just returning


def largest_connected_component(graph):
    visited = set()
    largest_size = 0

    for node in graph:
        if node not in visited:
            size = bfs(node, graph, visited)
            largest_size = max(largest_size, size)

    return largest_size


def calculate_distance(x1, y1, x2, y2):
    return math.dist((x1, y1), (x2, y2))


def get_points_of_neighbors(grid, row, col):
    # list to store the neighbors
    neighbors = []

    # total number of rows and columns in the grid
    num_rows = len(grid)
    num_cols = len(grid[0]) if grid else 0

    # possible directions to move in the grid, including diagonals
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),   # up, down, left, right
        (0, 0),                             # include itself
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # diagonal directions
    ]

    # check all directions
    for dr, dc in directions:
        # calculate the neighboring row and column
        n_row, n_col = row + dr, col + dc

        # check if the neighboring cell is within the grid boundaries
        if 0 <= n_row < num_rows and 0 <= n_col < num_cols:
            # add the neighboring cell to the list of neighbors
            neighbors += grid[n_row][n_col]

    return neighbors


def build_graph(graph, r):
    no_long_range_counter = 0
    for i in range(0, n):
        square_of_i = nodes[i][1]

        # create list of all points which might be inside the radius r
        candidate_points = get_points_of_neighbors(grid, square_of_i[1], square_of_i[0])

        # check if any of the candidates has a distance less than r
        for candidate in candidate_points:
            if calculate_distance(nodes[i][0][0], nodes[i][0][1], nodes[candidate][0][0], nodes[candidate][0][1]) < r:
                if candidate not in graph[i] and i != candidate:
                    graph[i].append(candidate)
                if i not in graph[candidate] and i != candidate:
                    graph[candidate].append(i)

        # add long range edge
        if include_long_range == 1:
            e_x = -1
            e_y = -1
            # draw new random values if the long range edge would land outside of the grid
            while not ((0 <= e_x < sqrt_n) and (0 <= e_y < sqrt_n)):
                angle = random.uniform(0, 2 * math.pi)
                x = random.uniform(0, 1)
                d = (math.pow(x, (-1 / (a - 1))))

                e_x = nodes[i][0][0] + (d * math.cos(angle))
                e_y = nodes[i][0][1] + (d * math.sin(angle))

            square_of_e = (math.floor(e_x / r), math.floor(e_y / r))

            # find possible candidates for the long range edge
            long_range_candidates = get_points_of_neighbors(grid, square_of_e[1], square_of_e[0])

            # choose closest neighbour, if there is any at all
            min_distance = sys.float_info.max
            v = None
            for candidate in long_range_candidates:
                distance_to_long_range_candidate = calculate_distance(e_x, e_y,
                                                                      nodes[candidate][0][0], nodes[candidate][0][1])
                if (distance_to_long_range_candidate <= r) and distance_to_long_range_candidate < min_distance:
                    min_distance = distance_to_long_range_candidate
                    v = candidate

            # add long range edge to adjacency liste
            if v is not None:
                if v not in graph[i] and v != i:
                    graph[i].append(v)
            else:
                no_long_range_counter += 1

            if False:
                print("old pos_x: " + str(nodes[i][0][0]) + "; new pos_x " + str(e_x))
                print("old pos_y: " + str(nodes[i][0][1]) + "; new pos_y " + str(e_y))

    print("building graph with radius " + str(r) + " done")
    print("No long range edge drawn in " + str(no_long_range_counter) + " cases")


def write_graph_to_file(graph, file_path):
    with open(file_path, 'w') as file:
        for node, neighbors in graph.items():
            # mark the initially infected nodes
            if nodes[node][2] == 'I':
                print("infectious node " + str(node) + " found")
                node = str(node) + "_I"

            # convert the list of neighbors to a string, and write to the file
            neighbors_str = ', '.join(map(str, neighbors))
            file.write(f"{node}: {neighbors_str}\n")


size_of_largest_component = 1
while not is_threshold_reached(n, size_of_largest_component, threshold):
    size_of_largest_component = 1
    # build grid with current radius
    grid = [[[] for _ in range(int(sqrt_n / r) + 1)] for _ in range(int(sqrt_n / r) + 1)]

    for i in range(0, n):
        current_node = nodes[i]

        grid_x = math.floor(current_node[0][0] / r)
        grid_y = math.floor(current_node[0][1] / r)
        grid[grid_y][grid_x].append(i)

        # store point and metadata
        nodes[i][1] = (grid_x, grid_y)

    # build graph according to grid
    build_graph(graph, r)

    # check graph with current radius
    size_of_largest_component = largest_connected_component(graph)
    print("radius " + str(r) + " generated largest connected component with " + str(size_of_largest_component)
          + " nodes")

    if not is_threshold_reached(n, size_of_largest_component, threshold):
        # init variables and increase radius
        r += 0.01
        grid = []
        # init graph
        graph = {}

        for i in range(0, n):
            graph[i] = list()

    print("--------------------------")

print("Found connected component which contains " + str((size_of_largest_component / n) * 100) +
      "% of all nodes using a radius of " + str(r))


# write graph to file to use it in the SIR simulation later on
graph_file_name = "graph_" + ("r" + str(r).replace('.', '_')) + ("_a" + str(a).replace(".", "_")) + \
                  ("_lr" + str(include_long_range)) + ("_t" + str(threshold).replace(".", "_"))
write_graph_to_file(graph, graph_file_name)
