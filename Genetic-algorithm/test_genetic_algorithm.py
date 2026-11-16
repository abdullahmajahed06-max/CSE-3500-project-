import random
import unittest
from genetic_algorithm import CITIES, initial_population, ordered_crossover, mutate_swap, route_distance, run_ga

class Tests(unittest.TestCase):
    def test_routes_valid(self):
        for route in initial_population(50, len(CITIES), random.Random(1)):
            self.assertEqual(sorted(route), list(range(len(CITIES))))
    def test_distance_square(self):
        self.assertAlmostEqual(route_distance([0, 1, 2, 3], [(0,0),(1,0),(1,1),(0,1)]), 4)
    def test_crossover_valid(self):
        rng = random.Random(2)
        for _ in range(100):
            child = ordered_crossover([0,1,2,3,4,5], [5,4,3,2,1,0], rng)
            self.assertEqual(sorted(child), list(range(6)))
    def test_mutation_valid(self):
        rng = random.Random(3)
        for _ in range(100):
            self.assertEqual(sorted(mutate_swap(list(range(6)), 1, rng)), list(range(6)))
    def test_ga_improvement(self):
        route, final, initial, history = run_ga(CITIES, population_size=30, generations=60)
        self.assertEqual(sorted(route), list(range(len(CITIES))))
        self.assertLessEqual(final, initial)
        self.assertTrue(all(history[i][1] >= history[i+1][1] for i in range(len(history)-1)))

if __name__ == '__main__':
    unittest.main()
