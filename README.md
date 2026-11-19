# Genetic Algorithm for the Traveling Salesman Problem

**CSE 3500 — Algorithms and Complexity**

## Overview

This project implements a Genetic Algorithm (GA) in Python to solve the Traveling Salesman Problem (TSP). The goal is to find a short route that visits every city exactly once and returns to the starting point.

The algorithm uses tournament selection, ordered crossover, swap mutation, and elitism to improve routes over multiple generations.

## Project Files

- `genetic_algorithm.py` — Main Genetic Algorithm implementation
- `visualize.py` — Animated visualization of the algorithm
- `test_genetic_algorithm.py` — Unit tests
- `results.csv` — Generated results from running the algorithm

## How to Run

**1. Run the Genetic Algorithm**

```bash
python genetic_algorithm.py --cities 30 --population 100 --generations 500
```

**2. Run the visualization**

Install dependencies:

```bash
python -m pip install matplotlib pillow
```

Then run:

```bash
python visualize.py --cities 30 --population 100 --generations 500
```

**3. Run the tests**

```bash
python -m unittest -v
```

## Results

In our experiments, the algorithm improved the best initial route by approximately 19%–68% across problems containing 10–50 cities.

The program outputs the shortest route found, its total distance, and the percentage improvement. It also saves generation-by-generation results to `results.csv`.

The Genetic Algorithm searches for good solutions but does not guarantee the mathematically optimal route.