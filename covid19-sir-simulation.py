# usage: py covid19-sir-simulation.py graph_r1_5_a1_1_lr1_t0_9 1000000 1.1 0.6 0.3 1
import os.path
import sys
import math
import statistics
import random

graph_input_file = sys.argv[1]
n = int(sys.argv[2])
alpha = float(sys.argv[3])
beta = float(sys.argv[4])
gamma = float(sys.argv[5])
write_to_output_file = 0
if len(sys.argv) > 6:
    write_to_output_file = int(sys.argv[6])

MAX_ROUNDS = math.sqrt(n)

SUSCEPTIBLE = 'S'
INFECTIOUS = 'I'
RECOVERED = 'R'
EMPTY_STATE = ''

def read_graph(file_path, infectious_nodes):
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
            is_infectious = False
            if "_I" in node:
                is_infectious = True
                node = node.replace("_I", "")
            node = int(node.strip())

            # Split the adjacent nodes string by commas and convert to integers
            adj_nodes = [int(adj_node.strip()) for adj_node in adj_list_str.split(',') if adj_node.strip().isdigit()]

            # Add to the graph
            # [adj_list, [curr_status, next_status]]
            if is_infectious:
                input_graph[node] = [adj_nodes, [INFECTIOUS, EMPTY_STATE]]
                infectious_nodes.add(node)
            else:
                input_graph[node] = [adj_nodes, [SUSCEPTIBLE, EMPTY_STATE]]

    return input_graph


number_of_simulations = 30
current_simulation = 1
simulations = list()
while current_simulation <= number_of_simulations:
    round_counter = 0
    # read graph
    infectious_nodes = set()
    graph = read_graph(graph_input_file, infectious_nodes)

    recovered_nodes = set()
    # execute infinite amount of rounds until either the outbreak threshold is reached or no infectious nodes are left
    while True: # round_counter < MAX_ROUNDS:
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

        if False:  #round_counter % 10 == 0:
            print("infected nodes: " + str(len(infectious_nodes)))
            print("recovered nodes: " + str(len(recovered_nodes)))

        round_counter += 1

    # do not execute this code since we deactivated the maximum number of rounds
    if False:  # round_counter >= 1000 and len(infectious_nodes) > 0:
        print("reached maximum number of rounds")
        print("infected nodes: " + str(len(infectious_nodes)))
        print("recovered nodes: " + str(len(recovered_nodes)))
        round_counter = math.inf

    print(graph_input_file + ";" + str(beta) + ";" + str(gamma) + ";" + str(round_counter))
    simulations.append(round_counter)

    current_simulation += 1
    graph = {}
    infectious_nodes = set()
    recovered_nodes = set() 

median = statistics.median(simulations)
print("median of " + str(number_of_simulations) + ": " + str(median))

if write_to_output_file == 1:
    output_filename = "covid19-sir-simulation-results-alpha-" + str(alpha)
    if os.path.exists(output_filename) and os.path.getsize(output_filename) > 0:
        # file already exists and there is already some result in it
        with open(output_filename, 'a') as results_file:
            results_file.write(str(alpha) + ";" + str(beta) + ";" + str(gamma) + ";" + str(median) + "\n")
    else:
        with open(output_filename, 'w') as results_file:
            results_file.write("alpha;beta;gamma;r_median\n")
            # write header line into file and append first result
            results_file.write(str(alpha) + ";" + str(beta) + ";" + str(gamma) + ";" + str(median) + "\n")

