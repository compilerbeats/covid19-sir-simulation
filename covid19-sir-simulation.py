# usage: py covid19-sir-simulation.py graph_r1_5_a1_1_lr1_t0_9 1000000 0.6 0.3

import sys
import random
import math
import statistics

graph_input_file = sys.argv[1]
n = int(sys.argv[2])
beta = float(sys.argv[3])
gamma = float(sys.argv[4])

MAX_ROUNDS = math.sqrt(n)

SUSCEPTIBLE = 'S'
INFECTIOUS = 'I'
RECOVERED = 'R'
EMPTY_STATE = ''

def read_graph(file_path):
    input_graph = {}
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
            input_graph[node] = [adj_nodes, [SUSCEPTIBLE, EMPTY_STATE]]

    return input_graph
number_of_simulations = 10
current_simulation = 1
simulations = list()
while current_simulation <= number_of_simulations:
    round_counter = 0
    # read graph
    graph = read_graph(graph_input_file)

    # print(graph[0])

    # set random node to I (infected)
    idx_infected = random.randint(0, len(graph) - 1)

    graph[idx_infected][1][0] = INFECTIOUS
    graph[idx_infected][1][1] = EMPTY_STATE

    # print(graph[idx_infected])

    infectious_nodes = {idx_infected}
    recovered_nodes = set()
    while round_counter < MAX_ROUNDS:
        for infected_node in infectious_nodes:
            # has infected_node any neighbours?
            if len(graph[infected_node][0]) > 0:
                random_neighbour = graph[infected_node][0][random.randint(0, len(graph[infected_node][0]) - 1)]
                if graph[random_neighbour][1][0] == SUSCEPTIBLE and random.random() < beta:
                    # infect random neighbour with probability beta
                    graph[random_neighbour][1][1] = INFECTIOUS

            if random.random() < gamma:
                # recover infected node with probability gamma
                graph[infected_node][1][1] = RECOVERED

        # set new status to every node and keep track of infectious and recovered nodes
        for node in graph:
            if not graph[node][1][1] == EMPTY_STATE:
                graph[node][1][0] = graph[node][1][1]
                graph[node][1][1] = EMPTY_STATE

                if graph[node][1][0] == INFECTIOUS:
                    infectious_nodes.add(node)

                if graph[node][1][0] == RECOVERED:
                    infectious_nodes.discard(node)
                    recovered_nodes.add(node)

        if (len(infectious_nodes) + len(recovered_nodes)) > (n / 3):
            # print("outbreak after " + str(round_counter) + " rounds!")
            break

        if len(infectious_nodes) == 0:
            # print("no infected nodes left!")
            round_counter = math.inf
            break
        round_counter += 1

        if False: #round_counter % 10 == 0:
            print("infected nodes: " + str(len(infectious_nodes)))
            print("recovered nodes: " + str(len(recovered_nodes)))

    print(graph_input_file + ";" + str(beta) + ";" + str(gamma) + ";" + str(round_counter))
    simulations.append(round_counter)

    current_simulation += 1
    graph = {}
    infectious_nodes = set()
    recovered_nodes = set() 

print("median of " + str(number_of_simulations) + ": " + str(statistics.median(simulations)))
