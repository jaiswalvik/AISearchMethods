import sys
import itertools

def read_input():
    # Read problem type
    tsp_type = sys.stdin.readline().strip()
    
    # Read number of cities
    N = int(sys.stdin.readline().strip())
    
    # Read coordinates (not used in computation, just for display)
    coordinates = [tuple(map(float, sys.stdin.readline().split())) for _ in range(N)]
    
    # Read distance matrix
    distance_matrix = []
    for _ in range(N):
        row = list(map(float, sys.stdin.readline().split()))
        distance_matrix.append(row)
    
    return tsp_type, N, coordinates, distance_matrix

def tsp_nearest_neighbor(N, distance_matrix):
    """ Solves TSP using Nearest Neighbor Heuristic for large N """
    unvisited = set(range(1, N))
    tour = [0]  # Start from city 0

    while unvisited:
        last = tour[-1]
        next_city = min(unvisited, key=lambda city: distance_matrix[last][city])
        tour.append(next_city)
        unvisited.remove(next_city)

    return tour

def solve_tsp():
    tsp_type, N, coordinates, distance_matrix = read_input()

    best_tour = tsp_nearest_neighbor(N, distance_matrix)

    print(" ".join(map(str, best_tour)))

if __name__ == "__main__":
    solve_tsp()
