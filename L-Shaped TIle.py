import numpy as np
import matplotlib.pyplot as plt
import random

# Function to initialize the grid
def initialize_grid(n):
    grid_size = 2**n
    grid = np.zeros((grid_size, grid_size), dtype=int)
    x, y = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
    grid[x][y] = 1  # Mark the removed grid
    return grid, (x, y)

class LTilingGameLShape:
    def __init__(self, grid):
        self.grid = grid
        self.fig, self.ax = plt.subplots(figsize=(8,8))
        self.tile_counter = 2  # Start from 2 as 1 is used for the removed grid
        self.center_point = None
        self.orientation = 0
        self.description = (
            "Fill the floor with L-shaped tiles.\n"
            "Left-click: select tile center.\n"
            "Right-click: choose orientation.\n"
            "Enter: place tile. R: remove tile.\n"  # Added instruction for removing a tile
            "Good luck!"
        )
        self.ax.set_title(self.description, fontsize=9, loc='left', wrap=True)

    def is_valid_tile_placement(self, center, orientation):
        x, y = center
        offsets = [
            [(0, -1), (-1, 0), (0, 0)],  
            [(-1, 0), (0, 1), (0, 0)],   
            [(0, 1), (1, 0), (0, 0)],    
            [(1, 0), (0, -1), (0, 0)]    
        ]
        cells = [(x + dx, y + dy) for dx, dy in offsets[orientation]]
        return all(0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]) and self.grid[x][y] == 0 for x, y in cells)

    def place_tile(self, center, orientation):
        x, y = center
        offsets = [
            [(0, -1), (-1, 0), (0, 0)],
            [(-1, 0), (0, 1), (0, 0)],
            [(0, 1), (1, 0), (0, 0)],
            [(1, 0), (0, -1), (0, 0)]
        ]
        cells = [(x + dx, y + dy) for dx, dy in offsets[orientation]]
        for x, y in cells:
            self.grid[x][y] = self.tile_counter
        self.tile_counter += 1

        # Check if the player has succeeded
        if np.all(self.grid != 0):
            print("Congratulations! You've successfully tiled the entire grid!")

    def remove_tile(self):
        # Removing the last placed tile
        last_tile = np.max(self.grid)
        if last_tile > 1:  # Ensure not to remove the initial removed grid
            self.grid[self.grid == last_tile] = 0
            self.tile_counter -= 1
            self.draw_grid()

    def on_click(self, event):
        if event.xdata is not None and event.ydata is not None:
            x, y = int(event.ydata), int(event.xdata)

            if event.button == 1:
                if self.grid[x][y] == 0:
                    self.center_point = (x, y)
                    self.orientation = 0
                    self.draw_grid(highlight_center=True)
            elif event.button == 3 and self.center_point is not None:
                self.orientation = (self.orientation + 1) % 4
                self.draw_grid(highlight_center=True)

    def on_key(self, event):
        if event.key == 'enter' and self.center_point is not None:
            if self.is_valid_tile_placement(self.center_point, self.orientation):
                self.place_tile(self.center_point, self.orientation)
                self.center_point = None
                self.orientation = 0
            self.draw_grid()
        elif event.key == 'r':
            self.remove_tile()

    def draw_grid(self, highlight_center=False):
        self.ax.clear()
        self.ax.imshow(self.grid, cmap='tab20c', vmin=0, vmax=20, extent=[0, len(self.grid), len(self.grid), 0])
        self.ax.set_title(self.description, fontsize=9, loc='left', wrap=True)

        for i in range(len(self.grid) + 1):
            self.ax.axhline(i, color='white', linewidth=0.5)
            self.ax.axvline(i, color='white', linewidth=0.5)

        if highlight_center and self.center_point is not None:
            self.ax.plot(self.center_point[1]+0.5, self.center_point[0]+0.5, 'ro')
            x, y = self.center_point
            offsets = [
                [(0, -1), (-1, 0), (0, 0)],
                [(-1, 0), (0, 1), (0, 0)],
                [(0, 1), (1, 0), (0, 0)],
                [(1, 0), (0, -1), (0, 0)]
            ]
            for dx, dy in offsets[self.orientation]:
                self.ax.plot(y + dy + 0.5, x + dx + 0.5, 'bs', fillstyle='none', markersize=10)
                self.ax.plot([y+0.5, y+dy+0.5], [x+0.5, x+dx+0.5], 'b--')

        plt.draw()

    def start(self):
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.draw_grid()
        plt.show()

# Adjusting grid to 8x8 and randomizing the removed grid
n = 3  
grid, empty_tile_position = initialize_grid(n)
print(f"Removed grid position: {empty_tile_position}")

# Start the L-shape game with the updated grid size and randomized removed grid
lshape_game = LTilingGameLShape(grid)
lshape_game.start()
