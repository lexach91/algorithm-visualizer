"""
Module for the Node class.
"""
from constants import (
    WIDTH,
    HEIGHT,
    START,
    END,
    WALL,
    EMPTY,
    PATH,
    VISITED,
    ACTIVE
)

class Node:
    """
    Class that represents every cell on the grid.
    """

    def __init__(self, row, col):
        # Row and column position of the node
        self.row = row
        self.col = col
        # Color (state) of the node. Node is empty by default.
        self.color = EMPTY
        # Empty list to store neighbors of the node in the future.
        self.neighbors = []
        # Distance from the start node to the current node.
        # Infinity by default. Used in all pathfinding algorithms.
        self.distance = float("inf")
        # Variable to store the previous node in the path.
        # Used in all pathfinding algorithms.
        self.previous = None
        # Variable to store the next node in the path.
        # Used in bidirectional BFS.
        self.next = None
        # Variable to store the manhattan distance to the end node.
        # Used in A* algorithm.
        self.manhattan_distance = float("inf")
        # Variable to store the total cost of traveling through this node.
        # Used in A* algorithm.
        self.total_cost = float("inf")

    def __str__(self):
        # Need this method to print the node.
        return self.color

    def get_position(self):
        """
        Returns the position of the node as a tuple.
        """
        return self.row, self.col

    def update_neighbors(self, grid):
        """
        Updates the neighbors of the current node skipping the walls.
        """
        # reset the neighbors list
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
        """
        Returns True if the node is the end node.
        """
        return self.color == END

    def is_start(self):
        """
        Returns True if the node is the start node.
        """
        return self.color == START

    def is_wall(self):
        """
        Returns True if the node is a wall.
        """
        return self.color == WALL

    def is_empty(self):
        """
        Returns True if the node is empty.
        """
        return self.color == EMPTY

    def is_visited(self):
        """
        Returns True if the node has been visited.
        """
        return self.color == VISITED

    def is_path(self):
        """
        Returns True if the node is a path.
        """
        return self.color == PATH

    def is_active(self):
        """
        Returns True if the node is the active node.
        """
        return self.color == ACTIVE

    def make_start(self):
        """
        Makes the node the start node.
        """
        self.color = START

    def make_end(self):
        """
        Makes the node the end node.
        """
        self.color = END

    def make_wall(self):
        """
        Makes the node a wall.
        """
        self.color = WALL

    def make_empty(self):
        """
        Makes the node empty.
        """
        self.color = EMPTY

    def make_visited(self):
        """
        Makes the node visited.
        """
        self.color = VISITED

    def make_active(self):
        """
        Makes the node active.
        """
        self.color = ACTIVE

    def make_path(self):
        """
        Makes the node a path.
        """
        self.color = PATH

    def reset(self):
        """
        Resets the node to its initial state.
        """
        self.color = EMPTY
        self.distance = float("inf")
        self.manhattan_distance = float("inf")
        self.total_cost = float("inf")
        self.previous = None
        self.next = None
