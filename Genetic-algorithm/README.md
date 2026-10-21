# CSE 3500 — Genetic Algorithm Project

## Project Overview
This project focuses on implementing a Genetic Algorithm to solve the Traveling Salesman Problem (TSP). The goal is to find a short route that visits every city once and returns to the starting city.

## Current Implementation
So far, we have implemented the initial population generation using Python. The program:
- Generates random routes between cities.
- Calculates the total distance of each route.
- Identifies the shortest route in the initial population.

## Testing
The program was tested in VS Code and successfully generated routes, calculated their distances, and identified the shortest route from the initial population.

## Next Steps
- Implement tournament selection to choose better routes.
- Implement crossover to combine parent routes.
- Implement mutation to introduce variation.
- Test the completed algorithm with different population sizes and numbers of cities.
- Analyze the time complexity and compare performance with other approaches.

## How to Run
1. Make sure Python is installed.
2. Clone or download this repository.
3. Open the project folder in VS Code.
4. Run the following command in the terminal:

`python genetic_algorithm.py`
