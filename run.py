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