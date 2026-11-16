"""Animated TSP genetic algorithm visualization. Requires matplotlib."""
import argparse
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from genetic_algorithm import CITIES, run_ga


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cities', type=int, default=30)
    parser.add_argument('--population', type=int, default=100)
    parser.add_argument('--generations', type=int, default=500)
    parser.add_argument('--mutation', type=float, default=0.1)
    parser.add_argument('--seed', type=int, default=3500)
    parser.add_argument('--step', type=int, default=5, help='Show every Nth generation')
    parser.add_argument('--save', default='', help='Optional GIF output path, e.g. demo.gif')
    args = parser.parse_args()
    if args.cities < 2 or args.step < 1:
        parser.error('--cities must be >= 2 and --step must be >= 1')
    rng = random.Random(args.seed)
    cities = CITIES[:] if args.cities == 6 else [
        (rng.uniform(0, 100), rng.uniform(0, 100)) for _ in range(args.cities)
    ]
    snapshots = []

    def capture(generation, route, distance):
        if generation == 0 or generation % args.step == 0 or generation == args.generations:
            snapshots.append((generation, route[:], distance))

    best_route, best_distance, initial, history = run_ga(
        cities, args.population, args.generations, args.mutation, args.seed,
        callback=capture
    )
    fig, (ax_route, ax_history) = plt.subplots(1, 2, figsize=(13, 6))
    fig.suptitle('Genetic Algorithm — Traveling Salesman Problem', fontsize=15)
    xs, ys = zip(*cities)
    ax_route.scatter(xs, ys, s=55, c='tab:blue', zorder=3)
    ax_route.set_title('Best Route So Far')
    ax_route.set_xlabel('X coordinate')
    ax_route.set_ylabel('Y coordinate')
    ax_route.set_aspect('equal', adjustable='datalim')
    ax_route.grid(alpha=0.2)
    (route_line,) = ax_route.plot([], [], '-', color='tab:orange', linewidth=1.8)
    info = ax_route.text(0.02, 0.98, '', transform=ax_route.transAxes,
                         va='top', bbox=dict(facecolor='white', alpha=0.85, edgecolor='none'))
    gens = [g for g, _ in history]
    distances = [d for _, d in history]
    (progress_line,) = ax_history.plot([], [], color='tab:green', linewidth=2.5,
                                      label='Progress so far')
    ax_history.set_xlim(0, max(1, args.generations))
    ax_history.set_ylim(min(distances) * 0.95, max(distances) * 1.05 if max(distances) > 0 else 1)
    ax_history.set_title('Convergence')
    ax_history.set_xlabel('Generation')
    ax_history.set_ylabel('Best route distance')
    ax_history.grid(alpha=0.25)
    ax_history.legend(loc='upper right')

    def update(frame):
        generation, route, distance = snapshots[frame]
        closed = route + [route[0]]
        route_line.set_data([cities[i][0] for i in closed], [cities[i][1] for i in closed])
        improvement = (initial - distance) / initial * 100 if initial else 0
        info.set_text(f'Generation: {generation}/{args.generations}\n'
                      f'Best distance: {distance:.2f}\n'
                      f'Improvement: {improvement:.1f}%')
        progress_line.set_data(gens[:generation + 1], distances[:generation + 1])
        return route_line, progress_line, info

    animation = FuncAnimation(fig, update, frames=len(snapshots), interval=100,
                              blit=False, repeat=False)
    plt.tight_layout()
    if args.save:
        animation.save(args.save, writer=PillowWriter(fps=10))
        print(f'Saved animation to {args.save}')
    else:
        plt.show()
    print(f'Initial: {initial:.3f}; final: {best_distance:.3f}; route: {best_route}')


if __name__ == '__main__':
    main()
