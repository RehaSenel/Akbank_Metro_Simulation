# Akbank Metro Simulation Project

This project simulates a metro network using a graph-based model where stations are nodes and the connections between them are weighted edged representing travel times. Here we implement two types of search algorithm to find the routes. Breadth-First Search (BFS) is used to determine the route with the minimum number of nodes, and A\* is used to identigy the fastest route based on travel time and a transfer penalty when switching metro lines.

Python is choosen to complete the project. Libraries like `collections`, `heapq` and `random` are used for implementation of queues, priority ques and heuristic functions.

## Table of Contents

- How it Works
- Usage
- Testing Scenarios
- Prequisites
- License

## How it Works

### BFS for Minimal Transfers

- The `en_az_aktarma_bul` method uses BFS to search for the route with the fewest transwers.
- It maintains a queue of tuples `(station, route_so_far)` and a set of visited stations to avoid cycles.

### A\* for Fastest Route

- The `en_hizli_rota_bul` method uses BFS to search for the route with the fewest transwers.
- Tuple stored in the heap is:
  `(total_estimated_cost, id(station), station, path_so_far)`
- A simple heuristic is used (by default returning 0), which makes the search behave like a Dijkstra's algorithm.

# Heuristic wih Transfer Penalty

- The `compute_heuristic` method applies a random penalty choosen between 3 and 10 minutes if the current station and the target station are on different metro lines. This is to represent the additional walking and waiting time required whe ntransferring between two metro lines in a real world metro system.

- The `aktarma_sureli_en_hizli_rota_bul` method applies this heuristic so that routes with fewer transfers are favored if they result in lower overall travel time.

## Usage

Open the terminal and run the Python file:

```python
python RehaSenel_MetroSimulation.py
```

## Testing Scenarios

There are 4 test scenarios that covers:

- M1 AŞTİ to K4 OSB
- T1 Batıkent to T4 Keçiören
- T4 Keçiören to M1 AŞTİ
- T1 Batıkent to M1 AŞTİ

Each scenario prints:

- The route with the fewest transfers.
- The fastest route determined by A\* search.
- The fastest route with random transfer penalties applied.

## Prequisites

- Python 3.x
- Standard Python Libraries:
  - `collections`
  - `heapq`
  - `random`

## License

This project is open source and available under the MIT License.
