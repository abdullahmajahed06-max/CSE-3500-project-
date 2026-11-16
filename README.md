# CSE 3500 — Genetic Algorithm for TSP

A Python standard-library implementation of a genetic algorithm for the Euclidean Traveling Salesman Problem. Routes are permutations of city indices and return to their starting city.

## Run

```powershell
python genetic_algorithm.py
python genetic_algorithm.py --cities 20 --population 100 --generations 500 --mutation 0.1 --seed 3500 --output results20.csv
python -m unittest -v
```

The script prints initial and final best route distances and writes `generation,best_distance` to a CSV file. Plot this CSV in Excel (generation on X, best distance on Y) for the final report. Python 3.10+; no external dependencies.

## How it works

1. Create random valid tours (initial population).
2. Score each tour by total Euclidean length, including return to start.
3. Select parents with size-3 tournament selection.
4. Produce valid child permutations using ordered crossover (OX).
5. Apply random swap mutation at the specified per-child probability.
6. Preserve the best-so-far route (elitism), then repeat for the specified number of generations.

## Complexity

For `n` cities, `P` population size, `G` generations, and fixed tournament size, route scoring costs O(n), OX costs O(n), and one generation costs O(Pn). Total time is O(GPn) (plus initial population work); population storage is O(Pn), and history is O(G). These bounds describe computational work for fixed G, not guaranteed convergence or global optimality.

## Notes

Genetic algorithms are randomized heuristics. They do not guarantee the optimal tour. A fixed seed makes runs reproducible. Compare multiple seeds, city counts, and mutation rates; avoid drawing conclusions from one run. For the six fixed cities, compare with brute force if desired.
