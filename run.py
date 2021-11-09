from blessed import Terminal, terminal
import random
import numpy as np
from time import sleep

# create a Terminal instance
terminal = Terminal()

# Constants for the grid colors and dimensions
WALL = "⬜️"
PATH = "🟦"
VISITED = "🟩"
ACTIVE = "🟨"
START = "🧐"
END = "🏁"
EMPTY = "　"

WIDTH = 41
HEIGHT = 31

class Node:
    """
    Class that represents every cell on the grid.
    """
    
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = EMPTY
        self.neighbors = []
        self.visited = False
        self.passage = False
        self.distance = float('inf')
        self.previous = None
        
    def __str__(self):
        return self.color
    
    def get_position(self):
        return self.row, self.col
    
    def update_neighbors(self, grid):
        self.neighbors = []
        row, col = self.get_position()
        # Node to the top of the current node
        if row > 0 and not grid[row - 1][col].is_wall():
            self.neighbors.append(grid[row - 1][col])
        # Node to the bottom of the current node
        if row < HEIGHT - 1 and not grid[row + 1][col].is_wall():
            self.neighbors.append(grid[row + 1][col])
        # Node to the left of the current node
        if col > 0 and not grid[row][col - 1].is_wall():
            self.neighbors.append(grid[row][col - 1])
        # Node to the right of the current node
        if col < WIDTH - 1 and not grid[row][col + 1].is_wall():
            self.neighbors.append(grid[row][col + 1])
    
    def is_end(self):
        return self.color == END
    
    def is_start(self):
        return self.color == START
    
    def is_wall(self):
        return self.color == WALL
    
    def is_empty(self):
        return self.color == EMPTY
    
    def is_visited(self):
        return self.visited
    
    def is_passage(self):
        return self.passage
    
    def make_start(self):
        self.color = START
        
    def make_end(self):
        self.color = END
        
    def make_wall(self):
        self.color = WALL
        
    def make_empty(self):
        self.color = EMPTY
        
    def make_visited(self):
        self.visited = True
        
    def make_active(self):
        self.color = ACTIVE
        
    def make_passage(self):
        self.passage = True
        self.color = EMPTY
    
    def make_path(self):
        self.color = PATH
        
    def reset(self):
        self.color = EMPTY
        self.visited = False
        self.passage = False
        self.distance = float('inf')
        self.previous = None
        
def generate_horizontal_maze(grid):
    """
    Generates a maze with horizontal walls with random passages
    """
    for row in range(2, HEIGHT - 2, 2):
        skip = random.randint(1, WIDTH - 1)
        for col in range(1, WIDTH - 1):
            if col == skip:
                continue
            grid[row][col].make_wall()
            
def generate_vertical_maze(grid):
    """
    Generates a maze with vertical walls with random passages
    """
    for col in range(2, WIDTH - 2, 2):
        skip = random.randint(1, HEIGHT - 1)
        for i in range(1, HEIGHT - 1):
            grid[:, col][i].make_wall()
        grid[:, col][skip].reset()