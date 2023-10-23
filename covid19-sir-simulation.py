import math
import sys
import random
import math

input_file = sys.argv[1]
n = int(sys.argv[2])
gamma = float(sys.argv[3])

round_counter = 0
MAX_ROUNDS = math.sqrt(n)

SUSCEPTIBLE = 'S'
INFECTED = 'I'
RECOVERED = 'R'

def read_graph(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        for line in file.readlines():
            # Split the line at the colon
            parts = line.split(':', 1)

            # If the line isn't in the correct format, skip it
            if len(parts) != 2:
                continue

            # Extract the node and the adjacent nodes
            node, adj_list_str = parts

            # Convert the node to an integer
            node = int(node.strip())

            # Split the adjacent nodes string by commas and convert to integers
            adj_nodes = [int(adj_node.strip()) for adj_node in adj_list_str.split(',') if adj_node.strip().isdigit()]

            # Add to the graph
            # [adj_list, [curr_status, next_status]]
            graph[node] = [adj_nodes, [SUSCEPTIBLE, SUSCEPTIBLE]]

    return graph

# read graph
graph = read_graph(input_file)

print(graph[0])

# set random node to I (infected)
idx_infected = random.randint(0, len(graph) - 1)

graph[idx_infected][1][1] = INFECTED

print(graph[idx_infected])

infected_nodes = []
recovered_nodes = []
beta = 0.6

# todo: why doesn't a outbreak occur for beta = 0.6?
while round_counter < MAX_ROUNDS:
    for infected_node in infected_nodes:
        # has infected_node any neighbours?
        if len(graph[infected_node][0]) > 0:
            random_neighbour = graph[infected_node][0][random.randint(0, len(graph[infected_node][0]) - 1)]
            if random.random() < beta and graph[random_neighbour][1][0] == SUSCEPTIBLE:
                # infect random neighbour with probability beta
                graph[random_neighbour][1][1] = INFECTED

        if random.random() < gamma:
            # recover infected node with probability gamma
            graph[infected_node][1][1] = RECOVERED

    # set new status to every node
    for node in graph:
        if graph[node][1][0] != graph[node][1][1]:
            graph[node][1][0] = graph[node][1][1]

        if graph[node][1][0] == INFECTED:
            infected_nodes.append(node)

        if graph[node][1][1] == RECOVERED:
            infected_nodes.remove(node)

        graph[node][1][1] = ''

    if (len(infected_nodes) + len(recovered_nodes)) > (n / 3):
        print("outbreak!")
        break
    round_counter += 1