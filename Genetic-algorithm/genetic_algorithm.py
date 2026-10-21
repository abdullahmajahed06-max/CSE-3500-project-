"""CSE 3500: Genetic Algorithm for TSP — initial implementation."""
import math
import random

# Example cities with (x, y) coordinates.
CITIES = [(0, 0), (2, 6), (5, 2), (7, 8), (9, 3), (4, 9)]


def generate_route(num_cities, rng):
    """Return a random route visiting each city index exactly once."""
    route = list(range(num_cities))
    rng.shuffle(route)
    return route


def route_distance(route, cities):
    """Calculate tour distance, including return to the starting city."""
    if len(route) != len(cities) or sorted(route) != list(range(len(cities))):
        raise ValueError('Route must contain each city exactly once')
    return sum(math.dist(cities[route[i]], cities[route[(i + 1) % len(route)]])
               for i in range(len(route)))


def initial_population(population_size, cities, rng):
    """Create random candidate TSP tours."""
    if population_size <= 0 or not cities:
        raise ValueError('Population size and number of cities must be positive')
    return [generate_route(len(cities), rng) for _ in range(population_size)]


def main():
    rng = random.Random(3500)  # Fixed seed makes results reproducible.
    population = initial_population(10, CITIES, rng)
    scored = [(route_distance(route, CITIES), route) for route in population]
    for i, (distance, route) in enumerate(scored, 1):
        print(f'Route {i:2d}: {route} | Distance: {distance:.2f}')
    best_distance, best_route = min(scored)
    print(f'\nBest initial route: {best_route}')
    print(f'Best initial distance: {best_distance:.2f}')


if __name__ == '__main__':
    main()
