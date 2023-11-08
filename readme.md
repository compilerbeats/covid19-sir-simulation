# Overview

These scripts can be used to simulate the SIR model on a geometric graph built upon $n$ points generated on a play field.

# Usage
## Generate points

First, we randomly place our $n$ points on the play field (square with side length $\sqrt{n}$) by executing

```
py covid19-sir-simulation-generate-points.py n k
```

where $k$ represents the number of points which are initially marked as infected.
We note that these $k$ points are the ones that are the nearest to the middle of the play field.

## Generate graph

After generating the points (or nodes from now on) on our play field, we can now generate a graph by using

```
py covid19-sir-simulation-generate-graph.py input_points n r a include_long_range threshold
```

The parameters are described by:
- $n$: number of points
- $r$: radius
- $a$: alpha
- $include$ \_ $long$ \_ $range$: either 0 or 1
- $threshold$: percentage of the total nodes that should be contained in the largest connected component (0.0, 1.0]

## Execute simulation

Now that all preparations are done, we can finally execute the simulation on the generated graph by

```
py covid19-sir-simulation.py graph_input_file n beta gamma
```

where $\beta$ is the probability for an infectious node to infect a random neighbour if it is susceptible and $\gamma$ 
represents the probability that an infectious node recovers after each simulation round.

