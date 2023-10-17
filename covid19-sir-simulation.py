import random
import math
from collections import deque

n = 1000000
r = 1.36

# init matrix with tupels
# (id, (x_coordinate, y_coordinate), current_state, next_state)

# matrix = np.reshape(np.arange(0,n),(1000,1000))

sqrt_n = int(math.sqrt(n))

# todo: make grid adjustable to r
grid = [[[] for _ in range(int(sqrt_n / r) + 1)] for _ in range(int(sqrt_n / r) + 1)]

nodes = {}
for i in range(0, n):
    x = math.trunc(random.uniform(0, sqrt_n) * 100.0) / 100.0
    y = math.trunc(random.uniform(0, sqrt_n) * 100.0) / 100.0

    # add point to square inside the grid
    grid_x = math.floor(x / r)
    grid_y = math.floor(y / r)
    grid[grid_y][grid_x].append(i)

    # store point and metadata
    nodes[i] = [(x, y), (grid_x, grid_y), 'S', '']

print(nodes[0])

print(grid[0][10])

# generate geometric graph
# i.e. connect vertices

# init graph
graph = {}

for i in range(0, n):
    graph[i] = list()

print(len(graph))

# new idea with grid and squares

# for every iteration of r
# go through every vertex v and check for neighbours who are reachable in radius r: create undirected edge
# calculate a random point e in the grid starting from the vertex v, check if some vertex e_u is inside the radius r going from this grid point (choose the closest one) and draw a directed edge to this vertex e_u
# check if we managed to get a connected component which includes 99% of all vertices (BFS to check connected components)
# if yes, then the graph is done
# otherwise change the radius r

threshold = 0.99

def is_threshold_reached(total, current, threshold):
    return total / current >= threshold

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
    # List to store the neighbors
    neighbors = []

    # Total number of rows and columns in the grid
    num_rows = len(grid)
    num_cols = len(grid[0]) if grid else 0

    # Possible directions to move in the grid, including diagonals
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # up, down, left, right
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # diagonal directions
    ]

    # Check all directions
    for dr, dc in directions:
        # Calculate the neighboring row and column
        n_row, n_col = row + dr, col + dc

        # Check if the neighboring cell is within the grid boundaries
        if 0 <= n_row < num_rows and 0 <= n_col < num_cols:
            # Add the neighboring cell to the list of neighbors
            neighbors += grid[n_row][n_col]

    return neighbors

def build_graph(graph, r):
    for i in range(0, n):
        square_of_i = nodes[i][1]

        # create list of all points which might be inside the radius r
        candidate_points = get_points_of_neighbors(grid, square_of_i[1], square_of_i[0])

        for candidate in candidate_points:
            if calculate_distance(nodes[i][0][0], nodes[i][0][1], nodes[candidate][0][0], nodes[candidate][0][1]) <= r:
                graph[i].append(candidate)
                graph[candidate].append(i)

# todo: parallelize building graph, i.e. split number number of nodes onto different processes
# give complete graph and subgraph (split according to the amount of cores) and process subgraphs separately
build_graph(graph, r)

print("building graph done.")

size_of_largest_component = largest_connected_component(graph)

print(size_of_largest_component)

size_of_largest_component = 0
while False:#not is_threshold_reached(n, size_of_largest_component, threshold):
    # build grid with current radius

    # build graph according to grid

    # check graph with current radius
    size_of_largest_component = largest_connected_component(graph)
    if (n / size_of_largest_component) > threshold:
        # decrease r
        break
    else:
        # increase r
        break
