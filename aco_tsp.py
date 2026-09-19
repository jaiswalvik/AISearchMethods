import sys
import random


def read_input():
    # Read problem type
    tsp_type = sys.stdin.readline().strip()

    # Read number of cities
    N = int(sys.stdin.readline().strip())

    # Read coordinates
    coordinates = [
        tuple(map(float, sys.stdin.readline().split()))
        for _ in range(N)
    ]

    # Read distance matrix
    distance_matrix = []

    for _ in range(N):
        row = list(map(float, sys.stdin.readline().split()))
        distance_matrix.append(row)

    return tsp_type, N, coordinates, distance_matrix


def tour_length(tour, distance_matrix):
    """
    Calculate the total length of a TSP tour.

    The tour is closed by returning from the last city
    back to the starting city.
    """

    total = 0.0

    for i in range(len(tour) - 1):
        total += distance_matrix[tour[i]][tour[i + 1]]

    # Return to the starting city
    total += distance_matrix[tour[-1]][tour[0]]

    return total


def choose_next_city(
    current_city,
    unvisited,
    pheromone,
    distance_matrix,
    alpha,
    beta
):
    """
    Choose the next city for an ant using the ACO probability rule.

    alpha = importance of pheromone
    beta  = importance of distance
    """

    probabilities = []
    total_probability = 0.0

    for city in unvisited:

        # Pheromone level on the edge
        pheromone_value = pheromone[current_city][city]

        # Prefer shorter distances
        distance = distance_matrix[current_city][city]

        if distance == 0:
            heuristic_value = 0
        else:
            heuristic_value = 1.0 / distance

        # ACO attractiveness formula
        attractiveness = (
            (pheromone_value ** alpha)
            * (heuristic_value ** beta)
        )

        probabilities.append((city, attractiveness))
        total_probability += attractiveness

    # Safety check
    if total_probability == 0:
        return random.choice(list(unvisited))

    # Convert attractiveness values into probabilities
    probabilities = [
        (city, value / total_probability)
        for city, value in probabilities
    ]

    # Roulette-wheel selection
    random_value = random.random()
    cumulative_probability = 0.0

    for city, probability in probabilities:
        cumulative_probability += probability

        if random_value <= cumulative_probability:
            return city

    # Fallback because of floating-point rounding
    return probabilities[-1][0]


def construct_tour(
    start_city,
    N,
    pheromone,
    distance_matrix,
    alpha,
    beta
):
    """
    Construct one complete tour for a single ant.
    """

    tour = [start_city]

    unvisited = set(range(N))
    unvisited.remove(start_city)

    current_city = start_city

    while unvisited:

        next_city = choose_next_city(
            current_city,
            unvisited,
            pheromone,
            distance_matrix,
            alpha,
            beta
        )

        tour.append(next_city)
        unvisited.remove(next_city)

        current_city = next_city

    return tour


def evaporate_pheromone(pheromone, evaporation_rate):
    """
    Reduce pheromone on every edge.

    evaporation_rate = rho
    """

    N = len(pheromone)

    for i in range(N):
        for j in range(N):

            pheromone[i][j] *= (1.0 - evaporation_rate)

            # Prevent pheromone from becoming exactly zero
            if pheromone[i][j] < 0.0001:
                pheromone[i][j] = 0.0001


def deposit_pheromone(
    pheromone,
    tours,
    tour_lengths
):
    """
    Deposit pheromone based on the quality of each ant's tour.

    Shorter tours deposit more pheromone.
    """

    for tour, length in zip(tours, tour_lengths):

        # Better tour -> more pheromone
        pheromone_amount = 1.0 / length

        for i in range(len(tour)):

            city_a = tour[i]
            city_b = tour[(i + 1) % len(tour)]

            # Because TSP is normally symmetric,
            # update both directions.
            pheromone[city_a][city_b] += pheromone_amount
            pheromone[city_b][city_a] += pheromone_amount


def ant_colony_optimization(
    N,
    distance_matrix,
    num_ants=50,
    num_iterations=200,
    alpha=1.0,
    beta=5.0,
    evaporation_rate=0.5
):
    """
    Solve TSP using Ant Colony Optimization.
    """

    # --------------------------------------------------
    # 1. Initialize pheromone
    # --------------------------------------------------

    pheromone = [
        [1.0 for _ in range(N)]
        for _ in range(N)
    ]

    # --------------------------------------------------
    # 2. Store the best solution found so far
    # --------------------------------------------------

    best_tour = None
    best_length = float("inf")

    # --------------------------------------------------
    # 3. Main ACO loop
    # --------------------------------------------------

    for iteration in range(num_iterations):

        tours = []
        tour_lengths = []

        # --------------------------------------------------
        # 4. Each ant constructs a complete tour
        # --------------------------------------------------

        for ant in range(num_ants):

            # Start every ant from city 0
            start_city = 0

            tour = construct_tour(
                start_city,
                N,
                pheromone,
                distance_matrix,
                alpha,
                beta
            )

            length = tour_length(
                tour,
                distance_matrix
            )

            tours.append(tour)
            tour_lengths.append(length)

            # --------------------------------------------------
            # 5. Update global best solution
            # --------------------------------------------------

            if length < best_length:
                best_length = length
                best_tour = tour.copy()

        # --------------------------------------------------
        # 6. Evaporate old pheromone
        # --------------------------------------------------

        evaporate_pheromone(
            pheromone,
            evaporation_rate
        )

        # --------------------------------------------------
        # 7. Add new pheromone
        # --------------------------------------------------

        deposit_pheromone(
            pheromone,
            tours,
            tour_lengths
        )

    return best_tour, best_length


def solve_tsp():

    tsp_type, N, coordinates, distance_matrix = read_input()

    best_tour, best_length = ant_colony_optimization(
        N,
        distance_matrix,

        # Number of ants
        num_ants=50,

        # Number of generations
        num_iterations=200,

        # Importance of pheromone
        alpha=1.0,

        # Importance of distance
        beta=5.0,

        # Pheromone evaporation rate
        evaporation_rate=0.5
    )

    # Keep the same output format as your original program
    print(" ".join(map(str, best_tour)))


if __name__ == "__main__":
    solve_tsp()