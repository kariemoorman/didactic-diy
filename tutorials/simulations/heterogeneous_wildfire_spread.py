import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
import argparse


class HeterogeneousWildfireModel:
    def __init__(self, size, neighbors1=1, neighbors2=1, steps=20, p_tree1=0.6, p_tree2=0.2, p_burning=0.01):
        self.size = size
        self.neighbors1 = neighbors1
        self.neighbors2 = neighbors2
        self.steps = steps
        self.p_tree1 = p_tree1
        self.p_tree2 = p_tree2
        self.p_burning = p_burning
        self.p_empty = 1 - p_tree1 - p_tree2 - p_burning

        self.grid = np.random.choice(['empty', 'tree1', 'tree2', 'burning'], size=(size, size),
                                     p=[self.p_empty, p_tree1, p_tree2, p_burning])

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
                if self.grid[x, y] == 'tree1':
                    num_burning_neighbors = self.count_burning_neighbors(x, y)
                    if num_burning_neighbors >= self.neighbors1:
                        new_grid[x, y] = 'burning'
                elif self.grid[x, y] == 'tree2':
                    num_burning_neighbors2 = self.count_burning_neighbors(x, y)
                    if num_burning_neighbors2 >= self.neighbors2:
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
        cmap = ListedColormap(['green', 'white', 'pink'])

        plt.imshow(np.where(self.grid == 'tree1', 0, np.where(self.grid == 'tree2', 1, 2)),
                   cmap=cmap, vmin=0, vmax=2)
        plt.title(f"Wildfire Spread - Step {step}")

    def animate(self):
        fig, ax = plt.subplots()
        ani = FuncAnimation(fig, self.plot, frames=self.steps + 1, interval=500, repeat=False)
        plt.show()



def main():
    parser = argparse.ArgumentParser(description="Agent-based wildfire spread simulation.")
    parser.add_argument("--size", type=int, default=50, help="Size of the forest grid.")
    parser.add_argument("--neighbors1", "-n1", type=int, default=1, help="Number of burning neighbors for tree1.")
    parser.add_argument("--neighbors2", "-n2", type=int, default=1, help="Number of burning neighbors for tree2.")
    parser.add_argument("--steps", type=int, default=20, help="Number of time steps.")
    parser.add_argument("--p_tree1", "-t1", type=float, default=0.6, help="Probability of a cell being tree type 1.")
    parser.add_argument("--p_tree2", "-t2", type=float, default=0.2, help="Probability of a cell being tree type 2.")
    parser.add_argument("--p_burning", "-f", type=float, default=0.01, help="Probability of a cell being on fire.")
    args = parser.parse_args()

    if args.p_tree1 + args.p_tree2 + args.p_burning > 1.0:
        print("Error: The sum of probabilities for tree and burning cells cannot exceed 1.")
        return

    model = HeterogeneousWildfireModel(args.size, args.neighbors1, args.neighbors2, args.steps, args.p_tree1, args.p_tree2,
                          args.p_burning)
    model.animate()


if __name__ == "__main__":
    main()
