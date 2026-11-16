
"""CSE 3500 — Genetic Algorithm for the Traveling Salesman Problem."""

import argparse
import csv
import math
import random
from pathlib import Path

CITIES = [(0, 0), (2, 6), (5, 2), (7, 8), (9, 3), (4, 9)]


def route_distance(route, cities):
    if len(route) != len(cities) or sorted(route) != list(range(len(cities))):
        raise ValueError("Route must visit every city exactly once")

    return sum(
        math.dist(cities[route[i]], cities[route[(i + 1) % len(route)]])
        for i in range(len(route))
    )


def initial_population(size, n, rng):
    if size < 2 or n < 2:
        raise ValueError("Need at least two individuals and two cities")

    population = []

    for _ in range(size):
        route = list(range(n))
        rng.shuffle(route)
        population.append(route)

    return population


def tournament_selection(population, distances, rng, tournament_size=3):
    indices = rng.sample(
        range(len(population)),
        min(tournament_size, len(population))
    )

    return population[min(indices, key=lambda i: distances[i])][:]


def ordered_crossover(parent1, parent2, rng):
    """Ordered crossover: combine parents while preserving valid city routes."""

    n = len(parent1)
    a, b = sorted(rng.sample(range(n), 2))

    child = [None] * n
    child[a:b + 1] = parent1[a:b + 1]

    used = set(child[a:b + 1])

    fill = [
        city
        for city in (parent2[(b + 1 + k) % n] for k in range(n))
        if city not in used
    ]

    positions = [
        (b + 1 + k) % n
        for k in range(n)
        if not (a <= (b + 1 + k) % n <= b)
    ]

    for position, city in zip(positions, fill):
        child[position] = city

    return child


def mutate_swap(route, rate, rng):
    """Randomly swap two cities based on the mutation rate."""

    route = route[:]

    if rng.random() < rate:
        i, j = rng.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]

    return route


def run_ga(
    cities,
    population_size=100,
    generations=300,
    mutation_rate=0.1,
    seed=3500,
    callback=None
):
    """Run the Genetic Algorithm and optionally report each generation."""

    if not 0 <= mutation_rate <= 1 or generations < 0:
        raise ValueError(
            "Mutation rate must be 0..1; generations must be nonnegative"
        )

    rng = random.Random(seed)

    # Step 1: Create the initial population
    population = initial_population(
        population_size,
        len(cities),
        rng
    )

    # Step 2: Evaluate initial fitness
    distances = [
        route_distance(route, cities)
        for route in population
    ]

    best_index = min(
        range(len(population)),
        key=lambda i: distances[i]
    )

    best_route = population[best_index][:]
    best_distance = distances[best_index]
    initial_best = best_distance

    history = [(0, best_distance)]

    # Send initial route to visualization
    if callback is not None:
        callback(0, best_route[:], best_distance)

    # Step 3: Evolve over multiple generations
    for generation in range(1, generations + 1):

        # Elitism: preserve the best solution
        new_population = [best_route[:]]

        while len(new_population) < population_size:

            # Selection
            parent1 = tournament_selection(
                population, distances, rng
            )
            parent2 = tournament_selection(
                population, distances, rng
            )

            # Crossover
            child = ordered_crossover(
                parent1, parent2, rng
            )

            # Mutation
            child = mutate_swap(
                child, mutation_rate, rng
            )

            new_population.append(child)

        population = new_population

        # Evaluate the new generation
        distances = [
            route_distance(route, cities)
            for route in population
        ]

        index = min(
            range(len(population)),
            key=lambda i: distances[i]
        )

        if distances[index] < best_distance:
            best_distance = distances[index]
            best_route = population[index][:]

        history.append((generation, best_distance))

        # Send current best route to visualization
        if callback is not None:
            callback(
                generation,
                best_route[:],
                best_distance
            )

    return best_route, best_distance, initial_best, history


def main():
    parser = argparse.ArgumentParser(
        description="Genetic Algorithm for Traveling Salesman Problem"
    )

    parser.add_argument("--cities", type=int, default=6)
    parser.add_argument("--population", type=int, default=100)
    parser.add_argument("--generations", type=int, default=300)
    parser.add_argument("--mutation", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=3500)
    parser.add_argument("--output", default="results.csv")

    args = parser.parse_args()

    rng = random.Random(args.seed)

    if args.cities == 6:
        cities = CITIES[:]
    else:
        cities = [
            (rng.uniform(0, 100), rng.uniform(0, 100))
            for _ in range(args.cities)
        ]

    route, distance, initial, history = run_ga(
        cities,
        population_size=args.population,
        generations=args.generations,
        mutation_rate=args.mutation,
        seed=args.seed
    )

    print(
        f"Cities: {len(cities)} | "
        f"Population: {args.population} | "
        f"Generations: {args.generations}"
    )

    print(f"Initial best distance: {initial:.3f}")
    print(f"Final best distance:   {distance:.3f}")

    print(
        f"Improvement: "
        f"{(initial - distance) / initial * 100:.2f}%"
    )

    print(
        f"Best route: {route} "
        f"(return to {route[0]})"
    )

    with Path(args.output).open(
        "w", newline="", encoding="utf-8"
    ) as file:

        writer = csv.writer(file)
        writer.writerow(["generation", "best_distance"])
        writer.writerows(history)

    print(f"History saved to {args.output}")


if __name__ == "__main__":
    main()
