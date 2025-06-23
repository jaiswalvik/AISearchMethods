# 🧭 Traveling Salesman Problem (TSP) Solver

This project implements a solver for the **Traveling Salesman Problem (TSP)** — a classic combinatorial optimization problem. The goal is to find the **shortest possible route** that visits each city **exactly once** and returns to the starting city.

---

## 📋 Problem Description

Given:
- A list of `N` cities
- 2D coordinates of each city
- A full distance matrix between all pairs of cities

Your task is to compute the shortest tour that:
- Starts at any city
- Visits each city exactly once
- Returns to the starting point

---

## 📥 Input Format

Your program must read from **standard input** with the following structure:

First line: EUCLIDEAN or NON-EUCLIDEAN
Second line: Integer N (number of cities)
Next N lines: 2D coordinates (used only for display)
Next N lines: N space-separated floats — distance matrix


### 🔹 Example Input
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

---

## 📤 Output Format

The output is written to **standard output** as:

- A single line per tour (in path representation)
- City indices are **zero-based** (`0` to `N-1`)
- Each line is a valid complete tour

### 🔹 Example Output

1 2 4 0 3
0 1 3 4 2
4 3 2 0 1
