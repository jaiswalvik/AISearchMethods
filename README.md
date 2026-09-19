# 🧭 Traveling Salesman Problem (TSP) Solver

This project explores algorithms for solving the **Traveling Salesman Problem (TSP)**, a classic combinatorial optimization problem.

The objective of the TSP is to find a tour that:

* Starts at a city
* Visits every city exactly once
* Returns to the starting city
* Minimizes the total travel distance

This project currently implements:

1. **Nearest Neighbor Heuristic**
2. **Ant Colony Optimization (ACO)**

The project is intended as an exploration of **Artificial Intelligence search and optimization methods**.

---

## 📋 Problem Description

Given:

* A list of `N` cities
* 2D coordinates for each city
* A full distance matrix between all pairs of cities

The program searches for a good TSP tour.

For a tour such as:

```text
0 → 3 → 4 → 1 → 2 → 0
```

the total tour length is:

```text
distance(0,3)
+ distance(3,4)
+ distance(4,1)
+ distance(1,2)
+ distance(2,0)
```

### Important

The TSP is computationally difficult as the number of cities increases.

The algorithms in this project are **heuristic methods**. They aim to find good solutions efficiently but do **not necessarily guarantee the globally optimal tour** for large problems.

---

# 📥 Input Format

The program reads input from **standard input**.

The input has the following structure:

```text
TSP_TYPE
N
coordinates
distance_matrix
```

### 1. Problem type

The first line specifies the type of TSP:

```text
EUCLIDEAN
```

or

```text
NON-EUCLIDEAN
```

### 2. Number of cities

The second line contains the number of cities:

```text
N
```

### 3. Coordinates

The next `N` lines contain the coordinates of each city:

```text
x y
```

The coordinates are currently read by the program but are not used directly by the optimization algorithms because the distance matrix is provided separately.

### 4. Distance matrix

The next `N` lines contain the distance between every pair of cities.

Each row contains `N` floating-point values.

---

## 🔹 Example Input

```text
EUCLIDEAN
5
10.391379 8.405525
14.780237 7.036543
1.511838 6.366090
9.276912 5.418818
11.376465 4.216809
0.0 4.597411 9.110738 3.187861 4.302992
4.597411 0.0 13.285327 5.736168 4.420019
9.110738 13.285327 0.0 7.822640 10.096052
3.187861 5.736168 7.822640 0.0 2.419287
4.302992 4.420019 10.096052 2.419287 0.0
```

---

# 📤 Output Format

The program outputs a tour as a sequence of **zero-based city indices**.

For example:

```text
0 3 4 1 2
```

represents the closed tour:

```text
0 → 3 → 4 → 1 → 2 → 0
```

The final return to the starting city is implicit and is included when calculating the total tour length.

---

# 🧠 Algorithms

## 1. Nearest Neighbor Heuristic

The Nearest Neighbor algorithm is a simple greedy approach.

Starting from a city, it repeatedly chooses the **closest unvisited city**.

For example:

```text
Current city
     ↓
Find closest unvisited city
     ↓
Move there
     ↓
Repeat
```

### Characteristics

* Simple to implement
* Very fast
* Easy to understand
* Useful for generating an initial solution
* Does not guarantee the optimal solution

The main decision is:

```python
next_city = min(
    unvisited,
    key=lambda city: distance_matrix[last][city]
)
```

---

# 🐜 2. Ant Colony Optimization (ACO)

Ant Colony Optimization is a **swarm intelligence** algorithm inspired by the behavior of real ants searching for food.

The central idea is that many simple agents can collectively discover good solutions through **local decisions and shared information**.

### Basic concept

Artificial ants construct TSP tours.

Each ant considers:

* The distance to possible next cities
* The amount of pheromone on the corresponding edge

Good tours contribute more pheromone, making their edges more attractive to future ants.

The process is repeated over multiple iterations.

```text
Initialize pheromone
        ↓
Create ants
        ↓
Each ant constructs a tour
        ↓
Calculate tour length
        ↓
Evaporate pheromone
        ↓
Deposit new pheromone
        ↓
Repeat
        ↓
Return best tour found
```

---

## 🔬 How ACO Makes Decisions

For an ant travelling from city `i` to city `j`, the probability of selecting city `j` depends on pheromone and distance.

The basic probability rule is:

$$
P_{ij} =
\frac{
\tau_{ij}^{\alpha}\eta_{ij}^{\beta}
}{
\sum_{k \in allowed}
\tau_{ik}^{\alpha}\eta_{ik}^{\beta}
}
$$

where:

* `τᵢⱼ` = pheromone level on edge `i → j`
* `ηᵢⱼ` = heuristic information, usually `1 / distance`
* `α` = importance of pheromone
* `β` = importance of distance

### Parameters

The current implementation uses:

```text
num_ants = 50
num_iterations = 200
alpha = 1.0
beta = 5.0
evaporation_rate = 0.5
```

These parameters can be changed to experiment with the behavior and performance of the algorithm.

---

## 💧 Pheromone Evaporation

Pheromone gradually evaporates after each iteration.

Conceptually:

$$
\tau_{ij} \leftarrow (1-\rho)\tau_{ij}
$$

where `ρ` is the evaporation rate.

Evaporation prevents old information from dominating the search forever and allows the ants to continue exploring alternative routes.

---

## 🐜 Pheromone Deposit

After the ants complete their tours, pheromone is deposited on the edges they used.

A shorter tour contributes more pheromone.

The implementation uses the basic relationship:

$$
\Delta\tau \propto \frac{1}{L}
$$

where `L` is the total length of the tour.

Therefore:

```text
Shorter tour
     ↓
More pheromone
     ↓
Higher probability of selecting those edges
```

This creates a feedback mechanism through which good solutions can become increasingly influential.

---

# 🎲 Why Can ACO Produce Different Answers?

Unlike the Nearest Neighbor algorithm, ACO uses **probabilistic decisions** when ants select their next cities.

Therefore, running the same input multiple times can produce different tours.

For example:

```text
Run 1:
0 3 4 1 2

Run 2:
0 2 1 4 3
```

Different tours are not necessarily an error.

The important comparison is the **total tour length**.

Because ACO is a stochastic heuristic, different runs may find different solutions.

For reproducible experiments, a fixed random seed can be used.

---

# ⚙️ Computational Considerations

ACO requires considerably more computation than the Nearest Neighbor heuristic.

The basic implementation repeatedly performs:

```text
iterations × ants × city-selection calculations
```

Therefore, increasing:

```text
N
num_ants
num_iterations
```

can significantly increase execution time.

For large TSP instances, reducing the number of ants or iterations can make experimentation faster.

---

# 📊 Nearest Neighbor vs. ACO

| Property                     | Nearest Neighbor    | Ant Colony Optimization           |
| ---------------------------- | ------------------- | --------------------------------- |
| Approach                     | Greedy              | Swarm-based optimization          |
| Randomness                   | No                  | Yes                               |
| Uses pheromone               | No                  | Yes                               |
| Multiple candidate solutions | No                  | Yes                               |
| Computational cost           | Low                 | Higher                            |
| Usually deterministic        | Yes                 | No                                |
| Guarantees optimal solution  | No                  | No                                |
| Main idea                    | Choose nearest city | Learn from collective exploration |

---

# 🚀 Running the Program

The program reads from standard input.

For example:

```bash
python tsp.py < input.txt
```

For the ACO implementation:

```bash
python aco_tsp.py < input.txt
```

The exact filename depends on the implementation being used.

---

# 📚 Learning Objectives

This project is also intended as a practical introduction to concepts in Artificial Intelligence and optimization, including:

* Heuristic search
* Combinatorial optimization
* Greedy algorithms
* Swarm intelligence
* Emergent behavior
* Probabilistic search
* Exploration vs. exploitation
* Distributed decision making
* Pheromone-based communication
* Optimization under computational constraints

---

# 🔭 Possible Future Improvements

Possible extensions include:

* Compare Nearest Neighbor and ACO on the same datasets
* Experiment with different ACO parameters
* Add random starting cities
* Implement elitist pheromone updates
* Add candidate lists for large TSP instances
* Implement **2-opt local search**
* Compare ACO with other optimization algorithms
* Visualize the tours and pheromone trails
* Measure convergence across iterations
* Run multiple ACO experiments and analyze statistical performance

---

## 📌 Project Status

This project is being developed as an exploration of **AI search methods and optimization techniques for the Traveling Salesman Problem**.

The current focus is on understanding and implementing heuristic and swarm-intelligence approaches rather than guaranteeing an exact optimal solution.