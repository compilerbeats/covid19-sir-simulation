import math
import random
import sys

n = int(sys.argv[1])
sqrt_n = int(math.sqrt(n))

# place nodes randomly on "play field"
nodes = {}
for i in range(0, n):
    x = math.trunc(random.uniform(0, sqrt_n) * 100.0) / 100.0
    y = math.trunc(random.uniform(0, sqrt_n) * 100.0) / 100.0

    # store point and metadata
    nodes[i] = [(x, y), None, 'S', '']

# print(nodes[0])

# print(grid[0][10])

# write to file
with open('points.txt', 'w') as file:
    for key, value in nodes.items():
        file.write(f"{key},{value[0][0]},{value[0][1]},{value[1]},{value[2]},{value[3]}\n")
