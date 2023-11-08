import math
import random
import sys
import heapq

n = int(sys.argv[1])
k = int(sys.argv[2])
sqrt_n = int(math.sqrt(n))

# place nodes randomly on "play field"
nodes = {}
for i in range(0, n):
    x = math.trunc(random.uniform(0, sqrt_n) * 100.0) / 100.0
    y = math.trunc(random.uniform(0, sqrt_n) * 100.0) / 100.0

    # store point and metadata
    nodes[i] = [(x, y), None, 'S', '']


def calculate_distance(point1, point2):
    return math.dist(point1, point2)


def k_nearest_points(nodes_dict, x, k):
    # Create a max heap of size k
    max_heap = []

    # Iterate over all nodes in the dictionary
    for key, point in nodes_dict.items():
        # Calculate the distance from the current point to x
        dist = calculate_distance(point[0], x)

        # Push the negative distance, key, and point onto the heap
        # The heap is maintained based on the negative distance as the first element of the tuple
        heapq.heappush(max_heap, (-dist, key, point[0]))

        # If heap is bigger than k, pop the farthest
        if len(max_heap) > k:
            heapq.heappop(max_heap)

    # Sort the heap based on distance and return the k closest points with their keys
    return sorted([key for dist, key, point in max_heap])


# find the 20 nodes that are the closest to the middle and mark them as INFECTIOUS
infectious_nodes = k_nearest_points(nodes, (sqrt_n / 2, sqrt_n / 2), k)

# print(infectious_nodes)

for idx in infectious_nodes:
    nodes[idx][2] = 'I'
    # print(nodes[idx])

# write to file
with open('points', 'w') as file:
    for key, value in nodes.items():
        file.write(f"{key},{value[0][0]},{value[0][1]},{value[1]},{value[2]},{value[3]}\n")
