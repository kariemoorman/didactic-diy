#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
import argparse


class HomogeneousWildfireModel:
    def __init__(self, size, neighbors=1, steps=20, p_tree=0.6, p_burning=0.01):
        self.size = size
        self.neighbors = neighbors
        self.steps = steps
        self.p_tree = p_tree
        self.p_burning = p_burning
        self.p_empty = 1 - p_tree - p_burning
        self.grid = np.random.choice(['empty', 'tree', 'burning'], size=(size, size),
                                     p=[self.p_empty, p_tree, p_burning])

        # Set a random cell on fire to start the wildfire
        x, y = np.random.randint(0, size), np.random.randint(0, size)
        self.grid[x, y] = 'burning'

    def count_burning_neighbors(self, x, y):
        neighbors = self.get_neighbors(x, y)
        count = sum(1 for i, j in neighbors if self.grid[i, j] == 'burning')
        return count

    def spread_fire(self):
        new_grid = np.copy(self.grid)

        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x, y] == 'tree':
                    num_burning_neighbors = self.count_burning_neighbors(x, y)
                    if num_burning_neighbors >= self.neighbors:
                        new_grid[x, y] = 'burning'

        self.grid = new_grid

    def get_neighbors(self, x, y):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    neighbors.append((nx, ny))
        return neighbors

    def plot(self, step):
        plt.cla()  # Clear the current plot
        if step < self.steps:
            self.spread_fire()

        # Define custom colormap for tree and burning cells
        cmap = ListedColormap(['green', 'pink'])

        plt.imshow(np.where(self.grid == 'tree', 0, 1), cmap=cmap, vmin=0, vmax=1)
        plt.title(f"Wildfire Spread - Step {step}")

    def animate(self):
        fig, ax = plt.subplots()
        ani = FuncAnimation(fig, self.plot, frames=self.steps + 1, interval=500, repeat=False)
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="Agent-based wildfire spread simulation.")
    parser.add_argument("--size", type=int, default=50, help="Size of the forest grid.")
    parser.add_argument("--neighbors", "-n", type=int, default=1, help="Number of burning neighbors.")
    parser.add_argument("--steps", type=int, default=20, help="Number of time steps.")
    parser.add_argument("--p_tree", "-t", type=float, default=0.6, help="Probability of a cell being a tree.")
    parser.add_argument("--p_burning", "-f", type=float, default=0.01, help="Probability of a cell being on fire.")
    args = parser.parse_args()

    if args.p_tree + args.p_burning > 1.0:
        print("Error: The sum of probabilities for tree and burning cells cannot exceed 1.")
        return

    model = HomogeneousWildfireModel(args.size, args.neighbors, args.steps, args.p_tree, args.p_burning)
    model.animate()


if __name__ == "__main__":
    main()
